from django.views.generic import (CreateView,ListView,DetailView,UpdateView,DeleteView)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post,Favorite,Message,PostView,Notification
from .forms import PostForm,MessageForm
from django.views import View
from django.shortcuts import redirect,render,get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponseForbidden

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'marketplace/post_create.html'
    success_url = reverse_lazy('profile_detail')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PostList(ListView):
    model = Post
    template_name = 'marketplace/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.select_related('owner','category').order_by('-cr_at')


class PostDetail(DetailView):
    model = Post
    template_name = 'marketplace/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.select_related('owner', 'category')
    
    def get_object(self, queryset = None):
        post = super().get_object(queryset)
        
        if not self.request.user.is_authenticated:
            return post
        
        if self.request.user == post.owner:
            return post
        
        already_viewed = PostView.objects.filter(post=post,user=self.request.user).exists()
        
        if not already_viewed:
            
            PostView.objects.create(
                post=post,
                user=self.request.user
            )
            
            
            post.views += 1
            post.save(update_fields=['views'])
            
        return post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['is_favorite'] = Favorite.objects.filter(user=self.request.user,post=self.object).exists()
        else:
            context['is_favorite'] = False

        return context


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'marketplace/post_update.html'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'marketplace/post_delete.html'
    success_url = reverse_lazy('profile_detail')

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)
    
    
    


class FavoriteView(LoginRequiredMixin, View):

    def post(self, request, pk):

        post = Post.objects.get(pk=pk)

        favorite = Favorite.objects.filter(user=request.user,post=post).first()

        if favorite:
            favorite.delete()
        else:
            Favorite.objects.create(user=request.user,post=post)

        return redirect('post_detail', pk=pk)
    
    
class FavoriteList(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = 'marketplace/favorite_list.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('post','post__category').order_by('-cr_at')
    

User = get_user_model()


class ChatView(LoginRequiredMixin, View):

    def get(self, request, pk, user_id):

        post = get_object_or_404(Post, pk=pk)
        other_user = get_object_or_404(User, pk=user_id)
        
        
        if request.user == other_user:
            return redirect('post_detail', pk=post.pk)
        

        if request.user != post.owner:


            if other_user != post.owner:
                return HttpResponseForbidden(
                    'Нельзя открыть этот чат.'
                )
        
        else:

            has_chat = Message.objects.filter(
                post=post
            ).filter(
                Q(sender=other_user, receiver=request.user) |
                Q(sender=request.user, receiver=other_user)
            ).exists()

            if not has_chat:
                return HttpResponseForbidden(
                    'Этот пользователь ещё не писал по объявлению.'
                )

        Message.objects.filter(
            post=post,
            sender=other_user,
            receiver=request.user,
            is_read=False
        ).update(is_read=True)

        messages = Message.objects.filter(
            post=post).filter(
            Q(sender=request.user, receiver=other_user) |
            Q(sender=other_user, receiver=request.user)).order_by('cr_at')

        form = MessageForm()

        return render(
            request,
            'marketplace/chat.html',
            {'post': post,'other_user': other_user,'messages': messages,'form': form,})


    def post(self, request, pk, user_id):

        post = get_object_or_404(Post, pk=pk)
        other_user = get_object_or_404(User, pk=user_id)

        
        
        
        if request.user == other_user:
            return redirect('post_detail', pk=post.pk)
        if request.user != post.owner:

            if other_user != post.owner:
                return HttpResponseForbidden(
                    'Нельзя отправить сообщение этому пользователю.'
                )
                
        else:

            has_chat = Message.objects.filter(
                post=post
            ).filter(
                Q(sender=other_user, receiver=request.user) |
                Q(sender=request.user, receiver=other_user)
            ).exists()

            if not has_chat:
                return HttpResponseForbidden(
                    'Этот пользователь ещё не писал по объявлению.'
                )

        form = MessageForm(request.POST)

        if form.is_valid():

            message = form.save(commit=False)

            message.sender = request.user
            message.receiver = other_user
            message.post = post

            message.save()

            return redirect('chat',pk=post.pk,user_id=other_user.pk)

        messages = Message.objects.filter(
            post=post).filter(
            Q(sender=request.user, receiver=other_user) |
            Q(sender=other_user, receiver=request.user)).order_by('cr_at')


        Message.objects.filter(post=post,sender=other_user,receiver=request.user,is_read=False).update(is_read=True)

        return render(
            request,
            'marketplace/chat.html',
            {'post': post,'other_user': other_user,'messages': messages,'form': form,})
        
        
        
        
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'marketplace/message_list.html'
    context_object_name = 'chats'

    def get_queryset(self):

        messages = Message.objects.filter(
            Q(sender=self.request.user) |
            Q(receiver=self.request.user)).select_related('sender','receiver','post').order_by('-cr_at')

        chats = []
        used = set()

        for message in messages:

            if message.sender == self.request.user:
                other_user = message.receiver
            else:
                other_user = message.sender

            key = (other_user.id, message.post.id)

            if key in used:
                continue

            used.add(key)

            unread_count = Message.objects.filter(post=message.post,sender=other_user,receiver=self.request.user,is_read=False).count()

            chats.append({
                'user': other_user,
                'post': message.post,
                'last_message': message,
                'unread_count': unread_count,
            })

        return chats
    
    
    
class NotificationListView(LoginRequiredMixin, ListView):

    model = Notification

    template_name = 'marketplace/notification_list.html'

    context_object_name = 'notifications'

    def get_queryset(self):

        return Notification.objects.filter(
            user=self.request.user
        ).select_related(
            'sender',
            'message',
            'message__post'
        ).order_by('-cr_at')