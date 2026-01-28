import os
import django
os.chdir('c:\\ALL\\OYO clone\\oyo_clone')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oyo_clone.settings')
django.setup()

from django.test import Client
import re

client = Client()

# Test home page
response = client.get('/')

if response.status_code == 200:
    html = response.content.decode('utf-8')
    
    # Extract featured hotels section
    featured_start = html.find('<h2 style="display: flex')
    featured_end = html.find('<hr style="margin: 40px 0;">')
    featured_section = html[featured_start:featured_end]
    
    # Extract all hotels section
    all_start = html.find('<!-- All Hotels Section -->')
    all_end = html.find('<!-- View All Link -->')
    all_hotels_section = html[all_start:all_end]
    
    # Find all hotel names and images in each section
    def extract_hotels_from_section(section_html):
        # Find all hotel-card divs
        cards = re.findall(r'<div class="hotel-card[^>]*>.*?</div>\s*</div>\s*</div>', section_html, re.DOTALL)
        
        hotels_data = []
        for card in cards:
            # Extract hotel name
            name_match = re.search(r'<h3>([^<]*)</h3>', card)
            hotel_name = name_match.group(1) if name_match else 'Unknown'
            
            # Extract image src
            img_match = re.search(r'<img[^>]*src="([^"]*)"', card)
            img_src = img_match.group(1) if img_match else ''
            
            # Check if it's a placeholder
            is_placeholder = 'no-image-placeholder' in card
            
            hotels_data.append({
                'name': hotel_name,
                'src': img_src,
                'has_image': bool(img_src and not is_placeholder)
            })
        
        return hotels_data
    
    featured = extract_hotels_from_section(featured_section)
    all_hotels = extract_hotels_from_section(all_hotels_section)
    
    print("=" * 80)
    print("FEATURED HOTELS SECTION")
    print("=" * 80)
    for h in featured:
        status = "✓" if h['has_image'] else "✗"
        print(f"{status} {h['name']:<35} {h['src'][:40] if h['src'] else 'PLACEHOLDER'}")
    
    print("\n" + "=" * 80)
    print("ALL HOTELS SECTION")
    print("=" * 80)
    with_img = sum(1 for h in all_hotels if h['has_image'])
    without_img = sum(1 for h in all_hotels if not h['has_image'])
    print(f"Total: {len(all_hotels)} | With images: {with_img} | Placeholders: {without_img}\n")
    
    for h in all_hotels:
        status = "✓" if h['has_image'] else "✗"
        src_display = h['src'][:40] if h['src'] else 'PLACEHOLDER'
        print(f"{status} {h['name']:<35} {src_display}")
