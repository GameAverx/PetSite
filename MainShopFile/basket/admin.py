from django.contrib import admin
from .models import Cart
from .models import PromoCode

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'dishes_id', 'quantity', 'total_sum', 'applied_promo', 'created_at']



@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'code','discount_value', 'is_active',
                    'created_at']
    search_fields = ['code', 'discount_value', 'is_active']
