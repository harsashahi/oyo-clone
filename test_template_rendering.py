import os
import django
os.chdir('c:\\ALL\\OYO clone\\oyo_clone')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oyo_clone.settings')
django.setup()

from django.template import Template, Context
from accounts.models import Hotel

# Get a hotel
hotel = Hotel.objects.filter(hotel_images__isnull=False).first()
if hotel:
    print(f"Hotel: {hotel.hotel_name}")
    print(f"Images: {hotel.hotel_images.count()}")
    
    # Test template rendering directly
    template_str = "{{ hotel.hotel_images.all }}"
    template = Template(template_str)
    context = Context({'hotel': hotel})
    result = template.render(context)
    print(f"\nTemplate result for '{{{{ hotel.hotel_images.all }}}}': {result}")
    
    # Test indexing
    template_str2 = "{{ hotel.hotel_images.0 }}"
    template2 = Template(template_str2)
    result2 = template2.render(context)
    print(f"Template result for '{{{{ hotel.hotel_images.0 }}}}': {result2}")
    
    # Test image.url
    template_str3 = "{{ hotel.hotel_images.0.image.url }}"
    template3 = Template(template_str3)
    result3 = template3.render(context)
    print(f"Template result for '{{{{ hotel.hotel_images.0.image.url }}}}': {result3}")
    
    # Test without .0
    template_str4 = "{{ hotel.hotel_images.first.image.url }}"
    template4 = Template(template_str4)
    result4 = template4.render(context)
    print(f"Template result for '{{{{ hotel.hotel_images.first.image.url }}}}': {result4}")
