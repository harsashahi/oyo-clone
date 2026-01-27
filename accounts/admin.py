from django.contrib import admin
from .models import (HotelUser, HotelVendor, Hotel, HotelImages, HotelManager, 
                     Ameneties, Room, Booking, Payment, Review)

@admin.register(HotelUser)
class HotelUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_verified', 'is_active')
    list_filter = ('is_verified', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'phone_number')

@admin.register(HotelVendor)
class HotelVendorAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_verified', 'is_active')
    list_filter = ('is_verified', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'phone_number')

@admin.register(Ameneties)
class AmenetiesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class HotelImagesInline(admin.TabularInline):
    model = HotelImages
    extra = 1

@admin.register(HotelImages)
class HotelImagesAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'created_at')
    list_filter = ('hotel', 'created_at')
    search_fields = ('hotel__hotel_name',)
    ordering = ('-created_at',)

class HotelManagerInline(admin.TabularInline):
    model = HotelManager
    extra = 1

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('hotel_name', 'hotel_location', 'hotel_offer_price', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured', 'created_at')
    search_fields = ('hotel_name', 'hotel_location', 'hotel_slug')
    prepopulated_fields = {'hotel_slug': ('hotel_name',)}
    inlines = [HotelImagesInline, HotelManagerInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('hotel_name', 'hotel_slug', 'hotel_owner', 'hotel_description', 'hotel_location')
        }),
        ('Pricing', {
            'fields': ('hotel_price', 'hotel_offer_price')
        }),
        ('Amenities', {
            'fields': ('ameneties',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
    )

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room_number', 'room_type', 'capacity', 'price_per_night', 'is_available')
    list_filter = ('room_type', 'is_available', 'hotel')
    search_fields = ('room_number', 'hotel__hotel_name')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'hotel', 'check_in_date', 'check_out_date', 'status', 'total_price')
    list_filter = ('status', 'check_in_date', 'created_at')
    search_fields = ('user__username', 'hotel__hotel_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount', 'payment_status', 'created_at')
    list_filter = ('payment_status', 'created_at')
    search_fields = ('transaction_id', 'booking__id')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('booking__id', 'booking__user__username')
