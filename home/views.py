from django.shortcuts import render
from django.views.generic import View
from jobs.models import CategoryJobModel , JobsModel
from django_countries import countries
from django.db.models import Count
# Create your views here.

class Home(View):
    def get(self,request):
        jobs = JobsModel.objects.prefetch_related('apply_not_users','apply_users')
        categories = CategoryJobModel.objects.all()
        categories_details = jobs.values('category__id','category__name').annotate(category_count=Count('category__name'))[:8]

        top_6_jobs = jobs.values('title','job_type','country','published_at','slug').annotate(users_count=Count('apply_users')).order_by('-users_count')[0:6]
        for job in top_6_jobs:
            job['country'] = dict(countries).get(job['country'])
        
        context = {
            'jobs_count' : jobs.count(),
            'countries':countries,
            'categories':categories,
            'categories_details':list(categories_details),
            'top_6_jobs':top_6_jobs
        }
        return render(request,'home/home.html',context)