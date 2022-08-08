from django.shortcuts import render

# Create your views here.


def startPageView(request):
    return render(request, 'start.html')


def secondPageView(request):
    return render(request, 'second.html')


def thirdPageView(request):
    return render(request, 'third.html')
