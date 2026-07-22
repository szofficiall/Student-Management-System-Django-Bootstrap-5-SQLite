from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Department(models.Model):
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.department


class StudentId(models.Model):
    student_id = models.CharField(max_length=100)

    def __str__(self):
        return self.student_id


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    student = models.OneToOneField(
        StudentId, related_name="studentid", on_delete=models.CASCADE
    )
    department = models.ForeignKey(
        Department, related_name="departname", on_delete=models.CASCADE
    )
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField(unique=True)
    student_age = models.IntegerField(default=18)
    student_address = models.TextField()

    def __str__(self):
        return self.student_name

    class Meta:
        ordering = ["student_name"]
        verbose_name = "Student"
        verbose_name_plural = "Students"
        db_table = "student_table"


class Subject(models.Model):
    subject_name = models.CharField(max_length=100)

    def __str__(self):
        return self.subject_name

    class Meta:
        ordering = ["subject_name"]
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        db_table = "Subjects"


class SubjectMarks(models.Model):
    subject = models.ForeignKey(
        Subject, related_name="subject", on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        Student, related_name="student_subject", on_delete=models.CASCADE
    )
    marks = models.IntegerField()

    def __str__(self):
        return f"{self.student.student_name} {self.subject.subject_name}"

    class Meta:
        unique_together = ["subject", "student"]
        verbose_name = "Subject Marks"
        verbose_name_plural = "Subjects Marks"
        db_table = "student_marks"


class ReportCard(models.Model):
    student = models.ForeignKey(
        Student, related_name="student_report_car", on_delete=models.CASCADE
    )
    student_rank = models.IntegerField(max_length=100)
    date_of_report_generation = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ["student_rank", "date_of_report_generation"]
        ordering = ["student_rank"]
        verbose_name = "Student Rank"
        db_table = "student_rank"
