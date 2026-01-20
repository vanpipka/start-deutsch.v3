from django.contrib import admin
from django.utils.safestring import mark_safe
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter
from .models import ExamAttempt, Test, Question, Answer, TestCategory, ExamLevel, Exam, UserAnswer, QuestionText

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    inlines = [AnswerInline]
    show_change_link = True
    

class TestInline(admin.StackedInline):
    model = Test
    inlines = [QuestionInline]
    extra = 1
    show_change_link = True
    
    
@admin.action(description="Дублировать выбранные объекты")
def duplicate_objects(modeladmin, request, queryset):
    for obj in queryset:
        obj.pk = None  # Сбрасываем ID, чтобы Django создал новую запись
        obj.title = f'copy_{obj.title}'
        obj.save()
    modeladmin.message_user(request, f"Успешно скопировано {queryset.count()} объектов.")


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    inlines = [TestInline]


@admin.register(TestCategory)
class TestCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(ExamLevel)
class ExamLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    
  
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title',  'category', 'exam', 'test_type', 'created_at')
    list_filter = ('category', 'exam')
    search_fields = ('title',)
    inlines = [QuestionInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        test = form.instance

        if test.is_yes_no():
            answers = Answer.objects.filter(question__test=test)

            correct_answers = answers.filter(is_correct=True)

            if correct_answers.count() != 1:
                raise ValueError(
                    "Для YES/NO теста должен быть ровно один правильный Answer"
                )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'test', 'test__test_type')
    search_fields = ('text',)
    list_filter = ('test',)
    inlines = [AnswerInline]

    def short_text(self, obj):
        return obj.text[:50]
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" />')
        return "Нет изображения"

    image_preview.allow_tags = True
    image_preview.short_description = "Превью"


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'question', 'is_correct')
    list_filter = (
        #('status', DropdownFilter),  # Для обычных полей или choices
        ('question', RelatedDropdownFilter),  # Для Foreign Key
    )
    search_fields = ('text',)
    actions = [duplicate_objects]


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('test', 'question', 'selected_answer', "yes_no_answer")
    search_fields = ('question__text', 'selected_answer__text', )
    

@admin.register(QuestionText)
class QuestionTextAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "user", "exam",
        "started_at", "finished_at",
        "total_score", "total_questions"
    )
    readonly_fields = (
        "user", "exam",
        "started_at", "finished_at",
        "total_score", "total_questions"
    )