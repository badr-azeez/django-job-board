from django.urls import path
from . import views
app_name = 'jobs'

urlpatterns = [
    path('',views.jobs_list,name='jobs'),
    path('add',views.add_job,name='add_job'),
    path("applied-jobs", views.AppliedJobsList.as_view(), name="applied_jobs"),
    path("user-jobs", views.UserJobsList.as_view(), name="user_jobs"),
    path('<slug:slug>/edit',views.JobUpdate.as_view(),name='job_update'),
    path('<slug:slug>/delete',views.JobDelete.as_view(),name='job_delete'),
    path('<slug:slug>/applicants_users',views.ApplicantsUsersJobList.as_view(),name='applicants_users'),
    path('<slug:slug>/applicants_non_users',views.ApplicantsNonUsersJobList.as_view(),name='applicants_non_users'),
    path('<slug:slug>',views.job_details,name='job_details'),
]
