from captcha.fields import CaptchaField
from django import forms

from Masquerade.settings import ENABLE_CAPTCHA_IN_FORMS


class DisplayNameForm(forms.Form):
    display_name = forms.CharField(label="display name", max_length=20)


class BaseForm(forms.Form):
    if ENABLE_CAPTCHA_IN_FORMS:
        captcha = CaptchaField()


class EntryForm(BaseForm):
    content = forms.CharField(
        label="Content",
        max_length=500,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "cols": 40
            }
        ),
        help_text="""
        Options: <br>
        #{entry_id} to create a link/reply. Example: (#13)<br>
        % to place file in specific place in entry.""",
    )
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
