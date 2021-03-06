# Generated by Django 3.2.7 on 2021-09-19 08:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20210905_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='from_cid',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='to_cid',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
    ]
