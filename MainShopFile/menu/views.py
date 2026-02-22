from django.shortcuts import render
from authorization.models import Users
from .models import Dishes

def index(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Users.objects.get(id=user_id)
        print(user_id)

        # dish = Dishes()
        # dish.name = 'Пицца Маргарита'
        # dish.price = 450
        # dish.description = 'Классическая итальянская пицца с томатным соусом и моцареллой'
        # dish.category = 'Пиццы'
        # dish.image_path = 'images/pizza.jpg'
        # dish.save()
        #
        # dish = Dishes()
        # dish.name = 'Роллы Калифорния'
        # dish.price = 320
        # dish.description = '11 шт. с крабом, авокадо и икрой масаго'
        # dish.category = 'Роллы'
        # dish.image_path = 'images/sushi.jpg'
        # dish.save()

        # Dishes.objects.all().delete()
        # Dishes.save()
        menu = Dishes.objects.all()
        # for i in menu:
        #     print(i.name)
        #     print(i.price)
        #     print(i.description)
        # print(dishes)

        return render(request, 'menuPageTest.html', {'user': user, 'menu': menu})
    return render(request, 'menuPage.html')

