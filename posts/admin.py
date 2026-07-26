from django.contrib import admin
from .models import Category, Tag, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name")
    search_fields = ("category_name",)
    ordering = ("category_name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "tag_name")
    search_fields = ("tag_name",)
    ordering = ("tag_name",)
    
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "status",
        "view_count",
        "created_at",
    )

    list_filter = (
        "status",
        "category",
        "created_at",
    )

    search_fields = (
        "title",
        "content",
    )

    prepopulated_fields = {}
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "post",
        "created_at",
    )

    search_fields = (
        "author__username",
        "post__title",
        "comment",
    )

    list_filter = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )