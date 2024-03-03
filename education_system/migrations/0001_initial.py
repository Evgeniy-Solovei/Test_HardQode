# Generated by Django 4.2 on 2024-03-01 23:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название продукта')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена продукта')),
                ('start_datetime', models.DateTimeField(verbose_name='Дата и время старта продукта')),
                ('min_student', models.PositiveIntegerField(default=1, verbose_name='Минимальное количество студентов')),
                ('max_student', models.PositiveIntegerField(default=20, verbose_name='Максимальное количество студентов')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_products', to=settings.AUTH_USER_MODEL, verbose_name='Автор продукта')),
                ('student', models.ManyToManyField(blank=True, related_name='student_products', to=settings.AUTH_USER_MODEL, verbose_name='Студент/ы продукта')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название урока')),
                ('video_link', models.URLField(verbose_name='Видео урока')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lesson', to='education_system.product', verbose_name='Урок продукта')),
            ],
            options={
                'verbose_name': 'Урок',
                'verbose_name_plural': 'Уроки',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название группы')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='education_system.product', verbose_name='Группы продукта')),
                ('student', models.ManyToManyField(related_name='student_groups', to=settings.AUTH_USER_MODEL, verbose_name='Студент/ы группы')),
            ],
            options={
                'verbose_name': 'Группа',
                'verbose_name_plural': 'Группы',
                'ordering': ['name'],
            },
        ),
    ]
