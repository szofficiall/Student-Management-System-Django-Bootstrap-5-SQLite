from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *
from django.db.models import Q, Sum
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings


# Home Page
def home_page(request):
    return render(request, "app/home.html")


# aboutpage
def about_page(request):
    return render(request, "app/about.html")


# contact page
def contact_page(request):
    return render(request, "app/contact.html")


# login Page
def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not User.objects.filter(username=email).exists():
            messages.error(request, "User Does't Exists")
            return redirect("/login_page/")

        user = authenticate(request, username=email, password=password)

        if user is None:
            messages.error(request, "Invalid Password")
            return redirect("login_page")
        else:
            login(request, user)
            return redirect("student_view")
    return render(request, "app/login.html")


def signup_page(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")

        if len(password) < 8 or len(confirmpassword) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect("/signup_page/")

        if len(password and confirmpassword) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect("/signup_page/")

        if User.objects.filter(email=email).exists():
            messages.error(request, "User already exists.")
            return redirect("/signup_page/")

        User.objects.create_user(
            username=email,  # ya fullname agar username wahi rakhna hai
            first_name=fullname,
            email=email,
            password=password,
        )

        messages.success(request, "Congratulations! Account created successfully.")
        return redirect("/login_page/")

    return render(request, "app/signup.html")


@login_required(login_url="login_page")
def student_view(request):
    queryset = Student.objects.all()

    if request.GET.get("search"):
        search = request.GET.get("search")
        queryset = queryset.filter(
            Q(student_name__icontains=search)
            | Q(department__department__icontains=search)
            | Q(student__student_id__icontains=search)
        )
        # print(queryset")
    paginator = Paginator(queryset, 20)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "queryset": queryset,
        "page_obj": page_obj,
    }
    return render(request, "app/student_view.html", context)


def logout_page(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("home_page")


@login_required(login_url="login_page")
def student_result(request, student_id):
    queryset = SubjectMarks.objects.filter(student__student__student_id=student_id)

    total_marks = queryset.aggregate(total_marks=Sum("marks"))["total_marks"]
    student = queryset.first().student
    student_id = student.student
    context = {
        "queryset": queryset,
        "total_marks": total_marks,
        "student": student,
        "student_id": student_id,
    }
    return render(request, "app/studentResult.html", context)


@login_required(login_url="login_page")
def download_result_pdf(request, student_id):

    student = Student.objects.get(student__student_id=student_id)

    queryset = SubjectMarks.objects.filter(student=student)

    total_marks = queryset.aggregate(total=Sum("marks"))["total"] or 0

    total_subjects = queryset.count()

    total_possible_marks = total_subjects * 100

    percentage = (
        (total_marks / total_possible_marks) * 100 if total_possible_marks else 0
    )

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "Fail"

    response = HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = (
        f'attachment; filename="{student.student.student_id}_Result.pdf"'
    )

    pdf = canvas.Canvas(response, pagesize=A4)

    width, height = A4

    # Border
    pdf.setStrokeColor(HexColor("#1d4ed8"))
    pdf.setLineWidth(3)
    pdf.rect(1 * cm, 1 * cm, width - 2 * cm, height - 2 * cm)

    # Heading
    pdf.setFillColor(HexColor("#1d4ed8"))
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawCentredString(width / 2, height - 2 * cm, "SULTAN ACADEMY")

    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(width / 2, height - 2.8 * cm, "Student Result Card")

    # Student Info
    y = height - 4 * cm

    pdf.setFont("Helvetica-Bold", 12)

    pdf.drawString(2 * cm, y, f"Student Name : {student.student_name}")

    y -= 0.8 * cm

    pdf.drawString(
        2 * cm,
        y,
        f"Student ID : {student.student.student_id}",
    )

    y -= 0.8 * cm

    pdf.drawString(
        2 * cm,
        y,
        f"Department : {student.department.department}",
    )

    y -= 0.8 * cm

    pdf.drawString(2 * cm, y, f"Total Marks : {total_marks}")

    y -= 0.8 * cm

    pdf.drawString(
        2 * cm,
        y,
        f"Percentage : {round(percentage,2)} %",
    )

    y -= 0.8 * cm

    pdf.drawString(2 * cm, y, f"Grade : {grade}")

    # Table
    y -= 1.5 * cm

    pdf.setFillColor(HexColor("#2563eb"))

    pdf.rect(2 * cm, y, 15 * cm, 0.8 * cm, fill=1)

    pdf.setFillColor(HexColor("#ffffff"))

    pdf.drawString(2.3 * cm, y + 0.25 * cm, "Subject")

    pdf.drawString(13.5 * cm, y + 0.25 * cm, "Marks")

    pdf.setFillColor(HexColor("#000000"))

    y -= 0.8 * cm

    pdf.setFont("Helvetica", 11)

    for mark in queryset:

        pdf.drawString(
            2.3 * cm,
            y,
            mark.subject.subject_name,
        )

        pdf.drawString(
            13.8 * cm,
            y,
            str(mark.marks),
        )

        y -= 0.7 * cm

        if y < 4 * cm:
            pdf.showPage()
            y = height - 3 * cm

    # Signature
    y -= 1 * cm

    pdf.line(2 * cm, y, 6 * cm, y)
    pdf.line(12 * cm, y, 16 * cm, y)

    y -= 0.5 * cm

    pdf.drawString(2.5 * cm, y, "Teacher Signature")

    pdf.drawString(12.3 * cm, y, "Principal Signature")

    pdf.save()

    return response
