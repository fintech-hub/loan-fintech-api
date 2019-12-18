from django.urls import path
from . import views
from api.views import schema_view


app_name = 'api'

urlpatterns = [
    # default
    path('', views.test),

    # swagger doc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # routes
    path('clients/', views.ClientCreateView.as_view(), name='clients'),
    path('client/<int:client_id>/', views.ClientView.as_view()),
    path('loans/', views.LoanCreateView.as_view(), name='loans'),
    path('loans/<int:loan_id>/payments/', views.PaymentCreateView.as_view(), name='payments'),
    path('loans/<int:loan_id>/balance/', views.BalanceView.as_view()),
]
