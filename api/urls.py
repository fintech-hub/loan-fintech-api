from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.test),
    path('clients/', views.ClientCreateView.as_view(), name='clients'),
    path('client/<int:client_id>/', views.ClientView.as_view()),
    path('loans/', views.LoanCreateView.as_view(), name='loans'),
    path('loans/<int:loan_id>/payments/', views.PaymentCreateView.as_view(), name='payments'),
    path('loans/<int:loan_id>/balance/', views.BalanceView.as_view()),
]
