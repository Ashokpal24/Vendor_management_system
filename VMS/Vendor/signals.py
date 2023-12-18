from django.db.models.signals import post_save
from django.dispatch import receiver,Signal
from POTracking.models import PurchaseOrder

ack_signal=Signal()

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

    