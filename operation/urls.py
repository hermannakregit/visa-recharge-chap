from django.urls import path

from operation import views 

urlpatterns = [
    path('client/<slug:slug>/', views.ClientOperations, name="client-operations"),
    path('create/<slug:slug>/', views.OperationCreate, name='create-operation'),
    path('payment/', views.OperationPayment, name="operation-payment"),
]