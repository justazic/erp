from django.urls import path
from . import views
app_name = 'finance'
urlpatterns = [
  path('payment/create/', views.PaymentCreateView.as_view(), name='payment_create'),
  path('report/', views.FinanceReportView.as_view(), name='finance_report'),
  path('my-payments/', views.StudentPaymentHistoryView.as_view(), name='student_payments'),
]
