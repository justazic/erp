from django.contrib import admin
from .models import Payment
import unfold
# Register your models here.

@admin.register(Payment)
class PaymentAdmin(unfold.admin.ModelAdmin):
    list_display = ('student', 'amount', 'payment_type', 'status', 'due_date', 'paid_date', 'created_at', 'updated_at')
    list_filter = ('status', 'payment_type', 'method', 'due_date')
    search_fields = ('student__user__username', 'reference_number')
    readonly_fields = ('created_at', 'updated_at', 'reference_number')
    fieldsets = (
        ('Payment Information', {
            'fields': ('student', 'amount', 'payment_type', 'reference_number')
        }),
        ('Dates', {
            'fields': ('due_date', 'paid_date')
        }),
        ('Payment Status', {
            'fields': ('status', 'method', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
