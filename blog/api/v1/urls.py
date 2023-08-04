from django.urls import path, include
from . import views

app_name = "api-v1"

urlpatterns = [
    # api with function -->
    # path('post/',views.postList,name="post-list"),
    # path('post/<int:id>/',views.postDetail,name="post-detail"),
    # <--

    # api with class -->
    # path('post/',views.PostList.as_view(),name="post-list"),
    # path('post/<int:pk>/',views.PostDetail.as_view(), name="post-detail"),

    # path('post/',views.PostViewSet.as_view({'get':'list', 'post':'create'}), name="post-list"),
    # path('post/<int:pk>/',views.PostViewSet.as_view({'get':'retrieve', 'put':'update', 'patch':'partial_update', 'delete':'destroy'}), name="post-detail"),


    path('post/',views.PostModelViewSet.as_view({'get':'list', 'post':'create'}), name="post-list"),
    path('post/<int:pk>/',views.PostModelViewSet.as_view({'get':'retrieve', 'put':'update', 'patch':'partial_update', 'delete':'destroy'}), name="post-detail"),
    
    path('category/',views.CategoryModelViewSet.as_view({'get':'list', 'post':'create'}), name="category-list"),
    path('category/<int:pk>/',views.CategoryModelViewSet.as_view({'get':'retrieve', 'put':'update', 'patch':'partial_update', 'delete':'destroy'}), name="category-detail"),


]
