from django.db.models import Sum
from .models import ExamAttempt, TestResult


def get_last_exam_result_preview(user, exam):
    """
    Возвращает превью последнего результата экзамена пользователя.
    """

    # последняя попытка пользователя по экзамену
    last_attempt = (
        ExamAttempt.objects
        .filter(user=user, exam=exam, finished_at__isnull=False)
        .order_by("-finished_at")
        .first()
    )

    if not last_attempt:
        return None

    # результаты всех тестов внутри попытки
    results = TestResult.objects.filter(attempt=last_attempt)

    totals = results.aggregate(
        total_score=Sum("score"),
        total_questions=Sum("total"),
    )

    total_score = totals["total_score"] or 0
    total_questions = totals["total_questions"] or 0

    percent = 0
    if total_questions > 0:
        percent = round((total_score / total_questions) * 100)

    return {
        "score": total_score,
        "total": total_questions,
        "percent": percent,
    }
