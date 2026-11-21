from django.shortcuts import render

# Create your views here.
from django.db import models


from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from .models import Category, Tag, Task
from .serializer import (
    CategorySerializer,
    TagSerializer,
    TaskDetailSerializer,
    TaskListSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["id", "name"]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["id", "name"]


class TaskViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "description", "category__name", "tags__name"]
    ordering_fields = ["id", "title", "created_at", "is_completed"]

    def get_queryset(self):
        queryset = Task.objects.select_related("category")
        if self.action != "list":
            queryset = queryset.prefetch_related("tags")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return TaskListSerializer
        return TaskDetailSerializer