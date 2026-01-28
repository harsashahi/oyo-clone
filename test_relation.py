import os
import django
os.chdir('c:\\ALL\\OYO clone\\oyo_clone')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oyo_clone.settings')
django.setup()

from accounts.models import Hotel

# Check a few hotels
hotels = Hotel.objects.filter(is_active=True)[:5]

for hotel in hotels:
    print(f"Hotel: {hotel.hotel_name}")
    print(f"  has hotel_images.all(): {hotel.hotel_images.all()}")
    print(f"  Count: {hotel.hotel_images.count()}")
    
    if hotel.hotel_images.count() > 0:
        img = hotel.hotel_images.first()
        print(f"  First image object: {img}")
        print(f"  Image field value: {img.image}")
        print(f"  Image.url: {img.image.url}")
    print()
