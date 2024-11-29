from django.contrib import admin  
from django.urls import path, include  
from articles.views import home_view, register_view, article_create_view, CustomLoginView, NewsListView

urlpatterns = [  
    path('admin/', admin.site.urls),  
    path('', include("articles.urls")),
]  