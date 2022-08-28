from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ARPictureBook.models import (
    StartPageResult,
    SecondPageResult,
    ThirdPageResult
)

# import os
# from datetime import datetime
# # from MindSystemBackend.kinectRecord import KinectRecord
# from MindSystemBackend.videoRecord import VideoRecord
# from MindSystemBackend.actionAnalysis import ActionAnalysis
# from MindSystemBackend.microExpressionAnalysis import MicroExpressionAnalysis
# from queue import SimpleQueue
# from threading import Thread
# from time import sleep

# kinect_record = KinectRecord()
# # will be different in different situations
# camera_id = 0
# video_record = VideoRecord(camera_id)
# action_analysis = ActionAnalysis()
# micro_expression_analysis = MicroExpressionAnalysis()

# video_data_save_path = 'VideoData'
# action_video_save_path = ''
# micro_expression_save_path = ''

# analysis_thread_queue = SimpleQueue()


# def analysis_thread():
#     while True:
#         while analysis_thread_queue.empty():
#             print(f'analysis_thread_queue is empty at {datetime.now()}')
#             sleep(10)
#         current_analysis_thread = analysis_thread_queue.get()
#         current_analysis_thread.start()
#         print(f'start analysis {current_analysis_thread.name} there still has {analysis_thread_queue.qsize()} analysis thread waited')
#         current_analysis_thread.join()


# def start_record():
#     start_time = datetime.now()
#     video_data_save_dir_this_round = f'{video_data_save_path}/{start_time.year:=04}_{start_time.month:=02}_{start_time.day:=02}_{start_time.hour:=02}_{start_time.minute:=02}_{start_time.second:=02}'
#     if not os.path.exists(video_data_save_dir_this_round):
#         os.mkdir(video_data_save_dir_this_round)

#     global action_video_save_path
#     global micro_expression_save_path

#     action_video_save_path = f'{video_data_save_dir_this_round}/kinect_action.avi'
#     micro_expression_save_path = f'{video_data_save_dir_this_round}/camera_micro_expression.avi'
#     # kinect_record.start_record(action_video_save_path)
#     video_record.start_record(micro_expression_save_path)


# def stop_record():
#     # kinect_record.stop_record()
#     video_record.stop_record()

#     action_thread = Thread(
#         name=f'analysis {action_video_save_path}',
#         target=action_analysis.analysis, args=(action_video_save_path,)
#     )
#     micro_expression_thread = Thread(
#         name=f'analysis {micro_expression_save_path}',
#         target=micro_expression_analysis.analysis, args=(micro_expression_save_path, )
#     )
#     analysis_thread_queue.put(action_thread)
#     analysis_thread_queue.put(micro_expression_thread)


# analysis_main_thread = Thread(name='analysis_main_thread', target=analysis_thread)
# analysis_main_thread.start()

# Create your views here.


def start_page_view(request):
    # start_record()
    return render(request, 'start.html')


def second_page_view(request):
    # start_record()
    return render(request, 'second.html')


def third_page_view(request):
    # start_record()
    return render(request, 'third.html')


@csrf_exempt
def get_query_result_view(request):
    # stop_record()
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
        second_page_result = SecondPageResult.objects.filter(
            start_page_result=start_page_result)
        if second_page_result:
            second_page_result = second_page_result.first()
        else:
            second_page_result = SecondPageResult(
                start_page_result=start_page_result)
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
        third_page_result = ThirdPageResult.objects.filter(
            start_page_result=start_page_result)
        if third_page_result:
            third_page_result = third_page_result.first()
        else:
            third_page_result = ThirdPageResult(
                start_page_result=start_page_result)
        third_page_result.first_result = result1
        third_page_result.second_result = result2
        third_page_result.third_result = result3
        third_page_result.save()
    else:
        return JsonResponse({"status": "error", "errormessage": "UnExpected Error... Maybe dismiss id..."})

    return JsonResponse({"status": "success", "result_id": result_id})
