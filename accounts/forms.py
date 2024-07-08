from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ProfileModel , ExperienceModel


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = ['country','phone_number','birth_day','website','image','cv_file','bio']
        widgets = {
            'birth_day':forms.DateInput(attrs={'type':'date'}),
            'cv_file':forms.FileInput(attrs={'accept':'.pdf'})
        }

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = ExperienceModel
        fields = ['skill','level','description','start_at']
        widgets = {
            'level' : forms.NumberInput(attrs={
                'type':'number',
                'min':'1',
                'max':'100'
                }),
            'description': forms.Textarea(attrs={
                'rows':'3',
                'cols':'3'
            }),
            'start_at' : forms.DateInput(attrs={'type':'date'})
        }