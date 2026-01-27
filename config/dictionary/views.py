from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import UserWordProgress
from .services import get_words_for_review, update_word_progress


@login_required
def review_words(request):
    mode = request.GET.get("mode", "flashcard")  # flashcard | test | input

    progress = (
        UserWordProgress.objects
        .filter(user=request.user, next_review__lte=timezone.now(), is_known=False)
        .select_related("word")
        .first()
    )

    if not progress:
        return render(request, "dictionary/review_done.html")

    template_map = {
        "flashcard": "dictionary/review_flashcard.html",
        "test": "dictionary/review_test.html",
        "input": "dictionary/review_input.html",
    }

    return render(request, template_map[mode], {
        "progress": progress,
        "word": progress.word,
        "mode": mode,
    })


@login_required
def submit_answer(request):
    if request.method != "POST":
        return redirect("dictionary:review")

    progress = get_object_or_404(
        UserWordProgress,
        id=request.POST.get("progress_id"),
        user=request.user
    )

    success = request.POST.get("success") == "1"
    update_word_progress(progress, success)

    return redirect(f"/dictionary/review/?mode={request.POST.get('mode')}")
