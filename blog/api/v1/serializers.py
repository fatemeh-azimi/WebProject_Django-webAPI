from rest_framework import serializers
from rest_framework import serializers
from ...models import Post, Category, Tag, Comment


'''
class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
'''
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        #fields = '__all__'
        fields = ['id', 'image', 'author', 'title', 'content', 'status', 'category', 
                  'tag', 'created_date', 'published_date']
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


