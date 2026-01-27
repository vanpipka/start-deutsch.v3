from datetime import timedelta
from django.utils import timezone

from dictionary.models import UserWordProgress


REVIEW_INTERVALS = [
    1,    # 1 день
    3,    # 3 дня
    7,    # 1 неделя
    14,   # 2 недели
    30,   # месяц
]


def update_word_progress(progress, success: bool):
    progress.last_review = timezone.now()
    progress.repetition_count += 1

    if success:
        progress.success_count += 1
        index = min(progress.success_count - 1, len(REVIEW_INTERVALS) - 1)
        days = REVIEW_INTERVALS[index]
        progress.next_review = timezone.now() + timedelta(days=days)

        if progress.success_count >= 5:
            progress.is_known = True
    else:
        # если ошибка — откатываем
        progress.success_count = max(0, progress.success_count - 1)
        progress.next_review = timezone.now() + timedelta(days=1)
        progress.is_known = False

    progress.save()


def get_words_for_review(user, limit=10):
    return UserWordProgress.objects.filter(
        user=user,
        next_review__lte=timezone.now(),
        is_known=False
    ).select_related("word")[:limit]
