import django_filters
from .models import JobsModel


class JobFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = JobsModel
        fields = ['title', 'description','experience','country' , 'job_type','category']