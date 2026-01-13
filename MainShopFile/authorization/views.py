from django.shortcuts import render


def index(request):
    return render(request, 'loginPage.html')


def test(request):
    return render(request, 'testfile.html')

# Create your views ere.
