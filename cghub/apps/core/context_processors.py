from django.conf import settings as django_settings


def settings(request):
    return {
        'MANY_FILES': django_settings.MANY_FILES,
        'SUPPORT_EMAIL': django_settings.SUPPORT_EMAIL,
        'TOOLTIP_HOVER_TIME': django_settings.TOOLTIP_HOVER_TIME
    }
