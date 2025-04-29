from django.contrib import admin
from portfolio.models import Project
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class CommentInlineAdmin(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('created_at',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'comments_count', 'share_comment')
    list_filter = ('categories', 'title')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CommentInlineAdmin]

    # def comments_count(self, obj):
    #     return obj.comments.count()
    def share_comment(self, obj):
        return obj.comments.count()
    share_comment.short_description = 'Share Comment'