from django.contrib import admin
from ARPictureBook.models import (
    StartPageResult,
    SecondPageResult,
    ThirdPageResult,
    MicroExpressionDetectionResult,
    ActionDetectionResult
)
# Register your models here.

admin.site.register(StartPageResult)
admin.site.register(SecondPageResult)
admin.site.register(ThirdPageResult)
admin.site.register(MicroExpressionDetectionResult)
admin.site.register(ActionDetectionResult)
