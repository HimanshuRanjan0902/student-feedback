from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Feedback, StudentProfile


# ==========================
# Login Form
# ==========================

class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Username"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Password"
        })
    )


# ==========================
# Student Registration Form
# ==========================

class StudentRegistrationForm(UserCreationForm):

    roll_number = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )

    department = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )

    year_of_study = forms.IntegerField(
        min_value=1,
        max_value=4,
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        })
    )

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control"
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control"
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control"
        })
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "roll_number",
            "department",
            "year_of_study",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

            StudentProfile.objects.create(
                user=user,
                roll_number=self.cleaned_data["roll_number"],
                department=self.cleaned_data["department"],
                year_of_study=self.cleaned_data["year_of_study"],
            )

        return user


# ==========================
# Feedback Form
# ==========================

class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback

        fields = [
            "category",
            "subject",
            "teaching_rating",
            "communication_rating",
            "knowledge_rating",
            "behaviour_rating",
            "overall_rating",
            "message",
            "is_anonymous",
        ]

        widgets = {

            "category": forms.Select(attrs={
                "class": "form-select"
            }),

            "subject": forms.Select(attrs={
                "class": "form-select"
            }),

            "teaching_rating": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
                "max": 5
            }),

            "communication_rating": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
                "max": 5
            }),

            "knowledge_rating": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
                "max": 5
            }),

            "behaviour_rating": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
                "max": 5
            }),

            "overall_rating": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
                "max": 5
            }),

            "message": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Write your feedback..."
            }),

            "is_anonymous": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }


# ==========================
# Admin Response Form
# ==========================

class AdminResponseForm(forms.ModelForm):

    class Meta:
        model = Feedback

        fields = [
            "status",
            "admin_response",
        ]

        widgets = {

            "status": forms.Select(attrs={
                "class": "form-select"
            }),

            "admin_response": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Enter admin response..."
            }),
        }