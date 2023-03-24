# Generated by Django 3.2.2 on 2021-05-14 00:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0010_auto_20210514_0505'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Signup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='profile_photo/')),
                ('phone', models.IntegerField()),
                ('mobile', models.IntegerField()),
                ('age', models.PositiveIntegerField()),
                ('address', models.TextField()),
                ('booked_mechanic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_content', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]