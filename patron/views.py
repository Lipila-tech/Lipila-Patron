from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from django.http import Http404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import requests
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
# custom modules
from lipila.utils import apology
from accounts.models import CreatorProfile, PayoutAccount
from lipila.utils import get_user_object
from patron.forms.forms import (
    CreateCreatorProfileForm, WithdrawalRequestForm)
from patron.forms.forms import DefaultUserChangeForm, EditCreatorProfileForm, PayoutAccountEditFrom, VerifyForm
from patron.models import Tier, TierSubscriptions, SubscriptionPayments, Payment, WithdrawalRequest
from patron.utils import (get_creator_subscribers, get_patrons,
                          get_creator_url, get_tier, calculate_total_payments,
                          calculate_total_contributions, calculate_total_withdrawals,
                          calculate_creators_balance)



class PatronPaymentRequestView(View):
    def post(self, request, *args, **kwargs):
        """
        This view will make a POST request to the AirtelPaymentRequestView in the 'payments' app.
        """
        # Extract data from the request
        reference = request.POST.get('reference')
        msisdn = request.POST.get('msisdn')
        transaction_id = request.POST.get('transaction_id')
        amount = request.POST.get('amount')

        # Prepare the payload for the API call
        payload = {
            'reference': reference,
            'msisdn': msisdn,
            'transaction_id': transaction_id,
            'amount': amount
        }

        # Make the request to AirtelPaymentRequestView API
        try:
            # Assuming the AirtelPaymentRequestView URL is /api/airtel/request-payment/
            response = requests.post('http://127.0.0.1:8000/api/airtel/request-payment/', json=payload)

            # Handle success
            if response.status_code == 201:
                data = response.json()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Payment request initiated successfully',
                    'data': data
                }, status=201)

            # Handle failure
            return JsonResponse({
                'status': 'error',
                'message': f'Failed to initiate payment: {response.json().get("detail", "Unknown error")}'
            }, status=response.status_code)

        except requests.exceptions.RequestException as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Request failed: {str(e)}'
            }, status=500)
        

def index(request):
    """
    Renders the page that displays benefits for different creators
    """
    return render(request, 'patron/categories/creators_info.html')


@login_required
def profile(request):
    context = {}
    if request.user.is_staff:
        messages.error(request, 'Contact Admin to update your profile')
        return redirect(reverse('staff_dashboard'))
    else:
        try:
            creator = request.user.creatorprofile
            context['user'] = get_user_object(creator)
            return render(request, 'patron/admin/profile/kyc.html', context)
        except CreatorProfile.DoesNotExist:
            context['user'] = get_user_object(request.user)
            return render(request, 'patron/admin/profile/profile_patron.html', context)


@login_required
def kyc(request):
    context = {}
    creator = request.user.creatorprofile
    try:
        bank = get_object_or_404(PayoutAccount, user_id=creator)
        context['bank'] = bank
    except Http404:
        messages.info(request, "Update your bank details.")
        PayoutAccount().create_default_bankaccount(creator)
        PayoutAccount().refresh_from_db()
    
    return render(request, 'patron/admin/profile/kyc.html', context)


@login_required
def kyc_review(request, pk):
    creator = get_user_model().objects.get(pk=pk)
    creator_profile = get_object_or_404(CreatorProfile, user__pk=pk)
    if request.method == 'POST':
        form = VerifyForm(request.POST, request.FILES)
        if form.is_valid():
            creator_profile.is_verified = True
            creator_profile.save()
            messages.success(request, f"{creator_profile.user.username} has been successfully verified.")
            return redirect(reverse('patron:kyc_review', kwargs={'pk':pk}))

    form = VerifyForm()
    creator = get_user_model().objects.get(pk=pk)        
    context = {'creator': creator, 'form':form}
    try:
        bank = get_object_or_404(
        PayoutAccount, user_id=creator.creatorprofile)
        context['bank'] = bank
    except Http404:
        bank = []
        context['bank'] = bank
    return render(request, 'patron/admin/profile/kyc_review.html', context)


