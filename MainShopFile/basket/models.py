from django.db import models
from authorization.models import Users
from menu.models import Dishes

class Cart(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    dishes_id = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_sum= models.DecimalField(default=0, max_digits=15, decimal_places=2, verbose_name="Цена товара")
    applied_promo = models.ForeignKey(
        'PromoCode',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

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


# class Full_Cart(models.Model):
#     user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
#     total_sum = models.DecimalField(default=0, max_digits=15, decimal_places=2, verbose_name="Общая цена товаров")
#     applied_promo = models.ForeignKey(
#         'PromoCode',
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL
#     )
#
#     discount_sum = models.DecimalField(default=0, max_digits=15, decimal_places=2, verbose_name="Общая цена товаров со скидкой")
#     pay_amount = models.DecimalField(default=0, max_digits=15, decimal_places=2, verbose_name="Сумма к оплате")
#     created_at = models.DateTimeField(auto_now_add=True)




class PromoCode(models.Model):
    # Код промокода (уникальный)
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Промокод"
    )

    # Значение скидки
    discount_value = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        verbose_name="Значение скидки"
    )

    # Активен
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.code


class PromoCodeUsage(models.Model):
    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='promo_usages'
    )
    promo_code = models.ForeignKey(
        PromoCode,
        on_delete=models.CASCADE,
        related_name='usages'
    )
    used_at = models.DateTimeField(auto_now_add=True)







