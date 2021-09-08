from django.contrib import admin
from django.db import models
from django.forms import Textarea
from .models import Academic


class AcademicAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'name',
        'username',
        'default_email',
    )


admin.site.register(Academic, AcademicAdmin)
