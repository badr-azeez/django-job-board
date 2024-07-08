from django import forms
from .models import CommentModel

class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(
        attrs={
            'class':'',
            'placeholder':'Write Comment',
            'minLength':3,
            'maxLength':250,
            'rows':5,
            'cols':20
            }
    ))
    class Meta:
        model = CommentModel
        fields = ['comment']

