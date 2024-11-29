from django.shortcuts import render, redirect, get_object_or_404  
from django.contrib.auth.decorators import login_required  
from django.contrib.auth.mixins import UserPassesTestMixin  
from django.views.generic import ListView, UpdateView, DetailView  
from .forms import UserRegistrationForm, ArticleForm   
from .models import Category, Article, UserSubscription  
from django.core.mail import send_mail  
from django.utils import timezone  
from django.contrib.auth import login  
from django.contrib.auth.views import LoginView  
from django.urls import reverse  
from django.contrib.auth.models import User  

# Список запрещенных слов  
CENSORED_WORDS = {  
    'плохое слово',   
    'плохое_слово_2',    
    # Добавьте сюда другие слова  
}  

def censor_text(text):  
    """Заменяет запрещенные слова на звездочки."""  
    for word in CENSORED_WORDS:  
        text = text.replace(word, '*' * len(word))  
    return text  

class CustomLoginView(LoginView):  
    template_name = 'articles/login.html'  

def home_view(request):  
    return render(request, 'articles/home.html')  

def register_view(request):  
    if request.method == 'POST':  
        form = UserRegistrationForm(request.POST)  
        if form.is_valid():  
            user = form.save(commit=False)  
            user.set_password(form.cleaned_data['password'])  
            user.save()  
            login(request, user)  
            send_welcome_email(user)  
            return redirect('home')  
        else:  
            print(form.errors)  # Вывод ошибок в консоль для отладки  
    else:  
        form = UserRegistrationForm()  
    return render(request, 'articles/register.html', {'form': form})  

def send_welcome_email(user):  
    subject = 'Добро пожаловать на новостной портал'  
    message = f'Здравствуйте, {user.username}! Спасибо за регистрацию на нашем портале!'  
    try:  
        send_mail(subject, message, 'from@example.com', [user.email])  
    except Exception as e:  
        print(f'Ошибка отправки почты: {e}')  # Логирование ошибок  

@login_required  
def article_create_view(request):  
    if request.method == 'POST':  
        form = ArticleForm(request.POST)  
        if form.is_valid():  
            article = form.save(commit=False)  
            article.author = request.user  # Устанавливаем текущего пользователя как автора  
            article.title = censor_text(article.title)  # Цензурируем заголовок  
            article.content = censor_text(article.content)  # Цензурируем содержание  
            article.save()  
            send_new_article_email(article)  
            return redirect('news')  # Перенаправление на страницу новостей  
    else:  
        form = ArticleForm()  
    return render(request, 'articles/article_form.html', {'form': form})  

def send_new_article_email(article):  
    subscriptions = UserSubscription.objects.filter(category=article.category)  
    for subscription in subscriptions:  
        subject = f'Новая статья в категории {subscription.category.name}'  
        message = (  
            f'Добавлена новая статья: {article.title}\n'  
            f'Краткое содержание: {article.content[:100]}...\n'  # Первые 100 символов статьи  
            f'Читать здесь: {article.get_absolute_url()}'  
        )  
        try:  
            send_mail(subject, message, 'from@example.com', [subscription.user.email])  
        except Exception as e:  
            print(f'Ошибка отправки почты: {e}')  # Логирование ошибок  

def send_weekly_updates():  
    one_week_ago = timezone.now() - timezone.timedelta(weeks=1)  
    subscriptions = UserSubscription.objects.all()  

    for subscription in subscriptions:  
        new_articles = Article.objects.filter(category=subscription.category, created_at__gte=one_week_ago)  
        if new_articles.exists():  
            article_links = '\n'.join(  
                [f'{censor_text(article.title)}: {article.get_absolute_url()}' for article in new_articles]  
            )  
            subject = 'Новинки в вашей подписке'  
            message = f'В этой категории появились новые статьи:\n{article_links}'  
            try:  
                send_mail(subject, message, 'from@example.com', [subscription.user.email])  
            except Exception as e:  
                print(f'Ошибка отправки почты: {e}')  # Логирование ошибок  

class NewsListView(ListView):  
    model = Article  
    template_name = 'articles/news.html'  
    context_object_name = 'articles'  
    ordering = ['-created_at']  # Сортировка по дате создания в обратном порядке  

    def get_queryset(self):  
        queryset = super().get_queryset()  
        sort_by = self.request.GET.get('sort_by', 'date')  
        sort_order = self.request.GET.get('sort_order', 'desc')  
        category_id = self.request.GET.get('category', None)  

        # Сортировка  
        if sort_by == 'name':  
            queryset = queryset.order_by('title')  
        elif sort_by == 'category':  
            queryset = queryset.order_by('category__name')  
        else:  
            queryset = queryset.order_by('created_at' if sort_order == 'asc' else '-created_at')  

        if category_id:  
            queryset = queryset.filter(category_id=category_id)  

        return queryset  

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        context['categories'] = Category.objects.all()  
        context['selected_category'] = self.request.GET.get('category', None)  
        context['sort_options'] = [  
            {'value': 'date', 'label': 'По дате'},  
            {'value': 'name', 'label': 'По имени'},  
            {'value': 'category', 'label': 'По категории'}  
        ]  
        context['sort_orders'] = [  
            {'value': 'asc', 'label': 'По возрастанию'},  
            {'value': 'desc', 'label': 'По убыванию'}  
        ]  
        if self.request.user.is_authenticated:  
            context['subscribed_categories'] = UserSubscription.objects.filter(user=self.request.user).values_list('category__name', flat=True)  
        else:  
            context['subscribed_categories'] = []  

        return context  

    def post(self, request, *args, **kwargs):  
        if request.user.is_authenticated:  
            category_id = request.POST.get('category')  
            if category_id:  
                category = get_object_or_404(Category, id=category_id)  
                UserSubscription.objects.get_or_create(user=request.user, category=category)  
        return redirect('news')  # Перенаправление на страницу новостей  

# Представление для редактирования статьи  
class ArticleUpdateView(UserPassesTestMixin, UpdateView):  
    model = Article  
    form_class = ArticleForm  
    template_name = 'articles/edit_article.html'  # Шаблон для редактирования статьи  

    def test_func(self):  
        article = self.get_object()  
        return self.request.user == article.author  # Проверка, является ли текущий пользователь автором статьи  

    def get_success_url(self):  
        return reverse('news')  # Перенаправление на страницу новостей после успешного редактирования  

# Представление для детального просмотра статьи  
class ArticleDetailView(DetailView):  
    model = Article  
    template_name = 'articles/article_detail.html'  # Верное название шаблона для детального просмотра  
    context_object_name = 'article'  

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        context['categories'] = Category.objects.all()  # Добавляем категории в контекст  
        # Цензурируем заголовок и содержание статьи  
        context['article'].title = censor_text(context['article'].title)  
        context['article'].content = censor_text(context['article'].content)  
        return context