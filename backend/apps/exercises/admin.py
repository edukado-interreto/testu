from django.contrib import admin

from .models import Sheet


@admin.register(Sheet)
class SheetAdmin(admin.ModelAdmin):
    list_display = ["__str__", "created_by", "created"]
