from django.contrib import admin
from django.db.models import *
from .models import *

# Register your models here.
admin.site.register(Department)
admin.site.register(StudentId)
admin.site.register(Student)


class SubjectMarksAdmin(admin.ModelAdmin):
    list_display = ["student", "subject", "marks"]


admin.site.register(SubjectMarks, SubjectMarksAdmin)


class ReportCardAdmin(admin.ModelAdmin):
    list_display = [
        "student",
        "student_rank",
        "total_marks",
        "date_of_report_generation",
    ]

    def total_marks(self, obj):
        subject_marks = SubjectMarks.objects.filter(student=obj.student)
        marks = subject_marks.aggregate(marks=Sum("marks"))
        return marks["marks"]


admin.site.register(ReportCard, ReportCardAdmin)
