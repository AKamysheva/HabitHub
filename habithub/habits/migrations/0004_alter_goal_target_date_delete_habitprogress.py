# Generated by Django 5.1.2 on 2024-12-03 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0003_alter_goal_status_alter_habit_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='target_date',
            field=models.DateField(verbose_name='Дата достижения цели'),
        ),
        migrations.DeleteModel(
            name='HabitProgress',
        ),
    ]
