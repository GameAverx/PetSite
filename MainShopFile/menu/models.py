from django.db import models
from django.utils import timezone

class Dishes(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    category = models.CharField(max_length=100, default='', verbose_name="Категория")
    image_path = models.CharField(max_length=255, default='error' )
    is_available = models.BooleanField(default=True, verbose_name="Доступно")
    created_at = models.DateTimeField(default=timezone.now)

    # auto_now_add = True, default=timezone.now
    # avatar = models.ImageField(upload_to='static/', blank=True, null=True)
    # is_available = models.BooleanField(default=True)
    # image = models.ImageField(upload_to='dishes/', blank=True, null=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Dish"  # Единственное число
        verbose_name_plural = "Dishes"  # Множественное число























