from django.shortcuts import render
from .models import MenuCategory, MenuItem
from django.shortcuts import render, get_object_or_404
from .models import MenuCategory, MenuItem

# Create your views here.
def menu_list(request):
    categories = MenuCategory.objects.all()
    menu_items = MenuItem.objects.filter(is_available=True)
    
    return render(request, 'menu/menu_list.html', {
        'categories': categories,
        'menu_items': menu_items
    })
def category_detail(request, category_id):
    category = get_object_or_404(MenuCategory, id=category_id)
    menu_items = MenuItem.objects.filter(category=category, is_available=True)
    
    return render(request, 'menu/category_detail.html', {
        'category': category,
        'menu_items': menu_items
    })
