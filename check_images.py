import os
import django
os.chdir('c:\\ALL\\OYO clone\\oyo_clone')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oyo_clone.settings')
django.setup()

from accounts.models import Hotel, HotelImages

# Get a hotel with images
hotel = Hotel.objects.filter(hotel_images__isnull=False).first()
if hotel:
    print(f"Hotel: {hotel.hotel_name}")
    images = hotel.hotel_images.all()
    print(f"Number of images: {images.count()}")
    for img in images[:3]:
        print(f"\n  Image: {img.image.name}")
        print(f"  URL: {img.image.url}")
        print(f"  Full path: {img.image.path}")
        print(f"  File exists: {os.path.exists(img.image.path)}")
else:
    print("No hotel with images found")
