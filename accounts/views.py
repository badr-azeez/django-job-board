from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login
from django.urls import reverse, reverse_lazy
from .forms import CreateUserForm ,UserForm,ProfileForm,ExperienceForm
from .models import ProfileModel,ExperienceModel
from django.views.generic import View , CreateView ,UpdateView, DeleteView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

def signup(request):

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user=  authenticate(username=username,password=password)
            login(request,user)
            return redirect('/accounts/profile')
    else:
        form = CreateUserForm()    

    context = {
        'form':form
    }
    return render(request,'registration/signup.html',context)


class Logout(View):
    def post(self,request,*args, **kwargs):
        if request.user:
            auth.logout(request)
        return redirect('jobs:jobs')


def password_done(request):
    return render(request,'registration/password_change_done.html')

@login_required
def profile(request):
    profile = ProfileModel.objects.get(user=request.user)
    experiences = ExperienceModel.objects.filter(user=request.user)
    context = {
        'profile':profile,
        'experiences':experiences
    }
    return render(request,'accounts/profile.html',context)

@login_required
def profile_edit(request):
    profile = ProfileModel.objects.get(user=request.user)
    if request.method == 'POST':
        userForm = UserForm(request.POST,request.FILES,instance=request.user)
        profileForm = ProfileForm(request.POST,request.FILES,instance=profile)
        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            print('hi')
            profile_data = profileForm.save(commit=False)
            profile_data.user= request.user
            profile_data.save()
            return redirect(reverse('accounts:profile'))
    else:
        userForm = UserForm(instance=request.user)
        profileForm = ProfileForm(instance=profile)

    context = {
        'userForm':userForm,
        'profileForm':profileForm
    }
    
    return render(request,'accounts/profile_edit.html',context)

class UserDetail(DetailView):
    model = User
    pk_url_kwarg = 'username'
    template_name = 'accounts/user_detail.html'
    def get_object(self):
        return User.objects.get(username=self.kwargs.get('username'))

class OwnUserCheck(UserPassesTestMixin):

    def test_func(self):
        return self.request.user == super().get_object().user
    
    def handle_no_permission(self):
        return redirect('accounts:profile')
    

class ExperienceLimit:
     def dispatch(self, request, *args, **kwargs):
        if self.request.user.experiences.count() >= 5:
            return redirect('accounts:profile')
        return super().dispatch(request, *args, **kwargs)

class ExperienceCreate(LoginRequiredMixin,ExperienceLimit,CreateView):
    login_url = reverse_lazy('login')
    model = ExperienceModel
    form_class = ExperienceForm
    success_url = reverse_lazy('accounts:profile')
    
    def form_valid(self, form):
        data = form.save(commit=False)
        data.user = self.request.user
        data.save()
        return super().form_valid(form)


class ExperienceUpdate(OwnUserCheck,UpdateView):
    model = ExperienceModel
    form_class = ExperienceForm
    success_url = reverse_lazy('accounts:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = True
        return context

class ExperienceDelete(OwnUserCheck,DeleteView):
    model = ExperienceModel
    success_url = reverse_lazy('accounts:profile')