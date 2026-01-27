from django.shortcuts import render



def index(request):
    return render(request, 'index.html')



def login_page(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


from .models import Hotel

def home(request):
    hotels = Hotel.objects.all()
    return render(request, 'home/home.html', {'hotels': hotels})
