from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from feedbacks.models import Feedback

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone')


class FeedbackSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(required=False, allow_null=False)

    class Meta:
        model = Feedback
        fields = '__all__'

    def validate_text(self, value):
        if 'http' in value:
            raise ValidationError("The 'text' field must not contain urls.")
        return value

    def create(self, validated_data):
        validated_data.update({'user': self.context['request'].user})
        instance = super().create(validated_data)
        return instance
