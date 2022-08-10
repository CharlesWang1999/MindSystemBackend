from django.urls import path
from ARPictureBook.views import (
    start_page_view,
    second_page_view,
    third_page_view,
    get_query_result_view,
)

urlpatterns = [
    path('start/', start_page_view),
    path('second/', second_page_view),
    path('third/', third_page_view),
    path('get_query_result/', get_query_result_view),
]
