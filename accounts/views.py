from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.utils import timezone
import random
import string
import uuid
from .forms import (UserRegistrationForm, UserLoginForm, OTPVerificationForm, 
                    VendorRegistrationForm, BookingForm, ReviewForm, PaymentForm)
from .models import (HotelUser, HotelVendor, Booking, Review, Payment, Hotel, Room)
from home.models import Hotel as HomeHotel


def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))


def send_otp_email(email, otp):
    """Send OTP to user email"""
    subject = "OTP Verification for OYO Clone"
    message = f"Your OTP for email verification is: {otp}\n\nThis OTP will expire in 10 minutes."
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


@require_http_methods(["GET", "POST"])
def user_register(request):
    """User registration view"""
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Generate and send OTP
            otp = generate_otp()
            user.otp = otp
            user.is_active = False  # Deactivate until OTP verification
            user.save()
            
            # Send OTP email
            if send_otp_email(user.email, otp):
                messages.success(request, "OTP sent to your email. Please verify to activate your account.")
                return redirect('verify_otp', user_id=user.id)
            else:
                user.delete()
                messages.error(request, "Failed to send OTP. Please try again.")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form, 'user_type': 'customer'})


@require_http_methods(["GET", "POST"])
def vendor_register(request):
    """Vendor registration view"""
    if request.method == "POST":
        form = VendorRegistrationForm(request.POST)
        if form.is_valid():
            vendor = form.save(commit=False)
            # Generate and send OTP
            otp = generate_otp()
            vendor.otp = otp
            vendor.is_active = False
            vendor.save()
            
            # Send OTP email
            if send_otp_email(vendor.email, otp):
                messages.success(request, "OTP sent to your email. Please verify to activate your account.")
                return redirect('verify_otp_vendor', user_id=vendor.id)
            else:
                vendor.delete()
                messages.error(request, "Failed to send OTP. Please try again.")
    else:
        form = VendorRegistrationForm()
    
    return render(request, 'register.html', {'form': form, 'user_type': 'vendor'})


@require_http_methods(["GET", "POST"])
def verify_otp(request, user_id):
    """OTP verification for users"""
    try:
        user = HotelUser.objects.get(id=user_id)
    except HotelUser.DoesNotExist:
        messages.error(request, "User not found!")
        return redirect('user_register')
    
    if user.is_active:
        messages.info(request, "Your account is already verified!")
        return redirect('login')
    
    if request.method == "POST":
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            if entered_otp == user.otp:
                user.is_active = True
                user.is_verified = True
                user.otp = None
                user.save()
                messages.success(request, "Your account has been verified! You can now login.")
                return redirect('login')
            else:
                messages.error(request, "Invalid OTP! Please try again.")
    else:
        form = OTPVerificationForm()
    
    return render(request, 'otp_auth.html', {'form': form, 'user': user})


@require_http_methods(["GET", "POST"])
def verify_otp_vendor(request, user_id):
    """OTP verification for vendors"""
    try:
        vendor = HotelVendor.objects.get(id=user_id)
    except HotelVendor.DoesNotExist:
        messages.error(request, "Vendor not found!")
        return redirect('vendor_register')
    
    if vendor.is_active:
        messages.info(request, "Your account is already verified!")
        return redirect('login')
    
    if request.method == "POST":
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            if entered_otp == vendor.otp:
                vendor.is_active = True
                vendor.is_verified = True
                vendor.otp = None
                vendor.save()
                messages.success(request, "Your vendor account has been verified! You can now login.")
                return redirect('login')
            else:
                messages.error(request, "Invalid OTP! Please try again.")
    else:
        form = OTPVerificationForm()
    
    return render(request, 'otp_auth.html', {'form': form, 'user': vendor})


