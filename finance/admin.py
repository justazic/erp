from django.contrib import admin
from .models import Payment

# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'method', 'created_at')
    list_filter = ('method',)