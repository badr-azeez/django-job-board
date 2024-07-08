from django.contrib import admin
from .models import ContactUsModel
# Register your models here.

@admin.register(ContactUsModel)
class ContactUs(admin.ModelAdmin):
    list_display = ('email','subject','created_at')
    search_fields = ('email','subject','created_at')
    list_per_page = 50
    date_hierarchy = 'created_at'