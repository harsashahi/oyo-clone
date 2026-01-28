import os
from pathlib import Path

media_path = Path('c:\\ALL\\OYO clone\\oyo_clone\\media\\hotels')

# Get all image files
images = list(media_path.glob('*'))
image_files = [f for f in images if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']]

print(f"Total image files in media/hotels: {len(image_files)}\n")
print("Files:")
for img in sorted(image_files):
    print(f"  - {img.name}")
