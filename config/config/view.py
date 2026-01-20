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
