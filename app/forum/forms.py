from django import forms


class EntryForm(forms.Form):
    content = forms.CharField(label="text", max_length=200)
    image = forms.ImageField(label="attachment image", required=False)
