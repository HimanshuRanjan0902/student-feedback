from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse

from departments.models import Department
from faculty.models import Faculty


class StudentProfile(models.Model):
    """Extra information attached to a student's user account."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
    )
    roll_number = models.CharField(max_length=30, unique=True)
    department = models.CharField(max_length=100, blank=True)
    year_of_study = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text='Current year of study (1, 2, 3, 4)',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['roll_number']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.roll_number})"


class Category(models.Model):
    """Feedback Category"""

    name = models.CharField(max_length=80, unique=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Subject(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    semester = models.PositiveSmallIntegerField()

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="subjects"
    )

    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name="subjects"
    )

    class Meta:
        ordering = ["semester", "name"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Feedback(models.Model):

    STATUS_PENDING = "pending"
    STATUS_REVIEWED = "reviewed"
    STATUS_RESOLVED = "resolved"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_REVIEWED, "Reviewed"),
        (STATUS_RESOLVED, "Resolved"),
    ]

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="feedback_entries",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="feedback_entries",
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="feedback_entries",
    )

    teaching_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
    )

    communication_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
    )

    knowledge_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
    )

    behaviour_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
    )

    overall_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
    )

    message = models.TextField()

    is_anonymous = models.BooleanField(default=False)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    admin_response = models.TextField(blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.subject.name} - {self.student.username}"

    def get_absolute_url(self):
        return reverse("feedback:feedback_detail", args=[self.pk])

    @property
    def display_name(self):
        if self.is_anonymous:
            return "Anonymous Student"
        return self.student.get_full_name() or self.student.username

    @property
    def average_rating(self):
        return round(
            (
                self.teaching_rating +
                self.communication_rating +
                self.knowledge_rating +
                self.behaviour_rating +
                self.overall_rating
            ) / 5,
            1,
        )