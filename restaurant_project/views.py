from django.shortcuts import render, redirect
from django.contrib import messages
from booking.models import Booking
from menu.models import MenuCategory, MenuItem

def home(request):
    categories = MenuCategory.objects.all()[:3]  # Get first 3 categories
    featured_items = MenuItem.objects.filter(is_available=True)[:6]  # Get 6 featured items
    return render(request, 'home.html', {
        'categories': categories,
        'featured_items': featured_items
    })

def contact(request):
    if request.method == 'POST':
        # Process contact form
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Here you would typically save to database or send email
        
        messages.success(request, 'Your message has been sent! We will get back to you soon.')
        return redirect('contact')
        
    return render(request, 'contact.html')