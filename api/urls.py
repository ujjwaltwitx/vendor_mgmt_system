from django.urls import path
from .views import VendorView, PurchaseOrderView


urlpatterns = [
    path("vendors/", VendorView.as_view(), name="all_vendors"),
    path("vendors/<int:vendor_id>", VendorView.as_view(), name="specific_vendor"),
    path("purchase_orders/", PurchaseOrderView.as_view(), name="purchase_orders"),
    path("purchase_orders/<int:po_id>", PurchaseOrderView.as_view(), name="purchase_orders"),

]