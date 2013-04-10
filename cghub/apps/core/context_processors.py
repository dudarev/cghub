from django.conf import settings as django_settings


def settings(request):
    return {
        'MANY_FILES': django_settings.MANY_FILES,
    }
