from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from .models import ExamAttempt, Question, Test, Answer, Exam, TestResult, UserAnswer


class ExamDetailView(DetailView):
    model = Exam
    template_name = "tests/exam_detail.html"
    context_object_name = "exam"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        letter = self.object

        context["seo_title"] = letter.get_seo_title()
        context["seo_description"] = letter.get_seo_description()

        return context

@login_required
def exam_start(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    # создаём новую попытку
    attempt = ExamAttempt.objects.create(
        user=request.user,
        exam=exam
    )

    # берём первый тест экзамена
    first_test = exam.tests.order_by("id").first()

    if not first_test:
        return redirect("tests:exam_list")

    # первый вопрос первого теста
    first_question = first_test.questions.order_by("id").first()

    return redirect(
        "tests:exam_test",
        exam_id=exam.id,
        attempt_id=attempt.id,
        test_id=first_test.id,
        question_id=first_question.id
    )


class ExamListView(ListView):
    model = Exam
    template_name = "tests/exam_list.html"
    context_object_name = "exams"

    def get_queryset(self):
        qs = Exam.objects.annotate(
            tests_count=Count("tests", distinct=True)
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
    if UserAnswer.objects.filter(attempt=attempt, question=question).exists():
        return HttpResponseForbidden("На этот вопрос уже был дан ответ")

    if request.method == "POST":
        if test.is_yes_no():
            value = request.POST.get("answer")  # "true" / "false"
            yes_no_value = value == "true"

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
    
    return render(request, "tests/exam_test.html", {
        "attempt": attempt,
        "test": test,
        "question": question,
        "answers": question.answers.all(),
        "question_index": question_index,
        "total_questions": total_questions,
        "progress_percent": int((question_index + 1) / total_questions * 100),
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
