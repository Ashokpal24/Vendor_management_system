from django.contrib import admin
from django.urls import path, include
from Vendor import urls as vendor_urls
from POTracking import urls as PO_urls
from Auth import urls as Auth_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(vendor_urls)),
    path("", include(PO_urls)),
    path("", include(Auth_urls))

]
