from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

urlpatterns = [
    path('post/', views.PostListView.as_view(), name="post-list"),
    path('post/<int:pk>', views.PostDetailView.as_view(), name="post-detail"),
    path('post/create/', views.PostCreateView.as_view(), name="post-create"),
    path('post/<int:pk>/edit/', views.PostEditView.as_view(), name="post-edit"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),
   ]
