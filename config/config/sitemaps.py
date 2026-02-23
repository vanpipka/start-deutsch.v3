from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from articles.models import Article
from tests.models import Exam, ExamAttempt


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
    

class ExamAttemptSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.6

    def items(self):
        return ExamAttempt.objects.filter(finished_at__isnull=False)

    def location(self, obj):
        return reverse('tests:exam_result_detail', args=[obj.id])

    def lastmod(self, obj):
        return obj.finished_at
    

class StaticSitemap(Sitemap):
    
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return [
            
            # SEO A1 rules pages
            "/nemetskiy-a1-testy/schreiben/rules",
            "/nemetskiy-a1-testy/lesen/rules",
            "/nemetskiy-a1-testy/hoeren/rules",
            
            # SEO A2 rules pages
            #"/nemetskiy-a2-testy/schreiben/rules",
            
            # SEO A1 pages
            "/nemetskiy-a1-testy/lesen/",
            "/nemetskiy-a1-testy/hoeren/",
            "/nemetskiy-a1-testy/grammatik/",
            "/nemetskiy-a1-testy/sprachen/",
            "/nemetskiy-a1-testy/schreiben/",
            "/nemetskiy-a1-testy/",
            
            # SEO A2 pages
            "/nemetskiy-a2-testy/lesen/",
            "/nemetskiy-a2-testy/hoeren/",
            "/nemetskiy-a2-testy/grammatik/",
            "/nemetskiy-a2-testy/sprachen/",
            "/nemetskiy-a2-testy/schreiben/",
            "/nemetskiy-a2-testy/",
        ]

    def location(self, item):
        return item