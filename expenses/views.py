from django.shortcuts import render
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin)
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ExpensesSerializers
from .models import Expense
from .permissions import IsOwner


class ExpensesList(ListCreateAPIView):
    serializer_class = ExpensesSerializers
    queryset = Expense.objects.all()
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        """
        Вызывается при создании объекта модели через API
        Сохраняет объект модели с указанными данными,
        в качестве владельца используем текущего пользователя
        """
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class ExpenseDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpensesSerializers
    queryset = Expense.objects.all()
    permission_classes = (IsOwner, IsAuthenticated)
    lookup_field = 'id'
    # Поле модели, которое следует использовать для
    # поиска объектов отдельных экземпляров модели. По умолчанию 'pk'

    def perform_create(self, serializer):
        """
        Вызывается при создании объекта модели через API
        Сохраняет объект модели с указанными данными,
        в качестве владельца используем текущего пользователя
        """
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

