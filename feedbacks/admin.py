from django.contrib import admin


from feedbacks.models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'rating', 'created_at',)
    list_filter = ('created_at', )
