# Generated by Django 5.0.6 on 2024-08-05 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nettraversal', '0003_alter_netforward_forward_port'),
    ]

    operations = [
        migrations.AddField(
            model_name='netforward',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='是否启用该转发'),
        ),
    ]
