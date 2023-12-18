from django.urls import path
from django.http import HttpResponse
from .views import (
    PurchaseOrderListApiView,
    PurchaseOrderDetailApiView,
    PurchaseOrderAckApiView
)

urlpatterns = [
    path("api/purchase_orders",PurchaseOrderListApiView.as_view()),
    path("api/purchase_orders/<int:po_id>",PurchaseOrderDetailApiView.as_view()),
    path("api/purchase_orders/<int:po_id>/acknowledge",PurchaseOrderAckApiView.as_view()),

]
