from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-transaction/', views.create_transaction, name='create_transaction'),
    path('transaction_history/', views.transaction_history, name='transaction_history'),
    #path('transaction-history/<int:user_id>/', views.transaction_history, name='transaction_history'),
    path('update-transaction-status/', views.update_transaction_status, name='update_transaction_status'),
    #path('update-transaction-status/<int:transaction_id>/', views.update_transaction_status, name='update_transaction_status'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]
