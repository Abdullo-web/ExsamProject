from django.urls import path
from .views import *

urlpatterns = [
    path('profile_create/',ProfileCreate.as_view(),name='profile_create'),
    path('profile/edit/',ProfileUpdate.as_view(),name='profile_update'),
    path('profile/',ProfileDetail.as_view(),name='profile_detail'),
    path('profile/user/<int:pk>/',PublicProfileDetail.as_view(),name='public_profile'),
]