from django.urls import path

from user import views 

urlpatterns = [
    path('', views.Login, name="login"),
    path('logout/', views.Logout, name="logout"),
    path('register/', views.RegisterUser, name="register"),

    path('users/', views.UserProfiles, name="profiles"),
    path('users/<slug:slug>/', views.UserProfile, name="profile"),

    path('clients/', views.Clients, name="clients"),
    path('clients/create/', views.ClientCreate, name="create-client"),
    path('clients/<slug:slug>/', views.ClientProfile, name="client-profile"),
    path('clients/update/<slug:slug>/', views.ClientUpdate, name="client-update"),
]