from django.shortcuts import render, redirect
from .models import Users
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import check_password

def index(request):
    return render(request, 'tets.html')
# Вход в акк
def user_login(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        # user = authenticate(request, username=email, password=password)
        # if user:
        #     login(request, user)

        if Users.objects.filter(email=email).exists():
            user = Users.objects.get(email=email)

            if user.check_password(password):

                # создаем сессию
                request.session['user_id'] = user.id
                request.session['user_email'] = user.email

                if remember_me:
                    #  таймер куки 30 дней
                    request.session.set_expiry(2592000)
                else:
                    #куки до закрытия браузера
                    request.session.set_expiry(0)
                print(user.is_authenticated)
                print(12312312)
                return redirect('/menu')

            else:
                context['error'] = 'Неверный Пароль или Email'
                return render(request, 'login.html', context)
        else:
            context['error'] = 'Неверный Email'
            return render(request, 'sign up.html', context)
    return render(request, 'login.html')

# Регистрация нового user
def sign_up(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Users()
            user
            user.name = name
            user.email = email
            user.set_password(password)
            user.save()
            # Users.objects.all().delete()
            users = Users.objects.all()
            print(users)
            return redirect('/authorization/login')
        except:
            context['error'] = 'Пользователь с таким email уже существует'
            return render(request, 'sign up.html', context)


    return render(request, 'sign up.html')



def test(request):
    users = Users.objects.all()
    for i in users.all():
        print(i.name)
        print(i.email)
        print(i.password)
        # Users.objects.all().delete()
        # Users.save()
    return render(request, 'testfile.html')





def check_session_view(request):
    # Способ 1: Проверить конкретную переменную в сессии
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        print(f"Сессия существует! user_id: {user_id}")
    else:
        print("Сессии нет или user_id не в сессии")

    # Способ 2: Проверить, есть ли вообще сессия
    if request.session.session_key:
        print(f"Сессия активна, ключ: {request.session.session_key}")
    else:
        print("Сессия не создана")

    # Способ 3: Проверить авторизацию пользователя
    if request.user.is_authenticated:
        print(f"✅ Авторизован: {request.user.email}")
    else:
        print("❌ Не авторизован")

    return render(request, 'testfile.html')


def profile_view(request):
    # Проверяем, есть ли пользователь в сессии
    user_id = request.session.get('user_id')

    if not user_id:
        # Не авторизован - отправляем на login
        return redirect('login')

    # Получаем данные пользователя из БД
    try:
        user = Users.objects.get(id=user_id)
        print(user.name)
        print(user.email)
        return render(request, 'testfile.html', {'user': user})
    except Users.DoesNotExist:
        # Пользователь удален - очищаем сессию
        del request.session['user_id']
        return redirect('login')