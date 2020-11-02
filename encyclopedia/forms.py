from django import forms

class NewPage(forms.Form):
    title = forms.CharField(required=True, label="Title")
    content = forms.CharField(required=True, label="Content", widget=forms.Textarea())