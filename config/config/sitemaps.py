from django.contrib.sitemaps import Sitemap
from articles.models import Article
from tests.models import Exam


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.created_at
    

class ExamSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Exam.objects.all()

    def lastmod(self, obj):
        return obj.created_at
    

class StaticSitemap(Sitemap):
    
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return [
            "/nemetskiy-a1-testy/schreiben/rules",
            "/nemetskiy-a1-testy/lesen/rules",
            "/nemetskiy-a1-testy/hoeren/rules",
            "/nemetskiy-a1-testy/lesen/",
            "/nemetskiy-a1-testy/hoeren/",
            "/nemetskiy-a1-testy/grammatik/",
            "/nemetskiy-a1-testy/sprachen/",
            "/nemetskiy-a1-testy/schreiben/",
            "/nemetskiy-a1-testy/",
            #"/nemetskiy-a2-testy/schreiben/rules",
            "/nemetskiy-a2-testy/lesen/",
            "/nemetskiy-a2-testy/hoeren/",
            "/nemetskiy-a2-testy/grammatik/",
            "/nemetskiy-a2-testy/sprachen/",
            "/nemetskiy-a2-testy/schreiben/",
            "/nemetskiy-a2-testy/",
        ]

    def location(self, item):
        return item