from django.db import models
from authorization.models import Users
from menu.models import Dishes

class Cart(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    dishes_id = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        dish = Dishes.objects.get(id=self.dishes_id)
        price = dish.price
        return float(price* self.quantity)
    # def __str__(self):
    #     return self.name


    # auto_now_add = True, default=timezone.now
    # avatar = models.ImageField(upload_to='static/', blank=True, null=True)
    # is_available = models.BooleanField(default=True)
    # image = models.ImageField(upload_to='dishes/', blank=True, null=True)








