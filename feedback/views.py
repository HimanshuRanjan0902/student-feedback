import json
import csv
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from openpyxl import Workbook

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
)

from faculty.models import Faculty

from .forms import (
    StudentRegistrationForm,
    FeedbackForm,
    AdminResponseForm,
)

from .models import (
    Category,
    Feedback,
    Subject,
)
# =====================================================
# Helper Function
# =====================================================

def is_staff_user(user):
    return user.is_authenticated and user.is_staff


# =====================================================
# Authentication Views
# =====================================================

class StudentLoginView(LoginView):
    template_name = "feedback/login.html"
    redirect_authenticated_user = True


class StudentLogoutView(LogoutView):
    next_page = reverse_lazy("feedback:login")


class StudentRegisterView(CreateView):
    form_class = StudentRegistrationForm
    template_name = "feedback/register.html"
    success_url = reverse_lazy("feedback:redirect_after_login")

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)

        messages.success(
            self.request,
            "Registration successful. Welcome!"
        )

        return response


# =====================================================
# Redirect After Login
# =====================================================

@login_required
def redirect_after_login(request):

    if request.user.is_staff:
        return redirect("feedback:admin_dashboard")

    return redirect("feedback:student_dashboard")


# =====================================================
# Student Dashboard
@login_required
def student_dashboard(request):
    recent_feedback = (
        Feedback.objects.filter(student=request.user)
        .select_related("category", "subject")
        .order_by("-submitted_at")[:5]
    )

    total_feedback = Feedback.objects.filter(
        student=request.user
    ).count()

    context = {
        "recent_feedback": recent_feedback,
        "total_feedback": total_feedback,
    }

    return render(
        request,
        "feedback/student_dashboard.html",
        context,
    )
# =====================================================
# Submit Feedback
# =====================================================
@login_required
def submit_feedback(request):

    if request.method == "POST":

        form = FeedbackForm(request.POST)

        if form.is_valid():

            feedback = form.save(commit=False)
            feedback.student = request.user
            feedback.save()

            messages.success(
                request,
                "Your feedback has been submitted successfully."
            )

            return redirect("feedback:feedback_history")

    else:

        form = FeedbackForm()

    return render(
        request,
        "feedback/submit_feedback.html",
        {
            "form": form,
        },
        
    )
# =====================================================
# Feedback History
# =====================================================

@login_required
def feedback_history(request):

    feedbacks = (
        Feedback.objects.filter(student=request.user)
        .select_related(
            "category",
            "subject",
        )
        .order_by("-submitted_at")
    )

    context = {
        "feedbacks": feedbacks,
    }

    return render(
        request,
        "feedback/feedback_history.html",
        context,
    )


# =====================================================
# Feedback Detail
# =====================================================
@login_required
def feedback_detail(request, pk):

    feedback = get_object_or_404(
        Feedback.objects.select_related(
            "student",
            "category",
            "subject",
        ),
        pk=pk,
    )

    # Student can only view their own feedback
    if (
        not request.user.is_staff
        and feedback.student != request.user
    ):
        messages.error(
            request,
            "You do not have permission to view this feedback."
        )
        return redirect("feedback:student_dashboard")

    form = None

    # Admin Response
    if request.user.is_staff:

        if request.method == "POST":

            form = AdminResponseForm(
                request.POST,
                instance=feedback,
            )

            if form.is_valid():

                old_status = feedback.status

                feedback = form.save()

                # Send email only if status changed
                if old_status != feedback.status:

                    if feedback.student.email:

                        send_mail(
                            subject="Feedback Status Updated",
                            message=f"""
Hello {feedback.student.username},

Your feedback has been updated.

Subject: {feedback.subject}

Current Status: {feedback.get_status_display()}

Admin Response:
{feedback.admin_response}

Thank you.

Student Feedback System
""",
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[feedback.student.email],
                            fail_silently=False,
                        )

                messages.success(
                    request,
                    "Feedback updated successfully."
                )

                return redirect(
                    "feedback:feedback_detail",
                    pk=feedback.pk,
                )

        else:

            form = AdminResponseForm(
                instance=feedback,
            )

    context = {
        "feedback": feedback,
        "form": form,
    }

    return render(
        request,
        "feedback/feedback_detail.html",
        context,
    )
# =====================================================
# Admin Dashboard
# =====================================================

