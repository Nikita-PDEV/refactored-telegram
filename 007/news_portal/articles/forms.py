from django import forms  
from django.contrib.auth.models import User  
from .models import Article, UserSubscription, Category

class UserRegistrationForm(forms.ModelForm):  
    password = forms.CharField(widget=forms.PasswordInput)  

    class Meta:  
        model = User  
        fields = ['username', 'email', 'password']  


class ArticleForm(forms.ModelForm):  
    class Meta:  
        model = Article  
        fields = ['title', 'content', 'category']
        
class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = UserSubscription
        fields = ['category']