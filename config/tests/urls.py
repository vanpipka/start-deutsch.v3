from django.urls import path, register_converter
from . import views
from articles.views import ArticleListView
from .converters import LevelConverter, TypeConverter

register_converter(LevelConverter, "level")
register_converter(TypeConverter, "type")
app_name = 'tests'

urlpatterns = [   
    # Main page
    path('', views.home, name='home'),           
    path("tests/", views.TestsListView.as_view(), name="exam_list"),
    path("tests/<level:level>/", views.TestsListView.as_view(), name="exam_list"),
    path("tests/<level:level>/<type:type>/", views.TestsListView.as_view(), name="exam_list"),
    path('tests/<int:exam_id>/start/', views.exam_start, name='exam_start'),
    path('tests/<int:exam_id>/continue/', views.exam_continue, name='exam_continue'),
    path("tests/<int:exam_id>/attempt/<int:attempt_id>/test/<int:test_id>/question/<int:question_id>/",
        views.exam_test_view,
        name="exam_test"
    ),
    path('tests/<int:pk>/', views.ExamDetailView.as_view(), name="exam_detail"),
    path("tests/finish/<int:attempt_id>/",
        views.exam_finish,
        name="exam_finish"
    ),   
    path("tests/result/<int:attempt_id>/", views.exam_result_detail, name="exam_result_detail"), 
    path("tests/attempts/", views.exam_attempt_list, name="exam_attempt_list"),
          
    path("<level:level>/rules/<type:type>/", 
        views.rules_view,
        name="tests_rules"),       
    path("<level:level>/",
        views.tests_by_level_page,
        name="tests_prev_page"),    
    path("<level:level>/<type:type>/",
        views.TestsListViewByLevel.as_view(),
        name="tests_list"),
        
]



    

    