from django.contrib import admin
from .models import Users
from .models import User_adresses

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'created_at']
    search_fields = ['email']
    # list_filter = ['is_active']



@admin.register(User_adresses)
class AdressesAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','address_type', 'is_default', 'city', 'street', 'house', 'apartment', 'entrance', 'floor', 'intercom', 'comment',
                    'created_at']
    search_fields = ['user', 'city', 'street']
    # list_filter = ['is_active']