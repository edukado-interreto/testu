from django.contrib import admin

from .models import Exercise, UploadedFile


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ["__str__", "created_by", "created"]


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ["__str__", "created_by", "file_type", "file"]
