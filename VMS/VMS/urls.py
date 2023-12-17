from django.contrib import admin
from django.urls import path,include
from Vendor import urls as vendor_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",include(vendor_urls))
]
