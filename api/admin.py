from django.contrib import admin
from .models import VendorModel, PurchaseOrderModel, HistoricPerformanceModel

# Register your models here.
admin.site.register([VendorModel, PurchaseOrderModel, HistoricPerformanceModel])






