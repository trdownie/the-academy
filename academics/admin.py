from django.contrib import admin
from .models import Academic

# Register your models here.

class AcademicAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'username',
        'image',
        'level',
        'default_email',
    )


admin.site.register(Academic, AcademicAdmin)
