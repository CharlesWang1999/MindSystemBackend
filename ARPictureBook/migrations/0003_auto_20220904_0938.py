# Generated by Django 2.2.27 on 2022-09-04 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ARPictureBook', '0002_actiondetectionresult_microexpressiondetectionresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startpageresult',
            name='second_result',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='startpageresult',
            name='third_result',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]