from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('new-account/', views.new_account, name='new_account'),
    path('creates-standard-accouts/', views.creates_standard_accouts, name='creates_standard_accouts'),
    path('account_statement/<int:account_id>/', views.account_statement, name='account_statement'),
    path('deposit/<int:account_id>/', views.deposit, name='deposit'),
    path('withdraw/<int:account_id>/', views.withdraw, name='withdraw'),
    path('transfer/', views.trasnfer, name='transfer')
]