# Generated by Django 3.2.2 on 2021-05-14 00:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_user_signup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_signup',
            name='booked_mechanic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.bookmechanic'),
        ),
    ]
