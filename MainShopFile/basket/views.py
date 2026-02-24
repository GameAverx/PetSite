from django.shortcuts import render, redirect
from authorization.models import Users

# import requests


# Create your views here.
def index(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Users.objects.get(id=user_id)
        print(user_id)
        # try
        # response = requests.get('https://gateway.timeapi.world/timezone/America/New_York')
        # data = response.json()
        # print(data)
        return render(request, 'basket.html', {'user': user})
    # не забыть проверить
    return redirect('/')



