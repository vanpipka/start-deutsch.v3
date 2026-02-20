from django.urls import path
from . import views

app_name = 'tests'

urlpatterns = [   
    # Main page
    path('', views.home, name='home'),           
    path("exams/", views.ExamListView.as_view(), name="exam_list"),
    path('exams/<int:exam_id>/start/', views.exam_start, name='exam_start'),
    path('exams/<int:exam_id>/continue/', views.exam_continue, name='exam_continue'),
    path(
        "exams/<int:exam_id>/attempt/<int:attempt_id>/test/<int:test_id>/question/<int:question_id>/",
        views.exam_test_view,
        name="exam_test"
    ),
    path('exams/<int:pk>/', views.ExamDetailView.as_view(), name="exam_detail"),
    path(
        "exams/finish/<int:attempt_id>/",
        views.exam_finish,
        name="exam_finish"
    ),   
    path("exams/result/<int:attempt_id>/", views.exam_result_detail, name="exam_result_detail"), 
    path("exams/attempts/", views.exam_attempt_list, name="exam_attempt_list"),
        
    #SEO pages
    path(
        "nemetskiy-a1-testy/lesen/",
        views.ExamListView.as_view(),
        {
            "category": "Lesen", 
            "level": "A1", 
            "header": "Тесты на понимание текста (Lesen) для уровня A1",
            "seo_title": "Тесты на понимание текста (Lesen) для уровня A1",
            "seo_description": "Тесты на понимание текста (Lesen) для уровня A1. Подготовка к экзамену Goethe Start Deutsch A1."
        },
        name="lesen_test",
    ),
    path(
        "nemetskiy-a1-testy/hoeren/",
        views.ExamListView.as_view(),
        {
            "category": "Hören", 
            "level": "A1", 
            "header": "Тесты на понимание текста (Hören) для уровня A1",
            "seo_title": "Тесты на понимание текста (Hören) для уровня A1",
            "seo_description": "Тесты на понимание текста (Hören) для уровня A1. Подготовка к экзамену Goethe Start Deutsch A1."
        },
        name="hoeren_test",
    ),
    path(
        "nemetskiy-a1-testy/grammatik/",
        views.ExamListView.as_view(),
        {
            "category": "Grammatik", 
            "level": "A1", 
            "header": "Тесты на понимание грамматики (Grammatik) для уровня A1",
            "seo_title": "Тесты на понимание грамматики (Grammatik) для уровня A1",
            "seo_description": "Тесты на понимание грамматики (Grammatik) для уровня A1. Подготовка к экзамену Goethe Start Deutsch A1."
        },
        name="grammatik_test",
    ),
    path("nemetskiy-a1-testy/sprachen/", 
         views.ExamListView.as_view(),
        {
            "category": "Sprachenschatz", 
            "level": "A1", 
            "header": "Тесты на словарный запас (Sprachenschatz) для уровня A1",
            "seo_title": "Тесты на словарный запас (Sprachenschatz) для уровня A1",
            "seo_description": "Тесты на словарный запас (Sprachenschatz) для уровня A1. Подготовка к экзамену Goethe Start Deutsch A1."
        },
        name="sprachen_test",
    ),
    
    path("nemetskiy-a1-testy/", views.money_page, name="money_page"),
     
]



    

    