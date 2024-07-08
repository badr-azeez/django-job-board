from django.contrib import admin
from django.urls import reverse
from .models import ProfileModel , ExperienceModel
from django.utils.html import format_html
from advanced_filters.admin import AdminAdvancedFiltersMixin


# Register your models here.

@admin.register(ExperienceModel)
class Experience(AdminAdvancedFiltersMixin,admin.ModelAdmin):
    list_display = ('skill','user_link','level_colored','created_at')
    advanced_filter_fields = ('skill','user__username','level')
    list_per_page = 50
    search_fields = ('user__username','skill')
    date_hierarchy = 'created_at'

    def level_colored(self,obj):
        if obj.level in range(76,101):
            color_code = "lawngreen"
        elif obj.level in range(50,76):
            color_code = 'yellow'
        elif obj.level in range(1,50):
            color_code = 'orangered'
        else:
            color_code = 'white'
        html = f"<div style='color:{color_code}'>{obj.level}</div>"
        return format_html(html)
    
    def user_link(self,obj):
        url = reverse('accounts:profile_username', kwargs={'username':obj.user.username})
        return format_html(f"<a href='{url}'>{obj.user.first_name} {obj.user.last_name}</a>")

@admin.register(ProfileModel)
class Profile(AdminAdvancedFiltersMixin,admin.ModelAdmin):
    list_display = ('user_link','country','phone_number','birth_day')
    advanced_filter_fields = ('country','user__username','level')
    list_per_page = 50
    search_fields = ('user__username','country','phone_number')


    def user_link(self,obj):
        url = reverse('accounts:profile_username', kwargs={'username':obj.user.username})
        return format_html(f"<a href='{url}'>{obj.user.first_name} {obj.user.last_name}</a>")