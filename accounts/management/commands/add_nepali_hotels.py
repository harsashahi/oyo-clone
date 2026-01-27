from django.core.management.base import BaseCommand
from django.utils.text import slugify
from accounts.models import HotelVendor, Hotel, Ameneties

class Command(BaseCommand):
    help = 'Add 20 popular Nepali hotels to the database'

    def handle(self, *args, **options):
        # Create a vendor for these hotels if not exists
        vendor, created = HotelVendor.objects.get_or_create(
            username='nepal_hotels_vendor',
            defaults={
                'email': 'hotels@nepal.com',
                'phone_number': '9800000000',
                'is_active': True,
                'is_verified': True,
            }
        )
        
        if created:
            vendor.set_password('password123')
            vendor.save()
            self.stdout.write(self.style.SUCCESS('Created vendor: nepal_hotels_vendor'))
        
        # Create common amenities
        amenities_data = [
            'Free WiFi', 'Swimming Pool', 'Spa & Wellness', 'Restaurant',
            'Bar', 'Gym', 'Room Service', 'Airport Shuttle', 'Parking',
            'Conference Room', 'Garden View', 'Mountain View', 'Cultural Tours',
            'Safari Activities'
        ]
        
        amenities_dict = {}
        for amenity_name in amenities_data:
            amenity, _ = Ameneties.objects.get_or_create(name=amenity_name)
            amenities_dict[amenity_name] = amenity
        
        # Popular Nepali hotels data
        hotels_data = [
            {
                'hotel_name': 'Dwarika\'s Hotel',
                'location': 'Kathmandu, Nepal',
                'description': 'Luxury heritage hotel in Kathmandu featuring traditional Newari architecture and modern amenities. Located in the heart of the city with easy access to cultural sites.',
                'price': 15000,
                'offer_price': 12000,
                'amenities': ['Free WiFi', 'Swimming Pool', 'Spa & Wellness', 'Restaurant', 'Bar'],
                'featured': True,
            },
            {
                'hotel_name': 'The Oberoi, Kathmandu',
                'location': 'Kathmandu, Nepal',
                'description': 'Five-star luxury hotel offering world-class hospitality with stunning views of the Kathmandu Valley and Himalayas. Premium dining and spa facilities.',
                'price': 18000,
                'offer_price': 14500,
                'amenities': ['Free WiFi', 'Swimming Pool', 'Spa & Wellness', 'Restaurant', 'Gym'],
                'featured': True,
            },
            {
                'hotel_name': 'Radisson Hotel Kathmandu',
                'location': 'Kathmandu, Nepal',
                'description': 'Modern upscale hotel in Lazimpat with contemporary design and excellent service. Close to shops, restaurants, and tourist attractions.',
                'price': 12000,
                'offer_price': 9500,
                'amenities': ['Free WiFi', 'Restaurant', 'Bar', 'Gym', 'Airport Shuttle'],
                'featured': True,
            },
            {
                'hotel_name': 'Hotel Yak & Yeti',
                'location': 'Kathmandu, Nepal',
                'description': 'Premium 5-star hotel in Thamel district. Features traditional Nepali décor mixed with modern luxury. Excellent for business and leisure travelers.',
                'price': 14000,
                'offer_price': 11200,
                'amenities': ['Free WiFi', 'Swimming Pool', 'Restaurant', 'Conference Room', 'Spa & Wellness'],
                'featured': True,
            },
            {
                'hotel_name': 'Sunset View Hotel',
                'location': 'Pokhara, Nepal',
                'description': 'Scenic hotel overlooking Phewa Lake with stunning sunset views. Perfect base for exploring Pokhara and trekking routes. Peaceful and comfortable ambiance.',
                'price': 8000,
                'offer_price': 6500,
                'amenities': ['Free WiFi', 'Restaurant', 'Bar', 'Garden View', 'Mountain View'],
                'featured': True,
            },
            {
                'hotel_name': 'Fewa Lake Hotel',
                'location': 'Pokhara, Nepal',
                'description': 'Waterfront hotel on the banks of Phewa Lake with panoramic views. Great for water sports and adventure activities. Warm hospitality and local charm.',
                'price': 9500,
                'offer_price': 7500,
                'amenities': ['Free WiFi', 'Swimming Pool', 'Restaurant', 'Mountain View', 'Room Service'],
                'featured': True,
            },
            {
                'hotel_name': 'Lakeside Spring Hotel',
                'location': 'Pokhara, Nepal',
                'description': 'Boutique hotel in the heart of Pokhara\'s lakeside district. Offers comfortable rooms with lake views and easy access to restaurants and shops.',
                'price': 7000,
                'offer_price': 5500,
                'amenities': ['Free WiFi', 'Restaurant', 'Bar', 'Garden View', 'Parking'],
                'featured': True,
            },
            {
                'hotel_name': 'Annapurna Boutique Hotel',
                'location': 'Pokhara, Nepal',
                'description': 'Charming boutique hotel near Phewa Lake featuring personalized service. Great base for Annapurna trekking and Pokhara city exploration.',
                'price': 8500,
                'offer_price': 6800,
                'amenities': ['Free WiFi', 'Restaurant', 'Spa & Wellness', 'Mountain View', 'Room Service'],
                'featured': True,
            },
            {
                'hotel_name': 'Soaltee Crowne Plaza',
                'location': 'Kathmandu, Nepal',
                'description': 'Premier 5-star hotel in central Kathmandu with world-class facilities. Ideal for both business and leisure travelers. Complete wellness center and multiple dining options.',
                'price': 16000,
                'offer_price': 13000,
                'amenities': ['Free WiFi', 'Swimming Pool', 'Gym', 'Restaurant', 'Conference Room'],
                'featured': True,
            },
            {
                'hotel_name': 'Tiger Mountain Pokhara Village',
                'location': 'Pokhara, Nepal',
                'description': 'Unique eco-resort experience in Pokhara with traditional Nepali village setup. Ideal for nature lovers and those seeking authentic cultural experiences.',
                'price': 7500,
                'offer_price': 6000,
                'amenities': ['Restaurant', 'Garden View', 'Mountain View', 'Spa & Wellness', 'Bar'],
                'featured': True,
            },
            {
                'hotel_name': 'Hotel Everest View',
                'location': 'Namche Bazaar, Nepal',
                'description': 'High-altitude hotel offering spectacular views of Mount Everest. Ideal base for Everest trekkers with warm hospitality and comfort at elevation.',
                'price': 9000,
                'offer_price': 7200,
                'amenities': ['Restaurant', 'Mountain View', 'Bar', 'Room Service', 'Parking'],
                'featured': False,
            },
            {
                'hotel_name': 'Banyan Village Resort',
                'location': 'Nagarkot, Nepal',
                'description': 'Scenic hilltop resort overlooking the Kathmandu Valley. Perfect for sunrise views and relaxation. Traditional architecture with modern comfort.',
                'price': 8500,
                'offer_price': 6800,
                'amenities': ['Free WiFi', 'Restaurant', 'Spa & Wellness', 'Garden View', 'Mountain View'],
                'featured': False,
            },
            {
                'hotel_name': 'Kathmandu Peace Hotel',
                'location': 'Kathmandu, Nepal',
                'description': 'Mid-range hotel in popular Thamel area. Friendly staff, clean rooms, and convenient location near shops and restaurants. Budget-friendly option.',
                'price': 5500,
                'offer_price': 4500,
                'amenities': ['Free WiFi', 'Restaurant', 'Bar', 'Room Service', 'Parking'],
                'featured': False,
            },
            {
                'hotel_name': 'Pokhara Serenity Resort',
                'location': 'Pokhara, Nepal',
                'description': 'Peaceful resort away from Pokhara city center. Serene environment with garden views, perfect for relaxation and meditation retreats.',
                'price': 6500,
                'offer_price': 5200,
                'amenities': ['Free WiFi', 'Swimming Pool', 'Garden View', 'Restaurant', 'Spa & Wellness'],
                'featured': False,
            },
            {
                'hotel_name': 'Bhaaktapur Heritage Hotel',
                'location': 'Bhaktapur, Nepal',
                'description': 'Traditional hotel in ancient Bhaktapur city. Experience authentic Nepali culture with heritage rooms and views of Durbar Square.',
                'price': 6000,
                'offer_price': 4800,
                'amenities': ['Free WiFi', 'Restaurant', 'Garden View', 'Cultural Tours', 'Room Service'],
                'featured': False,
            },
            {
                'hotel_name': 'Annapurna Circuit Lodge',
                'location': 'Besisahar, Nepal',
                'description': 'Gateway hotel for Annapurna Circuit trekkers. Well-equipped rooms, trek information, and equipment rental services available.',
                'price': 5000,
                'offer_price': 4000,
                'amenities': ['Restaurant', 'Bar', 'Room Service', 'Parking', 'Free WiFi'],
                'featured': False,
            },
            {
                'hotel_name': 'Chitwan Safari Lodge',
                'location': 'Chitwan, Nepal',
                'description': 'Wildlife-focused resort in Chitwan National Park. Jungle safari, elephant rides, and nature activities included. Rustic luxury experience.',
                'price': 10000,
                'offer_price': 8000,
                'amenities': ['Restaurant', 'Bar', 'Swimming Pool', 'Safari Activities', 'Spa & Wellness'],
                'featured': False,
            },
            {
                'hotel_name': 'Janai Valley Resort',
                'location': 'Janakpur, Nepal',
                'description': 'Cultural resort in sacred Janakpur. Close to Janaki Mandir temple and rich local heritage. Traditional Maithili art and hospitality.',
                'price': 5500,
                'offer_price': 4400,
                'amenities': ['Restaurant', 'Free WiFi', 'Bar', 'Cultural Tours', 'Room Service'],
                'featured': False,
            },
            {
                'hotel_name': 'Ilam Tea Garden Hotel',
                'location': 'Ilam, Nepal',
                'description': 'Tea plantation resort in eastern Nepal. Experience tea garden walks, local farming, and authentic village life in serene surroundings.',
                'price': 5000,
                'offer_price': 4000,
                'amenities': ['Restaurant', 'Garden View', 'Room Service', 'Free WiFi', 'Bar'],
                'featured': False,
            },
            {
                'hotel_name': 'Jhomolhari Resort',
                'location': 'Ilam, Nepal',
                'description': 'Scenic mountain resort in eastern Nepal with panoramic views of the Himalayas. Ideal for nature walks and cultural exploration of the region.',
                'price': 6500,
                'offer_price': 5200,
                'amenities': ['Free WiFi', 'Restaurant', 'Mountain View', 'Garden View', 'Room Service'],
                'featured': False,
            },
        ]
        
        # Add hotels
        for hotel_info in hotels_data:
            hotel, created = Hotel.objects.get_or_create(
                hotel_slug=slugify(hotel_info['hotel_name']),
                defaults={
                    'hotel_name': hotel_info['hotel_name'],
                    'hotel_location': hotel_info['location'],
                    'hotel_description': hotel_info['description'],
                    'hotel_price': hotel_info['price'],
                    'hotel_offer_price': hotel_info['offer_price'],
                    'hotel_owner': vendor,
                    'is_active': True,
                    'is_featured': hotel_info['featured'],
                }
            )
            
            # Add amenities
            for amenity_name in hotel_info['amenities']:
                hotel.ameneties.add(amenities_dict[amenity_name])
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created hotel: {hotel_info["hotel_name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'~ Hotel already exists: {hotel_info["hotel_name"]}'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Successfully added 20 popular Nepali hotels!'))
