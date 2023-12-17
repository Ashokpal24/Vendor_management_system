from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PurchaseOrder
from .serializer import PurchaseListSerializer,PurchaseDetailedSerializer
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import datetime

class PurchaseOrderListApiView(APIView):
    def get(self,request,*args, **kwargs):
        po_list=PurchaseOrder.objects.all()
        if po_list:
            serializer=PurchaseListSerializer(po_list,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(
            "[GET] No Purchase order found",
            status=status.HTTP_204_NO_CONTENT
        )

    def post(self,request,*args, **kwargs):
        new_items=request.data.get("items")
        new_quality_rating=request.data.get("quality_rating")
        temp_dt=request.data.get("delivery_date")
        new_delivery_date=datetime.strptime(temp_dt,"%d-%m-%Y %H:%M")
        new_delivery_date=timezone.make_aware(new_delivery_date, timezone.get_current_timezone())
        data={
            "po_number":get_random_string(length=3),
            "vendor":request.data.get("vendor"),
            "delivery_date":new_delivery_date,
            "items":"" if len(new_items)==0 else new_items,
            "quantity":len(new_items),
            "quality_rating": 0.0 if not new_quality_rating else new_quality_rating
        }
        serializer=PurchaseDetailedSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    