from django.db import models

# Create your models here.


class StartPageResult(models.Model):
    first_result = models.BooleanField()
    second_result = models.BooleanField(null=True, blank=True)
    third_result = models.BooleanField(null=True, blank=True)


class SecondPageResult(models.Model):
    start_page_result = models.ForeignKey(StartPageResult, on_delete=models.CASCADE)
    first_result = models.BooleanField()
    second_result = models.BooleanField()
    third_result = models.BooleanField()


class ThirdPageResult(models.Model):
    start_page_result = models.ForeignKey(StartPageResult, on_delete=models.CASCADE)
    first_result = models.BooleanField()
    second_result = models.BooleanField()
    third_result = models.BooleanField()


class MicroExpressionDetectionResult(models.Model):
    start_page_result = models.ForeignKey(StartPageResult, on_delete=models.CASCADE)
    page_name = models.CharField(max_length=255)
    question_num = models.IntegerField()
    detection_result = models.CharField(max_length=255)


class ActionDetectionResult(models.Model):
    start_page_result = models.ForeignKey(StartPageResult, on_delete=models.CASCADE)
    page_name = models.CharField(max_length=255)
    question_num = models.IntegerField()
    detection_result = models.CharField(max_length=255)
