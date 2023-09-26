from django.urls import path

from feedbacks.views import feedbacks, ContactView

urlpatterns = [
    path('feedbacks/', feedbacks, name='feedbacks'),
    path('contacts/', ContactView.as_view(), name='contacts'),
]
