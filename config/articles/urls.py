from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    # path('', views.article_list, name='article_list'),
    path("", views.ArticleListView.as_view(), name="article_list"),
    path("primer-pismennyy-nemetskiy-a1/", views.main_brief_view, name="article_detail"),
    path('<slug:slug>/', views.article_detail, name='article_detail'),
]
