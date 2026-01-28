import os
import django
os.chdir('c:\\ALL\\OYO clone\\oyo_clone')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oyo_clone.settings')
django.setup()

from accounts.models import Hotel, HotelImages

# Get all hotels with images
hotels = Hotel.objects.filter(hotel_images__isnull=False).distinct()
print(f"Total hotels with images: {hotels.count()}\n")

for hotel in hotels[:3]:
    print(f"Hotel: {hotel.hotel_name}")
    print(f"  Slug: {hotel.hotel_slug}")
    images = hotel.hotel_images.all()
    print(f"  Total images: {images.count()}")
    for img in images[:2]:
        print(f"    - {img.image.name}")
        print(f"      File exists: {os.path.exists(img.image.path)}")
    print()
