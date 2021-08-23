from django.contrib import admin
from .models import Subject, Article

# Register your models here.

class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'science',
        'subject',
        'friendly_name',
    )


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'date',
        'rating',
        'price',
        'image',
    )


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Article, ArticleAdmin)