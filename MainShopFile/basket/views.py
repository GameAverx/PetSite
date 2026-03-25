from django.shortcuts import render, redirect
from authorization.models import Users, User_adresses
from menu.models import Dishes
from .models import Cart
from .models import PromoCode, PromoCodeUsage


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

# import requests


# Create your views here.
def index(request):
    user_id = request.session.get('user_id')
    if user_id:
        # adress = User_adresses()
        # adress.user = Users.objects.get(id=user_id)
        # adress.address_type = 'work'
        # adress.city = 'Владивосток'
        # adress.street = 'Леонова'
        # adress.house = '90'
        # adress.apartment = '42'
        # adress.save()


        cart = Cart.objects.filter(user_id=user_id).all()
        adresses = User_adresses.objects.filter(user = user_id).all()
        if adresses.count() == 0:
            adresses = 0
        else:
            print(adresses)
            for i in adresses:
                print(i.city)
        if cart.count() >=1:
            print(user_id)

            total_summa = calculate_cart_total(user_id)

            return render(request, 'basket.html', {'cart': cart, 'total_summa' : total_summa, 'adresses': adresses})
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
    # тут какая-то проблема

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

@require_POST
def promocode(request):
    user_id = request.session.get('user_id')

    if user_id:

        # promo = PromoCode()
        # promo.code = 'WELCOME10'
        # promo.discount_value = 10
        # promo.save()

        # promouse = PromoCodeUsage()
        # promouse.user = Users.objects.get(id=user_id)
        # promouse.promo_code = PromoCode.objects.get(code=promo.code)
        # promouse.save()

        if not request.body:
            cart_items = Cart.objects.filter(user_id=user_id)

            for item in cart_items:
                item.applied_promo = None
                item.save()
            return JsonResponse({'success': True, 'new_price': calculate_cart_total(user_id)})

        data = json.loads(request.body)
        code = data.get('code', '').strip().upper() # код


        try:

            # Проверяем впервые ли используется промокод
            promo = PromoCode.objects.get(code=code, is_active=True)



            if promo:
            # print(promocode_id)
                promocode_usage = PromoCodeUsage.objects.filter(promo_code=promo.id, user=user_id)
                if not promocode_usage:


                    cart_items = Cart.objects.filter(user_id=user_id)

                    for item in cart_items:
                        item.applied_promo = promo
                        item.save()



                    # Ищем прокомод в базе
                    discount = float(promo.discount_value)
                    user_cart_sum = float(calculate_cart_total(user_id))
                    # пересчет корзины
                    discount_sum = (user_cart_sum / 100) * discount
                    new_amount = user_cart_sum - discount_sum

                    return JsonResponse({
                        'success': True,
                        'message': f'Промокод успешно использован',
                        'new_amount': new_amount,
                        'discount' : discount,
                        'discount_sum' : discount_sum * -1
                    })

                else:
                    return JsonResponse({
                    'success': False,
                    'message': f'Промокод уже был использован',
                    })
            else:
                return JsonResponse({
                    'success': False,
                    'message': f'Промокод не действителен',
                })




        except Exception as errors:
            print('123', errors)
            return JsonResponse({
                'success': False,
                'message': f'Ошибка прокода',
            })


    else:
        return JsonResponse({
            'success': False,
            'message': f'Не авторизован'
            })

@require_POST
def total_price(request):
    try:
        user_id = request.session.get('user_id')
        data = json.loads(request.body)
        delivery = data.get('delivery')
        price = calculate_discount(user_id)
        if delivery:
            price = price + 100
            return JsonResponse({
                'success': True,
                'message': f'',
                'price' : price
            })
        else:
            return JsonResponse({
                'success': True,
                'message': f'',
                'price': price
            })
    except Exception as error:
        print(123, error)
        return JsonResponse({
            'success': False,
            'message': f'{error}',
        })


@require_POST
def data_cart(request):
    user_id = request.session.get('user_id')

    if user_id:
        try:
            data = json.loads(request.body)
            code = data.get('code', '').strip().upper()  # код
            delivery = data.get('delivery')

            # обработка и проверка промокода
            new_price = calculate_cart_total(user_id)
            discount_sum = 0
            if code != '':
                promo = PromoCode.objects.get(code=code, is_active=True)
                if promo:
                    new_price, discount_sum = calculate_discount(user_id ,float(promo.discount_value))

                else:
                    return JsonResponse({
                        'success': False,
                        'message': f'Промокод не существует'
                    })
            # обработка доставки
            if delivery:
                new_price+=100

            return JsonResponse({
                'success': True,
                'discount_sum': discount_sum,
                'price': new_price
            })

        except Exception as Error:
            print(Error)
            return JsonResponse({
                'success': False,
                'message': f'{Error}'
            })

    else:
        return JsonResponse({
            'success': False,
            'message': f'Не авторизован'
            })

# старый подсчет скидки
# def calculate_discount(user_id):
#     cart_item = Cart.objects.filter(user_id=user_id).first()
#     discount = cart_item.applied_promo
#     if discount is not None:
#         discount = float(discount.discount_value)
#         total = float(calculate_cart_total(user_id))
#         discount_sum = (total / 100) * discount
#         new_total = (total - discount_sum)
#         return new_total, discount_sum
#     else:
#         return calculate_cart_total(user_id)

def calculate_discount(user_id, discound_value):
    total = float(calculate_cart_total(user_id))
    discount_sum = (total / 100) * discound_value
    new_total = (total - discount_sum)
    return new_total, discount_sum


@require_POST
def add_new_adress(request):
    try:
        data = json.loads(request.body)
        city = data.get('city', '').strip().capitalize()
        street = data.get('street', '').strip().capitalize()
        house = data.get('house', '').strip().upper()
        apartment = data.get('apartment', '').strip()
        address_type = data.get('address_type', '').strip()

        user_id = request.session.get('user_id')

        new_adress = User_adresses()

        new_adress.user = Users.objects.get(id=user_id)
        new_adress.address_type = address_type
        new_adress.city = city
        new_adress.street = street
        new_adress.house = house
        if apartment != '':
            new_adress.apartment = apartment
        new_adress.save()

        return JsonResponse({
            'success': True,
            'city' : city,
            'street' : street,
            'house' : house,
            'apartment' : apartment
        })

    except Exception as Error:
        return JsonResponse({
            'success': False,
            'message': f'{Error}'
        })












