from django.db import models
from django.utils import timezone
from Vendor.models import VendorProfile

class PurchaseOrder(models.Model):
    po_number=models.CharField(max_length=255,blank=False)
    vendor=models.ForeignKey(to=VendorProfile,on_delete=models.CASCADE)
    order_date=models.DateTimeField(default=timezone.now)
    delivery_date=models.DateTimeField(blank=False)
    items=models.JSONField(default=list)
    quantity=models.IntegerField()
    status=models.CharField(default="pending",max_length=255)
    quality_rating=models.FloatField(default=0.0)
    issue_date=models.DateTimeField(default=timezone.now)
    acknowledgment_date=models.DateTimeField(null=True)
    order_completed=models.DateTimeField(null=True)
    order_cancelled=models.DateTimeField(null=True)

    def __str__(self) -> str:
        items_arr=[]
        for item in self.items:
            items_arr.append(item)
        return "Purchase order: {} | vendor id: {} | Acknowledge date: {} | Issue date {}".format(self.po_number,self.vendor.pk,self.acknowledgment_date,self.issue_date)

        