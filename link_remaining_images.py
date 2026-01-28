import os
import django
os.chdir('c:\\ALL\\OYO clone\\oyo_clone')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oyo_clone.settings')
django.setup()

from accounts.models import Hotel, HotelImages
from pathlib import Path

# The 4 hotels without images
hotels_to_fix = [
    'Dwarika\'s Hotel',
    'Jhomolhari Resort',
    'Radisson Hotel Kathmandu',
    'Sunset View Hotel'
]

# Available unlinked images
unlinked_images = [
    'dwarika hotel.jpg',
    'dwarika_hotel.jpg',
    'jholmolhari resort.jpg',
    'raddison.jpg',
    'annapurna_rdDebQ0.jpg'  # Unknown
]

media_path = Path('c:\\ALL\\OYO clone\\oyo_clone\\media\\hotels')

print("Manually linking remaining images:\n")

# Dwarika's Hotel - use dwarika hotel.jpg
hotel = Hotel.objects.get(hotel_name='Dwarika\'s Hotel')
HotelImages.objects.create(
    hotel=hotel,
    image='hotels/dwarika hotel.jpg'
)
print(f"✓ Linked dwarika hotel.jpg to Dwarika's Hotel")

# Jhomolhari Resort - use jholmolhari resort.jpg
hotel = Hotel.objects.get(hotel_name='Jhomolhari Resort')
HotelImages.objects.create(
    hotel=hotel,
    image='hotels/jholmolhari resort.jpg'
)
print(f"✓ Linked jholmolhari resort.jpg to Jhomolhari Resort")

# Radisson Hotel Kathmandu - use raddison.jpg
hotel = Hotel.objects.get(hotel_name='Radisson Hotel Kathmandu')
HotelImages.objects.create(
    hotel=hotel,
    image='hotels/raddison.jpg'
)
print(f"✓ Linked raddison.jpg to Radisson Hotel Kathmandu")

# Sunset View Hotel - already has sunset_view_hotel.jpg from earlier, but check
hotel = Hotel.objects.get(hotel_name='Sunset View Hotel')
if hotel.hotel_images.count() == 0:
    HotelImages.objects.create(
        hotel=hotel,
        image='hotels/sunset view hotel.jpg'
    )
    print(f"✓ Linked sunset view hotel.jpg to Sunset View Hotel")
else:
    print(f"✓ Sunset View Hotel already has {hotel.hotel_images.count()} images")

print("\nDone!")
