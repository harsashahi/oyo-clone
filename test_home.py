import os
import django
os.chdir('c:\\ALL\\OYO clone\\oyo_clone')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oyo_clone.settings')
django.setup()

from django.test import Client

client = Client()

# Test home page
print("Testing Home Page\n")
response = client.get('/')
print(f"Status Code: {response.status_code}\n")

html = response.content.decode('utf-8')

# Find image tags
import re
img_tags = re.findall(r'<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*>', html)

print(f"Found {len(img_tags)} img tags with src and alt:\n")
for src, alt in img_tags[:10]:
    print(f"  Alt: {alt}")
    print(f"  Src: {src}\n")

# Check for "no images available" or placeholder messages
if 'No images available' in html:
    print("⚠ Found 'No images available' message in HTML")
else:
    print("✓ No 'No images available' message found")

if 'no-image-placeholder' in html:
    print("⚠ Found 'no-image-placeholder' in HTML")
else:
    print("✓ No 'no-image-placeholder' found")
