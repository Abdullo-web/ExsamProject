from django.urls import path

from .views import *


urlpatterns = [
    path('posts/',PostList.as_view(),name='post_list'),
    path('posts/create/',PostCreate.as_view(),name='post_create'),
    path('posts/<int:pk>/',PostDetail.as_view(),name='post_detail'),
    path('posts/<int:pk>/update/',PostUpdate.as_view(),name='post_update'),
    path('posts/<int:pk>/delete/',PostDelete.as_view(),name='post_delete'),
]