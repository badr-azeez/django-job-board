from django.urls import path
from . import views
from django.contrib.auth import views as auth

from django.views.generic import TemplateView
app_name = "accounts"
urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('account_logout/',views.Logout.as_view(),name="account_logout"),
    path('profile/',views.profile,name='profile'),
    path('profile/edit',views.profile_edit,name='profile_edit'),
    path('profile/<str:username>',views.UserDetail.as_view(),name='profile_username'),
    path('experience/add',views.ExperienceCreate.as_view(),name='experience_add'),
    path('experience/<int:pk>/edit',views.ExperienceUpdate.as_view(),name='experience_edit'),
    path('experience/<int:pk>/delete',views.ExperienceDelete.as_view(),name='experience_delete'),
]
