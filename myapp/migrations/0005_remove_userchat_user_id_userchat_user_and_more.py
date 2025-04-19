# Generated by Django 4.2.20 on 2025-04-19 10:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_userchat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userchat',
            name='user_id',
        ),
        migrations.AddField(
            model_name='userchat',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='sent_chats', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userchat',
            name='sent_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_chats', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userchat',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
