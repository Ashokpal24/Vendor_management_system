from django.db import models
from django.utils import timezone

class VendorProfile(models.Model):
    name=models.CharField(max_length=255,blank=False)
    contact_details=models.TextField(blank=False)
    address=models.TextField(blank=False)
    vendor_code=models.CharField(max_length=255,unique=True,blank=False,)
    on_time_delivery_rate=models.FloatField(default=0.0)
    quality_rating_avg=models.FloatField(default=0.0)
    average_response_time=models.FloatField(default=0.0)
    fulfillment_rate=models.FloatField(default=0.0)

    def __str__(self) -> str:
        return "vendor: {} | code: {} | vendor_id: {} ".format(self.name,self.vendor_code,self.pk)

class HistoricalPerformance(models.Model):
    vendor=models.ForeignKey(to=VendorProfile,on_delete=models.CASCADE)
    date=models.DateTimeField(default=timezone.now)
    on_time_delivery_rate=models.FloatField(default=0.0)
    quality_rating_avg=models.FloatField(default=0.0)
    average_response_time=models.FloatField(default=0.0)
    fulfillment_rate=models.FloatField(default=0.0)

    def __str__(self) -> str:
        return "vendor: {} | date: {} ".format(self.vendor,self.date)