# Generated by Django 3.1.4 on 2020-12-14 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='user_likes',
            field=models.ManyToManyField(related_name='fav_quotes', to='quotes_app.User'),
        ),
    ]