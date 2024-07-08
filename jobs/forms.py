from django import forms
from django.conf import settings
from .models import ApplyModel , JobsModel , CategoryJobModel
from ckeditor.widgets import CKEditorWidget
import bleach
class ApplyFrom(forms.ModelForm):
    class Meta:
        model = ApplyModel
        fields = [
            'name',
            'email',
            'website',
            'cv_file',
            'cover_latter',
        ]
       
        widgets = {
            'cv_file': forms.FileInput(attrs={'accept': '.pdf'})
        }

class AddJobForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = JobsModel
        fields = "__all__"
        exclude = ('user','slug')


    def description_clean(self):
        description = self.changed_data('description','')
        return bleach.clean(description,tags=settings.BLEACH_ALLOWED_TAGS,attributes=settings.BLEACH_ALLOWED_ATTRIBUTES)