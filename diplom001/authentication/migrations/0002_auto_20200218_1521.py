# Generated by Django 3.0.3 on 2020-02-18 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='total_bonuses',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
