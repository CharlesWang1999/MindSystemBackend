from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def start_page_view(request):
    return render(request, 'start.html')


def second_page_view(request):
    return render(request, 'second.html')


def third_page_view(request):
    return render(request, 'third.html')


@csrf_exempt
def get_query_result_view(request):
    print('test ajax function')
    print(request.POST)
    print(request.POST.get('data', 'no data'))
    return JsonResponse({"status": "success"})
