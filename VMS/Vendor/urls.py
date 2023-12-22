from django.urls import path
from django.http import HttpResponse
from .views import (
    VendorListApiView,
    VendorDetailApiView,
    VendorMetricApiView,
    HistoricalPerformanceApiView
)

def hello_world(request):
    return HttpResponse("Hello World!")


urlpatterns = [
    path("",hello_world,name="Hello World"),
    path("api/vendors",VendorListApiView.as_view()),
    path("api/vendors/<int:vendor_id>",VendorDetailApiView.as_view()),
    path("api/vendors/<int:vendor_id>/performance",VendorMetricApiView.as_view()),
    path("api/vendors/historical",HistoricalPerformanceApiView.as_view())
]
