from django.contrib import admin
# from .models import Dishes



# class DishesAdmin(admin.ModelAdmin):
#     # Поля, отображаемые в списке
#     list_display = ('id', 'name', 'price', 'category', 'is_available', 'created_at')
#
#     # Поля, по которым можно кликнуть для редактирования
#     list_display_links = ('id', 'name')
#
#     # Поля, которые можно редактировать прямо в списке
#     list_editable = ('price', 'is_available')
#
#     # Фильтры справа
#     list_filter = ('category', 'is_available', 'created_at')
#
#     # Поиск по полям
#     search_fields = ('name', 'description', 'category')
#
#     # Количество записей на странице
#     list_per_page = 20
#
#     # Поля для редактирования (разбивка на секции)
#     fieldsets = (
#         ('Основная информация', {
#             'fields': ('name', 'price', 'category')
#         }),
#         ('Детали', {
#             'fields': ('description', 'is_available')
#         }),
#         ('Даты', {
#             'fields': ('created_at',),
#             'classes': ('collapse',)  # свернутая секция
#         }),
#     )
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

