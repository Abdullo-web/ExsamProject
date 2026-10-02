from django.urls import path
from .views import RegisterUser,LoginUser,LogoutUser

urlpatterns = [
    path('registeruser/',RegisterUser.as_view(),name='registeruser'),
    path('login/',LoginUser.as_view(),name='login'),
    path('logout/',LogoutUser.as_view(),name='logout'),
]