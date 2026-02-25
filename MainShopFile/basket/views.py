from django.shortcuts import render, redirect
from authorization.models import Users
from menu.models import Dishes
from .models import Cart


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

# import requests


# Create your views here.
def index(request):
    user_id = request.session.get('user_id')
    if user_id:

        user = Users.objects.get(id=user_id)

        cart = Cart.objects.filter(user_id=user_id).all()
        if cart.count() >=1:
            print(user_id)
            total_summa = 0
            for i in cart:
                total_summa+= i.total_sum
                print(total_summa)


            return render(request, 'basket.html', {'cart': cart, 'total_summa' : total_summa })
        else:
            return redirect('/menu')
    # не забыть проверить
    return redirect('/')


@require_POST
def update_cart_quantity(request, cart_item_id):
    try:
        # Получаем данные из запроса
        data = json.loads(request.body)
        action = data.get('action')

        # Получаем элемент корзины
        cart_item = Cart.objects.get(id=cart_item_id)

        # Проверяем, что это корзина текущего пользователя
        user_id = request.session.get('user_id')

        if cart_item.user_id != Users.objects.get(id=user_id):
            return JsonResponse({
                'success': False,
                'error': 'Нет доступа'
            }, status=403)

        # Изменяем количество
        # cart = Cart.objects.filter(user_id=user_id, dishes_id=cart_item_id).first()

        if action == 'increase':
            cart_item.quantity += 1


        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                # Если количество 1 и нажали минус - удаляем товар
                cart_item.delete()
                item_count = Cart.objects.filter(user_id=user_id)
                item_count = item_count.count()

                return JsonResponse({
                    'success': True,
                    'deleted': True,
                    'cart_total': calculate_cart_total(user_id),
                    'cart_count': item_count
                })

        cart_item.save()

        # Количество уник товаров
        item_count = Cart.objects.filter(user_id=user_id)
        item_count = item_count.count()


        # Получаем цену товара
        dish_price = cart_item.dishes_id.price
        # Возвращаем обновленные данные
        return JsonResponse({
            'success': True,
            'new_quantity': cart_item.quantity,
            'item_total': cart_item.quantity * dish_price,
            'cart_total': calculate_cart_total(user_id),
            'item_price': dish_price,
            'cart_count': item_count
        })
    except Cart.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Товар не найден в корзине'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

# сумма корзины
def calculate_cart_total(user_id):
    cart_items = Cart.objects.filter(user_id=user_id)
    total = 0
    for item in cart_items:
        total += item.quantity * item.dishes_id.price
        item.total_sum = total
        item.save()
    return total

@require_POST
def delete_cart_item(request, cart_id):
    try:
        cart_item = Cart.objects.get(id=cart_id)

        user_id = request.session.get('user_id')

        if cart_item.user_id != Users.objects.get(id=user_id):
            return JsonResponse({
                'success': False,
                'error': 'Нет доступа'
            }, status=403)

        cart_item.delete()

        item_count = Cart.objects.filter(user_id=user_id)
        item_count = item_count.count()
        if item_count <= 0:
            return JsonResponse({
                'success': True,
                'cart_empty': True,
                'redirect_url': '/menu'
            })

        return JsonResponse({
            'success': True,
            'cart_empty': False,
            'message': 'Товар удален из корзины',
            'cart_total': calculate_cart_total(user_id),
            'cart_count': item_count,
        })
    except Exception as error:
        return JsonResponse({
            'success': False,
            'message': 'Error',
        })

@require_POST
def delete_cart(request):
    user_id = request.session.get('user_id')

    if user_id:
        # Удалить ВСЕ записи корзины для этого пользователя
        deleted_count = Cart.objects.filter(user_id=user_id).delete()

        return JsonResponse({
            'success': True,
            'message': f'Удалено {deleted_count[0]} товаров',
            'cart_empty': True
        })
    else:
        return JsonResponse({
            'success': False,
            'message': f'Не авторизован',
            'cart_empty': False
        })


