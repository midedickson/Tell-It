# Generated by Django 3.0 on 2020-04-11 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200411_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='static/blog/default.png', null=True, upload_to='users/'),
        ),
    ]