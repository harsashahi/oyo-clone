from django.core.management.base import BaseCommand
from accounts.models import Hotel, Room

class Command(BaseCommand):
    help = 'Add sample rooms to all hotels'

    def handle(self, *args, **options):
        hotels = Hotel.objects.all()
        
        room_types = ['single', 'double', 'suite', 'deluxe']
        
        for hotel in hotels:
            # Check if hotel already has rooms
            if hotel.rooms.exists():
                self.stdout.write(self.style.WARNING(f'~ Hotel "{hotel.hotel_name}" already has rooms, skipping...'))
                continue
            
            # Create 8 rooms for each hotel (2 of each type)
            room_count = 0
            for room_type in room_types:
                for i in range(1, 3):  # 2 rooms of each type
                    room_count += 1
                    
                    # Set room details based on type
                    if room_type == 'single':
                        capacity = 1
                        price = hotel.hotel_offer_price
                    elif room_type == 'double':
                        capacity = 2
                        price = hotel.hotel_offer_price * 1.3
                    elif room_type == 'suite':
                        capacity = 4
                        price = hotel.hotel_offer_price * 2
                    else:  # deluxe
                        capacity = 3
                        price = hotel.hotel_offer_price * 1.8
                    
                    room = Room.objects.create(
                        hotel=hotel,
                        room_type=room_type,
                        room_number=f"{room_type[0].upper()}{room_count:02d}",
                        capacity=capacity,
                        price_per_night=price,
                        is_available=True
                    )
                    
            self.stdout.write(self.style.SUCCESS(f'✓ Added 8 rooms to "{hotel.hotel_name}"'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Successfully added sample rooms to all hotels!'))
