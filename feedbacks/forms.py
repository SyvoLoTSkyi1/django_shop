from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField()
    text = forms.CharField(widget=forms.Textarea)
