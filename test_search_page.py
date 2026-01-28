import os
import django
os.chdir('c:\\ALL\\OYO clone\\oyo_clone')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oyo_clone.settings')
django.setup()

from django.test import Client
import re

client = Client()

# Test search/view all hotels page
print("Testing View All Hotels Page\n")
response = client.get('/search/')
print(f"Status Code: {response.status_code}\n")

if response.status_code == 200:
    html = response.content.decode('utf-8')
    
    # Find all img tags
    img_pattern = r'<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"'
    img_tags = re.findall(img_pattern, html)
    
    print(f"Found {len(img_tags)} images in search page:\n")
    
    # Group by hotel name
    hotel_images = {}
    for src, alt in img_tags:
        if alt not in hotel_images:
            hotel_images[alt] = []
        if src:
            hotel_images[alt].append(src)
    
    with_img = sum(1 for v in hotel_images.values() if v)
    without_img = sum(1 for v in hotel_images.values() if not v)
    
    print(f"Hotels WITH images: {with_img}")
    print(f"Hotels WITHOUT images: {without_img}\n")
    
    if without_img > 0:
        print("Hotels WITHOUT images:")
        for hotel, imgs in hotel_images.items():
            if not imgs:
                print(f"  ✗ {hotel}")
    else:
        print("✓ All hotels have images!\n")
        print("Sample of images:")
        count = 0
        for hotel, imgs in sorted(hotel_images.items())[:10]:
            print(f"  ✓ {hotel:<35} {imgs[0][:45]}...")
            count += 1
