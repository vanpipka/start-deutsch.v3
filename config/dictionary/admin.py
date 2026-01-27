from django.contrib import admin
from .models import Level, WordType, Word


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")


@admin.register(WordType)
class WordTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "translation",
        "word_type",
        "level",
    )

    list_filter = (
        "word_type",
        "level",
    )

    search_fields = (
        "text",
        "translation",
        "example",
    )

    ordering = ("text",)

    fieldsets = (
        ("Основная информация", {
            "fields": (
                "text",
                "translation",
                "word_type",
                "level",
            )
        }),
        ("Грамматика", {
            "fields": (
                "plural_form",
                "conjugation",
            ),
            "classes": ("collapse",),
        }),
        ("Примеры", {
            "fields": (
                "example",
                "example_translation",
            )
        }),
        ("Дополнительно", {
            "fields": (
                "notes",
            ),
            "classes": ("collapse",),
        }),
    )
