from django.shortcuts import render


def index(request):
    return render(request, 'mainList/MainPage.html')



# def index(request):
#     return render(request, 'mainList/mainPage.html')

# Create your views here.
def about(request):
    return render(request, 'mainList/about.html')
