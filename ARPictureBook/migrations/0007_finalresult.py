# Generated by Django 2.2.27 on 2022-10-02 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ARPictureBook', '0006_auto_20220917_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinalResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_round', models.CharField(max_length=255)),
                ('round_num', models.IntegerField()),
                ('question_result', models.CharField(blank=True, max_length=255, null=True)),
                ('self_report_result', models.CharField(blank=True, max_length=255, null=True)),
                ('micro_expression_detection_result', models.CharField(blank=True, max_length=255, null=True)),
                ('answer_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ARPictureBook.UserAnswerInfo')),
            ],
        ),
    ]