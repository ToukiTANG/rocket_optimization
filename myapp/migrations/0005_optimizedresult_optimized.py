# Generated by Django 4.1.3 on 2022-11-18 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0004_remove_optimizedstate_d_phi1_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="optimizedresult",
            name="optimized",
            field=models.BooleanField(default=False, verbose_name="是否是优化结果"),
        ),
    ]