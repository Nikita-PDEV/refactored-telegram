from django.urls import path 
from articles.views import (home_view, register_view, article_create_view, CustomLoginView, NewsListView, ArticleUpdateView, ArticleDetailView  # Не забудьте импортировать ваше представление
)

urlpatterns = [   
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register_view, name='register'),   
    path('news/', NewsListView.as_view(), name='news'),
    path('article/create/', article_create_view, name='article_create'),   
    path('article/edit/<int:pk>/', ArticleUpdateView.as_view(), name='edit_article'),   
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),  # Добавьте этот маршрут
    path('', home_view, name='home'),  # Добавляем маршрут для корневого URL  
]
