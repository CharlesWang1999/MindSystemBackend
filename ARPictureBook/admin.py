from django.contrib import admin
from ARPictureBook.models import (
    UserAnswerInfo,
    AnswerResult,
    FinalResult
)
# Register your models here.

admin.site.register(UserAnswerInfo)
admin.site.register(AnswerResult)
admin.site.register(FinalResult)
