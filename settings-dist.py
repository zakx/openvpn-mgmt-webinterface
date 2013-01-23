# Django settings.

DEBUG = False

BASE_PATH = '/opt/purple/' # set this to your base path
DATABASES = {
    'default': {
        'NAME': BASE_PATH+'purple.sqlite3',
        'ENGINE': 'django.db.backends.sqlite3',
    }
}
SECRET_KEY = 'SET THIS TO A RANDOM STRING'
ADMINS = (
    ('Your Name', 'mail@example.com'),
)

# password for the openvpn management interface
OPENVPN_PASSWORD = "change me"

# delete the following three lines and you're done configuring
import sys
print "Please configure purple in settings.py."
sys.exit(0)

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = "sendmail.EmailBackend"
    SESSION_COOKIE_SECURE = True
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True

TEMPLATE_DEBUG = DEBUG
APP_URL = "app"
MEDIA_ROOT = BASE_PATH + 'media/'
MEDIA_URL = '/media/'
STATIC_ROOT = BASE_PATH + 'static/'
STATIC_URL = '/static/'
TEMPLATE_DIRS = (
    BASE_PATH + "templates",
)
MANAGERS = ADMINS
TIME_ZONE = 'Europe/Berlin'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
ADMIN_MEDIA_PREFIX = '/static/admin/'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
AUTH_PROFILE_MODULE = 'app.UserProfile'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'app',
    'south',
    'django_extensions',
)

# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
