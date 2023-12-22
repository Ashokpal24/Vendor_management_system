from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import HistoricalPerformance, VendorProfile
from .serializer import (
    HistoricalPerformanceSerializer,
    VendorListSerializer,
    VendorDetailedSerializer,
    VendorMetricSerializer
    )
from django.utils .crypto import get_random_string
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



class VendorUtils():
    def get_object(self,vendor_id):
        try:
            return VendorProfile.objects.get(id=vendor_id)
        except VendorProfile.DoesNotExist:
            return None


class VendorListApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,*args, **kwargs):
        vendor_list=VendorProfile.objects.all()
        if vendor_list:
            serializer=VendorListSerializer(vendor_list,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(
            "[GET] No vendor data found",
            status=status.HTTP_204_NO_CONTENT
        )
    
    def post(self,request,*args, **kwargs):
        data={
            "name":request.data.get("name"),
            "contact_details":request.data.get("contact_details"),
            "address":request.data.get("address"),
            "vendor_code":get_random_string(length=3),
        }
        serializer=VendorDetailedSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VendorDetailApiView(APIView,VendorUtils):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,vendor_id,*args, **kwargs):
        vendor_instance=self.get_object(vendor_id)
        if not vendor_instance:
            return Response(
                "[GET] No vendor data found with id {}".format(vendor_id),
                status=status.HTTP_404_NOT_FOUND
            )
        serializer=VendorDetailedSerializer(vendor_instance)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,vendor_id,*args, **kwargs):
        vendor_instance=self.get_object(vendor_id)
        if not vendor_instance:
            return Response(
                "[PUT] No vendor data found with id {}".format(vendor_id),
                status=status.HTTP_404_NOT_FOUND
            )
        
        new_name=request.data.get("name")
        new_contact_details=request.data.get("contact_details")
        new_address=request.data.get("address")

        data={
            "name":vendor_instance.name if not new_name else new_name,
            "contact_details":vendor_instance.contact_details if not new_contact_details else new_contact_details,
            "address":vendor_instance.address if not new_address else new_address,
            "vendor_code":vendor_instance.vendor_code,
        }
        serializer=VendorDetailedSerializer(instance=vendor_instance,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,vendor_id,*args, **kwargs):
        vendor_instance=self.get_object(vendor_id)
        if not vendor_instance:
            return Response(
                "[DEL] No vendor data found with id {}".format(vendor_id),
                status=status.HTTP_404_NOT_FOUND
            )
        vendor_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
    
class VendorMetricApiView(APIView,VendorUtils):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,vendor_id,*args, **kwargs):
        vendor_instance=self.get_object(vendor_id)
        if not vendor_instance:
            return Response(
                "[GET] No vendor data found with id {}".format(vendor_id),
                status=status.HTTP_404_NOT_FOUND
            )
        serializer=VendorMetricSerializer(vendor_instance)
        return Response(serializer.data,status=status.HTTP_200_OK)

class HistoricalPerformanceApiView(APIView,VendorUtils):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,*args, **kwargs):
        hist_list=HistoricalPerformance.objects.all()
        if hist_list:
            serializer=HistoricalPerformanceSerializer(hist_list,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(
            "[GET] No vendor data found",
            status=status.HTTP_204_NO_CONTENT
        )