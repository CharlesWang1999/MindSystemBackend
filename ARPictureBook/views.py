from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from ARPictureBook.models import (
    UserAnswerInfo,
    AnswerResult
)
from ARPictureBook.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
def login_view(request):
    user_form = UserForm()
    user = None
    context = {"user_form": user_form}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
    if request.method == "POST" and not user:
        context['message'] = "invalid login"
    if user is not None:
        login(request, user)
        return redirect("choose_mode")
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect("login")


def smooth_music_view(request, uaid, round_num, page_round):
    valid_page_round = ['s1', 'link', 's2', 's3', 's4']
    if page_round not in valid_page_round:
        return render(request, 'error.html')
    user = request.user
    print('@144---', user)
    user_answer_info = UserAnswerInfo.objects.filter(pk=uaid).first()
    if user_answer_info and user_answer_info.user == user:
        return render(request, 'smooth_music.html', {'uaid': uaid, 'round_num': round_num, 'page_round': page_round})
    else:
        return render(request, 'error.html')


@login_required
def choose_mode_view(request):
    return render(request, 'choose_mode.html')


@login_required
@csrf_exempt
def question_click_view(request):
    uaid = request.POST.get('uaid', None)
    round_num = request.POST.get('round_num', None)
    page_round = request.POST.get('page_round', None)
    round_num = int(round_num)
    user = request.user
    if uaid and uaid.isdigit():
        uaid = int(uaid)
        user_answer_info = UserAnswerInfo.objects.filter(pk=uaid).first()
        if not user_answer_info or user_answer_info.user != user:
            return JsonResponse({"status": "error", "errormessage": "can not found answer info by uaid"})
    else:
        return JsonResponse({"status": "error", "errormessage": "UnExpected Error... Maybe dismiss id..."})
    running_mode = user_answer_info.running_mode
    have_next_page = round_num != settings.MAX_ROUND_NUM
    context = {
        "status": "success",
        "have_next_page": have_next_page,
        "uaid": uaid,
        "running_mode": running_mode,
        "round_num": round_num,
        "page_round": page_round
    }
    if page_round == 'link':
        if have_next_page:
            context['next_round_num'] = round_num + 1
        else:
            next_round_num = 1
            next_page_round = 's2'
            context['next_round_num'] = next_round_num
            context['next_page_round'] = next_page_round
    print('@193---', context)
    return JsonResponse(context)


@login_required
@csrf_exempt
def self_report_click_view(request):
    uaid = request.POST.get('uaid', None)
    round_num = request.POST.get('round_num', None)
    page_round = request.POST.get('page_round', None)
    print('@178---', page_round)
    round_num = int(round_num)
    user = request.user
    if uaid and uaid.isdigit():
        uaid = int(uaid)
        user_answer_info = UserAnswerInfo.objects.filter(pk=uaid).first()
        if not user_answer_info or user_answer_info.user != user:
            return JsonResponse({"status": "error", "errormessage": "can not found answer info by uaid"})
    else:
        return JsonResponse({"status": "error", "errormessage": "UnExpected Error... Maybe dismiss id..."})
    running_mode = user_answer_info.running_mode
    print('@189---', running_mode)
    have_next_page = round_num != settings.MAX_ROUND_NUM
    context = {
        "status": "success",
        "have_next_page": have_next_page,
        "uaid": uaid,
        "running_mode": running_mode,
        "round_num": round_num
    }
    if have_next_page:
        context['next_round_num'] = round_num + 1
    else:
        next_round_num = 1
        next_page_round = None
        if page_round == 's1':
            next_page_round = 'link'
        elif page_round == 'link':
            next_page_round = 's2'
        elif page_round == 's2':
            next_page_round = 's3'
        elif page_round == 's3':
            next_page_round = 's4'
        context['next_round_num'] = next_round_num
        context['next_page_round'] = next_page_round

    return JsonResponse(context)


