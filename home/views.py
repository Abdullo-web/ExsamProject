from django.views.generic import ListView
from marketplace.models import Post,Category
from django.db.models import Q

class HomeView(ListView):
    model = Post
    template_name = 'home/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        posts = Post.objects.select_related('owner','category').order_by('-cr_at')

        q = self.request.GET.get('q')
        category = self.request.GET.get('category')
        
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        
        city = self.request.GET.get('city')

        if q:
            posts = posts.filter(Q(title__icontains=q) | Q(description__icontains=q))

        if category:
            posts = posts.filter(category_id=category)
        
        if min_price:
            posts = posts.filter(price__gte=min_price)

        if max_price:
            posts = posts.filter(price__lte=max_price)
            
        if city:
            posts = posts.filter(city__icontains=city)

        return posts
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.all()

        return context
