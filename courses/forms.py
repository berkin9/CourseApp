from django import forms
from django.forms import SelectMultiple, TextInput, Textarea

from courses.models import Course, Category

class CourseCreateForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    imageUrl = forms.CharField()
    slug = forms.SlugField()
    isActive = forms.BooleanField()
    

class CourseEditForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title','description','imageUrl','slug','categories','isActive')
        labels = {
            'title':"kurs başlığı",
            'description':'açıklama'
        }
        widgets = {
            "title": TextInput(attrs={"class":"form-control"}),
            "description": Textarea(attrs={"class":"form-control"}),
            "imageUrl": TextInput(attrs={"class":"form-control"}),
            "slug": TextInput(attrs={"class":"form-control"}),
            "categories": SelectMultiple(attrs={"class":"form-control"})
        }
        error_messages = {
            "title": {
                "required":"kurs başlığı girmelisiniz.",
                "max_length": "maksimum 50 karakter girmelisiniz"
            },
            "description": {
                "required":"kurs açıklaması gereklidir."
            }
        }