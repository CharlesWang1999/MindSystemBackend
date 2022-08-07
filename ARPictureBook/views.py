from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def startPageView(request):
    # return render(request, 'start.html')
    return render(request, 'start.html')
