from urllib import response
from django.utils import timezone
from rest_framework.test import APIClient,APITestCase
from rest_framework import status
from Vendor.models import VendorProfile
from POTracking.models import PurchaseOrder
from POTracking.views import PurchaseOrderUtils






class MainTestCase(APITestCase):
    def setUp(self):
        self.client=APIClient()
        
        self.vendor_url="/api/vendors"

        self.po_url="/api/purchase_orders"
        
        self.vendor_data={
            "name":"Intel",
            "address":"Santa Clara, 2200 Mission College Blvd, United States",
            "contact_details":"800-440-2319",
        }

        self.po_data={
                "vendor": 2,
                "delivery_date": "21-12-2023 09:30",
                "items": [
                    {
                    "name": "i9 9th Gen",
                    "Type": "CPU",
                    "Price": "37000"
                    },
                    {
                    "name": "i5 9th Gen",
                    "Type": "CPU",
                    "Price": "27000"
                    }
                ],
                "quality_rating":0.0
        }

        self.vendor=VendorProfile.objects.create(
            name="AMD",
            address="Santa Clara, 2485 Augustine Dr, United States",
            contact_details= "877-284-1566",
            vendor_code="XYZ"
        )

        self.po=PurchaseOrder.objects.create(
            po_number="ABC",
            vendor=self.vendor,
            delivery_date=PurchaseOrderUtils().convert_to_timezone("20-12-2023 09:30"),
            items=[
                {
                    "name": "Ryzen 5900",
                    "Type": "CPU",
                    "Price": "37000"
                },
                {
                    "name": "Ryzen 5200x",
                    "Type": "CPU",
                    "Price": "27000"
                }
            ],
            quantity=2,
            quality_rating=0.0
        )
    
    def test_add_vendor(self):
        response=self.client.post(self.vendor_url,self.vendor_data)
        # print(VendorProfile.objects.all())
        self.assertEqual(VendorProfile.objects.count(),2)
        self.assertEqual(VendorProfile.objects.get(id=2).name,"Intel")
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_empty_name_request(self):
        err_data=self.vendor_data
        err_data["name"]=""
        response=self.client.post(self.vendor_url,err_data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_empty_address_request(self):
        err_data=self.vendor_data
        err_data["address"]=""
        response=self.client.post(self.vendor_url,err_data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_update_vendor(self):
        new_url=self.vendor_url+"/1"
        new_data={
            "name":"AMD new",
        }
        response=self.client.put(new_url,new_data)
        self.assertEqual(VendorProfile.objects.count(),1)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(VendorProfile.objects.get(id=1).name,"AMD new")

    def test_update_invalid_vendor(self):
        new_url=self.vendor_url+"/2"
        new_data={
            "name":"AMD new",
        }
        response=self.client.put(new_url,new_data)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        self.assertEqual(VendorProfile.objects.get(id=1).name,"AMD")

    def test_delete_vendor(self):
        new_url=self.vendor_url+"/1"
        response=self.client.delete(new_url)
        self.assertEqual(VendorProfile.objects.count(),0)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_delete_invalid_vendor(self):
        new_url=self.vendor_url+"/2"
        response=self.client.delete(new_url)
        self.assertEqual(VendorProfile.objects.count(),1)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)


    def test_add_po(self):
        po_cls_instance=PurchaseOrderUtils()
        response=self.client.post(self.vendor_url,self.vendor_data)
        self.assertEqual(VendorProfile.objects.count(),2)
        self.assertEqual(VendorProfile.objects.get(id=2).name,"Intel")
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        response=self.client.post(self.po_url,self.po_data)
        self.assertEqual(PurchaseOrder.objects.count(),2)
        self.assertEqual(PurchaseOrder.objects.get(id=2).delivery_date,po_cls_instance.convert_to_timezone("21-12-2023 09:30"))
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)


        
        






