# Generated by Django 5.1.1 on 2024-09-10 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new', '0005_hobby_remove_user_choices_user_choices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hobby',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
