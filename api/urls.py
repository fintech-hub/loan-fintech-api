from django.urls import path
from . import views
from api.views import schema_view
from rest_framework_simplejwt import views as jwt_views


app_name = 'api'

urlpatterns = [

    # JWT Authentication
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

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
