from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'group', 'text_preview', 'created_at')
    list_filter = ('group', 'created_at')
    search_fields = ('sender__username', 'text', 'group__name')

    def text_preview(self, obj):
        return obj.text[:50]
    text_preview.short_description = 'Message'
