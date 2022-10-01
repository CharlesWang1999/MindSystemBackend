from django.urls import path
from ARPictureBook.views import (
    login_view,
    logout_view,
    question_page_view,
    get_query_result_view,
    get_web_click_view,
    # PlayVideo_cartoon_view,
    choose_mode_view,
    choose_mode_submit_view,
    question_click_view,
    self_report_click_view,
    self_report_s1_view,
    smooth_music_click_view,
    smooth_music_view,
    question_s1_view,
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
    path('choose_mode_submit/', choose_mode_submit_view),
    path('smooth_music/<int:uaid>/<int:round_num>/<str:page_round>/', smooth_music_view, name='smooth_music'),
    path('question_s1/<int:uaid>/<int:round_num>/', question_s1_view, name='question_s1'),
    path('self_report_s1/<int:uaid>/<int:round_num>/', self_report_s1_view, name='self_report_s1'),
    # path('PlayVideo_cartoon/', PlayVideo_cartoon_view),
]
