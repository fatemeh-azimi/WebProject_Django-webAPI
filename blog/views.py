from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView
from .models import Post
from django.shortcuts import get_object_or_404
from .forms import PostForm
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

class PostListView(ListView):
    # queryset = Post.objects.all()
    model = Post
    context_object_name = 'posts'
    paginate_by = 2
    ordering = 'id'

    '''
    def get_queryset(self):
        posts = Post.objects.filter(statuse=True)
        return posts
    '''



class PostDetailView(DetailView):
    model = Post   



# section "save" dont work for me -->
'''
class PostCreateView(FormView):
    template_name = 'contact1.html'   
    form_class = PostForm
    success_url = '/blog/post/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
'''
'''
class PostCreateView(FormView):
    template_name = 'contact1.html'
    form_class = PostForm
    success_url = '/blog/post/'
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
'''
class PostCreateView(CreateView):
    model = Post
    # fields = ['author', 'title', 'content', 'status', 'category', 'published_date']
    form_class = PostForm
    success_url = '/blog/post/'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class PostEditView(UpdateView):
    model = Post
    form_class = PostForm
    success_url = '/blog/post/'



class PostDeleteView(DeleteView):
    model = Post
    success_url = "/blog/post/"

