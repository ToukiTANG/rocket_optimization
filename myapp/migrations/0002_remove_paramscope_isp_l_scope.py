# Generated by Django 4.1.3 on 2022-11-17 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="paramscope", name="isp_l_scope",),
    ]
