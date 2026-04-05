from django.shortcuts import render, redirect

from authorization.models import Users
from authorization.models import User_adresses
from .models import Profile

from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json


# Create your views here.
def index(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Users.objects.get(id=user_id)
        try:
            profile = Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            user = Users.objects.get(id=user_id)
            profile = Profile.objects.create(user=user)
        addresses = User_adresses.objects.filter(user = user_id).all()

        return render(request, 'profile.html', {'user': user, 'profile': profile, 'addresses': addresses})
    # не забыть проверить
    return redirect('/')


@require_POST
def profile_edit(request):
    user_id = request.session.get('user_id')
    if user_id:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip() # нужна проверка на цифры
        birth_date = data.get('birth_date', '').strip()
        about = data.get('about', '').strip()
        print(name, email, phone, birth_date, about)
        if phone.isdigit() is False:
            return JsonResponse({
                'success': False,
                'error': 'Номер должен содержать только цифры'
            })
        else:
            try:
                profile = Profile.objects.get(user_id=user_id)
                user = Users.objects.get(id=user_id)
                user.name = name
                user.email = email
                user.save()

                profile.phone = phone
                profile.birth_date = birth_date
                profile.about = about
                profile.save()
                return JsonResponse({
                    'success': True,
                    'error': 'Успешно'
                })
            except Exception as error:
                return JsonResponse({
                    'success': False,
                    'error': 'Произошла ошибка при сохранении'
                })
    else:
        return JsonResponse({
            'success': False,
            'error': 'Нет авторизации'
        })

@require_POST
def address_add(request):
    user_id = request.session.get('user_id')
    if user_id:
        data = json.loads(request.body)
        address_type = data.get('address_type', '').strip()
        city = data.get('city', '').strip()
        street = data.get('street', '').strip()
        house = data.get('house', '').strip()
        apartment = data.get('apartment', '').strip()
        entrance = data.get('entrance', '').strip()
        floor = data.get('floor', '').strip()
        intercom = data.get('intercom', '').strip()
        comment = data.get('comment')
        address_default = data.get('address_default')

        if not city:
            return JsonResponse({'success': False, 'error': 'Город обязателен'}, status=400)

        if not street:
            return JsonResponse({'success': False, 'error': 'Улица обязательна'}, status=400)

        if not house:
            return JsonResponse({'success': False, 'error': 'Дом обязателен'}, status=400)

            # 2. Проверка длины
        if len(city) > 100:
            return JsonResponse({'success': False, 'error': 'Слишком длинное название города'}, status=400)

        if len(street) > 200:
            return JsonResponse({'success': False, 'error': 'Слишком длинное название улицы'}, status=400)

        if len(house) > 20:
            return JsonResponse({'success': False, 'error': 'Некорректный номер дома'}, status=400)

        if not city.isalpha():
            return JsonResponse({'success': False, 'error': 'Город содержит цифры'}, status=400)

        if not street.isalpha():
            return JsonResponse({'success': False, 'error': 'Название улицы не может содержать цифр'}, status=400)

        if not apartment.isdigit() and apartment != '':
            return JsonResponse({'success': False, 'error': 'Квартира/офис не должен содержать буквы'}, status=400)

        if not entrance.isdigit() and entrance != '':
            return JsonResponse({'success': False, 'error': 'Подъезд не должен содержать буквы'}, status=400)

        if not floor.isdigit() and entrance != '':
            return JsonResponse({'success': False, 'error': 'Этаж не должен содержать буквы'}, status=400)

        if not intercom.isdigit() and intercom != '':
            return JsonResponse({'success': False, 'error': 'Домофон не должен содержать буквы'}, status=400)

        user = Users.objects.get(id=user_id)
        new_address = User_adresses.objects.create(user=user)
        new_address.address_type = address_type
        new_address.is_default = address_default
        new_address.city = city
        new_address.street = street
        new_address.house = house
        new_address.apartment = apartment
        new_address.entrance = entrance
        new_address.floor = floor
        new_address.intercom = intercom
        new_address.comment = comment
        new_address.save()
        print(new_address.id)
        print(new_address.id)
        print(new_address.id)

        return JsonResponse({
            'success': True,
            'error': 'Успех',
            'id': new_address.id
        })

    else:
        return JsonResponse({
            'success': False,
            'error': 'Нет авторизации'
        })


@require_POST
def address_edit(request):
    user_id = request.session.get('user_id')
    if user_id:
        data = json.loads(request.body)
        action = data.get('action')
        address_id = data.get('address_id')
        try:
            address_data = User_adresses.objects.get(id=address_id)
            if action == 'edit':
                return JsonResponse({
                    'success': True,
                    'address_type': address_data.address_type,
                    'is_default': address_data.is_default,
                    'city': address_data.city,
                    'street': address_data.street,
                    'house': address_data.house,
                    'apartment': address_data.apartment,
                    'entrance': address_data.entrance,
                    'floor': address_data.floor,
                    'intercom': address_data.intercom,
                    'comment': address_data.comment,
                })
            else:
                address_data.delete()
                return JsonResponse({
                    'success': True,
                })
        except Exception as error:
            return JsonResponse({
                'success': False,
                'error': 'Ошибка'
            })

    else:
        return JsonResponse({
            'success': False,
            'error': 'Нет авторизации'
        })

@require_POST
def address_update(request):
    user_id = request.session.get('user_id')
    if user_id:
        data = json.loads(request.body)
        address_id = data.get('address_id')
        address_type = data.get('address_type', '').strip()
        city = data.get('city', '').strip()
        street = data.get('street', '').strip()
        house = data.get('house', '').strip()
        apartment = data.get('apartment', '').strip()
        entrance = data.get('entrance', '').strip()
        floor = data.get('floor', '').strip()
        intercom = data.get('intercom', '').strip()
        comment = data.get('comment')
        address_default = data.get('address_default')
        # print(address_type)
        # print(city)
        # print(street)
        # print(house)
        # print(apartment)
        # print(entrance)
        # print(floor)
        # print(intercom)

        if not city:
            return JsonResponse({'success': False, 'error': 'Город обязателен'}, status=400)

        if not street:
            return JsonResponse({'success': False, 'error': 'Улица обязательна'}, status=400)

        if not house:
            return JsonResponse({'success': False, 'error': 'Дом обязателен'}, status=400)

            # 2. Проверка длины
        if len(city) > 100:
            return JsonResponse({'success': False, 'error': 'Слишком длинное название города'}, status=400)

        if len(street) > 200:
            return JsonResponse({'success': False, 'error': 'Слишком длинное название улицы'}, status=400)

        if len(house) > 20:
            return JsonResponse({'success': False, 'error': 'Некорректный номер дома'}, status=400)

        if not city.isalpha():
            return JsonResponse({'success': False, 'error': 'Город содержит цифры'}, status=400)

        if not street.isalpha():
            return JsonResponse({'success': False, 'error': 'Название улицы не может содержать цифр'}, status=400)

        if not apartment.isdigit() and apartment != '':
            return JsonResponse({'success': False, 'error': 'Квартира/офис не должен содержать буквы'}, status=400)

        if not entrance.isdigit() and entrance != '':
            return JsonResponse({'success': False, 'error': 'Подъезд не должен содержать буквы'}, status=400)

        if not floor.isdigit() and entrance != '':
            return JsonResponse({'success': False, 'error': 'Этаж не должен содержать буквы'}, status=400)

        if not intercom.isdigit() and intercom != '':
            return JsonResponse({'success': False, 'error': 'Домофон не должен содержать буквы'}, status=400)

        try:

            address_data = User_adresses.objects.get(id=address_id)


            address_data.address_type = address_type
            address_data.city = city
            address_data.street = street
            address_data.house = house
            address_data.apartment = apartment
            address_data.entrance = entrance
            address_data.floor = floor
            address_data.intercom = intercom
            address_data.comment = comment
            address_data.is_default = address_default
            address_data.save()
            return JsonResponse({
                'success': True,
                'error': 'Успех',
                'address_type': address_type,
                'is_default': address_default,
                'city': city,
                'street': street,
                'house': house,
                'apartment': apartment,
                'entrance': entrance,
                'floor': floor,
                'intercom': intercom,
                'comment': comment
            })
        except Exception as error:
            return JsonResponse({
                'success': False,
                'error': 'Ошибка'
            })
    else:
        return JsonResponse({
            'success': False,
            'error': 'Нет авторизации'
        })


























