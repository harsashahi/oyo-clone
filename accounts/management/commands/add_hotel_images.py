from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from accounts.models import Hotel, HotelImages
from PIL import Image, ImageDraw
import io
import os

class Command(BaseCommand):
    help = 'Add sample images to all hotels'

    def handle(self, *args, **options):
        hotels = Hotel.objects.all()
        
        # Color palette for different hotels
        colors = [
            (70, 130, 180),    # Steel blue
            (220, 20, 60),     # Crimson
            (34, 139, 34),     # Forest green
            (184, 134, 11),    # Dark goldenrod
            (139, 69, 19),     # Saddle brown
            (72, 209, 204),    # Medium turquoise
            (199, 21, 133),    # Medium violet red
            (255, 140, 0),     # Dark orange
            (25, 25, 112),     # Midnight blue
            (210, 105, 30),    # Chocolate
            (147, 112, 219),   # Medium purple
            (50, 205, 50),     # Lime green
            (219, 112, 147),   # Pale violet red
            (100, 149, 237),   # Cornflower blue
            (240, 230, 200),   # Beige
            (255, 192, 203),   # Pink
            (173, 255, 47),    # Green yellow
            (100, 100, 100),   # Gray
            (139, 0, 139),     # Dark magenta
            (0, 128, 128),     # Teal
        ]
        
        for idx, hotel in enumerate(hotels):
            # Check if hotel already has images
            if hotel.hotel_images.exists():
                self.stdout.write(self.style.WARNING(f'~ Hotel "{hotel.hotel_name}" already has images, skipping...'))
                continue
            
            # Generate 3 sample images per hotel
            for img_num in range(1, 4):
                # Create image
                img = Image.new('RGB', (800, 600), color=colors[idx % len(colors)])
                draw = ImageDraw.Draw(img)
                
                # Add text
                text = f"{hotel.hotel_name}\nImage {img_num}"
                text_color = (255, 255, 255)
                
                # Draw text on image
                draw.text((50, 250), text, fill=text_color, font=None)
                
                # Save to bytes
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='JPEG')
                img_bytes.seek(0)
                
                # Create HotelImages entry
                image_name = f"{hotel.hotel_slug}_img_{img_num}.jpg"
                
                hotel_image = HotelImages(hotel=hotel)
                hotel_image.image.save(image_name, ContentFile(img_bytes.read()), save=True)
                
                self.stdout.write(self.style.SUCCESS(f'✓ Added image {img_num}/3 to "{hotel.hotel_name}"'))
            
        self.stdout.write(self.style.SUCCESS('\n✓ Successfully added sample images to all hotels!'))
