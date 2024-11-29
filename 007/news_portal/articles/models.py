from django.db import models  
from django.contrib.auth.models import User  

# Список запрещенных слов  
CENSORED_WORDS = {  
    'плохое_слово_1',  # Замените на реальные слова  
    'плохое_слово_2',  # Замените на реальные слова  
    # Добавьте сюда другие слова  
}  

def censor_text(text):  
    """Заменяет запрещенные слова на звездочки."""  
    for word in CENSORED_WORDS:  
        text = text.replace(word, '*' * len(word))  
    return text  

class Category(models.Model):  
    name = models.CharField(max_length=100)  

    def __str__(self):  
        return self.name  


class Article(models.Model):  
    title = models.CharField(max_length=200)  
    content = models.TextField()  
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):  
        return self.title  

    def get_absolute_url(self):  
        from django.urls import reverse  
        return reverse('article_detail', args=[str(self.id)])  

    def save(self, *args, **kwargs):  
        """Переопределяем метод save для цензурирования контента."""  
        self.title = censor_text(self.title)  # Цензурируем название  
        self.content = censor_text(self.content)  # Цензурируем содержание  
        super().save(*args, **kwargs)  # Сохраняем объект  
class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Subscription(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  

    def __str__(self):  
        return f"{self.user.username} - {self.category.name}"