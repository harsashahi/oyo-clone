import os
import django
os.chdir('c:\\ALL\\OYO clone\\oyo_clone')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oyo_clone.settings')
django.setup()

from django.test import Client
from accounts.models import Hotel

client = Client()

# Get a hotel slug
hotel = Hotel.objects.filter(hotel_images__isnull=False).first()
if hotel:
    print(f"Testing hotel: {hotel.hotel_name}")
    print(f"Slug: {hotel.hotel_slug}\n")
    
    url = f'/hotel/{hotel.hotel_slug}/'
    response = client.get(url)
    
    print(f"Status Code: {response.status_code}\n")
    
    # Get the HTML content
    html = response.content.decode('utf-8')
    
    # Find image tags
    import re
    img_tags = re.findall(r'<img[^>]*src="([^"]*)"[^>]*>', html)
    
    print(f"Found {len(img_tags)} img tags:\n")
    for img_url in img_tags[:5]:
        print(f"  - {img_url}")
    
    # Check if media URL is in HTML
    print(f"\n'/media/' in HTML: {'/media/' in html}")
    
    # Show context data
    if response.context:
        print(f"\nContext 'images' count: {response.context.get('images', {}).count() if response.context.get('images') else 0}")
