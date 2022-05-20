from django.urls import path

from carte import views 

urlpatterns = [
    path('', views.CarteList, name="cartes"),
    path('<slug:slug>', views.CarteView, name="carte"),
    path('create/', views.CarteCreate, name="create-carte"),
    path('update/<slug:slug>/', views.CarteUpdate, name="update-carte"),
    path('delete/<slug:slug>/', views.CarteDelete, name="delete-carte"),
]