from django.db import models

# Create your models here.

class VendorModel(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField(max_length=1000)
    address = models.TextField(max_length=1000)
    vendor_code = models.CharField(max_length=255, primary_key=True)

class PurchaseOrderModel(models.Model):
    po_number = models.CharField(max_length=255, primary_key=True)
    vendor = models.ForeignKey(to=VendorModel, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=255)
    quality_rating = models.FloatField()
    issue_date = models.DateTimeField()
    acknowledgement_date = models.DateTimeField()

class HistoricPerformanceModel(models.Model):
    vendor = models.ForeignKey(to=VendorModel, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()