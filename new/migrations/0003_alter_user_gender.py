# Generated by Django 5.1.1 on 2024-09-10 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new', '0002_user_choices_user_gender_alter_hobby_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='NULL', max_length=10),
        ),
    ]
