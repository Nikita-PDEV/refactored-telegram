from pathlib import Path  

# Путь к вашему проекту  
BASE_DIR = Path(__file__).resolve().parent.parent  

# SECURITY WARNING: don't run with debug turned on in production!  
DEBUG = True  

ALLOWED_HOSTS = []  

SECRET_KEY = 'ваш_секретный_ключ_здесь'
# Application definition  
INSTALLED_APPS = [  
    'django.contrib.admin',  
    'django.contrib.auth',  
    'django.contrib.contenttypes',  
    'django.contrib.sessions',  
    'django.contrib.messages',  
    'django.contrib.staticfiles',  
    'articles',    
]  

MIDDLEWARE = [  
    'django.middleware.security.SecurityMiddleware',  
    'django.contrib.sessions.middleware.SessionMiddleware',  
    'django.middleware.common.CommonMiddleware',  
    'django.middleware.csrf.CsrfViewMiddleware',  
    'django.contrib.auth.middleware.AuthenticationMiddleware',  
    'django.contrib.messages.middleware.MessageMiddleware',  
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  
]  

ROOT_URLCONF = 'news_portal.urls'  

# templates settings  
TEMPLATES = [  
    {  
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  
        'DIRS': [],  # Папка для дополнительных шаблонов 
        'APP_DIRS': True,    
        'OPTIONS': {  
            'context_processors': [  
                'django.template.context_processors.debug',  
                'django.template.context_processors.request',  
                'django.contrib.auth.context_processors.auth',  
                'django.contrib.messages.context_processors.messages',  
            ],  
        },  
    },  
]

CELERY_BROKER_URL = 'redis://localhost:6379/0'  

LOGIN_URL = '/accounts/login/'  # Путь к странице входа  
LOGIN_REDIRECT_URL = '/'  # URL, на который пользователи перенаправляются после входа  
LOGOUT_REDIRECT_URL = '/'  # URL, на который пользователи перенаправляются после выхода 

WSGI_APPLICATION = 'news_portal.wsgi.application'  

# Database  
DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.sqlite3',  
        'NAME': BASE_DIR / 'db.sqlite3',  
    }  
}  

# Password validation  
AUTH_PASSWORD_VALIDATORS = [  
    {  
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  
    },  
    {  
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  
    },  
    {  
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  
    },  
    {  
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  
    },  
]  

LANGUAGE_CODE = 'en-us'  

TIME_ZONE = 'UTC'  

USE_I18N = True  

USE_L10N = True  

USE_TZ = True  

STATIC_URL = '/static/'  

# Email settings  
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587  
EMAIL_USE_TLS = True  
EMAIL_HOST_USER = 'nikitavaul228556@gmail.com'  
EMAIL_HOST_PASSWORD = 'mgtjrraubuajpeal'  
DEFAULT_FROM_EMAIL = 'your_email@gmail.com'  