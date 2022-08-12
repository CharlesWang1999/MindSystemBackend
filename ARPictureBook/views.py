from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ARPictureBook.models import (
    StartPageResult,
    SecondPageResult,
    ThirdPageResult
)

# Create your views here.


def start_page_view(request):
    return render(request, 'start.html')


def second_page_view(request):
    return render(request, 'second.html')


def third_page_view(request):
    return render(request, 'third.html')


@csrf_exempt
def get_query_result_view(request):
    page_name = request.POST.get('page_name')
    result_id = request.POST.get('result_id', None)
    result1 = request.POST.get('result1', None)
    result2 = request.POST.get('result2', None)
    result3 = request.POST.get('result3', None)
    result1 = result1 == 'correct'
    result2 = result2 == 'correct'
    result3 = result3 == 'correct'
    print(result1, result2, result3, result_id)
    if page_name == 'start' and result_id is None:
        start_page_result = StartPageResult(
            first_result=result1,
            second_result=result2,
            third_result=result3,
        )
        start_page_result.save()
        result_id = start_page_result.id
    elif page_name == 'start' and result_id.isdigit():
        result_id = int(result_id)
        start_page_result = StartPageResult.objects.filter(id=result_id)
        if start_page_result:
            start_page_result = start_page_result.first()
        else:
            start_page_result = StartPageResult()
        start_page_result.first_result = result1
        start_page_result.second_result = result2
        start_page_result.third_result = result3
        start_page_result.save()
        result_id = start_page_result.id
    elif page_name == 'second' and result_id.isdigit():
        result_id = int(result_id)
        start_page_result = StartPageResult.objects.filter(id=result_id)
        if start_page_result:
            start_page_result = start_page_result.first()
        else:
            return JsonResponse({"status": "error", "errormessage": 'can not find the id in start page!'})
        second_page_result = SecondPageResult.objects.filter(start_page_result=start_page_result)
        if second_page_result:
            second_page_result = second_page_result.first()
        else:
            second_page_result = SecondPageResult(start_page_result=start_page_result)
        second_page_result.first_result = result1
        second_page_result.second_result = result2
        second_page_result.third_result = result3
        second_page_result.save()
    elif page_name == 'third' and result_id.isdigit():
        result_id = int(result_id)
        start_page_result = StartPageResult.objects.filter(id=result_id)
        if start_page_result:
            start_page_result = start_page_result.first()
        else:
            return JsonResponse({"status": "error", "errormessage": 'can not find the id in start page!'})
        third_page_result = ThirdPageResult.objects.filter(start_page_result=start_page_result)
        if third_page_result:
            third_page_result = third_page_result.first()
        else:
            third_page_result = ThirdPageResult(start_page_result=start_page_result)
        third_page_result.first_result = result1
        third_page_result.second_result = result2
        third_page_result.third_result = result3
        third_page_result.save()
    else:
        return JsonResponse({"status": "error", "errormessage": "UnExpected Error... Maybe dismiss id..."})

    return JsonResponse({"status": "success", "result_id": result_id})
