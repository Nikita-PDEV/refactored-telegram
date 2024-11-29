from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse
from .models import Article, Subscription
from datetime import datetime, timedelta
@shared_task
def send_weekly_newsletter():
    # Получаем все категории, на которые есть подписки
    categories = Subscription.objects.values_list('category', flat=True).distinct()

    for category in categories:
        # Получаем новые новости за последнюю неделю для данной категории
        last_week = datetime.now() - timedelta(days=7)
        articles = Article.objects.filter(category=category, published_date__gte=last_week)

        # Получаем всех пользователей, подписанных на данную категорию
        subscribers = Subscription.objects.filter(category=category).values_list('user__email', flat=True)

        # Отправляем письма подписчикам
        for email in subscribers:
            subject = f"Новые новости за неделю: {category}"
            message = "\n\n".join([f"{article.title} - {reverse('article_detail', args=[article.slug])}" for article in articles])
            message += f"\n\nПросмотреть все новости: {reverse('news_portal')}"
            send_mail(
                subject=subject,
                message=message,
                from_email="noreply@your-news-portal.com",
                recipient_list=[email],
                fail_silently=False,
            )