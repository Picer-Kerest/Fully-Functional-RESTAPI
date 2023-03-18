from rest_framework.serializers import ModelSerializer
from .models import Income


class IncomesSerializers(ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'date', 'description', 'amount', 'source']
