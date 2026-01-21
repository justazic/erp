from django.contrib import admin
from .models import Payment
from unfold.admin import ModelAdmin


@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display = ('student',
                    'enrollment',
                    'amount',
                    'payment_type',
                    'status',
                    'due_date',
                    'paid_date',
                    'created_at',
                    'updated_at')
    list_filter = ('status',
                   'payment_type',
                   'method',
                   'due_date',
                   'created_at')
    search_fields = ('student__user__username',
                     'enrollment__course__name',
                     'reference_number')
    readonly_fields = ('created_at', 'updated_at', 'reference_number')
    fieldsets = (
        ('Payment',
         {
             'fields': ('student',
                        'enrollment',
                        'amount',
                        'payment_type',
                        'reference_number'),
             }),
        ('Dates',
         {
             'fields': ('due_date',
                        'paid_date'),
             }),
        ('Status',
         {
             'fields': ('status',
                        'method',
                        'notes'),
             }),
        ('Timestamps',
         {
             'fields': ('created_at',
                        'updated_at'),
             'classes': ('collapse',),
             }),
    )

