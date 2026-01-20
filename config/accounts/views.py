from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm


@login_required
def profile(request):

    return render(request, 'accounts/profile.html', {
        'results': [],
        'total_tests': 0,
        'avg_score': 0
    })
    
    
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
