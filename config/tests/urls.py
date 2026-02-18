from django.urls import path
from . import views

app_name = 'tests'

urlpatterns = [   
    # path('', views.exam_list, name='exam_list'),
    path("", views.ExamListView.as_view(), name="exam_list"),
    path('<int:exam_id>/start/', views.exam_start, name='exam_start'),
    path('<int:exam_id>/continue/', views.exam_continue, name='exam_continue'),
    path(
        "<int:exam_id>/attempt/<int:attempt_id>/test/<int:test_id>/question/<int:question_id>/",
        views.exam_test_view,
        name="exam_test"
    ),
    path('<int:pk>/', views.ExamDetailView.as_view(), name="exam_detail"),
    path(
        "finish/<int:attempt_id>/",
        views.exam_finish,
        name="exam_finish"
    ),   
    path("result/<int:attempt_id>/", views.exam_result_detail, name="exam_result_detail"), 
    path("attempts/", views.exam_attempt_list, name="exam_attempt_list"),
]



    

    