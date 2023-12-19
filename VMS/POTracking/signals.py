from django.dispatch import receiver,Signal
from .models import PurchaseOrder
from Vendor.models import VendorProfile
from django.utils import timezone
from django.db.models import F

ack_signal=Signal()
status_signal=Signal()

@receiver(ack_signal)
def cal_average_response_time(sender,**kwargs):
    print("Signal received from PO!!")
    print(sender)
    instance=kwargs['instance']
    time_differences = []
    for po in PurchaseOrder.objects.filter(vendor=instance.vendor.pk):
        if po.acknowledgment_date and po.issue_date:
            time_diff=(po.acknowledgment_date-po.issue_date).total_seconds()/3600
            time_differences.append(time_diff)
    avg_response_time=sum(time_differences)/len(time_differences) if time_differences else 0
    print(avg_response_time)
    hours, minutes = divmod(avg_response_time * 60, 60)
    print(hours,minutes)
    formatted_time = "{:02.0f}:{:02.0f}".format(hours, minutes)
    print(formatted_time)

@receiver(status_signal)
def status_completed(sender,**kwargs):
    instance=kwargs['instance']

    po_count=PurchaseOrder.objects.filter(vendor=instance.vendor.pk).count()
    
    #quality rating
    quality_rate_arr=[]
    for po in PurchaseOrder.objects.filter(vendor=instance.vendor.pk):
        quality_rate_arr.append(po.quality_rating)

    print("Quality rating: "+str(sum(quality_rate_arr)/len(quality_rate_arr)))

    # on_time_delivery_rate
    completed_po=PurchaseOrder.objects.filter(
        vendor=instance.vendor.pk,
        status="completed",
        order_completed__lt=F('delivery_date')
    ).count()
    print("Time delivery rate: "+str(completed_po*100/po_count))

    # fulfilment_rate
    completed_po=PurchaseOrder.objects.filter(
        vendor=instance.vendor.pk,
        status="completed"
    ).count()
    print("Fulfilment Rate: "+str(completed_po*100/po_count))


