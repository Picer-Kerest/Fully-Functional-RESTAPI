from rest_framework.serializers import ModelSerializer
from .models import Expense


class ExpensesSerializers(ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'date', 'description', 'amount', 'category']
