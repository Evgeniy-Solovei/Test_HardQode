from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    """Модель Product представляет информацию о продукте."""

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name', ]

    name = models.CharField(max_length=255, verbose_name='Название продукта')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена продукта')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_products',
                               verbose_name='Автор продукта')
    start_datetime = models.DateTimeField(verbose_name='Дата и время старта продукта')
    min_student = models.PositiveIntegerField(default=1, verbose_name='Минимальное количество студентов')
    max_student = models.PositiveIntegerField(default=20, verbose_name='Максимальное количество студентов')
    student = models.ManyToManyField(User, blank=True, related_name='student_products',
                                     verbose_name='Студент/ы продукта')

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Модель Lesson представляет информацию об уроке."""

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['name', ]

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='lesson',
                                   verbose_name='Урок продукта')
    name = models.CharField(max_length=255, verbose_name='Название урока')
    video_link = models.URLField(verbose_name='Видео урока')

    def __str__(self):
        return self.name


class Group(models.Model):
    """Модель Group представляет информацию о группе."""

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['name', ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='groups',
                                verbose_name='Группы продукта')
    name = models.CharField(max_length=255, verbose_name='Название группы')
    student = models.ManyToManyField(User, related_name='student_groups', verbose_name='Студент/ы группы')

    def __str__(self):
        return self.name
