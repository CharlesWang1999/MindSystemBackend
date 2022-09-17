from django.db import models
from django.contrib.auth.models import User

import json

# Create your models here.


class UserAnswerInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_id = models.IntegerField()
    page_order = models.CharField(max_length=200)
    running_mode = models.CharField(max_length=50)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def set_page_order(self, x):
        self.page_order = json.dumps(x)

    def get_page_order(self):
        return json.loads(self.page_order)


class AnswerResult(models.Model):
    answer_info = models.ForeignKey(UserAnswerInfo, on_delete=models.CASCADE)
    page_name = models.CharField(max_length=255)
    question_num = models.IntegerField()
    question_result = models.BooleanField(null=True, blank=True)
    micro_expression_detection_result = models.CharField(max_length=255, null=True, blank=True)
    action_detection_result = models.CharField(max_length=255, null=True, blank=True)
