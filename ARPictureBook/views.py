from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from ARPictureBook.models import (
    UserAnswerInfo,
    AnswerResult
)
from django.contrib.auth.models import User

import os
from datetime import datetime
import random
if settings.KINECT_RECORD:
    from MindSystemBackend.kinectRecord import KinectRecord
    from MindSystemBackend.actionAnalysis import ActionAnalysis
if settings.CAMERA_RECORD:
    from MindSystemBackend.videoRecord import VideoRecord
    from MindSystemBackend.microExpressionAnalysis import MicroExpressionAnalysis
from queue import SimpleQueue
from threading import Thread
from time import sleep
import cv2
from ffpyplayer.player import MediaPlayer

if settings.KINECT_RECORD:
    kinect_record = KinectRecord()
    action_analysis = ActionAnalysis()
    action_video_save_path = ''

# will be different in different situations, plz overwrite camera id in settings.
if settings.CAMERA_RECORD:
    camera_id = settings.CAMERA_ID
    video_record = VideoRecord(camera_id)
    micro_expression_analysis = MicroExpressionAnalysis()
    micro_expression_save_path = ''

video_data_save_path = 'VideoData'
analysis_thread_queue = SimpleQueue()


def analysis_thread():
    while True:
        while analysis_thread_queue.empty():
            print(f'analysis_thread_queue is empty at {datetime.now()}')
            sleep(10)
        current_analysis_thread = analysis_thread_queue.get()
        current_analysis_thread.start()
        print(f'start analysis {current_analysis_thread.name} there still has {analysis_thread_queue.qsize()} analysis thread waited')
        current_analysis_thread.join()


def start_record():
    start_time = datetime.now()
    video_data_save_dir_this_round = f'{video_data_save_path}/{start_time.year:=04}_{start_time.month:=02}_{start_time.day:=02}_{start_time.hour:=02}_{start_time.minute:=02}_{start_time.second:=02}'
    if not os.path.exists(video_data_save_dir_this_round):
        os.mkdir(video_data_save_dir_this_round)

    global action_video_save_path
    global micro_expression_save_path

    if settings.KINECT_RECORD:
        action_video_save_path = f'{video_data_save_dir_this_round}/kinect_action.avi'
        kinect_record.start_record(action_video_save_path)
    if settings.CAMERA_RECORD:
        micro_expression_save_path = f'{video_data_save_dir_this_round}/camera_micro_expression.avi'
        video_record.start_record(micro_expression_save_path)


def stop_record(uaid=None, page_name=None, question_num=None):
    if settings.KINECT_RECORD:
        kinect_record.stop_record()
    if settings.CAMERA_RECORD:
        video_record.stop_record()

    if settings.KINECT_RECORD:
        action_thread = Thread(
            name=f'analysis {action_video_save_path}',
            target=action_analysis.analysis, args=(action_video_save_path,)
        )
        analysis_thread_queue.put(action_thread)
    if settings.CAMERA_RECORD:
        micro_expression_thread = Thread(
            name=f'analysis {micro_expression_save_path}',
            target=micro_expression_analysis.analysis,
            args=(micro_expression_save_path, uaid, page_name, question_num, )
        )
        analysis_thread_queue.put(micro_expression_thread)


def cartoon_video_thread(file_name):
    cv2.destroyAllWindows()
    video_path = os.path.join(settings.BASE_DIR, 'ARPictureBook', 'static', 'cartoon', file_name)
    video = cv2.VideoCapture(video_path)
    player = MediaPlayer(video_path)
    while True:
        grabbed, frame = video.read()
        audio_frame, val = player.get_frame()
        if not grabbed:
            print("End of video")
            break
        if cv2.waitKey(28) & 0xFF == ord("q"):
            break
        cv2.imshow("Video", frame)
        if val != 'eof' and audio_frame is not None:
            # audio
            img, t = audio_frame
    video.release()
    # sleep(10)
    # cv2.destroyAllWindows()


if settings.KINECT_RECORD or settings.CAMERA_RECORD:
    analysis_main_thread = Thread(name='analysis_main_thread', target=analysis_thread)
    analysis_main_thread.start()


# Create your views here.
def choose_mode_view(request):
    return render(request, 'choose_mode.html')


