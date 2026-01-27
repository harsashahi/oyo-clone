from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hotel/<slug:slug>/', views.hotel_detail, name='hotel_detail'),
    path('search/', views.hotel_search, name='hotel_search'),]