from django.urls import path
from django.http import HttpResponse
from .views import (
    PurchaseOrderListApiView
)

urlpatterns = [
    path("api/purchase_orders",PurchaseOrderListApiView.as_view()),
]
