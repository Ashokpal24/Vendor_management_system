from django.db import models

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
        return "vendor: {} | code: {} ".format(self.name,self.vendor_code)

