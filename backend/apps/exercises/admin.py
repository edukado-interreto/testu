from django.contrib import admin

from .models import Exam, Exercise, Submission, Tag, UploadedFile


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["__str__", "pk", "created", "modified"]


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ["__str__", "created_by", "searchable", "created"]
    list_filter = ["created_by"]
    search_fields = ["name", "description", "created_by__email", "created_by__username"]
    date_hierarchy = "created"


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ["__str__", "exercise", "created_by", "created"]
    list_filter = ["created_by"]
    date_hierarchy = "created"


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ["__str__", "exam", "exercise", "created_by", "created"]
    search_fields = ["guest", "exam__name", "exercise__name"]
    date_hierarchy = "created"


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ["__str__", "created_by", "file_type", "file"]
    list_filter = ["file_type", "created_by"]
    search_field = ["file_name"]
    date_hierarchy = "created"
