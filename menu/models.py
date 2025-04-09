from django.db import models

# Create your models here.
class MenuCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Menu Categories"

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')  

    def __str__(self):
        return f"{self.name} - ${self.price}"      