import math
from django.db.models import Count
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.generics import ListAPIView
from education_system.models import Product, Group, Lesson
from education_system.serializers import ProductSerializer, LessonSerializer


class ProductGroup(View):
    def __init__(self, product_id):
        super().__init__()
        self.product = get_object_or_404(Product, pk=product_id)

    def distribute_students(self):
        # Получаем всех пользователей, которых нужно распределить по группам
        student_in_product = self.product.student.all()
        num_students = student_in_product.count()

        # Получаем максимальное количество участников в группе
        max_students = self.product.max_student

        # Вычисляем количество групп (округляем вверх, до ближайшего целого числа)
        num_groups = math.ceil(num_students / max_students)

        # Вычисляем, сколько участников должно быть в каждой группе (целое значение)
        students_per_group = num_students // num_groups

        # Вычисляем количество групп, в которых нужно будет добавить дополнительного участника
        groups_with_extra_student = num_students % num_groups

        # Переменная для хранения текущего индекса пользователя
        user_index = 0

        # Создаем или обновляем группы
        for i in range(num_groups):
            # Создаем новую группу или выбираем существующую
            if i < self.product.groups.count():
                group = self.product.groups.all()[i]
                group.student.clear()  # Очищаем студентов в группе перед добавлением новых
            else:
                group = Group.objects.create(product=self.product, name=f"Группа {i + 1}")

            # Вычисляем количество студентов для текущей группы
            students_count = students_per_group

            # Если это группа, в которой нужно добавить дополнительного участника, увеличиваем количество студентов
            if i < groups_with_extra_student:
                students_count += 1

            # Добавляем студентов в группу
            for j in range(students_count):
                group.student.add(student_in_product[user_index])
                user_index += 1

    def access_product(self, request):
        # Проверяем, начался ли продукт
        if self.product.start_datetime <= timezone.now():
            # Получаем группу для этого продукта, если она существует
            group = self.product.groups.order_by('-id').first()

            if group and group.student.count() < self.product.max_student:
                # Если группа существует и не заполнена, добавляем пользователя в нее
                group.student.add(request.user)
            else:
                # Если нет доступной группы, создаем новую и добавляем пользователя в нее
                group = Group.objects.create(product=self.product, name=f"Группа {self.product.groups.count() + 1}")
                group.student.add(request.user)
        else:
            # Если продукт еще не начался, выполним перераспределение пользователей по группам
            self.distribute_students()

        return JsonResponse({'message': 'Доступ к продукту разрешен.'})


class ProductListView(ListAPIView):
    queryset = Product.objects.all().annotate(num_lessons=Count('lesson'))
    serializer_class = ProductSerializer


class LessonListView(ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Lesson.objects.filter(product__student=user)
        return queryset
