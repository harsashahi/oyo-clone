import os
import django
os.chdir('c:\\ALL\\OYO clone\\oyo_clone')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oyo_clone.settings')
django.setup()

from accounts.models import Hotel

# Get all active hotels
hotels = Hotel.objects.filter(is_active=True).order_by('hotel_name')

print(f"Total active hotels: {hotels.count()}\n")
print("=" * 70)

hotels_with_images = 0
hotels_without_images = 0

print(f"{'Hotel Name':<40} {'Images':<10}")
print("=" * 70)

for hotel in hotels:
    img_count = hotel.hotel_images.count()
    if img_count > 0:
        hotels_with_images += 1
        status = f"✓ {img_count}"
    else:
        hotels_without_images += 1
        status = "✗ 0"
    
    print(f"{hotel.hotel_name:<40} {status:<10}")

print("=" * 70)
print(f"\nSummary:")
print(f"  Hotels WITH images: {hotels_with_images}")
print(f"  Hotels WITHOUT images: {hotels_without_images}")
