from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from api import views
from api import api_view

urlpatterns = [

    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', views.user),

    path('fiche/', views.userFiche),
    path('user/operations/', views.getUserOperations),
    path('user/operations/<slug:slug>/', views.getUserOperation),
    path('user/cartes/', views.getUserCartes),
    path('user/cartes/<slug:slug>/', views.getUserCarte),
    path('cartes/', views.getAllCarte),

    path('operation/montant/', views.calculFrais),
    path('payment/', views.setPayment),

    #api user
    path('sales/add/', api_view.createClient),
    path('cards/all/', api_view.getAllCarte),
    path('clients/cards/', api_view.getClientsCards),

    path('operations/', api_view.getOperations),
    path('operations/actions/', api_view.operationActions),
    path('operations/history/', api_view.getOperationHistory),
    path('operations/<slug:slug>/', api_view.getOperation),

]
