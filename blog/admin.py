from django.contrib import admin
from django.contrib.auth import get_user_model
from . models import Author, AuthorPost, Comment
from . forms import UserAdminChangeForm, UserAdminCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
# Register your models here.
User = get_user_model()

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin',)
    list_filter = ('admin','staff', 'active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('admin','staff','active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('email', 'password', 'password2'),
            }),
        )
    search_fields = ['email','full_name',]
    ordering = ['email']
    filter_horizontal = ()

admin.site.unregister(Group) # Remove Group Model from admin. We're not using it.

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