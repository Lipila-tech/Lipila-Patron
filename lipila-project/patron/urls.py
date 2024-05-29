from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from business.views import CreateProductView, EditProductView, DeleteProductView

urlpatterns = [
     # Public URLS
     path('', views.index, name='index'),
     path('<str:user>/contribute', views.contribute, name='contribute'),

     path('creators/list', views.list_creators, name='creators'),
     path('my-tiers', views.view_tiers, name='tiers'),
     path('my-tiers/edit/<str:tier>', views.edit_tiers, name='edit_tier'),
     path('join/<str:tier>/<str:creator>/', views.join, name='join_tier'),
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)