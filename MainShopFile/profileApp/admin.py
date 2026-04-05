from django.contrib import admin
from .models import Profile
# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'birth_date', 'address', 'about', 'telegram')

    list_display_links = ('id', 'user')

    # list_editable = ('telegram', 'is_available')

    list_filter = ('user', 'phone', 'telegram')

    search_fields = ('user', 'telegram', 'birth_date')
