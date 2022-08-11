from tkinter import CASCADE
from django.db import models

# Create your models here.


class StartPageResult(models.Model):
    first_result = models.BooleanField()
    second_result = models.BooleanField()
    third_result = models.BooleanField()


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
