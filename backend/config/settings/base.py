from datetime import timedelta
from pathlib import Path

from decouple import AutoConfig, Config, Csv, RepositorySecret

from config.decouple import NamedEmail

config = Config(RepositorySecret()) if Path("/run/secrets/").exists() else AutoConfig()


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)

ADMINS = config("ADMINS", cast=Csv(NamedEmail()), default=None)

USE_I18N = True

USE_TZ = True
TIME_ZONE = "Europe/Bratislava"

AUTH_USER_MODEL = "core.User"
AUTHENTICATION_BACKENDS = ["apps.core.auth.EmailBackend"]

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USER_DISPLAY = lambda user: user.__str__()
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""

DEFAULT_FROM_EMAIL = "Testu team <noreply@testu.eu>"
SERVER_EMAIL = DEFAULT_FROM_EMAIL  # For mail_admins()
EMAIL_SUBJECT_PREFIX = ""  # Instead of "[Django] "

STATIC_URL = "/assets/static/"
STATIC_ROOT = config("STATIC_ROOT", default=str(BASE_DIR / "assets/static/"))
MEDIA_URL = "/assets/media/"
MEDIA_ROOT = config("MEDIA_ROOT", default=str(BASE_DIR / "assets/media/"))

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

SITE_ID = config("SITE_ID", cast=int, default=1)
USE_X_FORWARDED_HOST = True
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv(), default="")
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS", cast=Csv(), default="http://localhost"
)
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", cast=Csv(), default="")
CORS_ALLOW_ALL_ORIGINS = config("CORS_ALLOW_ALL_ORIGINS", cast=bool, default=False)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",  # migrate socialaccount zero
    "django.contrib.messages",
    "django_extensions",
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "corsheaders",
    "django.contrib.staticfiles",
    "apps.core",
    "apps.exercises",
    # allauth is at the end so that we can easily override its templates
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB", default="testu"),
        "USER": config("POSTGRES_USER", default="testu"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST", default="postgres"),
        "PORT": config("POSTGRES_PORT", cast=int, default=5432),
        "ATOMIC_REQUESTS": True,
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 300,
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
}
REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "jwt-access",
    "JWT_AUTH_REFRESH_COOKIE": "jwt-refresh",
    "USER_DETAILS_SERIALIZER": "apps.core.serializers.UserSerializer",
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

if SENDGRID_API_KEY := config("SENDGRID_API_KEY", default=None):
    INSTALLED_APPS += ["anymail"]
    EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
    ANYMAIL = {
        "SENDGRID_API_KEY": SENDGRID_API_KEY,
        "SENDGRID_API_URL": config(
            "SENDGRID_API_URL", default="https://api.sendgrid.com/v3/"
        ),
    }


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
