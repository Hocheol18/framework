from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article),
    path('articles/<int:article_pk>/', views.article_detail),
    path('comments/<int:comment_pk>/', views.comment_list)
]
