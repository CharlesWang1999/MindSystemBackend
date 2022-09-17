from django.contrib import admin
from ARPictureBook.models import (
    UserAnswerInfo,
    AnswerResult
)
# Register your models here.

admin.site.register(UserAnswerInfo)
admin.site.register(AnswerResult)
