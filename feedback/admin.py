from django.contrib import admin
from .models import StudentProfile, Category, Subject, Feedback


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "roll_number", "department", "year_of_study")
    search_fields = ("user__username", "roll_number")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "department",
        "faculty",
        "semester",
    )
    list_filter = ("department", "semester")
    search_fields = ("code", "name")


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "subject",
        "overall_rating",
        "status",
        "submitted_at",
    )

    list_filter = (
        "status",
        "subject",
    )

    search_fields = (
        "student__username",
        "subject__name",
    )