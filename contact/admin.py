from django.contrib import admin

from .models import ContactSubmission


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "budget", "created_at")
    list_filter = ("budget", "hear_about", "created_at")
    search_fields = ("full_name", "email", "phone", "company_name")
    readonly_fields = ("created_at",)
