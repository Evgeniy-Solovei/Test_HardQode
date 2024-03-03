from rest_framework import serializers
from education_system.models import Product, Lesson


class ProductSerializer(serializers.ModelSerializer):
    num_lessons = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'author', 'start_datetime', 'min_student', 'max_student', 'student',
                  'num_lessons')


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = 'id', 'name', 'video_link'
