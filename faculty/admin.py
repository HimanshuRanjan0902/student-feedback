from django.contrib import admin
from .models import Faculty


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'employee_id',
        'department',
        'designation'
    )

    search_fields = (
        'name',
        'employee_id'
    )

    list_filter = (
        'department',
    )