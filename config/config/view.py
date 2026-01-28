from django.http import HttpResponse
from django.shortcuts import render
from articles.models import Article
from tests.models import Exam


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


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "Allow: /",
        "",
        "Sitemap: https://start-deutsch.ru/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")