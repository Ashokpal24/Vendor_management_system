from datetime import datetime
from django.utils import timezone
from rest_framework.test import APIClient,APITestCase
from rest_framework import status
from POTracking.serializer import PurchaseDetailedSerializer
from Vendor.models import VendorProfile
from POTracking.models import PurchaseOrder
from POTracking.views import PurchaseOrderUtils
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class MainTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.token = Token.objects.create(user=self.user)

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
                "delivery_date": "19-12-2023 09:30",
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
            delivery_date=PurchaseOrderUtils().convert_to_timezone("24-12-2023 09:30"),
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

    # Auth
        
    # TODO add auth test
    
    # Vendor
    def test_add_vendor(self):

        response=self.client.post(self.vendor_url,self.vendor_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(VendorProfile.objects.count(),2)
        self.assertEqual(VendorProfile.objects.get(id=2).name,"Intel")

    def test_empty_name_request(self):
        err_data=self.vendor_data
        err_data["name"]=""
        response=self.client.post(self.vendor_url,err_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_empty_address_request(self):
        err_data=self.vendor_data
        err_data["address"]=""
        response=self.client.post(self.vendor_url,err_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_update_vendor(self):
        new_url=self.vendor_url+"/1"
        new_data={
            "name":"AMD new",
        }
        response=self.client.put(new_url,new_data,HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.assertEqual(VendorProfile.objects.count(),1)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(VendorProfile.objects.get(id=1).name,"AMD new")

    def test_update_invalid_vendor(self):
        new_url=self.vendor_url+"/2"
        new_data={
            "name":"AMD new",
        }
        response=self.client.put(new_url,new_data,HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        self.assertEqual(VendorProfile.objects.get(id=1).name,"AMD")

    def test_delete_vendor(self):
        new_url=self.vendor_url+"/1"
        response=self.client.delete(new_url,HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(VendorProfile.objects.count(),0)

    def test_delete_invalid_vendor(self):
        new_url=self.vendor_url+"/2"
        response=self.client.delete(new_url,HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        self.assertEqual(VendorProfile.objects.count(),1)

    def test_get_vendor_performance(self):
        new_url=self.vendor_url+"/1/performance"
        response=self.client.get(new_url,HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.assertEqual(response.status_code,status.HTTP_200_OK,)


    # Purchase Order

    def test_add_po(self):
        po_cls_instance=PurchaseOrderUtils()
        response=self.client.post(self.vendor_url,self.vendor_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')

        response=self.client.post(self.po_url,self.po_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(),2)
        self.assertEqual(PurchaseOrder.objects.get(id=2).delivery_date,po_cls_instance.convert_to_timezone(self.po_data["delivery_date"]))


    def test_add_po_to_invalid_vendor(self):
        err_data=self.po_data
        err_data["vendor"]=2 # type: ignore
        response=self.client.post(self.po_url,self.po_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_add_empty_delivery_date(self):
        err_data=self.po_data
        err_data["delivery_date"]=""
        # create vendor
        # response=self.client.post(self.vendor_url,self.vendor_data)
        response=self.client.post(self.po_url,err_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_add_empty_items_data(self):
        response=self.client.post(self.vendor_url,self.vendor_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')
        
        new_data=self.po_data
        new_data["items"]=[]
        # create vendor
        # response=self.client.post(self.vendor_url,self.vendor_data)
        response=self.client.post(self.po_url,new_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(),2)
        self.assertEqual(PurchaseOrder.objects.get(id=2).quantity,0)

    def test_update_items(self):
        response=self.client.post(self.vendor_url,self.vendor_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')
        response=self.client.post(self.po_url,self.po_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')
        
        new_data={
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
                    },
                    {
                    "name": "i3 9th Gen",
                    "Type": "CPU",
                    "Price": "12000"
                    }
                ]
        }

        new_url=self.po_url+"/2"
        response=self.client.put(new_url,new_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(PurchaseOrder.objects.get(id=2).quantity,3)


    def test_delete_po(self):
        new_url=self.po_url+"/1"
        response=self.client.delete(new_url,HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(PurchaseOrder.objects.count(),0)
        
    def test_po_ack(self):
        new_url=self.po_url+"/1/acknowledge"
        
        response=self.client.post(new_url,{},HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertIsNotNone(PurchaseOrder.objects.get(id=1).acknowledgment_date)

    def test_po_status(self):
        response=self.client.post(self.vendor_url,self.vendor_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')
        response=self.client.post(self.po_url,self.po_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')
        
        new_data={"status":"completed"}

        new_url=self.po_url+"/2"
        response=self.client.put(new_url,new_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(PurchaseOrder.objects.get(id=2).status,"completed")

    def test_po_quality_rating_avg(self):
        response=self.client.post(self.vendor_url,self.vendor_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')
        response=self.client.post(self.po_url,self.po_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')
        
        new_data={"quality_rating":80.0,"status":"completed"}

        new_url=self.po_url+"/2"
        response=self.client.put(new_url,new_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        self.assertEqual(PurchaseOrder.objects.get(id=2).quality_rating,80.0)
        self.assertEqual(VendorProfile.objects.get(id=2).name,"Intel")
        self.assertEqual(VendorProfile.objects.get(id=2).quality_rating_avg,80.0)

    def test_po_on_delivery_rate(self):
        response=self.client.post(self.vendor_url,self.vendor_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')
        response=self.client.post(self.po_url,self.po_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')
        
        new_data={"status":"completed"}

        new_url=self.po_url+"/2"
        response=self.client.put(new_url,new_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        target_datetime = datetime.strptime(self.po_data["delivery_date"], "%d-%m-%Y %H:%M")
        if target_datetime>datetime.now():
            self.assertEqual(VendorProfile.objects.get(id=2).on_time_delivery_rate,100)
        else:
            self.assertEqual(VendorProfile.objects.get(id=2).on_time_delivery_rate,0)

    def test_po_fulfilment_rate(self):
        response=self.client.post(self.vendor_url,self.vendor_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')
        response=self.client.post(self.po_url,self.po_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')
        
        new_data={"status":"completed"}

        new_url=self.po_url+"/2"
        response=self.client.put(new_url,new_data,HTTP_AUTHORIZATION=f'Token {self.token.key}',format='json')
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(VendorProfile.objects.get(id=2).fulfillment_rate,100)







