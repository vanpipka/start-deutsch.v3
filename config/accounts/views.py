from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.db.models import Avg, Count, F, FloatField, ExpressionWrapper

from tests.models import ExamAttempt
from .forms import LoginForm, RegisterForm


@login_required
def profile(request):

    user = request.user

    # Все попытки пользователя
    exam_attempts = (
        ExamAttempt.objects
        .filter(user=user)
        .filter(finished_at__isnull=False)
        .select_related("exam")
        .order_by("-started_at")
    )

    # Общее количество попыток
    attempts_count = exam_attempts.count()

    # Средний процент (score / total * 100)
    avg_score = (
        exam_attempts
        .annotate(
            percent=ExpressionWrapper(
                F("total_score") * 100.0 / F("total_questions"),
                output_field=FloatField()
            )
        )
        .aggregate(avg=Avg("percent"))
        .get("avg")
    )

    avg_score = round(avg_score) if avg_score else 0

    # Последние 5 попыток
    recent_attempts = exam_attempts[:5]

    context = {
        "user": user,
        "attempts_count": attempts_count,
        "avg_score": avg_score,
        "recent_attempts": recent_attempts,
    }

    return render(request, "accounts/profile.html", context)
    
    
def login_view(request):
    if request.user.is_authenticated:
        return redirect("tests:exam_list")

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"]
        )
        if user:
            login(request, user)
            return redirect("tests:exam_list")
        else:
            form.add_error(None, "Неверный логин или пароль")

    return render(request, "accounts/login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("tests:exam_list")

    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password1"])
        user.save()

        login(request, user)
        return redirect("tests:exam_list")

    return render(request, "accounts/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("accounts:login")
