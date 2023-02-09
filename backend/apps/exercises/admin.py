from django.contrib import admin

try:
    from .models import Exercise as Sheet, UploadedFile
except ImportError:
    from .models import Sheet, UploadedFile


@admin.register(Sheet)
class SheetAdmin(admin.ModelAdmin):
    list_display = ["__str__", "created_by", "created"]


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ["__str__", "created_by", "file_type", "file"]
