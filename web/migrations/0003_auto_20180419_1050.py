# Generated by Django 2.0.1 on 2018-04-19 02:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20180419_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditlog',
            name='content',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='auditlog',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='auditlog',
            name='host_to_remote_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.HostToRemoteUser'),
        ),
        migrations.AddField(
            model_name='auditlog',
            name='login_type',
            field=models.SmallIntegerField(choices=[(0, 'login'), (1, 'cmd'), (2, 'logout')], default=0),
        ),
        migrations.AddField(
            model_name='auditlog',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='堡垒机帐号'),
        ),
    ]