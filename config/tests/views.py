from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, OuterRef, Subquery, Sum, IntegerField, Value, Exists
from django.db.models.functions import Coalesce

from articles.models import Article
from .models import ExamAttempt, Question, Test, Answer, Exam, TestResult, UserAnswer
from .utils import get_last_exam_result_preview


def home(request):
    latest_articles = (
        Article.objects
        .filter(status=Article.PUBLISHED)
        .select_related('category', 'author')
        .prefetch_related('tags')
        .order_by('-published_at')[:6]
    )

    exams = Exam.objects.all().order_by('created_at')[:5]

    return render(request, 'core/home.html', {
        'latest_articles': latest_articles,
        'exams': exams
    })


class ExamDetailView(DetailView):
    model = Exam
    template_name = "tests/exam_detail.html"
    context_object_name = "exam"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam = self.object
        user = self.request.user

        context["seo_title"] = exam.get_seo_title()
        context["seo_description"] = exam.get_seo_description()
        
        # -----------------------------------
        # ДАННЫЕ О РЕЗУЛЬТАТАХ ПОЛЬЗОВАТЕЛЯ
        # -----------------------------------
        result_preview = None
        attempts_count = 0
        active_attempt = None

        if user.is_authenticated:

            # все попытки пользователя
            attempts = ExamAttempt.objects.filter(
                user=user,
                exam=exam
            )

            attempts_count = attempts.count()

            # незавершённая попытка (если есть)
            active_attempt = attempts.filter(
                finished_at__isnull=True
            ).first()

            # последняя завершённая попытка
            last_finished_attempt = (
                attempts.filter(finished_at__isnull=False)
                .order_by("-started_at")
                .first()
            )
            
            if active_attempt and last_finished_attempt and last_finished_attempt.started_at > active_attempt.started_at:
                active_attempt = None

            if last_finished_attempt:
                totals = TestResult.objects.filter(
                    attempt=last_finished_attempt
                ).aggregate(
                    total_score=Sum("score"),
                    total_questions=Sum("total")
                )

                score = totals["total_score"] or 0
                total = totals["total_questions"] or 0

                percent = 0
                if total > 0:
                    percent = round((score / total) * 100)

                result_preview = {
                    "attempt": last_finished_attempt,
                    "score": score,
                    "total": total,
                    "percent": percent,
                }

        context["attempts_count"] = attempts_count
        context["active_attempt"] = active_attempt
        context["result_preview"] = result_preview

        return context


