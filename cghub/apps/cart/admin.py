from django.contrib import admin

from .models import Analysis


class AnalysisAdmin(admin.ModelAdmin):
    list_display = ('analysis_id', 'last_modified',)


admin.site.register(Analysis, AnalysisAdmin)
