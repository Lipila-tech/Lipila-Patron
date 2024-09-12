from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

#  custom modules
from .utils import basic_auth_encode, basic_auth_decode
from .forms import SignUpForm

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings

import random
import string

TIKTOK_CLIENT_KEY = settings.TIKTOK_CLIENT_KEY
TIKTOK_SERVER_ENDPOINT_REDIRECT=settings.TIKTOK_SERVER_ENDPOINT_REDIRECT
TIKTOK_CLIENT_SECRET = settings.TIKTOK_CLIENT_SECRET

from django.http import HttpResponse, HttpResponseBadRequest
import requests


def tiktok_callback(request):
    # Get the 'code' and 'state' parameters from the URL
    code = request.GET.get('code')
    state = request.GET.get('state')

    # Verify that 'code' and 'state' are present
    if not code or not state:
        return HttpResponseBadRequest("Invalid callback parameters")

    # Optionally: Verify the 'state' to prevent CSRF attacks
    csrf_state = request.COOKIES.get('csrfState')
    if state != csrf_state:
        return HttpResponseBadRequest(f"Invalid state parameter {state} != {csrf_state}")

    # Now you can use the 'code' to exchange for an access token
    # Example: make a POST request to TikTok's token endpoint
    payload = {
        'client_key': TIKTOK_CLIENT_KEY,
        'client_secret': TIKTOK_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': TIKTOK_SERVER_ENDPOINT_REDIRECT
    }
    token_response = requests.post('https://www.tiktok.com/v2/oauth/token/', data=payload)
    token_data = token_response.json()

    # Handle the response and return to the user
    return HttpResponse(f"Authorization successful! Code: {code}, State: {state}")


def oauth(request):
    # Generate a random CSRF token
    csrf_state = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))

    # Set the CSRF token as a cookie
    response = HttpResponse()
    response.set_cookie('csrfState', csrf_state, max_age=60)

    # Build the TikTok authorization URL
    url = 'https://www.tiktok.com/v2/auth/authorize/'
    url += f'?client_key={TIKTOK_CLIENT_KEY}'
    url += '&scope=user.info.basic'
    url += '&response_type=code'
    url += f'&redirect_uri={TIKTOK_SERVER_ENDPOINT_REDIRECT}'
    url += f'&state={csrf_state}'
    

    # Redirect to the TikTok authorization URL
    return redirect(url)




def sign_in(request):
    return render(request, 'registration/signin.html')


@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    token = request.POST.get('credential')

    if not token:
        return HttpResponse(status=400)  # Bad request if no token is provided

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), settings.GOOGLE_OAUTH_CLIENT_ID)
    except ValueError:
        return HttpResponse(status=403)  # Forbidden if token is invalid

    email = user_data.get('email')

    if not email:
        return HttpResponse(status=400)  # Bad request if no email in token

    # Get or create the user
    user, created = get_user_model().objects.get_or_create(email=email, defaults={
        'username': email.split('@')[0],  # You can modify this as needed
        'first_name': user_data.get('given_name', ''),
        'last_name': user_data.get('family_name', ''),
    })

    if created:
        messages.success(request, "Account created.")
        user.set_unusable_password()  # Set unusable password if creating a new user
        user.save()

    # Authenticate and log in the user
    user = authenticate(request, email=email)
    if user is not None:
        messages.success(request, f"Welcome back, {user.username}!")
        login(request, user)
        request.session['user_data'] = user_data
        return redirect(reverse('dashboard'))
    else:
        messages.error(request, "Authentication failed")
        return redirect(reverse('accounts:signup'))


def sign_out(request):
    del request.session['user_data']
    return redirect('accounts:signin')


def activation_sent_view(request):
    return render(request, 'registration/activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = basic_auth_decode(uidb64)
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # Default backend or specific one
        backend = settings.AUTHENTICATION_BACKENDS[0]
        login(request, user, backend=backend)
        return redirect('patron:create_creator_profile')
    else:
        return render(request, 'registration/activation_invalid.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            uid64 = basic_auth_encode(user.pk)
            token = default_token_generator.make_token(user)
            message = render_to_string('registration/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid64,
                'token': token,
            })
            user.email_user(subject, message)
            return redirect('accounts:activation_sent')
        else:
            messages.error(request, "Invalid form fields.")
            form = SignUpForm()
            return render(request, 'registration/signup.html', {'form': form})

    form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def custom_login_view(request):
    if request.method == 'POST':
        next_url = request.GET.get('next', 'dashboard')
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.has_group or user.is_staff:
                    messages.success(request, f"Welcome back, {user.username}!")
                    return redirect(next_url)
                else:
                    return redirect('patron:create_creator_profile')
            else:
                form = AuthenticationForm()
                return render(request, 'registration/login.html', {'form': form})
        else:
            messages.error(request, "Invalid username or password.")
            form = AuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
