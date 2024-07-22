from django.contrib import admin
from .models import Post, Category, Location, Comment, User
from django.contrib.auth.admin import UserAdmin


admin.site.empty_value_display = 'Не задано'


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'title',
    )


class LocationAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'name',
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'post'
    )


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'is_published',
        'pub_date',
        'author',
        'location',
        'category'
    )
    list_editable = (
        'is_published',
        'category'
    )
    search_fields = ('title',)
    list_filter = ('category',)
    list_display_links = ('title',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Comment, CommentAdmin)


class ListUsers(UserAdmin):
    list_display = ('username', 'email', 'is_staff')


admin.site.unregister(User)
admin.site.register(User, ListUsers)
