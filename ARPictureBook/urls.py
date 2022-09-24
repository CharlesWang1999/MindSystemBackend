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
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('choose_mode/', choose_mode_view, name='choose_mode'),
    path('question/<int:uaid>/<int:page_index>/', question_page_view),
    path('get_query_result/', get_query_result_view),
    path('get_web_click/', get_web_click_view),
    path('choose_mode_submit/', choose_mode_submit_view),
    # path('PlayVideo_cartoon/', PlayVideo_cartoon_view),
]