@login_required
@csrf_exempt
def smooth_music_click_view(request):
    uaid = request.POST.get('uaid', None)
    round_num = request.POST.get('round_num', None)
    page_round = request.POST.get('page_round', None)
    round_num = int(round_num)
    have_next_page = round_num != settings.MAX_ROUND_NUM
    if have_next_page:
        next_page_round = page_round
        next_round_num = round_num + 1
    else:
        next_round_num = 1
        if page_round == 's1':
            next_page_round = 'link'
        elif page_round == 'link':
            next_page_round = 's2'
        elif page_round == 's2':
            next_page_round = 's3'
        elif page_round == 's3':
            next_page_round = 's4'
    context = {
        'uaid': uaid,
        'next_round_num': next_round_num,
        'next_page_round': next_page_round
    }
    print('@241---', context)
    return JsonResponse(context)


@login_required
def question_s1_view(request, uaid, round_num):
    # command = 'python PlayVideo/playVideoAtWeb.py sub01-1.mp4'
    command = 'python PlayVideo/playImageAtWeb.py start2.jpg'
    os.system(command)
    return render(request, 'question_s1.html', {'uaid': uaid, 'round_num': round_num})


@login_required
def question_link_view(request, uaid, round_num):
    command = 'python PlayVideo/playImageAtWeb.py start2.jpg'
    os.system(command)
    if round_num == 1:
        img_name = 'start.jpg'
    elif round_num == 2:
        img_name = 'start2.jpg'
    elif round_num == 3:
        img_name = 'start.jpg'
    elif round_num == 4:
        img_name = 'start2.jpg'
    elif round_num == 5:
        img_name = 'start.jpg'
    elif round_num == 6:
        img_name = 'start2.jpg'
        
    return render(request, 'question_link.html', {'uaid': uaid, 'round_num': round_num, 'img_name': img_name})


@login_required
def question_s2_view(request, uaid, round_num):
    command = 'python PlayVideo/playVideoAtWeb.py sub01-1.mp4'
    os.system(command)
    return render(request, 'question_s2.html', {'uaid': uaid, 'round_num': round_num})


@login_required
def question_s3_view(request, uaid, round_num):
    command = 'python PlayVideo/playVideoAtWeb.py sub01-1.mp4'
    os.system(command)
    return render(request, 'question_s3.html', {'uaid': uaid, 'round_num': round_num})


@login_required
def question_s4_view(request, uaid, round_num):
    command = 'python PlayVideo/playVideoAtWeb.py sub01-1.mp4'
    os.system(command)
    return render(request, 'question_s4.html', {'uaid': uaid, 'round_num': round_num})


@login_required
def self_report_s1_view(request, uaid, round_num):
    return render(request, 'self_report_s1.html', {'uaid': uaid, 'round_num': round_num})


@login_required
def self_report_s2_view(request, uaid, round_num):
    return render(request, 'self_report_s2.html', {'uaid': uaid, 'round_num': round_num})


@login_required
def self_report_s3_view(request, uaid, round_num):
    return render(request, 'self_report_s3.html', {'uaid': uaid, 'round_num': round_num})


@login_required
def self_report_s4_view(request, uaid, round_num):
    return render(request, 'self_report_s4.html', {'uaid': uaid, 'round_num': round_num})


@login_required
def system_evaluate_view(request, uaid):
    return render(request, 'system_evaluate.html', {'uaid': uaid})


@login_required
def experiment_evaluate_view(request, uaid):
    return render(request, 'experiment_evaluate.html', {'uaid': uaid})


@login_required
def finish_view(request, uaid):
    return render(request, 'finish.html', {'uaid': uaid})


@csrf_exempt
@login_required
def system_evaluate_click_view(request):
    return JsonResponse({'status': "success"})


@csrf_exempt
@login_required
def experiment_evaluate_click_view(request):
    return JsonResponse({'status': "success"})


@login_required
def question_page_view(request, uaid, page_index):
    user = request.user
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


@login_required
def choose_mode_submit_view(request):
    running_mode = request.POST.get('mode')
    user = request.user
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
    return JsonResponse({"status": "success", "uaid": user_answer_info.id})


@csrf_exempt
@login_required
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
    user = request.user
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
    running_mode = user_answer_info.running_mode
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
        "uaid": uaid,
        "running_mode": running_mode
    }
    if have_next_page:
        context['next_page_index'] = page_index + 1

    return JsonResponse(context)


@csrf_exempt
@login_required
def get_web_click_view(request):
    page_name = request.POST.get('page_name', None)
    question_num = request.POST.get('question_num', None)
    uaid = request.POST.get('uaid', None)
    user = request.user
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
