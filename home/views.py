from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from accounts.models import Hotel
from .models import Hotel as HomeHotel


def home(request):
    """Display all hotels with basic filtering"""
    hotels = Hotel.objects.filter(is_active=True)
    featured_hotels = Hotel.objects.filter(is_active=True, is_featured=True)[:5]  # Limit to 5 featured hotels
    
    # Get featured hotel IDs to exclude them from all hotels section
    featured_ids = [hotel.id for hotel in featured_hotels]
    all_hotels = hotels.exclude(id__in=featured_ids)  # Show other hotels in "All Hotels"
    
    # Filter by location if provided
    location = request.GET.get('location')
    if location:
        featured_hotels = Hotel.objects.filter(is_active=True, is_featured=True, hotel_location__icontains=location)[:5]
        featured_ids = [hotel.id for hotel in featured_hotels]
        all_hotels = hotels.filter(hotel_location__icontains=location).exclude(id__in=featured_ids)
    
    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        featured_hotels = featured_hotels.filter(hotel_price__gte=min_price)
        all_hotels = all_hotels.filter(hotel_price__gte=min_price)
    if max_price:
        featured_hotels = featured_hotels.filter(hotel_price__lte=max_price)
        all_hotels = all_hotels.filter(hotel_price__lte=max_price)
    
    context = {
        'hotels': all_hotels,
        'featured_hotels': featured_hotels,
        'location': location,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'home/home.html', context)


def hotel_detail(request, slug):
    """Display hotel details page"""
    hotel = get_object_or_404(Hotel, hotel_slug=slug, is_active=True)
    images = hotel.hotel_images.all()
    managers = hotel.hotel_managers.all()
    
    context = {
        'hotel': hotel,
        'images': images,
        'managers': managers,
    }
    return render(request, 'home/hotel_detail.html', context)


def hotel_search(request):
    """Advanced hotel search with filters"""
    hotels = Hotel.objects.filter(is_active=True)
    
    # Search by name or location
    query = request.GET.get('q')
    if query:
        hotels = hotels.filter(
            Q(hotel_name__icontains=query) | 
            Q(hotel_location__icontains=query) |
            Q(hotel_description__icontains=query)
        )
    
    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        hotels = hotels.filter(hotel_price__gte=min_price)
    if max_price:
        hotels = hotels.filter(hotel_price__lte=max_price)
    
    # Filter by amenities
    amenities = request.GET.getlist('amenities')
    if amenities:
        hotels = hotels.filter(ameneties__id__in=amenities).distinct()
    
    # Sorting
    sort_by = request.GET.get('sort_by', '-hotel_price')
    if sort_by in ['hotel_price', '-hotel_price', 'hotel_name']:
        hotels = hotels.order_by(sort_by)
    
    context = {
        'hotels': hotels,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'home/search.html', context)
