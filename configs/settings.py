from pathlib import Path
from os.path import join
from environ import Env
from datetime import timedelta
from core.constants import DEFAULT_PAGE_NUMBER_LIST
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent
if Env().bool('DJANGO_READ_DOT_ENV_FILE',default=False):
    Env.read_env(join(BASE_DIR , '.env'))
    
env = Env()
SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG" , default=False)
ALLOWED_HOSTS = ['*']
TRIDY_APPS = [
    'rest_framework',
    'django_filters',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'corsheaders',
    'oauth2_provider',
]
PROJECT_APPS = [
    'users',
    'product',
    'core',
]
DJANGO_APPS = [  
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
INSTALLED_APPS = DJANGO_APPS + TRIDY_APPS + PROJECT_APPS
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'configs.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'configs.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env("DATABASE_NAME"),
        'USER' : env("DATABASE_USER"),
        'HOST' : env("DATABASE_HOST"),
        'PASSWORD' : env("DATABASE_PASSWORD"),
        'PORT' : env("DATABASE_PORT"),
        'ATOMIC_REQUESTS' : True,
        'TEST' : {
            'NAME' : "EclipseTest",
        }
    }
}
FIXTURE_DIRS = [
    BASE_DIR / "fixtures",
]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CACHES = {
    'default': {
        'BACKEND' : 'django_redis.cache.RedisCache',
        'LOCATION' : env("REDIS_URL"),
        'OPTIONS' : {
            'CLIENT_CLASS' : 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': False,
        },  
        'KEY_PREFIX': 'django_orm'
    },
}
if env.bool('REDIS_USE_PASSWORD', default=False):
    CACHES['default']['OPTIONS']['PASSWORD'] = env('REDIS_PASSWORD')
    
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
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.ScryptPasswordHasher',
]
SPECTACULAR_SETTINGS = {
    'TITLE': 'Eclipse API',
    'DESCRIPTION': 'Uma loja virtual',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR', 
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    'AUTHENTICATION_CLASS' : [
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'TOKEN_OBTAIN_SERIALIZER': 'users.serializers.AuthenticationSerializer',
}
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    
    'DEFAULT_PAGINATION_CLASS': 'core.ConfigsClass.DefaultPagination',
    'PAGE_SIZE' : DEFAULT_PAGE_NUMBER_LIST,
    
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/m',
        'user': '100/m',
    }
}
REST_FRAMEWORK.update(SIMPLE_JWT)
CORS_ALLOW_ALL_ORIGINS = True
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
LENGUAGES = [
    ('en' , 'English'),
    ('pt-br' , 'Português'),
]
LOCALE_PATHS = [
    join(BASE_DIR , 'locale')
]
STATIC_URL = "/static/"
STATIC_ROOT = join(BASE_DIR , 'static')
MEDIA_ROOT = join(BASE_DIR , 'media')
MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'users.User'
LOGIN_URL = reverse_lazy("auth:token_obtain_pair")