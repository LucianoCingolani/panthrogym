"""
settings.py
"""
import dj_database_url
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# ─── Rutas ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent


# ─── Seguridad ────────────────────────────────────────────────────────────────
SECRET_KEY = os.environ.get("SECRET_KEY", "cambia-esto-antes-de-subir-a-produccion")

DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = ["localhost", "panthrogym-production.up.railway.app"]

# ─── Aplicaciones ─────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic", 
    "members",
]


# ─── Middleware ───────────────────────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]


# ─── URLs y WSGI ──────────────────────────────────────────────────────────────
ROOT_URLCONF = "gimnasio.urls"
WSGI_APPLICATION = "gimnasio.wsgi.app"


# ─── Templates ────────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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


# ─── Base de datos ────────────────────────────────────────────────────────────
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}


# ─── Internacionalización ─────────────────────────────────────────────────────
LANGUAGE_CODE = "es-ar"
TIME_ZONE     = "America/Argentina/Buenos_Aires"
USE_I18N      = True
USE_TZ        = True


# ─── Archivos estáticos ───────────────────────────────────────────────────────
STATIC_URL  = "/static/"
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ─── Clave primaria por defecto ───────────────────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ─── Login / Logout ───────────────────────────────────────────────────────────
LOGIN_URL           = "/login/"
LOGIN_REDIRECT_URL  = "/"
LOGOUT_REDIRECT_URL = "/login/"

# ─── Trusted Origins ───────────────────────────────

CSRF_TRUSTED_ORIGINS = [
    "https://panthrogym-production.up.railway.app",
    "http://localhost:8000",
]