@user_passes_test(is_staff_user)
def admin_dashboard(request):

    feedbacks = (
        Feedback.objects.select_related(
            "student",
            "category",
            "subject",
        )
        .order_by("-submitted_at")
    )

    status = request.GET.get("status")
    category = request.GET.get("category")
    search = request.GET.get("q") or ""

    if status:
        feedbacks = feedbacks.filter(status=status)

    if category:
        feedbacks = feedbacks.filter(category_id=category)

    if search:
        feedbacks = feedbacks.filter(
            subject__name__icontains=search
        )

    # Statistics
    stats = {
        "total": Feedback.objects.count(),
        "pending": Feedback.objects.filter(
            status=Feedback.STATUS_PENDING
        ).count(),
        "reviewed": Feedback.objects.filter(
            status=Feedback.STATUS_REVIEWED
        ).count(),
        "resolved": Feedback.objects.filter(
            status=Feedback.STATUS_RESOLVED
        ).count(),
        "avg_rating": Feedback.objects.aggregate(
            avg=Avg("overall_rating")
        )["avg"] or 0,
    }

    # Monthly feedback chart
    monthly_feedback = (
        Feedback.objects
        .annotate(month=TruncMonth("submitted_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    months = [
        item["month"].strftime("%b")
        for item in monthly_feedback
    ]

    monthly_counts = [
        item["total"]
        for item in monthly_feedback
    ]

    # Rating distribution
    rating_counts = [
        Feedback.objects.filter(overall_rating=i).count()
        for i in range(1, 6)
    ]

    # Pagination
    paginator = Paginator(feedbacks, 10)
    page_number = request.GET.get("page")
    feedbacks = paginator.get_page(page_number)

    context = {
        "feedbacks": feedbacks,
        "stats": stats,
        "categories": Category.objects.all(),
        "status_choices": Feedback.STATUS_CHOICES,
        "selected_status": status,
        "selected_category": category,
        "search": search,

        # Chart data
        "months": months,
        "monthly_counts": monthly_counts,
        "rating_counts": rating_counts,
    }

    return render(
        request,
        "feedback/admin_dashboard.html",
        context,
    )


# =====================================================
# Reports
# =====================================================

@user_passes_test(is_staff_user)
def reports(request):

    by_category = (
        Feedback.objects.values("category__name")
        .annotate(
            total=Count("id"),
            average=Avg("overall_rating"),
        )
        .order_by("-total")
    )

    by_status = (
        Feedback.objects.values("status")
        .annotate(total=Count("id"))
        .order_by("status")
    )

    by_subject = (
        Feedback.objects.values("subject__name")
        .annotate(
            total=Count("id"),
            average=Avg("overall_rating"),
        )
        .order_by("-total")
    )

    chart_data = {
        "category_labels": [
            item["category__name"] or "Unknown"
            for item in by_category
        ],
        "category_counts": [
            item["total"]
            for item in by_category
        ],
        "status_labels": [
            dict(Feedback.STATUS_CHOICES)[item["status"]]
            for item in by_status
        ],
        "status_counts": [
            item["total"]
            for item in by_status
        ],
    }

    context = {
        "total_feedback": Feedback.objects.count(),
        "average_rating": Feedback.objects.aggregate(
            avg=Avg("overall_rating")
        )["avg"] or 0,
        "by_category": by_category,
        "by_subject": by_subject,
        "by_status": by_status,
        "chart_data": json.dumps(chart_data),
    }

    return render(
        request,
        "feedback/reports.html",
        context,
    )


# =====================================================
# Faculty Dashboard
# =====================================================

@user_passes_test(is_staff_user)
def faculty_dashboard(request):

    faculty_list = (
        Faculty.objects.select_related("department")
        .prefetch_related("subjects")
        .order_by("name")
    )

    context = {
        "faculty_list": faculty_list,
        "total_faculty": faculty_list.count(),
    }

    return render(
        request,
        "feedback/faculty_dashboard.html",
        context,
    )
@user_passes_test(is_staff_user)
def export_csv(request):

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="feedback.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "Student",
        "Category",
        "Subject",
        "Rating",
        "Status",
        "Submitted Date",
    ])

    feedbacks = Feedback.objects.select_related(
        "student",
        "category",
        "subject",
    )

    for fb in feedbacks:
        writer.writerow([
            fb.student.username,
            fb.category.name,
            fb.subject.name,
            fb.overall_rating,
            fb.status,
            fb.submitted_at.strftime("%d-%m-%Y"),
        ])

    return response
@user_passes_test(is_staff_user)
def export_excel(request):

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Student Feedback"

    sheet.append([
        "Student",
        "Category",
        "Subject",
        "Rating",
        "Status",
        "Submitted Date",
    ])

    feedbacks = Feedback.objects.select_related(
        "student",
        "category",
        "subject",
    )

    for fb in feedbacks:
        sheet.append([
            fb.student.username,
            fb.category.name,
            fb.subject.name,
            fb.overall_rating,
            fb.status,
            fb.submitted_at.strftime("%d-%m-%Y"),
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="feedback.xlsx"'

    workbook.save(response)

    return response
@user_passes_test(is_staff_user)
def export_pdf(request):

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="feedback.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)

    data = [[
        "Student",
        "Category",
        "Subject",
        "Rating",
        "Status",
    ]]

    feedbacks = Feedback.objects.select_related(
        "student",
        "category",
        "subject",
    )

    for fb in feedbacks:
        data.append([
            fb.student.username,
            fb.category.name,
            fb.subject.name,
            str(fb.overall_rating),
            fb.status,
        ])

    table = Table(data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))

    doc.build([table])

    return response