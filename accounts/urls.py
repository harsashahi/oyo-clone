from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.user_register, name='user_register'),
    path('vendor-register/', views.vendor_register, name='vendor_register'),
    path('verify-otp/<int:user_id>/', views.verify_otp, name='verify_otp'),
    path('verify-otp-vendor/<int:user_id>/', views.verify_otp_vendor, name='verify_otp_vendor'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    
    # Bookings
    path('booking/create/<int:hotel_id>/', views.create_booking, name='create_booking'),
    path('booking/<int:booking_id>/payment/', views.booking_payment, name='booking_payment'),
    path('booking/<int:booking_id>/details/', views.booking_details, name='booking_details'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('booking/<int:booking_id>/review/', views.add_review, name='add_review'),
]