@require_http_methods(["GET", "POST"])
def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Try to authenticate as HotelUser
            try:
                user = HotelUser.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f"Welcome back, {user.username}!")
                    return redirect('home')
            except HotelUser.DoesNotExist:
                pass
            
            # Try to authenticate as HotelVendor
            try:
                vendor = HotelVendor.objects.get(email=email)
                vendor = authenticate(request, username=vendor.username, password=password)
                if vendor is not None:
                    login(request, vendor)
                    messages.success(request, f"Welcome back, {vendor.username}!")
                    return redirect('vendor_dashboard')
            except HotelVendor.DoesNotExist:
                pass
            
            messages.error(request, "Invalid email or password!")
    else:
        form = UserLoginForm()
    
    return render(request, 'login.html', {'form': form})


@login_required(login_url='login')
def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('home')


@login_required(login_url='login')
def user_profile(request):
    """User profile view"""
    if isinstance(request.user, HotelVendor):
        return redirect('vendor_dashboard')
    
    user_bookings = Booking.objects.filter(user=request.user)
    context = {
        'user': request.user,
        'bookings': user_bookings,
        'total_bookings': user_bookings.count(),
        'total_spent': sum(b.total_price for b in user_bookings if b.status != 'cancelled'),
    }
    return render(request, 'profile.html', context)


# Booking Views
@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def create_booking(request, hotel_id):
    """Create a booking for a hotel"""
    hotel = get_object_or_404(Hotel, id=hotel_id, is_active=True)
    
    # Check if user is a HotelUser
    if not isinstance(request.user, HotelUser):
        messages.error(request, "Only customers can make bookings!")
        return redirect('hotel_detail', slug=hotel.hotel_slug)
    
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.hotel = hotel
            
            # Calculate total price
            nights = booking.get_number_of_nights()
            booking.total_price = nights * hotel.hotel_offer_price
            
            booking.save()
            messages.success(request, "Booking created! Please proceed to payment.")
            return redirect('booking_payment', booking_id=booking.id)
    else:
        form = BookingForm()
    
    context = {
        'form': form,
        'hotel': hotel,
    }
    return render(request, 'booking/create_booking.html', context)


@login_required(login_url='login')
def booking_payment(request, booking_id):
    """Payment page for a booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Check if payment already exists
    payment = Payment.objects.filter(booking=booking, payment_status='completed').first()
    if payment:
        messages.info(request, "This booking has already been paid!")
        return redirect('booking_details', booking_id=booking.id)
    
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                payment = form.save(commit=False)
                payment.booking = booking
                payment.amount = booking.total_price
                payment.transaction_id = str(uuid.uuid4())
                payment.payment_status = 'completed'
                payment.save()
                
                booking.status = 'confirmed'
                booking.save()
                
                messages.success(request, "Payment successful! Your booking is confirmed.")
                return redirect('booking_details', booking_id=booking.id)
    else:
        form = PaymentForm()
    
    context = {
        'form': form,
        'booking': booking,
    }
    return render(request, 'booking/payment.html', context)


@login_required(login_url='login')
def booking_details(request, booking_id):
    """View booking details"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    payment = Payment.objects.filter(booking=booking).first()
    review = Review.objects.filter(booking=booking).first()
    
    context = {
        'booking': booking,
        'payment': payment,
        'review': review,
    }
    return render(request, 'booking/booking_details.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status == 'cancelled':
        messages.info(request, "This booking is already cancelled!")
        return redirect('booking_details', booking_id=booking.id)
    
    if booking.status in ['checked_in', 'checked_out']:
        messages.error(request, "Cannot cancel checked-in or checked-out bookings!")
        return redirect('booking_details', booking_id=booking.id)
    
    booking.status = 'cancelled'
    booking.save()
    
    messages.success(request, "Booking cancelled successfully!")
    return redirect('user_profile')


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def add_review(request, booking_id):
    """Add a review for a booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status not in ['checked_out', 'completed']:
        messages.error(request, "You can only review completed bookings!")
        return redirect('booking_details', booking_id=booking.id)
    
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.save()
            messages.success(request, "Thank you for your review!")
            return redirect('booking_details', booking_id=booking.id)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'booking': booking,
    }
    return render(request, 'booking/add_review.html', context)
