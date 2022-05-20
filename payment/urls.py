from django.urls import path

from payment import views

urlpatterns = [

    path('notification/', views.notificationURl),
    path('notification/force/', views.forceNotificationURl),

    path('<slug:slug>/', views.PaymentPage, name="payment-page"),
    path('payment/<slug:slug>/', views.GetPayment, name="get-payment"),
]