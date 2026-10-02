from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import CreateView,ListView,UpdateView,DetailView
from .models import Profile
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from marketplace.models import Post
class ProfileCreate(LoginRequiredMixin,CreateView):
    model = Profile
    form_class = ProfileCreateForm
    template_name = 'profile/profile_create.html'
    success_url = reverse_lazy('profile_detail')
    
    def dispatch(self, request, *args, **kwargs):
        if Profile.objects.filter(owner=request.user).exists():
            return redirect('profile_detail')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    
class ProfileUpdate(LoginRequiredMixin,UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'profile/profile_update.html'
    success_url = reverse_lazy('home')
    
    def get_object(self, queryset=None):
        return self.request.user.profile_user
    
class ProfileDetail(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = 'profile/profile_detail.html'
    context_object_name = 'profile'
    
    def get_object(self, queryset =None):
        return self.request.user.profile_user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_posts'] = self.request.user.post_set.all().order_by('-cr_at')
        return context
    
class PublicProfileDetail(DetailView):
    model = Profile
    template_name = 'profile/public_profile_detail.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile,owner_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user_posts'] = Post.objects.filter(owner=self.object.owner).order_by('-cr_at')

        return context
    

    
  

    
    
