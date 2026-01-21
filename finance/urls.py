from django.urls import path
from . import views

urlpatterns = [
  path('payment/create/', views.PaymentCreateView.as_view(), name='payment_create'),
  path('report/', views.FinanceReportView.as_view(), name='finance_report'),
]
