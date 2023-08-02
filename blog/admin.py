
from django.contrib import admin
from .models import Post, Category, Comment, Tag

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ['author', 'title', 'status', 'category', 'tag', 'created_date', 'published_date']
    date_hierarchy = 'created_date'
    empty_value_display = '_empty_'
    list_filter = ('author', 'status', 'category', 'tag')
    search_field = ['title', 'content']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'email', 'subject', 'message', 'approved', 'created_date', 'updated_date']
    date_hierarchy = 'created_date'
    list_filter = ('post', 'email', 'subject', 'approved')
    search_field = ['post', 'email', 'message', 'subject']
    empty_value_display = '_empty_'


    
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

