from django.contrib import admin

from .models import Exam, Exercise, Submission, UploadedFile


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ["__str__", "created_by", "created"]


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ["__str__", "exercise", "created_by", "created"]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ["__str__", "exam", "exercise", "created_by", "created"]


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ["__str__", "created_by", "file_type", "file"]
