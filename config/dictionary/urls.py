from django.urls import path
from . import views

app_name = "dictionary"

urlpatterns = [
    path("review/", views.review_words, name="review"),
    path("review/answer/", views.submit_answer, name="submit_answer"),
]
