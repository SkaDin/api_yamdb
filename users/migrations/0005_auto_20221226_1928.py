# Generated by Django 3.2 on 2022-12-26 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.RemoveConstraint(
            model_name='user',
            name='User with such username and email is already registered',
        ),
    ]