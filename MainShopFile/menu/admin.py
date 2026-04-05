from django.contrib import admin
from .models import Dishes


@admin.register(Dishes)
class DishesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'is_available', 'created_at')

    list_display_links = ('id', 'name')

    list_editable = ('price', 'is_available')

    list_filter = ('category', 'is_available', 'created_at')

    search_fields = ('name', 'description', 'category')

    list_per_page = 20

    # Поля для редактирования (разбивка на секции)
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'price', 'category')
        }),
        ('Детали', {
            'fields': ('description', 'is_available')
        }),
        ('Изображения', {
            'fields': ('image_path',),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('created_at',),
            'classes': ('collapse',)  # свернутая секция
        }),
    )
#
#     # Только для чтения поля
#     readonly_fields = ('created_at',)
#
#     # Действия с выбранными элементами
#     actions = ['make_available', 'make_unavailable']
#
#     def make_available(self, request, queryset):
#         queryset.update(is_available=True)
#
#     make_available.short_description = "Сделать доступными"
#
#     def make_unavailable(self, request, queryset):
#         queryset.update(is_available=False)
#
#     make_unavailable.short_description = "Сделать недоступными"
#
#
#
# admin.site.register(Dishes, DishesAdmin)

