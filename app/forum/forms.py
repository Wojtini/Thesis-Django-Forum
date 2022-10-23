from captcha.fields import CaptchaField
from django import forms

from forum.models import Category


class BaseForm(forms.Form):
    captcha = CaptchaField()


class EntryForm(BaseForm):
    content = forms.CharField(label="text", max_length=500, widget=forms.Textarea)
    files = forms.FileField(
        label="attached files",
        widget=forms.ClearableFileInput(
            attrs={'multiple': True}
        ),
        required=False,
    )


class CategoryForm(BaseForm):
    name = forms.CharField(label="Category Name", max_length=30)


class ThreadForm(BaseForm):
    title = forms.CharField(label="Thread title", max_length=50)
    description = forms.CharField(label="Description", max_length=200, widget=forms.Textarea)
    category = forms.ModelChoiceField(queryset=Category.objects.all().order_by("name"), required=False)
    indexed = forms.BooleanField(required=False, initial=True)
