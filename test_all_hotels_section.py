import os
import django
os.chdir('c:\\ALL\\OYO clone\\oyo_clone')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oyo_clone.settings')
django.setup()

from django.test import Client
import re

client = Client()

# Test home page
print("Testing Home Page - All Hotels Section\n")
response = client.get('/')
print(f"Status Code: {response.status_code}\n")

if response.status_code == 200:
    html = response.content.decode('utf-8')
    
    # Find all hotel cards in the "All Hotels" section
    # Extract the part after "All Hotels" header
    all_hotels_section = html[html.find('<h2>All Hotels</h2>'):]
    
    # Find all img tags in hotel cards
    img_pattern = r'<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"'
    img_tags = re.findall(img_pattern, all_hotels_section)
    
    print(f"Found {len(img_tags)} images in 'All Hotels' section:\n")
    
    # Group by hotel name
    hotel_images = {}
    for src, alt in img_tags:
        if alt not in hotel_images:
            hotel_images[alt] = []
        if src:  # Only count non-empty src
            hotel_images[alt].append(src)
    
    # Show summary
    with_img = sum(1 for v in hotel_images.values() if v)
    without_img = sum(1 for v in hotel_images.values() if not v)
    
    print(f"Hotels WITH images: {with_img}")
    print(f"Hotels WITHOUT images (placeholder only): {without_img}\n")
    
    print("Hotels WITHOUT images:")
    for hotel, imgs in hotel_images.items():
        if not imgs:
            print(f"  ✗ {hotel}")
    
    print("\nFirst 10 hotels with images:")
    count = 0
    for hotel, imgs in hotel_images.items():
        if imgs:
            print(f"  ✓ {hotel}: {imgs[0][:50]}...")
            count += 1
            if count >= 10:
                break
