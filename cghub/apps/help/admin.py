from django.contrib import admin

from .models import HelpText


class HelpTextAdmin(admin.ModelAdmin):
    list_display = ('title', 'modified',)
    fields = ('title', 'slug', 'content',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(HelpText, HelpTextAdmin)
