import os
import django
os.chdir('c:\\ALL\\OYO clone\\oyo_clone')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oyo_clone.settings')
django.setup()

from accounts.models import Hotel, HotelImages
from django.test import Client

# Test what the view returns
client = Client()

# Get a hotel with images
hotel = Hotel.objects.filter(hotel_images__isnull=False).first()
if hotel:
    print(f"\n=== TESTING HOTEL: {hotel.hotel_name} ===")
    print(f"Hotel slug: {hotel.hotel_slug}")
    print(f"Number of images: {hotel.hotel_images.count()}")
    
    for i, img in enumerate(hotel.hotel_images.all()[:2]):
        print(f"\n  Image {i+1}:")
        print(f"    - DB path: {img.image.name}")
        print(f"    - URL: {img.image.url}")
        print(f"    - File path: {img.image.path}")
        print(f"    - File exists: {os.path.exists(img.image.path)}")
    
    # Test the URL endpoint
    url = f'/hotel/{hotel.hotel_slug}/'
    print(f"\n=== TESTING URL: {url} ===")
    try:
        response = client.get(url)
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            print(f"Template: {[t.name for t in response.templates]}")
            print(f"Context keys: {response.context.keys() if response.context else 'No context'}")
            
            # Check if images are in context
            if 'images' in response.context:
                images_in_context = response.context['images']
                print(f"Images in context: {images_in_context.count()}")
                for img in images_in_context[:2]:
                    print(f"  - {img.image.url}")
            else:
                print("No 'images' in context!")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("No hotel found")
