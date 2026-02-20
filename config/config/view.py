from django.http import HttpResponse
from django.shortcuts import render
from articles.models import Article
from tests.models import Exam


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
