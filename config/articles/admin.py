from django.contrib import admin
from django.utils.html import format_html
from .models import Article, Category, Tag, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'status',
        'author',
        'published_at',
        'created_at',
        'preview_image'
    )

    list_filter = (
        'status',
        'category',
        'tags',
        'created_at',
        'published_at'
    )

    search_fields = (
        'title',
        'short_description',
        'content'
    )

    prepopulated_fields = {'slug': ('title',)}

    readonly_fields = ('created_at', 'updated_at', 'preview_image')

    filter_horizontal = ('tags',)

    fieldsets = (
        ('Основное', {
            'fields': ('title', 'slug', 'short_description', 'content')
        }),
        ('Медиа', {
            'fields': ('image', 'preview_image')
        }),
        ('Классификация', {
            'fields': ('category', 'tags')
        }),
        ('Публикация', {
            'fields': ('status', 'published_at')
        }),
        ('Служебное', {
            'fields': ('author', 'created_at', 'updated_at')
        }),
         ('SEO', {
            'fields': ('seo_title', 'seo_description')
        }),
    )

    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; border-radius: 4px;" />',
                obj.image.url
            )
        return "—"
    
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)


    preview_image.short_description = "Превью"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'user', 'short_text', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('text', 'user__username', 'article__title')
    actions = ['approve_comments']

    def short_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    short_text.short_description = "Текст"

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    approve_comments.short_description = "Одобрить выбранные комментарии"