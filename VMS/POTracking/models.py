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

    def __str__(self) -> str:
        return "Purchase order: {} | vendor id: {} ".format(self.po_number,self.vendor)

        