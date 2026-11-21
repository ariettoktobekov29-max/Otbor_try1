from .models import Category, Task , Tag 
from rest_framework.serializers import (
    BaseSerializer,
    Serializer,
    ModelSerializer,
    HyperlinkedModelSerializer,
    ListSerializer,
)
from rest_framework import serializers



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class TaskListSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для списка задач."""

    category_name = serializers.CharField(
        source="category.name", read_only=True, allow_null=True
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "is_completed",
            "created_at",
            "category",
            "category_name",
        ]
        read_only_fields = ["id", "created_at"]


class TaskDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор с полными данными Category и Tag."""

    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    # Поля для записи (POST / PUT / PATCH) по первичным ключам (ID)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
        allow_null=True,
        required=False,
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        source="tags",
        many=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "is_completed",
            "created_at",
            "category",
            "category_id",
            "tags",
            "tag_ids",
        ]
        read_only_fields = ["id", "created_at"]