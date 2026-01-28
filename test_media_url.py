import os
import django
os.chdir('c:\\ALL\\OYO clone\\oyo_clone')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oyo_clone.settings')
django.setup()

from django.test import Client
from django.conf import settings

client = Client()

# Test serving a media file directly
image_url = '/media/hotels/ilam%20tea%20garden%20hotel.jpg'
print(f"Testing direct image URL: {image_url}\n")

response = client.get(image_url)
print(f"Status Code: {response.status_code}")
print(f"Content-Type: {response.get('Content-Type', 'Not set')}")
print(f"Content-Length: {len(response.content)} bytes")

# Also check file path
file_path = os.path.join(settings.MEDIA_ROOT, 'hotels', 'ilam tea garden hotel.jpg')
print(f"\nFile path: {file_path}")
print(f"File exists: {os.path.exists(file_path)}")
print(f"File size: {os.path.getsize(file_path) if os.path.exists(file_path) else 'N/A'} bytes")