@login_required
def exam_continue(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    attempt = (
        ExamAttempt.objects
        .filter(
            user=request.user,
            exam=exam,
            finished_at__isnull=True
        )
        .order_by("-started_at")
        .first()
    )

    if not attempt:
        attempt = ExamAttempt.objects.create(
            user=request.user,
            exam=exam
        )

    answered_subquery = UserAnswer.objects.filter(
        attempt=attempt,
        question=OuterRef("pk")
    )

    next_question = (
        Question.objects
        .filter(test__exam=exam)
        .annotate(answered=Exists(answered_subquery))
        .filter(answered=False)
        .select_related("test")
        .order_by("test__id", "id")
        .first()
    )

    if not next_question:
        return redirect("tests:exam_finish", attempt_id=attempt.id)

    return redirect(
        "tests:exam_test",
        exam_id=exam.id,
        attempt_id=attempt.id,
        test_id=next_question.test.id,
        question_id=next_question.id,
    )
    

@login_required
def exam_start(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    attempt = ExamAttempt.objects.create(
        user=request.user,
        exam=exam
    )

    answered_subquery = UserAnswer.objects.filter(
        attempt=attempt,
        question=OuterRef("pk")
    )

    next_question = (
        Question.objects
        .filter(test__exam=exam)
        .annotate(answered=Exists(answered_subquery))
        .filter(answered=False)
        .select_related("test")
        .order_by("test__id", "id")
        .first()
    )

    if not next_question:
        return redirect("tests:exam_finish", attempt_id=attempt.id)

    return redirect(
        "tests:exam_test",
        exam_id=exam.id,
        attempt_id=attempt.id,
        test_id=next_question.test.id,
        question_id=next_question.id,
    )


class ExamListView(ListView):
    model = Exam
    template_name = "tests/exam_list.html"
    context_object_name = "exams"
    
    def get_queryset(self):
        
        self.extra_context = {
            "seo_title": self.kwargs.get("seo_title") if self.kwargs.get("header") else "Бесплатные тесты по немецкому A1 онлайн",
            "seo_description": self.kwargs.get("seo_description") if self.kwargs.get("header") else "Пройдите бесплатные тесты по немецкому языку уровня A1 онлайн. Подготовка к экзамену Goethe Start Deutsch A1.",
        }
        
        qs = Exam.objects.annotate(
            tests_count=Count("tests", distinct=True)
        )

        category = self.kwargs.get("category")
        if category: qs = qs.filter(category__name=category)
            
        level = self.kwargs.get("level")
        if level: qs = qs.filter(level__name=level)
            
        header = self.kwargs.get("header")
        if header: self.extra_context["header"] = header    
            
        user = self.request.user

        # если пользователь не авторизован — просто список экзаменов
        if not user.is_authenticated:
            return qs.order_by("title")

        # -----------------------------
        # последняя попытка пользователя
        # -----------------------------
        last_attempt = ExamAttempt.objects.filter(
            user=user,
            exam=OuterRef("pk"),
            finished_at__isnull=False
        ).order_by("-finished_at")

        # id последней попытки
        qs = qs.annotate(
            last_attempt_id=Subquery(
                last_attempt.values("id")[:1]
            )
        )

        # -----------------------------
        # сумма правильных ответов
        # -----------------------------
        score_subquery = TestResult.objects.filter(
            attempt_id=OuterRef("last_attempt_id")
        ).values("attempt").annotate(
            total_score=Sum("score")
        ).values("total_score")

        total_subquery = TestResult.objects.filter(
            attempt_id=OuterRef("last_attempt_id")
        ).values("attempt").annotate(
            total_questions=Sum("total")
        ).values("total_questions")

        qs = qs.annotate(
            user_score=Coalesce(
                Subquery(score_subquery, output_field=IntegerField()),
                Value(0)
            ),
            user_total=Coalesce(
                Subquery(total_subquery, output_field=IntegerField()),
                Value(0)
            ),
        )

        return qs.order_by("title")

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)     
  
        if self.request.user.is_authenticated:
            passed_exam_ids = [] 
            '''Result.objects.filter(
                user=self.request.user
            ).values_list("exam_id", flat=True).distinct()
            '''

            context["passed_exam_ids"] = set(passed_exam_ids)
        else:
            context["passed_exam_ids"] = set()

        return context


@login_required
def exam_finish(request, attempt_id):
    attempt = get_object_or_404(
        ExamAttempt,
        id=attempt_id,
        user=request.user
    )

    total_exam_score = 0
    total_exam_questions = 0

    for test in attempt.exam.tests.all():
        answers = attempt.answers.filter(test=test)

        total = test.questions.count()
        score = sum(1 for a in answers if a.is_correct())

        TestResult.objects.create(
            attempt=attempt,
            test=test,
            score=score,
            total=total
        )

        total_exam_score += score
        total_exam_questions += total

    attempt.total_score = total_exam_score
    attempt.total_questions = total_exam_questions
    attempt.finished_at = timezone.now()
    attempt.save()

    return redirect("tests:exam_result_detail", attempt_id=attempt.id)


@login_required
def exam_test(request, exam_id, test_id):
    exam = get_object_or_404(Exam, id=exam_id)
    tests = list(exam.tests.all())
    if test_id >= len(tests):
        return redirect('tests:exam_result', exam_id=exam.id)

    test = tests[test_id]
    questions = test.questions.prefetch_related('answers')

    session_key = f'exam_{exam_id}_answers'
    exam_answers = request.session.get(session_key, {})

    if request.method == 'POST':
        # сохраняем ответы для этого теста
        test_answers = {}
        for question in questions:
            answer_id = request.POST.get(str(question.id))
            if answer_id:
                test_answers[str(question.id)] = answer_id
        exam_answers[str(test.id)] = test_answers
        request.session[session_key] = exam_answers

        return redirect('tests:exam_test', exam_id=exam.id, test_id=test_id + 1)

    return render(request, 'tests/exam_test.html', {
        'exam': exam,
        'test': test,
        'questions': questions,
        'test_index': test_id,
        'total_tests': len(tests),
    })


@login_required
def exam_next_test(request, exam_id, test_id):
    exam = get_object_or_404(Exam, id=exam_id)
    current_test = get_object_or_404(Test, id=test_id, exam=exam)

    # получаем все тесты экзамена в фиксированном порядке
    tests = list(exam.tests.order_by("id"))

    try:
        current_index = tests.index(current_test)
    except ValueError:
        # на всякий случай
        return redirect("tests:exam_list")

    # если есть следующий тест
    if current_index + 1 < len(tests):
        next_test = tests[current_index + 1]
        return redirect(
            "tests:exam_test",
            exam_id=exam.id,
            test_id=next_test.id,
            question_index=0
        )

    # если тесты закончились — экзамен завершён
    return redirect("tests:exam_finish", exam_id=exam.id)


@login_required
def exam_test_view(request, exam_id, attempt_id, test_id, question_id):
    attempt = get_object_or_404(
        ExamAttempt,
        id=attempt_id,
        exam_id=exam_id,
        user=request.user
    )

    test = get_object_or_404(Test, id=test_id, exam_id=exam_id)
    question = get_object_or_404(Question, id=question_id, test=test)

    # защита от повторного ответа
    #if UserAnswer.objects.filter(attempt=attempt, question=question).exists():
    #    return HttpResponseForbidden("На этот вопрос уже был дан ответ")

    if request.method == "POST":
        
        action = request.POST.get("action")

        if action == "back":
            
            # ищем предыдущий вопрос в текущем тесте
            prev_question = (
                test.questions
                .filter(id__lt=question.id)
                .order_by("-id")
                .first()
            )

            if prev_question:
                return redirect(
                    "tests:exam_test",
                    exam_id=exam_id,
                    attempt_id=attempt.id,
                    test_id=test.id,
                    question_id=prev_question.id
                )

            # если вопросов больше нет — ищем предыдущий тест
            prev_test = (
                attempt.exam.tests
                .filter(id__lt=test.id)
                .order_by("-id")
                .first()
            )

            if prev_test:
                last_question = prev_test.questions.order_by("-id").first()
                return redirect(
                    "tests:exam_test",
                    exam_id=exam_id,
                    attempt_id=attempt.id,
                    test_id=prev_test.id,
                    question_id=last_question.id
                )

            # если это первый вопрос первого теста — остаёмся на месте
            return redirect(
                "tests:exam_test",
                exam_id=exam_id,
                attempt_id=attempt.id,
                test_id=test.id,
                question_id=question.id
            )
            

        elif action == "next":
        
            if test.is_yes_no():
                value = request.POST.get("answer")  # "true" / "false"
                yes_no_value = value == "true"

                if UserAnswer.objects.filter(attempt=attempt, question=question).exists():
                    # обновляем существующий ответ
                    user_answer = UserAnswer.objects.get(attempt=attempt, question=question)
                    user_answer.yes_no_answer = yes_no_value
                    user_answer.save()
                    
                else:
                    UserAnswer.objects.create(
                        attempt=attempt,
                        test=test,
                        question=question,
                        yes_no_answer=yes_no_value
                    )

            else:
                answer_id = request.POST.get("answer")
                selected_answer = get_object_or_404(
                    Answer,
                    id=answer_id,
                    question=question
                )
                
                if UserAnswer.objects.filter(attempt=attempt, question=question).exists():
                    # обновляем существующий ответ
                    user_answer = UserAnswer.objects.get(attempt=attempt, question=question)
                    user_answer.selected_answer = selected_answer
                    user_answer.save()
                
                else:

                    UserAnswer.objects.create(
                        attempt=attempt,
                        test=test,
                        question=question,
                        selected_answer=selected_answer
                    )

            # следующий вопрос
            next_question = (
                test.questions
                .filter(id__gt=question.id)
                .order_by("id")
                .first()
            )

            if next_question:
                return redirect(
                    "tests:exam_test",
                    exam_id=exam_id,
                    attempt_id=attempt.id,
                    test_id=test.id,
                    question_id=next_question.id
                )

            # если вопросов больше нет — следующий тест
            next_test = (
                attempt.exam.tests
                .filter(id__gt=test.id)
                .order_by("id")
                .first()
            )

            if next_test:
                first_question = next_test.questions.order_by("id").first()
                return redirect(
                    "tests:exam_test",
                    exam_id=exam_id,
                    attempt_id=attempt.id,
                    test_id=next_test.id,
                    question_id=first_question.id
                )

            # если тестов больше нет — завершаем экзамен
            return redirect("tests:exam_finish", attempt_id=attempt.id)
    
    questions = list(test.questions.prefetch_related("answers"))
    total_questions = len(questions)
    question_index = questions.index(question)
    
    # восстанавливаем ранее сохранённый ответ для отображения
    try:
        user_answer = UserAnswer.objects.get(attempt=attempt, question=question)
        if test.is_yes_no():
            selected_value = "true" if user_answer.yes_no_answer else "false"
        else:
            selected_value = user_answer.selected_answer.id
    except UserAnswer.DoesNotExist:
        selected_value = None
    
    return render(request, "tests/exam_test.html", {
        "attempt": attempt,
        "test": test,
        "question": question,
        "answers": question.answers.all(),
        "question_index": question_index,
        "total_questions": total_questions,
        "progress_percent": int((question_index + 1) / total_questions * 100),
        "selected_value": selected_value,
    })


@login_required
def exam_attempt_list(request):
    attempts = (
        ExamAttempt.objects
        .filter(user=request.user, finished_at__isnull=False)
        .select_related("exam")
        .order_by("-started_at")
    )

    return render(request, "tests/exam_attempt_list.html", {
        "attempts": attempts
    })


@login_required
def exam_result_detail(request, attempt_id):
    attempt = get_object_or_404(
        ExamAttempt.objects.prefetch_related(
            "test_results__test",
            "answers__question__answers",
            "answers__selected_answer",
        ),
        id=attempt_id,
        user=request.user
    )

    # сгруппируем ответы по тестам
    answers_by_test = {}
    for answer in attempt.answers.all():
        answers_by_test.setdefault(answer.test, []).append(answer)

    return render(request, "tests/exam_result.html", {
        "attempt": attempt,
        "answers_by_test": answers_by_test,
    })


def money_page(request):
    
    context = {
        "seo_title": "Бесплатные тесты по немецкому A1 онлайн",
        "seo_description": "Пройдите бесплатные тесты по немецкому языку уровня A1 онлайн. Подготовка к экзамену Goethe Start Deutsch A1.",
    }
    
    return render(
        request, 
        "tests/A1/nemetskiy_a1_testy.html",
        context=context)
