from django.shortcuts import render
from authorization.models import Users

def index(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Users.objects.get(id=user_id)
        print(user_id)
        return render(request, 'menuPage.html', {'user': user})
    return render(request, 'menuPage.html')

