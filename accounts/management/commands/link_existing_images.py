from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from accounts.models import Hotel, HotelImages
import os
from pathlib import Path

class Command(BaseCommand):
    help = 'Link existing image files from media/hotels folder to hotel records'

    def handle(self, *args, **options):
        media_hotels_path = Path('media/hotels')
        
        if not media_hotels_path.exists():
            self.stdout.write(self.style.ERROR('✗ media/hotels folder not found!'))
            return
        
        # Get all image files
        image_files = [f for f in media_hotels_path.iterdir() if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']]
        
        if not image_files:
            self.stdout.write(self.style.WARNING('~ No image files found in media/hotels'))
            return
        
        self.stdout.write(f'\n📁 Found {len(image_files)} image files\n')
        
        hotels = Hotel.objects.all()
        linked_count = 0
        
        for image_file in image_files:
            filename = image_file.name
            filename_lower = filename.lower().replace('.jpg', '').replace('.jpeg', '').replace('.png', '').replace('.gif', '')
            
            # Try to match image filename with hotel name
            matched_hotel = None
            
            for hotel in hotels:
                hotel_name_lower = hotel.hotel_name.lower()
                hotel_slug = hotel.hotel_slug.lower()
                
                # Match by slug
                if hotel_slug in filename_lower or filename_lower in hotel_slug:
                    matched_hotel = hotel
                    break
                
                # Match by name
                if hotel_name_lower in filename_lower or filename_lower in hotel_name_lower:
                    matched_hotel = hotel
                    break
                
                # Match by individual words
                hotel_words = hotel_name_lower.split()
                filename_words = filename_lower.split()
                
                # If multiple words match, it's likely the right hotel
                matching_words = sum(1 for word in hotel_words if word in filename_lower)
                if matching_words >= 2:
                    matched_hotel = hotel
                    break
            
            if matched_hotel:
                # Check if this image is already linked
                existing = HotelImages.objects.filter(
                    hotel=matched_hotel,
                    image=f'hotels/{filename}'
                ).exists()
                
                if existing:
                    self.stdout.write(self.style.WARNING(f'~ {filename} already linked to "{matched_hotel.hotel_name}"'))
                    continue
                
                # Create HotelImages record - use relative path from media folder
                try:
                    hotel_image = HotelImages(hotel=matched_hotel)
                    hotel_image.image = f'hotels/{filename}'
                    hotel_image.save()
                    
                    self.stdout.write(self.style.SUCCESS(f'✓ Linked "{filename}" to "{matched_hotel.hotel_name}"'))
                    linked_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'✗ Error linking {filename}: {str(e)}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ No matching hotel found for "{filename}"'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully linked {linked_count} images to hotels!'))
