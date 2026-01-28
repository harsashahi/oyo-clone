import os
import django
os.chdir('c:\\ALL\\OYO clone\\oyo_clone')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oyo_clone.settings')
django.setup()

from django.test import Client

client = Client()

# Test a few image URLs directly
image_urls = [
    '/media/hotels/tiger%20mountain%20lodge.jpg',
    '/media/hotels/soaltee%20crowne%20plaza.jpg',
    '/media/hotels/annapurna%20boutique%20hotel.jpg',
    '/media/hotels/jholmolhari%20resort.jpg',
    '/media/hotels/ilam%20tea%20garden%20hotel.jpg',
    '/media/hotels/dwarika%20hotel.jpg'
]

print("Testing image URLs:\n")
for url in image_urls:
    response = client.get(url)
    status_icon = "✓" if response.status_code == 200 else "✗"
    content_type = response.get('Content-Type', 'Unknown')
    print(f"{status_icon} {url[:50]:<50} Status: {response.status_code} | Type: {content_type}")
