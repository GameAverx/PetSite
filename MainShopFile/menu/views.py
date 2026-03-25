from django.shortcuts import render, redirect
from authorization.models import Users
from .models import Dishes
from basket.models import Cart

def index(request):
    user_id = request.session.get('user_id')
    menu = Dishes.objects.all()
    if user_id:
        user = Users.objects.get(id=user_id)

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
        # for i in menu:
        #     print(i.name)
        #     print(i.price)
        #     print(i.description)
        # print(dishes)

        return render(request, 'menuPage.html', {'user': user, 'menu': menu})
    return render(request, 'menuPage.html', {'menu': menu})

def add_to_cart(request, product_id):
    user_id = request.session.get('user_id')
    if user_id:
        user = Users.objects.get(id=user_id)
        if user.is_authenticated:
            if request.method == 'POST':
                quantity = request.POST.get('quantity')
                try:
                    dish = Dishes.objects.get(id=product_id)

                    if Cart.objects.filter(user_id=user_id, dishes_id=product_id).exists():
                        cart = Cart.objects.filter(user_id=user_id, dishes_id=product_id).first()
                        cart.quantity +=1
                        cart.total_sum = float(Dishes.objects.get(id=product_id).price) * (int(quantity) + 1)
                        cart.save()
                        return redirect('/menu')

                    elif dish.is_available is True:
                        position = Cart()
                        position.user_id = Users(id=user_id)
                        position.dishes_id = Dishes(id=product_id)
                        position.quantity = quantity
                        position.total_sum = float(Dishes.objects.get(id=product_id).price) * int(quantity)
                        position.save()
                        return redirect('/menu')
                    else:
                        print('ERROR-1')
                        return redirect('/menu')
                except Exception as error:
                    print('ERROR-2')
                    print(error)
                    return redirect('/menu')
            else:
                return redirect('/menu')
        else:
            return redirect('/menu')
    else:
        return redirect('/menu')

