from django.contrib import admin
from .models import Academic

# Register your models here.

class AcademicAdmin(admin.ModelAdmin):
    list_display = (
        'image',
        'name',
        'username',
        'level',
    )


admin.site.register(Academic, AcademicAdmin)
