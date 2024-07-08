from django.contrib import admin
from django.urls import reverse
from .models import BlogModel,CommentModel, TagModel ,CategoryModel
from django.utils.html import format_html
from advanced_filters.admin import AdminAdvancedFiltersMixin


# Register your models here.

@admin.register(BlogModel)
class Blog(AdminAdvancedFiltersMixin,admin.ModelAdmin):
    list_display = ('title','user_link','status','category','comments_enable','publish_date')
    search_fields = ('user__username','summary_text','full_text','title')
    advanced_filter_fields = ('user__username','comments_enable','publish_date','category','status','publish_date')
    list_per_page = 50
    date_hierarchy = 'publish_date'

    def save_model(self, request, obj, form, change):
        if not change: 
            obj.user = request.user 
        super().save_model(request, obj, form, change)

    def user_link(self,obj):
        url = reverse('accounts:profile_username', kwargs={'username':obj.user.username})
        return format_html(f"<a href='{url}'>{obj.user.first_name} {obj.user.last_name}</a>")



@admin.register(CommentModel)
class Comments(AdminAdvancedFiltersMixin,admin.ModelAdmin):
    list_display = ('comment','user_link','post','created_at')
    search_fields = ('comment','user__username','post__title')
    advanced_filter_fields = ('user__username','comment','created_at')
    list_per_page = 50
    date_hierarchy = 'created_at'

    def user_link(self,obj):
        url = reverse('accounts:profile_username', kwargs={'username':obj.user.username})
        return format_html(f"<a href='{url}'>{obj.user.first_name} {obj.user.last_name}</a>")

admin.site.register(TagModel)
admin.site.register(CategoryModel)

