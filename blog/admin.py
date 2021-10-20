from django.contrib import admin
from django.contrib.auth import get_user_model
from . models import Author, AuthorPost, Comment
# Register your models here.
User = get_user_model()
admin.site.register(User)
@admin.register(AuthorPost)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish', 'status')
    list_filter = ('status', 'created_on', 'publish', 'author')
    search_fields = ('title', 'article')
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('username',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'post',)
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)