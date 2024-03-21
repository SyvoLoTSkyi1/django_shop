from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.feedbacks.serializers import FeedbackSerializer
from feedbacks.models import Feedback


class FeedbacksViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]



