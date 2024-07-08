from django.contrib import admin
from django.urls import reverse

from django.utils.html import format_html

from advanced_filters.admin import AdminAdvancedFiltersMixin


# Register your models here.
from .models import JobsModel , CategoryJobModel ,ApplyModel , ApplyUsersModel

@admin.register(JobsModel)
class Job(AdminAdvancedFiltersMixin,admin.ModelAdmin):
    list_display = ('user_link','title','country','category','job_type','experience','vacancy','salary','published_at')
    advanced_filter_fields = ('user__username','title','country','category','job_type','experience','vacancy','salary')
    list_per_page = 50
    search_fields = ('user__username','title','country','job_type','category')
    date_hierarchy = 'published_at'


    def user_link(self,obj):
        url = reverse('accounts:profile_username', kwargs={'username':obj.user.username})
        return format_html(f"<a href='{url}'>{obj.user.first_name} {obj.user.last_name}</a>")
    

@admin.register(ApplyModel)
class ApplyNonUser(AdminAdvancedFiltersMixin,admin.ModelAdmin):
    list_display = ('job','name','email','created_at')
    advanced_filter_fields = ('job','name','email')
    search_fields = ('job','name','email','created_at')
    list_per_page = 50
    date_hierarchy = 'created_at'

@admin.register(ApplyUsersModel)
class ApplyUser(AdminAdvancedFiltersMixin,admin.ModelAdmin):
    list_display = ('job','user_link','created_at')
    advanced_filter_fields = ('user__username','job')
    search_fields = ('user__username','job','created_at')
    list_per_page = 50
    date_hierarchy = 'created_at'
    def user_link(self,obj):
        url = reverse('accounts:profile_username', kwargs={'username':obj.user.username})
        return format_html(f"<a href='{url}'>{obj.user.first_name} {obj.user.last_name}</a>")
    
admin.site.register(CategoryJobModel)