from audioop import avg
from django.dispatch import receiver,Signal
from .models import PurchaseOrder
from Vendor.serializer import VendorMetricSerializer
from Vendor.models import VendorProfile
from django.db.models import F
from rest_framework.response import Response
from rest_framework import status

ack_signal=Signal()
status_signal=Signal()

#TODO start with unit test
#TODO documentation on 21st

@receiver(ack_signal)
def cal_average_response_time(sender,**kwargs):
    print("Signal received from PO!!")
    instance=kwargs['instance']
    vendor_instance=VendorProfile.objects.get(id=instance.vendor.pk)

    time_differences = []
    data={}

    for po in PurchaseOrder.objects.filter(vendor=instance.vendor.pk):
        if po.acknowledgment_date and po.issue_date:
            time_diff=(po.acknowledgment_date-po.issue_date).total_seconds()
            time_differences.append(time_diff)

    avg_response_time=sum(time_differences)/len(time_differences) #avg in secs
    # print(avg_response_time)

    # extra formatting if required
    avg_response_time_hrs=(sum(time_differences)/3600)/len(time_differences) if time_differences else 0 # avg in hrs
    hours, minutes = divmod(avg_response_time_hrs * 60, 60)
    # print(hours,minutes)
    formatted_time = "{:02.0f}:{:02.0f}".format(hours, minutes)
    # print(formatted_time)


    data["average_response_time"]=avg_response_time
    serializer=VendorMetricSerializer(instance=vendor_instance,data=data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

@receiver(status_signal)
def status_completed(sender,**kwargs):
    instance=kwargs['instance']

    vendor_instance=VendorProfile.objects.get(id=instance.vendor.pk)

    po_count=PurchaseOrder.objects.filter(vendor=instance.vendor.pk).count()
    data={}
    
    #quality rating
    quality_rate_arr=[]
    for po in PurchaseOrder.objects.filter(vendor=instance.vendor.pk):
        quality_rate_arr.append(po.quality_rating)

    new_quality_rating_avg=sum(quality_rate_arr)/len(quality_rate_arr)
    # print("Quality rating: "+str(new_quality_rating_avg))
    data['quality_rating_avg']=new_quality_rating_avg

    # on_time_delivery_rate
    completed_po=PurchaseOrder.objects.filter(
        vendor=instance.vendor.pk,
        status="completed",
        order_completed__lt=F('delivery_date')
    ).count()
    new_on_time_delivery_rate=completed_po*100/po_count
    # print("Time delivery rate: "+str(new_on_time_delivery_rate))
    data['on_time_delivery_rate']=new_on_time_delivery_rate


    # fulfilment_rate
    completed_po=PurchaseOrder.objects.filter(
        vendor=instance.vendor.pk,
        status="completed"
    ).count()
    new_fulfillment_rate=completed_po*100/po_count
    # print("Fulfilment Rate: "+str(new_fulfillment_rate))
    data['fulfillment_rate']=new_fulfillment_rate

    serializer=VendorMetricSerializer(instance=vendor_instance,data=data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


