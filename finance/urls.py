from django.urls import path
from .views import PaymentCreateView, FinanceReportView

urlpatterns = [
    path('payment/create/', PaymentCreateView.as_view(), name='payment_create'),
    path('report/', FinanceReportView.as_view(), name='report'),
]
