from django.urls import path
from ARPictureBook.views import (
    startPageView,
    secondPageView,
    thirdPageView,
)

urlpatterns = [
    path('start/', startPageView),
    path('second/', secondPageView),
    path('third/', thirdPageView),
]
