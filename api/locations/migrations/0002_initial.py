# Generated by Django 4.1 on 2022-08-16 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('travels', '0001_initial'),
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='travel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='travels.travel'),
        ),
        migrations.AddField(
            model_name='location',
            name='traveler',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.traveler'),
        ),
    ]
