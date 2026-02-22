from django.shortcuts import render, redirect
from authorization.models import Users

# Create your views here.
def index(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Users.objects.get(id=user_id)
        print(user_id)
        user_data = Users.objects.get(id=user_id)
        print(user_data.email)
        print(user_data.name)
        print(user_data.created_at)
        return render(request, 'profile.html', {'user': user})
    # не забыть проверить
    return redirect('/')