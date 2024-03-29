from django.urls import path, include
from rest_framework import routers
from sgdapi.views import (
    AccountViewSet, AccountHolderViewSet, TransactionViewSet,
   AllTransactionsForAnAccountHolderView, AllTransactionsForAnAccountView,
   LogView, PhysicalAccountViewSet
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token

schema_view = get_schema_view(
   openapi.Info(
      title="SGD API",
      default_version='v1',
      description="Sistema de gerenciamento de dinheiro",
      terms_of_service="#",
      contact=openapi.Contact(email="janderson.m.araujo@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register('accounts', AccountViewSet, basename='Accounts')
router.register('physical_accounts', PhysicalAccountViewSet, basename='physical_accounts')
router.register('account-holders', AccountHolderViewSet, basename='Account-Holders')
router.register('transactions', TransactionViewSet, basename='Transactions')

urlpatterns = [
    path('', include(router.urls)),
    path('account/<str:pk>/transactions/', AllTransactionsForAnAccountView.as_view()),
    path('account-holder/<str:pk>/transactions/', AllTransactionsForAnAccountHolderView.as_view()),
    path('log/', LogView.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('token-auth/', obtain_auth_token)
]