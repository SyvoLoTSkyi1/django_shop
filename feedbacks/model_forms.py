from django import forms
from feedbacks.models import Feedback


class FeedbackModelForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ('text', 'rating')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.user = user


def check_text(text):

    clear_text = ''
    for i in text:
        if i.isalnum() or i in [' ', '.', ',', '-', ':', ';', '\n']:
            clear_text += i

    return clear_text
