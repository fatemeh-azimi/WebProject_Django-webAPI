from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, )#DjangoModelPermissions)
from .serializers import PostSerializer, CategorySerializer
from ...models import Post, Category #blog.models
from rest_framework import status, mixins
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import (GenericAPIView, ListAPIView, ListCreateAPIView, 
                                     RetrieveAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, 
                                     RetrieveUpdateDestroyAPIView)
from rest_framework import viewsets
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_role_filters.viewsets import RoleFilterModelViewSet
from .role_filters import StaffRoleFilter, UserRoleFilter
from .permissions import IsOwnerOrReadOnly, DjangoModelPermissions
from .paginations import DefaultPagination




# Example for Function Based View -->
'''
@api_view()
def postList(request):
    posts = Post.objects.filter(status=True)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
'''
'''
@api_view(["GET","POST"])
def postList(request):
    if request.method == "GET":
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
'''
'''
@api_view(["GET","POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def postList(request):
    if request.method == "GET":
        posts = Post.objects.filter(status=True)
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
'''
# <--
# Example for ApiView in Class Based View -->
'''
class PostList(APIView):
    """getting a list of posts and creating new posts"""
    #permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer #form kardan gesmat post or put
    def get(self,request):
        """retriveing a list of posts"""
        posts = Post.objects.filter(status=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        """creating a post with provided data"""
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
'''
# <--
# Example for GenericApiView in Class Based View -->
'''
class PostList(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)

    def get(self,request):
        """retriveing a list of posts"""
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        """creating a post with provided data"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
'''
'''
class PostList(GenericAPIView, mixins.ListModelMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer #form kardan gesmat post or put
    queryset = Post.objects.filter(status=True)

    def get(self,request):
        """retriveing a list of posts"""
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        """creating a post with provided data"""
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
'''
'''
class PostList(GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)

    def get(self, request, *args, **kwargs):
        """returning a list of posts"""
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
'''
'''
class PostList(GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    """getting a list of posts and creating new posts"""
    #permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    # queryset = Post.objects.filter(status=True)
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'author', 'status']
    # filterset_fields = {'category':['exact','in'], 'author':['exact'],'status':['exact']}
    search_fields = ['title', 'content']
    ordering_fields = ['published_date']
    pagination_class = DefaultPagination

    def get(self, request, *args, **kwargs):
        """returning a list of posts"""
        permission_classes = [IsAuthenticatedOrReadOnly]
        return self.list(request, permission_classes, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        permission_classes = [IsAdminUser]
        return self.create(request, permission_classes, *args, **kwargs)
'''
'''
class PostList(ListCreateAPIView):
    """getting a list of posts and creating new posts"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
'''
# <--



# Example for Function Based View -->
'''
@api_view()
def postDetail(request, id):
    try:
        post = Post.objects.get(pk=id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    except:
        return Response({"detail":"post dose not exsist"}, status=status.HTTP_404_NOT_FOUND)
'''
'''
@api_view()
def postDetail(request, id):
    post = get_object_or_404(Post, pk=id, status=True)
    serializer = PostSerializer(post)
    return Response(serializer.data)
'''
'''
@api_view(["GET","PUT", "DELETE"])
@permission_classes([IsAuthenticatedOrReadOnly])
def postDetail(request, id):
    post = get_object_or_404(Post, pk=id, status=True)
    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        post.delete()
        return Response({"detail":"item removed successfully"},status=status.HTTP_204_NO_CONTENT)
'''
# <--
# Example for ApiView in Class Based View -->
'''
class PostDetail(APIView):
    """ getting detail of the post and edit plus removing it """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer #form kardan gesmat post or put
    def get(self,request,id):
        """ retriveing the post data """
        post = get_object_or_404(Post,pk=id,status=True)
        serializer = self.serializer_class(post)    
        return Response(serializer.data)
    
    def put(self,request,id):
        """ editing the post data """
        post = get_object_or_404(Post,pk=id,status=True)
        serializer = PostSerializer(post,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self,request,id):
        """ deleting the post object """
        post = get_object_or_404(Post,pk=id,status=True)
        post.delete()
        return Response({"detail":"item removed successfully"},status=status.HTTP_204_NO_CONTENT)
'''
# <--
# Example for GenericApiView in Class Based View -->
'''
class PostDetail(GenericAPIView):
    """ getting detail of the post and edit plus removing it """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    def get(self,request,id):
        """ retriveing the post data """
        post = get_object_or_404(Post,pk=id,status=True)
        serializer = self.serializer_class(post)    
        return Response(serializer.data)
'''
'''
class PostDetail(GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    """ getting detail of the post and edit plus removing it """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    
    def get(self, request, *args, **kwargs):
       return self.retrieve(request, *args, **kwargs)
    def put(self, request, *args, **kwargs):
       return self.update(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
       return self.destroy(request, *args, **kwargs)
'''
'''
# just get ->
class PostDetail (RetrieveAPIView):
    """ getting detail of the post and edit plus removing it """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
'''
'''
# just get and put/patch ->
class PostDetail (RetrieveUpdateAPIView):
    """ getting detail of the post and edit plus removing it """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
'''
'''
# just get and delete ->
class PostDetail(RetrieveDestroyAPIView):
    """ getting detail of the post and edit plus removing it """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
'''
'''
# get and delete and put/patch ->
class PostDetail(RetrieveUpdateDestroyAPIView):
    """ getting detail of the post and edit plus removing it """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
'''
# <--



# Example for ViewSet in CBV -->
'''
# just get in postList ->
class PostViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)  
'''
'''
# just get in postList & postDtail ->
class PostViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)    
        
    def retrieve(self, request, pk=None):
        post_object = get_object_or_404(self.queryset ,pk=pk)
        serializer = self.serializer_class(post_object)    
        return Response(serializer.data)
'''
'''
class PostViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)    
        
    def retrieve(self, request, pk=None):
        post_object = get_object_or_404(self.queryset ,pk=pk)
        serializer = self.serializer_class(post_object)    
        return Response(serializer.data)
    
    def create(self, request):
        pass
    
    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
'''
'''
# evry things for postList & postDtail ->
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
'''
'''
class PostModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)

    @action(methods=['get'], defult=False)
    def get_ok(self, request):
        return Response({"detail":"ok"})
'''
class PostModelViewSet(viewsets.ModelViewSet): # اگر احیانا دوباره کار نکرد، از دوتا کلاس بالاتر استفاده کن.
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]#, IsAdminUser, IsAuthenticatedOrReadOnly, DjangoModelPermissions ]
    serializer_class = PostSerializer
    # queryset = Post.objects.filter(status=True)
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['category', 'author', 'status'] # اگر این فعال باشه کار نمیکنه ولی مال بخش فیلتر ها است.
    # filterset_fields = {'category':['exact','in'], 'author':['exact'],'status':['exact']}
    search_fields = ['title', 'content']
    ordering_fields = ['published_date']
    pagination_class = DefaultPagination
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # for role_filters.py
    # def get_role_id(self, request):
    #     return request.user.role.role_id



class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name']
# <--  

