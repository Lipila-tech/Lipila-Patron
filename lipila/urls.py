from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from patron import views as patron_views
from django.conf.urls import handler404


handler404 = views.custom_404_view


urlpatterns = [
    # message
    path('messages/', views.customer_messages_view, name='customer_messages'),
    path('messages/reply/<int:message_id>/', views.reply_to_message_view, name='reply_to_message'),
    # checkout urls
    path('checkout/<int:id>', views.checkout_subscription, name ="checkout_subscription"),
    path('support/<str:payee>/', views.checkout_momo, name ="checkout_momo"),
    path('checkout/visa/', views.create_purchase, name ="create_purchase"),

    # Luso public urls
    path('', views.index, name='index'),
    path('about/luso', views.about, name='about'),
    path('<str:title>/', views.creator_index, name='creator_index'),
    path('contact/lpa/', views.contact, name='contact'),

    # PatronUser defined authenticated user views
    path('dashboard/me/', patron_views.dashboard, name='dashboard'),
    path('dashboard/staff/', views.staff_users, name='staff_dashboard'),
        
    # lipila difened authenticated user views
    path('approve_withdrawals/lpa/', views.approve_withdrawals, name ='approve_withdrawals'),
    path('processed_withdrawals/lpa/', views.processed_withdrawals, name ='processed_withdrawals'),
    path('faq/ls/', views.pages_faq, name='faq'),
    path('terms-of-use/ls/', views.pages_terms, name='terms'),
    path('privacy-policy/ls', views.pages_privacy, name='privacy'),

    path('history/transfers/', views.transfers_history, name='transfers_history'),
    # Authenticated User's Transaction History endpoints
    path('history/withdrawals/', patron_views.withdrawal_history, name='withdrawals_history'),
    path('subscription/history/paid/', patron_views.payments_history, name='subscriptions_history'),
    
    # Modal-forms urls
    path('money/transfer/', views.money_transfer_view, name ='money_transfer'),
    path('withdrawals/request', views.CreateWithdrawalRequest.as_view(), name ='withdrawals'),
    path('update/<int:pk>', views.TierUpdateView.as_view(), name ='update_tier'),
    path('view/<int:pk>', views.TierReadView.as_view(), name ='view_tier'),
    path('delete/<int:pk>', views.TierDeleteView.as_view(), name ='delete_tier'),

    path('unsubscribe/<int:tier_id>', views.UnsubScribeView.as_view(), name='unsubscribe'),
    path('tiers/ls', views.tiers, name = 'tiers'),

    path('approve/<int:pk>', views.ApproveWithdrawModalView.as_view(), name='approve_withdraw'),
    path('reject/<int:pk>', views.RejectWithdrawModalView.as_view(), name='reject_withdraw'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