def question_page_view(request, uaid, page_index):
    user = User.objects.filter(pk=1).first()
    user_answer_info = UserAnswerInfo.objects.filter(pk=uaid).first()
    if user_answer_info and user_answer_info.user == user:
        start_record()
        # show_cartoon_video_thread = Thread(name='show_cartoon_video_thread', target=cartoon_video_thread, args=('cartoon_first.avi',))
        # show_cartoon_video_thread.start()
        page_name = settings.PAGE_NUM_TO_NAME[user_answer_info.get_page_order()[page_index]]
        print('@131---', page_name)
        return render(request, f'{page_name}.html', {'uaid': uaid, 'page_index': page_index})
    else:
        return render(request, 'error.html')


def choose_mode_submit_view(request):
    running_mode = request.POST.get('mode')
    user = User.objects.filter(pk=1).first()
    page_order = [i for i in range(settings.MAX_QUESTION_PAGE)]
    random.shuffle(page_order)
    print('@140--', running_mode, user, page_order)
    previous_user_answer_info = UserAnswerInfo.objects.filter(user=user).order_by('-answer_id')
    answer_id = 1
    if previous_user_answer_info:
        answer_id = previous_user_answer_info.first().answer_id + 1
    user_answer_info = UserAnswerInfo(
        user=user,
        answer_id=answer_id,
        running_mode=running_mode
    )
    user_answer_info.set_page_order(page_order)
    print('@156---', user_answer_info.page_order)
    user_answer_info.save()
    return JsonResponse({"status": "success", 'answer_id': answer_id, 'next_page': settings.PAGE_NUM_TO_NAME[page_order[0]], 'index': 0})


@csrf_exempt
def get_query_result_view(request):
    page_name = request.POST.get('page_name')
    uaid = request.POST.get('uaid', None)
    page_index = request.POST.get('page_index', None)
    result1 = request.POST.get('result1', None)
    result2 = request.POST.get('result2', None)
    result3 = request.POST.get('result3', None)
    result1 = result1 == 'correct'
    result2 = result2 == 'correct'
    result3 = result3 == 'correct'
    user = User.objects.filter(pk=1).first()
    print(result1, result2, result3, uaid, type(uaid), page_index)
    if uaid and uaid.isdigit():
        uaid = int(uaid)
        user_answer_info = UserAnswerInfo.objects.filter(pk=uaid).first()
        if not user_answer_info or user_answer_info.user != user:
            return JsonResponse({"status": "error", "errormessage": "can not found answer info by uaid"})
    else:
        return JsonResponse({"status": "error", "errormessage": "UnExpected Error... Maybe dismiss id..."})
    if page_index and page_index.isdigit():
        page_index = int(page_index)
    else:
        return JsonResponse({"status": "error", "errormessage": "UnExpected Error... Maybe dismiss page index..."})
    result_list = [result1, result2, result3]
    for question_num in range(3):
        answer_result = AnswerResult.objects.filter(
            answer_info=user_answer_info,
            page_name=page_name,
            question_num=question_num
        ).first()
        if not answer_result:
            answer_result = AnswerResult(
                answer_info=user_answer_info,
                page_name=page_name,
                question_num=question_num
            )
        answer_result.question_result = result_list[question_num]
        answer_result.save()

    stop_record(uaid=uaid, page_name=page_name, question_num=2)

    have_next_page = page_index != settings.MAX_QUESTION_PAGE - 1
    context = {
        "status": "success",
        "have_next_page": have_next_page,
        "uaid": uaid
    }
    if have_next_page:
        context['next_page_index'] = page_index + 1

    return JsonResponse(context)


@csrf_exempt
def get_web_click_view(request):
    page_name = request.POST.get('page_name', None)
    question_num = request.POST.get('question_num', None)
    uaid = request.POST.get('uaid', None)
    user = User.objects.filter(pk=1).first()
    if uaid and uaid.isdigit():
        uaid = int(uaid)
        user_answer_info = UserAnswerInfo.objects.filter(pk=uaid).first()
        if not user_answer_info or user_answer_info.user != user:
            return JsonResponse({"status": "error", "errormessage": "can not found answer info by uaid"})
    else:
        return JsonResponse({"status": "error", "errormessage": "UnExpected Error... Maybe dismiss id..."})
    print('@186---', page_name, question_num, type(question_num))
    question_num = int(question_num)
    stop_record(uaid=uaid, page_name=page_name, question_num=question_num)
    print("继续开始录制")
    start_record()

    return JsonResponse({"status": "success"})
