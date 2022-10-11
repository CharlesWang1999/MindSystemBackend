from django.urls import path
from ARPictureBook.views import (
    experiment_evaluate_click_view,
    experiment_evaluate_view,
    finish_view,
    login_view,
    logout_view,
    question_link_view,
    question_page_view,
    get_query_result_view,
    get_web_click_view,
    # PlayVideo_cartoon_view,
    choose_mode_view,
    choose_mode_submit_view,
    question_click_view,
    self_report_click_view,
    self_report_s1_view,
    self_report_s2_view,
    self_report_s3_view,
    self_report_s4_view,
    smooth_music_click_view,
    smooth_music_view,
    question_s1_view,
    question_s2_view,
    question_s3_view,
    question_s4_view,
    system_evaluate_click_view,
    system_evaluate_view,
    imitation_finish_view,
    imitation_view,
    score_view,
    task_click_view,
    task_s1_view,
    task_link_view,
    task_s2_view,
    task_s3_view,
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('choose_mode/', choose_mode_view, name='choose_mode'),
    path('question/<int:uaid>/<int:page_index>/', question_page_view),
    path('get_query_result/', get_query_result_view),
    path('get_web_click/', get_web_click_view),
    path('question_click/', question_click_view),
    path('self_report_click/', self_report_click_view),
    path('smooth_music_click/', smooth_music_click_view),
    path('system_evaluate_click/', system_evaluate_click_view),
    path('experiment_evaluate_click/', experiment_evaluate_click_view),
    path('choose_mode_submit/', choose_mode_submit_view),
    path('smooth_music/<int:uaid>/<int:round_num>/<str:page_round>/', smooth_music_view, name='smooth_music'),
    path('question_s1/<int:uaid>/<int:round_num>/<str:running_mode>/', question_s1_view, name='question_s1'),
    path('question_s2/<int:uaid>/<int:round_num>/<str:running_mode>/', question_s2_view, name='question_s2'),
    path('question_s3/<int:uaid>/<int:round_num>/<str:running_mode>/', question_s3_view, name='question_s3'),
    path('question_s4/<int:uaid>/<int:round_num>/', question_s4_view, name='question_s4'),
    path('question_link/<int:uaid>/<int:round_num>/<str:running_mode>/', question_link_view, name='question_link'),
    path('self_report_s1/<int:uaid>/<int:round_num>/', self_report_s1_view, name='self_report_s1'),
    path('self_report_s2/<int:uaid>/<int:round_num>/', self_report_s2_view, name='self_report_s2'),
    path('self_report_s3/<int:uaid>/<int:round_num>/', self_report_s3_view, name='self_report_s3'),
    path('self_report_s4/<int:uaid>/<int:round_num>/', self_report_s4_view, name='self_report_s4'),
    path('system_evaluate/<int:uaid>/', system_evaluate_view, name='system_evaluate'),
    path('experiment_evaluate/<int:uaid>/', experiment_evaluate_view, name='experiment_evaluate'),
    path('finish/<int:uaid>/', finish_view, name='finish'),
    path('imitation_finish/', imitation_finish_view),
    # path('task1/', task1_view, name='task1'),
    path('imitation/', imitation_view, name='imitation'),
    path('score/', score_view, name='score'),
    path('task_click/', task_click_view),
    path('task_s1/<int:uaid>/', task_s1_view, name='task_s1'),
    path('task_s2/<int:uaid>/', task_s2_view, name='task_s2'),
    path('task_s3/<int:uaid>/', task_s3_view, name='task_s3'),
    path('task_link/<int:uaid>/', task_link_view, name='task_link'),
    
]
