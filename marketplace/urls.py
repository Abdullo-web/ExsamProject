from django.urls import path

from .views import *


urlpatterns = [
    path('posts/',PostList.as_view(),name='post_list'),
    path('posts/create/',PostCreate.as_view(),name='post_create'),
    path('posts/<int:pk>/',PostDetail.as_view(),name='post_detail'),
    path('posts/<int:pk>/update/',PostUpdate.as_view(),name='post_update'),
    path('posts/<int:pk>/delete/',PostDelete.as_view(),name='post_delete'),
    path('posts/<int:pk>/favorite/',FavoriteView.as_view(),name='favorite'),
    path('favorites/',FavoriteList.as_view(),name='favorite_list'),
    path('posts/<int:pk>/chat/<int:user_id>/',ChatView.as_view(),name='chat'),
    path('messages/',MessageListView.as_view(),name='message_list'),
]