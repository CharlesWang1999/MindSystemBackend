# Generated by Django 2.2.27 on 2022-09-16 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ARPictureBook', '0003_auto_20220904_0938'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_name', models.CharField(max_length=255)),
                ('question_num', models.IntegerField()),
                ('question_result', models.BooleanField()),
                ('micro_expression_detection_result', models.CharField(max_length=255)),
                ('action_detection_result', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswerInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_id', models.IntegerField()),
                ('page_order', models.CharField(max_length=200)),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='microexpressiondetectionresult',
            name='start_page_result',
        ),
        migrations.RemoveField(
            model_name='secondpageresult',
            name='start_page_result',
        ),
        migrations.RemoveField(
            model_name='thirdpageresult',
            name='start_page_result',
        ),
        migrations.DeleteModel(
            name='ActionDetectionResult',
        ),
        migrations.DeleteModel(
            name='MicroExpressionDetectionResult',
        ),
        migrations.DeleteModel(
            name='SecondPageResult',
        ),
        migrations.DeleteModel(
            name='StartPageResult',
        ),
        migrations.DeleteModel(
            name='ThirdPageResult',
        ),
        migrations.AddField(
            model_name='answerresult',
            name='answer_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ARPictureBook.UserAnswerInfo'),
        ),
    ]