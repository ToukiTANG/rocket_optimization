# Generated by Django 4.1.3 on 2022-11-21 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0005_optimizedresult_optimized"),
    ]

    operations = [
        migrations.AddField(
            model_name="optimizedresult",
            name="record_arr",
            field=models.CharField(default="", max_length=255, verbose_name="迭代过程数组"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="optimizedresult",
            name="t_arr",
            field=models.CharField(default="", max_length=255, verbose_name="时间数组"),
            preserve_default=False,
        ),
    ]