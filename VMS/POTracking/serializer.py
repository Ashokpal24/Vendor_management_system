from rest_framework import serializers
from .models import PurchaseOrder


class PurchaseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ["id",
                  "po_number",
                  "vendor",
                  "order_date",
                  "items",
                  "status"]


class PurchaseDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"
