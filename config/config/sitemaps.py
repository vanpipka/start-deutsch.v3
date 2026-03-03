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
            
            #      
            "/tests/",
            
            # tests rules pages
            "/a1/rules/",
            "/a1/rules/schreiben/",
            "/a1/rules/lesen/",
            "/a1/rules/hoeren/",
            "/a1/rules/sprechen/",
            "/a2/rules/",
            "/a2/rules/schreiben/",
            "/a2/rules/lesen/",
            "/a2/rules/hoeren/",
            "/a2/rules/sprechen/",
            "/b1/rules/",
            "/b1/rules/schreiben/",
            "/b1/rules/lesen/",
            "/b1/rules/hoeren/",
            "/b1/rules/sprechen/",
            "/b2/rules/",
            "/b2/rules/schreiben/",
            "/b2/rules/lesen/",
            "/b2/rules/hoeren/",
            "/b2/rules/sprechen/",        
            
            # SEO A1 pages
            "/a1/"
            "/a1/lesen/",
            "/a1/hoeren/",
            "/a1/grammatik/",
            "/a1/sprechen/",
            "/a1/schreiben/",
            
            # SEO A2 pages
            "/a2/",
            "/a2/lesen/",
            "/a2/hoeren/",
            "/a2/grammatik/",
            "/a2/sprechen/",
            "/a2/schreiben/",
            
            # SEO B1 pages
            "/b1/",
            "/b1/lesen/",
            "/b1/hoeren/",
            "/b1/grammatik/",
            "/b1/sprechen/",
            "/b1/schreiben/",
            
            # SEO B2 pages
            "/b2/",
            "/b2/lesen/",
            "/b2/hoeren/",
            "/b2/grammatik/",
            "/b2/sprechen/",
            "/b2/schreiben/",
            
        ]

    def location(self, item):
        return item