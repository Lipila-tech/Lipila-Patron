from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path('request-payment/', views.PatronPaymentRequestView.as_view(), name='request-payment'),
     # Public URLS
     path('creators/', views.index, name='index'),

     path('creators/list', views.browse_creators, name='creators'),
     path('my-tiers', views.view_tiers, name='tiers'),
     path('join/<int:tier_id>', views.subscribe_view, name='join_tier'),
     path('patron/all/', views.view_patrons_view, name='patrons'),
     path('subscriptions/', views.subscriptions, name='subscriptions'),
     path('subscription/<int:tier_id>', views.subscription_detail, name='subscription_detail'),
     path('withdraw/', views.withdrawal_request, name='withdraw_request'),

     # Profile views
     # cretaor kyc
     path('accounts/profile/kyc/overview', views.kyc, name='kyc'),
     path('accounts/profile/kyc/<int:pk>', views.kyc_review, name='kyc_review'),
     path('accounts/profile/continue/fans', views.continue_has_fan, name="continue_has_fan"),
     path('accounts/profile/', views.profile, name='profile'),
     path('accounts/profile/edit/<str:user>/patron', views.ProfileEdit.as_view(), name='update_profile'),
     path('accounts/profile/edit/<str:user>', views.EditPersonalInfo.as_view(), name='update_personal_info'),
     path('accounts/profile/create/creator', views.create_creator_profile,
          name='create_creator_profile'),
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)