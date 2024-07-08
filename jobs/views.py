from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import JobsModel ,ApplyUsersModel
from .forms import ApplyFrom , AddJobForm 
from .filters import JobFilter
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin ,UserPassesTestMixin

# Create your views here.

def jobs_list(request):
    jobs = JobsModel.objects.all()
    jobs_count = JobsModel.objects.all().count()
    jobs_filter = JobFilter(request.GET, queryset=jobs)
    paginator = Paginator(jobs_filter.qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'jobs':page_obj,
        'jobs_filter':jobs_filter,
        'jobs_count':jobs_count
    }
    return render(request,'jobs/jobs_list.html',context)

def job_details(request,slug):
    job_data = JobsModel.objects.prefetch_related('apply_users').get(slug=slug)
    if request.method  == 'POST':
        apply = request.POST.get('apply')
        if request.user.is_authenticated:
            if apply == 'unapply':
                ApplyUsersModel.objects.filter(user=request.user,job=job_data).delete()
            elif apply == 'apply':
                ApplyUsersModel.objects.create(user=request.user,job=job_data)
        else:
            form = ApplyFrom(request.POST,request.FILES)
            if form.is_valid():
                apply_data = form.save(commit=False)
                apply_data.job = job_data
                apply_data.save()
                return render(request,'jobs/message-non-users.html',context={'apply_data':apply_data})
            else:
                form = ApplyFrom()
        return redirect('jobs:job_details',slug=slug)
    else:
        form = ApplyFrom()

    context = {
        'job':job_data,
        'form':form,
        'user_apply': job_data.apply_users.filter(user=request.user.pk,job=job_data).exists()
    }
    return render(request,'jobs/job_details.html',context)

@login_required
def add_job(request):
    if request.method == 'POST':
        form = AddJobForm(request.POST,request.FILES)
        if form.is_valid():
            job_data = form.save(commit=False)
            job_data.user = request.user
            job_data.save()
            return redirect(reverse('jobs:jobs'))
    else:
        form = AddJobForm()
    context = {
        'form':form
    }
    return render(request,'jobs/add_job.html',context)


class OwnUserCheck(UserPassesTestMixin):

    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        return redirect('jobs:jobs')

class AppliedJobsList(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('login')

    model= ApplyUsersModel
    template_name = 'jobs/applied_jobs_list.html'
    paginate_by = 12
    def get_queryset(self):
        return ApplyUsersModel.objects.filter(user=self.request.user)

    

class UserJobsList(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('login')
    model = JobsModel
    template_name = 'jobs/job_user_list.html'
    paginate_by = 12
    def get_queryset(self):
        return JobsModel.objects.filter(user=self.request.user)

class JobUpdate(LoginRequiredMixin,OwnUserCheck,UpdateView):
    login_url = reverse_lazy('login')
    model = JobsModel
    form_class = AddJobForm

    def get_success_url(self):
        return reverse_lazy('jobs:job_details', kwargs={'slug': self.object.slug})
    

class JobDelete(LoginRequiredMixin,OwnUserCheck,DeleteView):
    model = JobsModel
    context_object_name = 'job'
    success_url = reverse_lazy('jobs:jobs')

class ApplicantsUsersJobList(LoginRequiredMixin,OwnUserCheck,DetailView):
    login_url = reverse_lazy('login')
    model = JobsModel
    template_name = 'jobs/applicants_users_jobs_list.html'
    paginate_by = 12

class ApplicantsNonUsersJobList(LoginRequiredMixin,OwnUserCheck,DetailView):
    login_url = reverse_lazy('login')
    model = JobsModel
    template_name = 'jobs/applicants_non_users_jobs_list.html'
    paginate_by = 12