class ProfileEdit(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        creator = request.user.creatorprofile
        context = {}
        try:
            bank = get_object_or_404(PayoutAccount, user_id=creator)
            context['bank'] = bank
        except Http404:
            messages.info(request, "Update your bank details.")
            PayoutAccount().create_default_bankaccount(creator)
            PayoutAccount().refresh_from_db()

        creator = request.user.creatorprofile
        form1 = EditCreatorProfileForm(instance=creator, prefix='form1')
        form2 = DefaultUserChangeForm(instance=request.user, prefix='form2')
        form3 = PayoutAccountEditFrom(instance=bank, prefix='form3')
        context['form1'] = form1
        context['form2'] = form2
        context['form3'] = form3
        return render(request,
                      'patron/admin/profile/edit_patron_info.html',
                      context)

    def post(self, request, *args, **kwargs):
        creator = request.user.creatorprofile
        bank = get_object_or_404(PayoutAccount, user_id=creator)
        form1 = EditCreatorProfileForm(
            request.POST, request.FILES, instance=creator, prefix='form1')
        form2 = DefaultUserChangeForm(
            request.POST, request.FILES, instance=request.user, prefix='form2')
        form3 = PayoutAccountEditFrom(
            request.POST, request.FILES, instance=bank, prefix='form3')
        if form1.is_valid() or form2.is_valid() or form3.is_valid():
            form1.save()
            form2.save()
            form3.instance.user_id = creator
            form3.save()
            messages.success(
                request, "Profile Updated Successfully.")
        else:
            messages.error(
                request, "Failed to update profile.")
            return redirect(reverse('patron:profile'))


class EditPersonalInfo(LoginRequiredMixin, View):
    def get(self, request, user, *args, **kwargs):
        form = DefaultUserChangeForm(instance=request.user)
        return render(request,
                      'patron/admin/profile/edit_personal_info.html',
                      {'form': form, 'user': request.user})

    def post(self, request, user, *args, **kwargs):
        form = DefaultUserChangeForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your profile has been updated.")
            return redirect(reverse('patron:profile'))
        else:
            messages.error(
                request, "Failed to update profile.")
            return redirect(reverse('patron:profile'))


@login_required
def create_creator_profile(request):
    creator = request.user
    if request.method == 'POST':
        form = CreateCreatorProfileForm(
            request.POST)
        if form.is_valid():
            creator_profile = form.save(commit=False)  # Don't save yet
            creator_profile.user = creator  # Set the user based on the logged-in user
            request.user.has_group = True
            request.user.is_creator = True
            request.user.save()
            creator_profile.save()
            request.user.refresh_from_db()
            creator_profile.refresh_from_db()
            messages.success(
                request, "Your profile data has been saved.")
            return redirect(reverse('patron:tiers'))
        else:
            messages.error(
                request, "Failed to save profile. data")
            return render(request,
                          'patron/admin/profile/create_creator_profile.html',
                          {'form': form, 'creator': creator})
    if request.user.is_staff:
        return redirect(reverse('staff_dashboard'))
    elif request.user.is_creator:
        return redirect(reverse('patron:profile'))
    else:
        form = CreateCreatorProfileForm()
        return render(request,
                      'patron/admin/profile/create_creator_profile.html',
                      {'form': form, 'creator': creator})


@login_required
def continue_has_fan(request):
    request.user.has_group = True
    request.user.save()
    request.user.refresh_from_db()
    messages.success(
        request, "Your profile data has been saved.")
    return redirect(reverse('patron:creators'))


@login_required
def dashboard(request):
    """
    Renders the appropriate dashboard based on user type (patron or creator).
    Redirects staff users to a dedicated staff dashboard.

    Args:
        request: The incoming HTTP request object.
        user: The username of the logged-in user (unused).

    Returns:
        A rendered response with the dashboard template and context.
    """
    context = {}
    now = timezone.now()
    request.session['last_login_time'] = now.strftime("%H:%M:%S")
    last_login_time = request.session.get('last_login_time')
    if last_login_time:
        context['last_login'] = last_login_time

    if request.user.is_staff:
        return redirect(reverse('staff_dashboard'))
    else:
        try:
            # Creator summary
            creator = request.user.creatorprofile
            total_payments = calculate_total_payments(creator)
            total_contributions = calculate_total_contributions(
                request.user.creatorprofile)
            withdrawals = calculate_total_withdrawals(creator)
            balance = total_contributions - withdrawals
            context['summary'] = {
                'balance': balance,
                'total_payments': total_payments + total_contributions,
                'withdrawals': withdrawals,
                'patrons': len(get_patrons(creator)),
                'tiers': len(Tier.objects.filter(creator=creator)),
                'updated_at': timezone.now,
                'last_login_time': last_login_time
            }

            domain = settings.DOMAIN

            url = get_creator_url('index', creator, domain=domain)
            context['user'] = get_user_object(creator)
            context['url'] = url
            return render(request, 'patron/admin/pages/index_creator.html', context)
        except CreatorProfile.DoesNotExist:
            return redirect(reverse('patron:creators'))
        except (ValueError, TypeError) as e:
            # print(e)
            msg = {
                'message': "Sorry! An Error occured. It's not your fault but ours.", 'status': 500}
            return apology(request, data=msg)


@login_required
def view_patrons_view(request):
    """
    Retrives all patrons subscribed to a user.
    """
    context = {}
    contributions = get_patrons(request.user.creatorprofile)
    context['contributions'] = contributions
    return render(request, 'patron/admin/pages/view_patrons.html', context)


@login_required
def view_tiers(request):
    """
    Retrives a an authenticated Creator User's tiers.
    """
    creator = CreatorProfile.objects.get(user=request.user)
    tiers = Tier.objects.filter(creator=creator).values()

    # Ensure defaults exist
    if not tiers.exists():
        Tier().create_default_tiers(creator)
        messages.info(
            request, "Default tier created. You can update the details.")
    return render(request,
                  'patron/admin/pages/view_tiers.html',
                  {'user': request.user, 'tiers': tiers})


@login_required
def subscribe_view(request, tier_id):
    """Handles user subscription to a creator.
    Args:
        request: The incoming HTTP request object.
        tier: The tier the user wants to join
        creator: the creator the user wants to support.

    Returns:
        A rendered response with the join form and subscription status.
    """
    tier = get_tier(tier_id)
    creator = tier.creator

    patron_title = CreatorProfile.objects.get(user=creator)
    if request.method == 'POST':
        patron = request.user
        TierSubscriptions.objects.get_or_create(patron=patron, tier=tier)
        messages.success(
            request, f"Welcome! You Joined my {tier.name} patrons.")
    return redirect(reverse('patron:subscription_detail', kwargs={"tier_id": tier_id}))


def browse_creators(request):
    """
    Retrieves all the User's with a CreatorProfile.
    """
    creators = CreatorProfile.objects.all()
    if request.user.is_authenticated:
        return render(request, 'patron/admin/pages/view_creators.html', {'creators': creators})
    else:
        return render(request, 'patron/admin/pages/view_creators_visitor.html', {'creators': creators})


@login_required
def subscriptions(request):
    """
    Retrieves all tiers an authenticated User is subscribed to.
    """
    user_object = get_object_or_404(get_user_model(), username=request.user)
    subscriptions = TierSubscriptions.objects.filter(patron=user_object)
    return render(request, 'patron/admin/pages/view_subscriptions.html', {'subscriptions': subscriptions})


@login_required
def subscription_detail(request, tier_id):
    """
    Renders a detailed view of a tier
    """
    context = {}
    tier = Tier.objects.get(pk=tier_id)
    try:
        context['tier_id'] = tier_id
        context['subscription'] = get_object_or_404(TierSubscriptions,
                                                    tier=tier, patron=request.user)
    except Http404:
        pass
    return render(request, 'patron/admin/pages/view_subscription_detail.html', context)


# PAYMENT HANDLING VIEWS
@login_required
def withdrawal_request(request):
    form = WithdrawalRequestForm()
    form.id = 'withdraw-form'
    total_payments = calculate_creators_balance(request.user.creatorprofile)
    pending_requests = WithdrawalRequest.objects.filter(
        creator=request.user.creatorprofile, status='pending')
    total_withdrawn = calculate_total_withdrawals(request.user.creatorprofile)

    context = {'form': form, 'pending_requests': pending_requests,
               'total_withdrawn': total_withdrawn, 'total_payments': total_payments}
    return render(request, 'patron/admin/actions/cashout.html', context)


# ACCOUNT HISTORY VIEWS

@login_required
def withdrawal_history(request):
    """
    This view retrives all the history of a creator's withdraw requests.
    """
    full_history = WithdrawalRequest.objects.filter(
        creator=request.user.creatorprofile)
    history = []
    context = {}
    if full_history:
        for obj in full_history:
            item = {}
            item['amount'] = obj.amount
            item['transaction_date'] = obj.request_date
            item['transaction_type'] = 'Withdraw Request'
            item['account_number'] = obj.account_number
            item['status'] = obj.status
            item['transaction_id'] = obj.transaction_id
            history.append(item)

    context['history'] = history
    return render(request, 'patron/admin/pages/withdrawal_history.html', context)


@login_required
def payments_history(request):
    """
    Retrieves an authenticated User's payment/contribution history history.
    """
    context = {}
    try:
        creator = request.user.creatorprofile
        payments = SubscriptionPayments.objects.filter(
            payee__tier__creator=creator)

        contributions = get_patrons(request.user.creatorprofile)
        context['contributions'] = contributions
        context['payments'] = payments
        return render(request, 'patron/admin/pages/payments_received.html', context)
   

    except get_user_model().creatorprofile.RelatedObjectDoesNotExist:
        payments = SubscriptionPayments.objects.filter(
            payee__patron=request.user)
        contributions = Payment.objects.filter(
            authenticated_payer=request.user, status='success')
        context['contributions'] = contributions
        context['payments'] = payments
        return render(request, 'patron/admin/pages/payments_made.html', context)
