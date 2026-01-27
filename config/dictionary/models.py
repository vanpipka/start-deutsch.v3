from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class Level(models.Model):
    code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Уровень (A1, A2, B1...)"
    )

    name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Название"
    )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Уровень"
        verbose_name_plural = "Уровни"
        ordering = ["code"]


class WordType(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Тип слова"
    )

    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип слова"
        verbose_name_plural = "Типы слов"


class Word(models.Model):
    text = models.CharField(
        max_length=255,
        verbose_name="Слово"
    )

    translation = models.CharField(
        max_length=255,
        verbose_name="Перевод"
    )

    word_type = models.ForeignKey(
        WordType,
        on_delete=models.PROTECT,
        related_name="words",
        verbose_name="Тип слова"
    )

    level = models.ForeignKey(
        Level,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="words",
        verbose_name="Уровень"
    )

    plural_form = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Множественное число"
    )

    conjugation = models.TextField(
        blank=True,
        verbose_name="Спряжения"
    )

    example = models.TextField(
        blank=True,
        verbose_name="Пример использования"
    )

    example_translation = models.TextField(
        blank=True,
        verbose_name="Перевод примера"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Примечания"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Слово"
        verbose_name_plural = "Слова"
        unique_together = ("text", "word_type")
        ordering = ["text"]


class UserWordProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="word_progress"
    )

    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="user_progress"
    )

    repetition_count = models.PositiveIntegerField(default=0)
    success_count = models.PositiveIntegerField(default=0)

    next_review = models.DateTimeField(default=timezone.now)
    last_review = models.DateTimeField(null=True, blank=True)

    is_known = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "word")
        verbose_name = "Прогресс слова"
        verbose_name_plural = "Прогресс слов"

    def __str__(self):
        return f"{self.user} — {self.word}"
