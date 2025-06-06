from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('news/', views.articles_list , name='articles_list'),
    path('articles/view/<slug:slug>/', views.article_page , name='article_page'),
    path('article/toggle_status/<int:id>/', views.toggle_article_status, name='toggle_article_status'),
]