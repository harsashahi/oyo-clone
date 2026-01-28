import os
from pathlib import Path

media_path = Path('c:\\ALL\\OYO clone\\oyo_clone\\media\\hotels')

# Image files that are in the featured section
featured_images = [
    'tiger mountain lodge.jpg',
    'soaltee crowne plaza.jpg',
    'annapurna boutique hotel.jpg',
    'lakeside spring hotel.jpg',
    'fewa lake hotel.jpg'
]

print("Checking featured hotel images:\n")
for img in featured_images:
    file_path = media_path / img
    exists = file_path.exists()
    status = "✓" if exists else "✗"
    size = f"{file_path.stat().st_size} bytes" if exists else "N/A"
    print(f"{status} {img:<40} {size}")

print("\n" + "=" * 60)

# Image files from all hotels section
all_images = [
    'jholmolhari resort.jpg',
    'ilam tea garden hotel.jpg',
    'janai resort.jpg',
    'chitwan safari lodge.jpg',
    'annapurna circuit.jpg',
    'bhaktapur heritage hotel.jpg',
    'pokhara serenity resort.jpg',
    'kathmandu peace hotel.jpg',
    'banyan resort.jpg',
    'hotel everest.jpg',
    'sunset view hotel.jpg',
    'hotel yak & yeti.jpg',
    'raddison.jpg',
    'the oberoi kathmandu.jpg',
    'dwarika hotel.jpg'
]

print("\nChecking all hotels images:\n")
missing = []
for img in all_images:
    file_path = media_path / img
    exists = file_path.exists()
    status = "✓" if exists else "✗"
    size = f"{file_path.stat().st_size} bytes" if exists else "MISSING"
    print(f"{status} {img:<40} {size}")
    if not exists:
        missing.append(img)

if missing:
    print(f"\n⚠ Missing files: {missing}")
else:
    print("\n✓ All image files exist!")
