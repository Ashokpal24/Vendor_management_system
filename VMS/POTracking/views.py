from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PurchaseOrder
from .serializer import PurchaseListSerializer,PurchaseDetailedSerializer
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import datetime
from Vendor.signals import ack_signal

class PurchaseOrderUtils():
    def get_object(self,vendor_id):
        try:
            return PurchaseOrder.objects.get(id=vendor_id)
        except PurchaseOrder.DoesNotExist:
            return None
        
    def convert_to_timezone(self,temp_dt):
        if temp_dt:
            try:
                new_dt=datetime.strptime(temp_dt,"%d-%m-%Y %H:%M")
                new_dt=timezone.make_aware(new_dt, timezone.get_current_timezone())
                return new_dt
            except:
                return None
        return None
        

class PurchaseOrderListApiView(APIView,PurchaseOrderUtils):
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
        new_delivery_date=self.convert_to_timezone(request.data.get("delivery_date"))
        
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
    
class PurchaseOrderDetailApiView(APIView,PurchaseOrderUtils):
    def get(self,request,po_id,*args, **kwargs):
        po_instance=self.get_object(po_id)
        if not po_instance:
            return Response(
                "[GET] No Purchase order found with id {}".format(po_id),
                status=status.HTTP_404_NOT_FOUND
            )
        serializer=PurchaseDetailedSerializer(po_instance)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,po_id,*args, **kwargs):
        po_instance=self.get_object(po_id)
        if not po_instance:
            return Response(
                "[GET] No Purchase order found with id {}".format(po_id),
                status=status.HTTP_404_NOT_FOUND
            )
        
        new_items=request.data.get("items")
        new_quality_rating=request.data.get("quality_rating")
        new_delivery_date=self.convert_to_timezone(request.data.get("delivery_date"))
        
        data={
            # "po_number":po_instance.po_number,
            # "vendor":po_instance.vendor.pk,
            "delivery_date":po_instance.delivery_date if not new_delivery_date else new_delivery_date,
            "items":po_instance.items if not new_items else new_items,
            "quantity":po_instance.quantity if not new_items else len(new_items),
            "quality_rating": po_instance.quality_rating if not new_quality_rating else new_quality_rating
        }

        serializer=PurchaseDetailedSerializer(instance=po_instance,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,po_id,*args, **kwargs):
        po_instance=self.get_object(po_id)
        if not po_instance:
            return Response(
                "[DEL] No Purchase order found with id {}".format(po_id),
                status=status.HTTP_404_NOT_FOUND
            )
        po_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
    
class PurchaseOrderAckApiView(APIView,PurchaseOrderUtils):
    def get(self,request, po_id,*args, **kwargs):
        po_instance=self.get_object(po_id)
        if not po_instance:
            return Response(
                "[GET] No Purchase order found with id {}".format(po_id),
                status=status.HTTP_404_NOT_FOUND
            )
        serializer=PurchaseDetailedSerializer(po_instance)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request, po_id,*args, **kwargs):
        po_instance=self.get_object(po_id)
        if not po_instance:
            return Response(
                "[POST] No Purchase order found with id {}".format(po_id),
                status=status.HTTP_404_NOT_FOUND
            )
        data={
            "acknowledgment_date":timezone.make_aware(datetime.now(),timezone.get_current_timezone())
        }
        serializer=PurchaseDetailedSerializer(instance=po_instance,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            ack_signal.send(sender=self,request=request,instance=po_instance)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
