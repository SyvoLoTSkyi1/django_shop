from django import forms
from feedbacks.models import Feedback


class FeedbackModelForm(forms.ModelForm):
    contact_info = forms.CharField(label="Contact Info", disabled=True)

    class Meta:
        model = Feedback
        fields = ('contact_info', 'text', 'rating')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contact_info'].disabled = True
        contact_info = user.email if user.email else user.phone
        self.fields['contact_info'].initial = contact_info
        self.instance.user = user


def check_text(text):

    clear_text = ''
    for i in text:
        if i.isalnum() or i == ' ':
            clear_text += i

    return clear_text
