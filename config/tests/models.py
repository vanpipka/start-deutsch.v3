from django.conf import settings
from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class TestCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория теста"
        verbose_name_plural = "Категории тестов"


class ExamLevel(models.Model):
    name = models.CharField(max_length=100, verbose_name="Уровень экзамена")
    description = models.TextField(blank=True, verbose_name="Описание экзамена")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Уровень экзамена"
        verbose_name_plural = "Уровни экзаменов"


class Exam(models.Model):  
    level = models.ForeignKey(ExamLevel, on_delete=models.CASCADE, related_name="exams", verbose_name="Уровень")
    category = models.ForeignKey(TestCategory, on_delete=models.CASCADE, related_name="exams", verbose_name="Категория", null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name="Название экзамена")
    description = models.TextField(blank=True, verbose_name="Описание экзамена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    seo_title = models.CharField(
        max_length=60,
        blank=True,
        help_text="До 60 символов",
        default=""
    )
    seo_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="До 160 символов",
        default=""
    )

    def __str__(self):
        return self.title
    
    def get_seo_title(self):
        return self.seo_title or f"{self.title} – Exam Start Deutsch"

    def get_seo_description(self):
        return (
            self.seo_description
            or f"Пример экзамена «{self.title}». Шаблон, перевод и разбор."
        )
        
    def get_absolute_url(self):
        return reverse('tests:exam_detail', args=[self.id])
    

class Test(models.Model):
    YES_NO = 'yes_no'
    MULTIPLE_CHOICE = 'multiple_choice'

    TEST_TYPE_CHOICES = [
        (YES_NO, 'Да / Нет'),
        (MULTIPLE_CHOICE, 'Выбор из вариантов'),
    ]
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="tests", verbose_name="Экзамен")
    #category = models.ForeignKey(TestCategory, on_delete=models.CASCADE, related_name="exams", verbose_name="Категория")
    title = models.CharField(max_length=255, verbose_name="Название теста")
    description = models.TextField(blank=True, verbose_name="Описание")
    test_type = models.CharField(
        max_length=20,
        choices=TEST_TYPE_CHOICES,
        default=MULTIPLE_CHOICE,
        verbose_name="Тип теста"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"
        
    def is_yes_no(self):
        return self.test_type == self.YES_NO

    def is_multiple_choice(self):
        return self.test_type == self.MULTIPLE_CHOICE


class QuestionText(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название теста")
    description = RichTextUploadingField(verbose_name="Описание", blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Текст вопроса"
        verbose_name_plural = "Тексты вопросов"
    

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions", verbose_name="Тест")
    question_text = models.ForeignKey(QuestionText, on_delete=models.CASCADE, related_name="question_texts", verbose_name="Вопрос", null=True, blank=True) 
    description = RichTextUploadingField(verbose_name="Описание", blank=True)
    text = models.TextField(verbose_name="Текст вопроса")
    

    image = models.ImageField(
        upload_to='questions/images/',
        blank=True,
        null=True,
        verbose_name="Картинка"
    )

    audio = models.FileField(
        upload_to='questions/audio/',
        blank=True,
        null=True,
        verbose_name="Аудио"
    )

    def __str__(self):
        return self.text[:60]

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        
    def get_correct_answer(self):
        if self.test.test_type == self.test.YES_NO:
            return self.answers.first() # у таких вопросов только один ответ
        else:
            return self.answers.filter(is_correct=True).first()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers", verbose_name="Вопрос")
    title = models.CharField(max_length=100, verbose_name="Заголовок", blank=True)
    text = models.CharField(max_length=500, verbose_name="Текст ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
    
    
class ExamAttempt(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="exam_attempts",
        verbose_name="Пользователь"
    )
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="Экзамен"
    )

    started_at = models.DateTimeField(auto_now_add=True, verbose_name="Начало")
    finished_at = models.DateTimeField(blank=True, null=True, verbose_name="Завершение")

    total_score = models.IntegerField(default=0, verbose_name="Всего правильных")
    total_questions = models.IntegerField(default=0, verbose_name="Всего вопросов")

    def __str__(self):
        return f"{self.user} — {self.exam} ({self.started_at:%d.%m.%Y %H:%M})"

    class Meta:
        verbose_name = "Попытка экзамена"
        verbose_name_plural = "Попытки экзаменов"
        ordering = ["-started_at"]


class TestResult(models.Model):
    attempt = models.ForeignKey(
        ExamAttempt,
        on_delete=models.CASCADE,
        related_name="test_results",
        verbose_name="Попытка экзамена"
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name="results",
        verbose_name="Тест"
    )

    score = models.IntegerField(default=0, verbose_name="Правильных ответов")
    total = models.IntegerField(default=0, verbose_name="Всего вопросов")

    def __str__(self):
        return f"{self.test} — {self.score}/{self.total}"

    class Meta:
        verbose_name = "Результат теста"
        verbose_name_plural = "Результаты тестов"
        unique_together = ("attempt", "test")


class UserAnswer(models.Model):
    attempt = models.ForeignKey(
        ExamAttempt,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Попытка экзамена"
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        verbose_name="Тест"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name="Вопрос"
    )

    # для multiple_choice
    selected_answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Выбранный ответ"
    )

    # для yes/no
    yes_no_answer = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Ответ Да/Нет"
    )

    answered_at = models.DateTimeField(auto_now_add=True)

    def is_correct(self):
        if self.question.test.is_yes_no():
            correct = self.question.get_correct_answer()
            return correct.is_correct == self.yes_no_answer
        return self.selected_answer.is_correct

    def __str__(self):
        return f"{self.question}"

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователей"
        unique_together = ("attempt", "question")



