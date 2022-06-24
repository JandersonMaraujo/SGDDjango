from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from sgdapi.views import AccountViewSet, AccountHolderViewSet, TransactionViewSet, AllTransactionsForAnAccountHolderView, AllTransactionsForAnAccountView

router = routers.DefaultRouter()
router.register('accounts', AccountViewSet, basename='Accounts')
router.register('account-holders', AccountHolderViewSet, basename='Account-Holders')
router.register('transactions', TransactionViewSet, basename='Transactions')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('account/<int:pk>/transactions/', AllTransactionsForAnAccountView.as_view()),
    path('account-holder/<str:pk>/transactions/', AllTransactionsForAnAccountHolderView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
