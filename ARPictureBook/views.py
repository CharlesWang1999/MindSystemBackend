from cmath import pi
from decimal import Rounded
from math import exp
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from ARPictureBook.models import (
    UserAnswerInfo,
    AnswerResult,
    FinalResult
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
from time import sleep, time
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
time_txt_save_path = 'VideoData/time'


def analysis_thread():
    while True:
        while analysis_thread_queue.empty():
            print(f'analysis_thread_queue is empty at {datetime.now()}')
            sleep(10)
        current_analysis_thread = analysis_thread_queue.get()
        current_analysis_thread.start()
        print(f'start analysis {current_analysis_thread.name} there still has {analysis_thread_queue.qsize()} analysis thread waited')
        current_analysis_thread.join()


def start_record(uaid, page_round, round_num, imi=False):
    start_time = datetime.now()
    this_time_txt_save_path = time_txt_save_path+'/'+str(uaid)+'.txt'
    with open(str(this_time_txt_save_path), "a") as f:
        if (imi):
            str_write = str(start_time)+' '+str(page_round)+'??????'+'???'+str(round_num)+'???'+" ??????????????????\n"
        else:
            str_write = str(start_time)+' ??????????????????'+'???'+str(round_num)+'???'+" ??????????????????\n"
        f.write(str_write)
    video_data_save_dir_this_round = f'{video_data_save_path}/{start_time.year:=04}_{start_time.month:=02}_{start_time.day:=02}_{start_time.hour:=02}_{start_time.minute:=02}_{start_time.second:=02}_{uaid}_{page_round}_{round_num}'
    if imi:
        video_data_save_dir_this_round += '_imi'
    if not os.path.exists(video_data_save_dir_this_round):
        os.mkdir(video_data_save_dir_this_round)

    global action_video_save_path
    global micro_expression_save_path

    if settings.KINECT_RECORD:
        action_video_save_path = f'{video_data_save_dir_this_round}/kinect_action.avi'
        kinect_record.start_record(action_video_save_path)
    if settings.CAMERA_RECORD:
        micro_expression_save_path = f'{video_data_save_dir_this_round}/camera_micro_expression.mp4'
        video_record.start_record(micro_expression_save_path)


def stop_record(uaid, page_round, round_num, imi=False):
    start_time = datetime.now()
    this_time_txt_save_path = time_txt_save_path+'/'+str(uaid)+'.txt'
    with open(str(this_time_txt_save_path), "a") as f:
        str_write = str(start_time)+' '+str(page_round)+'??????'+'???'+str(round_num)+'???'+" ??????????????????\n"
        f.write(str_write)
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
            args=(micro_expression_save_path, uaid, page_round, round_num, imi, )
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
        start_time = datetime.now()
        this_time_txt_save_path=time_txt_save_path+'/'+str(uaid)+'.txt'
        with open(str(this_time_txt_save_path),"a") as f:
            str_write=str(start_time)+' '+str(page_round)+'??????'+'???'+str(round_num)+'???'+" ????????????????????????\n"
            f.write(str_write)
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
    question_info = request.POST.get('question_info', None)
    print('@178---', page_round, question_info)
    round_num = int(round_num)
    user = request.user
    if uaid and uaid.isdigit():
        uaid = int(uaid)
        user_answer_info = UserAnswerInfo.objects.filter(pk=uaid).first()
        if not user_answer_info or user_answer_info.user != user:
            return JsonResponse({"status": "error", "errormessage": "can not found answer info by uaid"})
    else:
        return JsonResponse({"status": "error", "errormessage": "UnExpected Error... Maybe dismiss id..."})
    stop_record(uaid, page_round, round_num)
    running_mode = user_answer_info.running_mode
    have_next_page = round_num != settings.MAX_ROUND_NUM
    final_result_queryset = FinalResult.objects.filter(
        answer_info=user_answer_info,
        page_round=page_round,
        round_num=round_num
    )
    final_result = None
    if final_result_queryset:
        final_result = final_result_queryset.first()
    else:
        final_result = FinalResult(
            answer_info=user_answer_info,
            page_round=page_round,
            round_num=round_num
        )
    final_result.question_result = question_info
    final_result.save()
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
    start_time = datetime.now()
    this_time_txt_save_path=time_txt_save_path+'/'+str(uaid)+'.txt'
    with open(str(this_time_txt_save_path),"a") as f:
        str_write=str(start_time)+' question_'+str(page_round)+'??????'+'???'+str(round_num)+'???'+" ????????????\n"
        f.write(str_write)
    return JsonResponse(context)


@login_required
@csrf_exempt
def self_report_click_view(request):
    uaid = request.POST.get('uaid', None)
    round_num = request.POST.get('round_num', None)
    page_round = request.POST.get('page_round', None)
    question_info = request.POST.get('question_info', None)
    other_info = request.POST.get('other_info', None)
    print('@178---', page_round, question_info, other_info)
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
    final_result_queryset = FinalResult.objects.filter(
        answer_info=user_answer_info,
        page_round=page_round,
        round_num=round_num
    )
    final_result = None
    if final_result_queryset:
        final_result = final_result_queryset.first()
    else:
        final_result = FinalResult(
            answer_info=user_answer_info,
            page_round=page_round,
            round_num=round_num
        )
    final_result.self_report_result = question_info
    if question_info == 'D':
        final_result.self_report_result_detail = other_info
    print('@254--', final_result.self_report_result)
    final_result.save()
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
    start_time = datetime.now()
    this_time_txt_save_path=time_txt_save_path+'/'+str(uaid)+'.txt'
    with open(str(this_time_txt_save_path),"a") as f:
        str_write=str(start_time)+' self_report_'+str(page_round)+'??????'+'???'+str(round_num)+'???'+" ????????????\n"
        f.write(str_write)
    return JsonResponse(context)


@login_required
@csrf_exempt
def smooth_music_click_view(request):
    uaid = request.POST.get('uaid', None)
    round_num = request.POST.get('round_num', None)
    page_round = request.POST.get('page_round', None)
    round_num = int(round_num)
    have_next_page = round_num != settings.MAX_ROUND_NUM
    next_page_round = None
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
    user_answer_info = UserAnswerInfo.objects.filter(pk=uaid).first()
    running_mode = user_answer_info.running_mode
    print('@189---', running_mode)
    context = {
        'uaid': uaid,
        'next_round_num': next_round_num,
        'next_page_round': next_page_round,
        "running_mode": running_mode,
        "have_next_page": have_next_page
    }
    print('@241---', context)
    start_time = datetime.now()
    this_time_txt_save_path=time_txt_save_path+'/'+str(uaid)+'.txt'
    with open(str(this_time_txt_save_path),"a") as f:
        str_write=str(start_time)+' smooth_music_'+str(page_round)+'??????'+'???'+str(round_num)+'???'+" ????????????\n"
        f.write(str_write)
    return JsonResponse(context)



@login_required
@csrf_exempt
def task_click_view(request):
    uaid = request.POST.get('uaid', None)
    round_num = request.POST.get('round_num', None)
    page_round = request.POST.get('page_round', None)
    round_num = int(round_num)
    have_next_page = round_num != settings.MAX_ROUND_NUM
    next_page_round = None
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
    user_answer_info = UserAnswerInfo.objects.filter(pk=uaid).first()
    running_mode = user_answer_info.running_mode
    print('@189---', running_mode)
    context = {
        'uaid': uaid,
        'next_round_num': next_round_num,
        'next_page_round': next_page_round,
        "running_mode": running_mode,
        "have_next_page": have_next_page
    }
    print('@241---', context)
    start_time = datetime.now()
    this_time_txt_save_path=time_txt_save_path+'/'+str(uaid)+'.txt'
    with open(str(this_time_txt_save_path),"a") as f:
        str_write=str(start_time)+' task_'+str(page_round)+'??????'+'???'+str(round_num)+'???'+" ????????????\n"
        f.write(str_write)
    return JsonResponse(context)



@login_required
def question_s1_view(request, uaid, round_num,running_mode):
    # command = 'python PlayVideo/playVideoAtWeb.py sub01-1.mp4'
    # command = 'python PlayVideo/playImageAtWeb.py start2.jpg' 

    command = 'python PlayVideo/playImageAtWeb.py '+str(running_mode)+'-s1-'+str(round_num)+'.jpg'
    os.system(command)
    start_time = datetime.now()
    this_time_txt_save_path=time_txt_save_path+'/'+str(uaid)+'.txt'
    with open(str(this_time_txt_save_path),"a") as f:
        str_write=str(start_time)+' question_s1??????'+'???'+str(round_num)+'???'+" ????????????\n"
        f.write(str_write)
    start_record(uaid, 's1', round_num)
    img_name = str(running_mode) +'-s1-'+str(round_num)+'.jpg'
    return render(request, 'question_s1.html', {'uaid': uaid, 'round_num': round_num, 'img_name': img_name})


@login_required
def question_link_view(request, uaid, round_num,running_mode):
    # if(running_mode=='Extra'):
    #     command = 'python PlayVideo/playImageAtWeb.py extra-link-'+str(round_num)+'.jpg'
    # else:
    #     command = 'python PlayVideo/playImageAtWeb.py link-'+str(round_num)+'.jpg'
    command ='python PlayVideo/playImageAtWeb.py '+str(running_mode)+'-link.jpg'
    os.system(command)
    start_time = datetime.now()
    this_time_txt_save_path=time_txt_save_path+'/'+str(uaid)+'.txt'
    with open(str(this_time_txt_save_path),"a") as f:
        str_write=str(start_time)+' question_link??????'+'???'+str(round_num)+'???'+" ????????????\n"
        f.write(str_write)
    start_record(uaid, 'link', round_num)
    img_name = str(running_mode) +'-link-'+str(round_num)+'.jpg'
    return render(request, 'question_link.html', {'uaid': uaid, 'round_num': round_num, 'img_name': img_name})


@login_required
def question_s2_view(request, uaid, round_num,running_mode):
    command = 'python PlayVideo/playImageAtWeb.py ARmaker.jpg' #??????ARmaker
    os.system(command)
    sleep(0.1)
    command = 'python PlayVideo/playVideoAtWeb.py '+str(running_mode)+'-s2-'+str(round_num)+'.mp4'
    os.system(command)
    start_time = datetime.now()
    this_time_txt_save_path=time_txt_save_path+'/'+str(uaid)+'.txt'
    with open(str(this_time_txt_save_path),"a") as f:
        str_write=str(start_time)+' question_s2??????'+'???'+str(round_num)+'???'+" ????????????\n"
        f.write(str_write)
    start_record(uaid, 's2', round_num)
    video_name=str(running_mode)+'-s2-'+str(round_num)+'.mp4'
    return render(request, 'question_s2.html', {
        'uaid': uaid,
        'round_num': round_num,
        'video_name': video_name,
        'running_mode': running_mode,
    })


@login_required
def question_s3_view(request, uaid, round_num,running_mode):
    print(running_mode)
    if (running_mode == 'Extra'):
        command = 'python PlayVideo/playImageAtWeb.py ARmaker-'+str(round_num)+'.jpg'  #??????ARmaker
    elif (running_mode == 'Production'):
        command = 'python PlayVideo/playImageAtWeb.py ARmaker-'+str((round_num+2)%6+1)+'.jpg'  #??????ARmaker
    else:
        command = 'python PlayVideo/playImageAtWeb.py ARmaker.jpg'  #??????ARmaker
    os.system(command)
    sleep(0.1)
    
    start_time = datetime.now()
    this_time_txt_save_path = time_txt_save_path+'/'+str(uaid)+'.txt'
    with open(str(this_time_txt_save_path), "a") as f:
        str_write = str(start_time)+' question_s3??????'+'???'+str(round_num)+'???'+" ????????????\n"
        f.write(str_write)
    start_record(uaid, 's3', round_num, imi=True)
    return render(request, 'question_s3.html', {'uaid': uaid, 'round_num': round_num})

@login_required
def question_s4_view(request, uaid, round_num):
    command = 'python PlayVideo/playVideoAtWeb.py sub01-1.mp4'
    os.system(command)
    start_record(uaid, 's4', round_num)
    return render(request, 'question_s4.html', {'uaid': uaid, 'round_num': round_num})


@login_required
def self_report_s1_view(request, uaid, round_num):
    start_time = datetime.now()
    this_time_txt_save_path=time_txt_save_path+'/'+str(uaid)+'.txt'
    with open(str(this_time_txt_save_path),"a") as f:
        str_write=str(start_time)+' self_report_s1??????'+'???'+str(round_num)+'???'+" ????????????\n"
        f.write(str_write)
    return render(request, 'self_report_s1.html', {'uaid': uaid, 'round_num': round_num, 'img_name': 'start.jpg'})


@login_required
def self_report_s2_view(request, uaid, round_num):
    start_time = datetime.now()
    this_time_txt_save_path=time_txt_save_path+'/'+str(uaid)+'.txt'
    with open(str(this_time_txt_save_path),"a") as f:
        str_write=str(start_time)+' self_report_s2??????'+'???'+str(round_num)+'???'+" ????????????\n"
        f.write(str_write)
    return render(request, 'self_report_s2.html', {'uaid': uaid, 'round_num': round_num, 'img_name': 'start.jpg'})


@login_required
def self_report_s3_view(request, uaid, round_num):
    start_time = datetime.now()
    this_time_txt_save_path=time_txt_save_path+'/'+str(uaid)+'.txt'
    with open(str(this_time_txt_save_path),"a") as f:
        str_write=str(start_time)+' self_report_s3??????'+'???'+str(round_num)+'???'+" ????????????\n"
        f.write(str_write)
    return render(request, 'self_report_s3.html', {'uaid': uaid, 'round_num': round_num, 'img_name': 'start.jpg'})


@login_required
def self_report_s4_view(request, uaid, round_num):
    start_time = datetime.now()
    this_time_txt_save_path=time_txt_save_path+'/'+str(uaid)+'.txt'
    with open(str(this_time_txt_save_path),"a") as f:
        str_write=str(start_time)+' self_report_s4??????'+'???'+str(round_num)+'???'+" ????????????\n"
        f.write(str_write)
    return render(request, 'self_report_s4.html', {'uaid': uaid, 'round_num': round_num})


@login_required
def system_evaluate_view(request, uaid):
    return render(request, 'system_evaluate.html', {'uaid': uaid})


@login_required
def experiment_evaluate_view(request, uaid):
    return render(request, 'experiment_evaluate.html', {'uaid': uaid})


@login_required
def finish_view(request, uaid):
    start_time = datetime.now()
    this_time_txt_save_path=time_txt_save_path+'/'+str(uaid)+'.txt'
    with open(str(this_time_txt_save_path),"a") as f:
        str_write=str(start_time)+" ????????????\n"
        f.write(str_write)
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
    return JsonResponse({"status": "success", "uaid": user_answer_info.id,"mode":user_answer_info.running_mode})


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
    print("??????????????????")
    start_record()

    return JsonResponse({"status": "success"})


@csrf_exempt
@login_required
def imitation_finish_view(request):
    uaid = request.POST.get('uaid', None)
    round_num = request.POST.get('round_num', None)
    uaid = int(uaid)
    round_num = int(round_num)
    command = 'python PlayVideo/playVideoAtWeb.py s3-'+str(round_num)+'.mp4'
    os.system(command)
    stop_record(uaid=uaid, page_round='s3', round_num=round_num, imi=True)
    print('@627--- imi finish, restart record ')
    start_record(uaid=uaid, page_round='s3', round_num=round_num)
    return JsonResponse({"status": "success"})


@login_required
def task_s1_view(request, uaid):
    start_time = datetime.now()
    this_time_txt_save_path=time_txt_save_path+'/'+str(uaid)+'.txt'
    with open(str(this_time_txt_save_path),"a") as f:
        str_write=str(start_time)+' task_s1??????'+" ????????????\n"
        f.write(str_write)
    return render(request, 'task_s1.html',{'uaid': uaid})


@login_required
def task_s2_view(request, uaid):
    start_time = datetime.now()
    this_time_txt_save_path=time_txt_save_path+'/'+str(uaid)+'.txt'
    with open(str(this_time_txt_save_path),"a") as f:
        str_write=str(start_time)+' task_s2??????'+" ????????????\n"
        f.write(str_write)
    return render(request, 'task_s2.html',{'uaid': uaid})


@login_required
def task_s3_view(request, uaid):
    start_time = datetime.now()
    this_time_txt_save_path=time_txt_save_path+'/'+str(uaid)+'.txt'
    with open(str(this_time_txt_save_path),"a") as f:
        str_write=str(start_time)+' task_s3??????'+" ????????????\n"
        f.write(str_write)
    return render(request, 'task_s3.html',{'uaid': uaid})


@login_required
def task_link_view(request, uaid):
    print("??????1")
    print(uaid)
    print("??????2")
    start_time = datetime.now()
    this_time_txt_save_path=time_txt_save_path+'/'+str(uaid)+'.txt'
    with open(str(this_time_txt_save_path),"a") as f:
        str_write=str(start_time)+' task_link??????'+" ????????????\n"
        f.write(str_write)
    print("??????3")
    return render(request, 'task_link.html',{'uaid': uaid})


@login_required
def imitation_view(request):
    return render(request, 'imitation.html')


@login_required
def score_view(request, uaid):
    real_answer_s1 = ['D', 'A', 'C', 'E', 'F', 'B']
    real_answer_other = ['C', 'E', 'D', 'A', 'B', 'F']
    # A/C 0 angry 1 disgust 2 fear 3 happiness 4 sadness 5 surprise
    # B 0 happiness 1 sadness 2 surprise 3 angry 4 disgust 5 fear
    # needed order [0 happy, 1 sadness, 2 anger, 3 fear, 4 disgust, 5 surprise]
    user_answer_info = UserAnswerInfo.objects.filter(pk=uaid).first()
    running_mode = user_answer_info.running_mode
    mapping_dict = {}
    if running_mode == 'Production':
        mapping_dict = {0: 0, 1: 1, 2: 5, 3: 2, 4: 4, 5: 3}
    else:
        mapping_dict = {0: 2, 1: 4, 2: 3, 3: 0, 4: 1, 5: 5}
    s1_answer = []
    link_answer = []
    s2_answer = []
    s3_answer = []
    s3_detection_imi = [None, None, None, None, None, None]
    s3_detection_video = [None, None, None, None, None, None]
    for i in range(6):
        final_result = FinalResult.objects.filter(
            answer_info=user_answer_info,
            page_round='s1',
            round_num=i+1
        )
        if final_result:
            final_result = final_result.first().question_result
            s1_answer.append(0 if final_result == real_answer_s1[i] else 1)
        else:
            final_result = None
            s1_answer.append(None)
    for i in range(6):
        final_result = FinalResult.objects.filter(
            answer_info=user_answer_info,
            page_round='link',
            round_num=i+1
        )
        if final_result:
            final_result = final_result.first().question_result
            link_answer.append(0 if final_result == real_answer_other[i] else 1)
        else:
            final_result = None
            link_answer.append(None)
    for i in range(6):
        final_result = FinalResult.objects.filter(
            answer_info=user_answer_info,
            page_round='s2',
            round_num=i+1
        )
        if final_result:
            final_result = final_result.first().question_result
            s2_answer.append(0 if final_result == real_answer_other[i] else 1)
        else:
            final_result = None
            s2_answer.append(None)
    for i in range(6):
        final_result = FinalResult.objects.filter(
            answer_info=user_answer_info,
            page_round='s3',
            round_num=i+1
        )
        if final_result:
            final_result = final_result.first()
            final_question_result = final_result.question_result
            s3_answer.append(0 if final_question_result == real_answer_other[i] else 1)
            s3_detection_imi[mapping_dict[i]] = [
                    final_result.happiness_prob_imi,
                    final_result.sadness_prob_imi,
                    final_result.anger_prob_imi,
                    final_result.fear_prob_imi,
                    final_result.disgust_prob_imi,
                    final_result.surprise_prob_imi
                ]
            s3_detection_video[mapping_dict[i]] = [
                    final_result.happiness_prob,
                    final_result.sadness_prob,
                    final_result.anger_prob,
                    final_result.fear_prob,
                    final_result.disgust_prob,
                    final_result.surprise_prob
                ]
        else:
            final_result = None
            s3_answer.append(None)
    print(s1_answer, link_answer, s2_answer, s3_answer, s3_detection_imi, s3_detection_video)
    print(s3_detection_imi)
    #????????????
    cog_empathy=[]
    emo_empathy=[]
    average_E=[]
    for i in range(6):
        s1_answer[i]=s1_answer[i] if s1_answer[i]!=None else 1
        link_answer[i]=link_answer[i] if link_answer[i]!=None else 1
        s2_answer[i]=s2_answer[i] if s2_answer[i]!=None else 1
        s3_answer[i]=s3_answer[i] if s3_answer[i]!=None else 1
        cog_empathy.append(exp(-1*pi/2*pow(0.15*s1_answer[i]+0.20*link_answer[i]+0.30*s2_answer[i]+0.35*s3_answer[i],2)))
    print(cog_empathy)
    for i in range(6):
        E_all=0
        s3_detection_imi[i][i]= s3_detection_imi[i][i] if s3_detection_imi[i][i] !=None else 1
        for j in range(6):
            print(s3_detection_video[i][j])
            s3_detection_video[i][j]=s3_detection_video[i][j] if s3_detection_video[i][j] !=None else 0
            print(s3_detection_video[i][j])
            E_all+=s3_detection_video[i][j]
        average_E.append(E_all/6)
        emo_empathy.append((s3_detection_video[i][i]-average_E[i])/s3_detection_imi[i][i])
    return render(request, 'score.html', {
        'cognitive_score': ','.join(map(str, cog_empathy)),
        'emotion_score': ','.join(map(str, emo_empathy))
    })


@login_required
def eq_evaluate_view(request, uaid):
    return render(request, 'eq_evaluate.html', {'uaid': uaid})
