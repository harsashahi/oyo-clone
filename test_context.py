import os
import django
os.chdir('c:\\ALL\\OYO clone\\oyo_clone')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oyo_clone.settings')
django.setup()

from django.test import Client

client = Client()

# Test home page
response = client.get('/')

if response.context:
    featured = response.context.get('featured_hotels')
    all_hotels = response.context.get('hotels')
    
    print("FEATURED HOTELS:")
    if featured:
        for h in featured:
            print(f"  - {h.hotel_name} ({h.hotel_images.count()} images)")
    
    print(f"\nALL HOTELS (excluding featured):")
    if all_hotels:
        print(f"Total: {all_hotels.count()}")
        for h in all_hotels:
            img_count = h.hotel_images.count()
            status = "✓" if img_count > 0 else "✗"
            print(f"  {status} {h.hotel_name} ({img_count} images)")
