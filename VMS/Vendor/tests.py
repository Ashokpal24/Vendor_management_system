from urllib import response
from rest_framework.test import APIClient,APITestCase
from rest_framework import status
from .models import VendorProfile
from .serializer import VendorDetailedSerializer


class VendorTestCase(APITestCase):
    def setUp(self):
        self.client=APIClient()
        self.vendor=VendorProfile.objects.create(
            name="AMD",
            address="Santa Clara, 2485 Augustine Dr, United States",
            contact_details= "877-284-1566",
            vendor_code="XYZ"
        )
        self.url="/api/vendors"
        self.data={
            "name":"Intel",
            "address":"Santa Clara, 2200 Mission College Blvd, United States",
            "contact_details":"800-440-2319",
        }

    def test_add_vendor(self):
        response=self.client.post(self.url,self.data)
        # print(VendorProfile.objects.all())
        self.assertEqual(VendorProfile.objects.count(),2)
        self.assertEqual(VendorProfile.objects.get(id=2).name,"Intel")
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_empty_name_request(self):
        err_data=self.data
        err_data["name"]=""
        response=self.client.post(self.url,err_data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_empty_address_request(self):
        err_data=self.data
        err_data["address"]=""
        response=self.client.post(self.url,err_data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_update_vendor(self):
        new_url=self.url+"/1"
        new_data={
            "name":"AMD new",
        }
        response=self.client.put(new_url,new_data)
        self.assertEqual(VendorProfile.objects.count(),1)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(VendorProfile.objects.get(id=1).name,"AMD new")

    def test_update_invalid_vendor(self):
        new_url=self.url+"/2"
        new_data={
            "name":"AMD new",
        }
        response=self.client.put(new_url,new_data)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        self.assertEqual(VendorProfile.objects.get(id=1).name,"AMD")

    def test_delete_vendor(self):
        new_url=self.url+"/1"
        response=self.client.delete(new_url)
        self.assertEqual(VendorProfile.objects.count(),0)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_delete_invalid_vendor(self):
        new_url=self.url+"/2"
        response=self.client.delete(new_url)
        self.assertEqual(VendorProfile.objects.count(),1)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

        
        






