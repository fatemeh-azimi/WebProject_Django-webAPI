from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic import ListView, DetailView, FormView, CreateView
from .models import Post
from django.shortcuts import get_object_or_404
# from .forms import PostForm


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
