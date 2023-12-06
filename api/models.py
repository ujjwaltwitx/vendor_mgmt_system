import datetime
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from pytz import timezone

# Create your models here.

class VendorModel(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField(max_length=1000)
    address = models.TextField(max_length=1000)
    vendor_id = models.CharField(max_length=255, primary_key=True)

class PurchaseOrderModel(models.Model):
    status_list = [('pending', 'Pending'),('completed', 'Completed')]

    po_id = models.CharField(max_length=255, primary_key=True)
    vendor = models.ForeignKey(to=VendorModel, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.TextField() #to convert to JSONField
    quantity = models.IntegerField()
    status = models.CharField(max_length=255, choices=status_list)
    quality_rating = models.FloatField()
    issue_date = models.DateTimeField()
    acknowledgement_date = models.DateTimeField()

@receiver(pre_save, sender=PurchaseOrderModel)
def po_status_change(sender, instance, **kwargs):
    print(instance.po_id)
    try:
        orignal_po = PurchaseOrderModel.objects.get(po_id=instance.po_id)
        #create historic_performace_row for the vendor
        if orignal_po.status != 'completed' and instance.status == 'completed':
            on_time_delivery_rate(instance.vendor_id, instance.delivery_date)
            quality_rating_average(vendor_id=instance.vendor_id, rating=3.5)
            fulfillment_rate(vendor_id=instance.vendor_id)
         #to fetch rating form the body of the request
        if orignal_po.acknowledgement_date != instance.acknowledgement_date:
            average_response_time(instance.vendor_id, instance.acknowledgement_date, orignal_po.issue_date)
    except PurchaseOrderModel.DoesNotExist:
        print("eror updating")


class HistoricPerformanceModel(models.Model):
    id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(to=VendorModel, on_delete=models.CASCADE)
    date = models.DateTimeField()
    total_deliveries = models.IntegerField(default=0)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.IntegerField(default=0)
    fulfillment_rate = models.FloatField(default=0)


def on_time_delivery_rate(vendor_id, deliveryDate):
    tz = timezone('UTC')
    vendor = HistoricPerformanceModel.objects.get(vendor_id = vendor_id)
    on_time_count = vendor.on_time_delivery_rate
    total_deliveries = vendor.total_deliveries
    if datetime.datetime.now(tz=tz) < deliveryDate : 
        updated_count = (on_time_count*total_deliveries + 1)/(total_deliveries + 1)
        updated_count = float("{:.2f}".format(updated_count))
        vendor.on_time_delivery_rate = updated_count
    vendor.total_deliveries = total_deliveries + 1
    vendor.save()

def quality_rating_average(vendor_id, rating):
    try:
        vendor = HistoricPerformanceModel.objects.get(vendor_id = vendor_id)
        total_deliveries = vendor.total_deliveries
        average_rating = vendor.quality_rating_avg
        new_average = (average_rating * total_deliveries + rating)/(total_deliveries + 1)
        vendor.quality_rating_avg = new_average
        vendor.save();
    except HistoricPerformanceModel.DoesNotExist:
        print("Vendor has not")

def average_response_time(vendor_id, ack_date : datetime, issue_date : datetime):
    try:
        vendor = HistoricPerformanceModel.objects.get(vendor_id = vendor_id)
        total_deliveries = vendor.total_deliveries
        old_total_resp_time = vendor.average_response_time * total_deliveries
        diff = ((ack_date - issue_date).total_seconds())/60
        new_avg_time = (old_total_resp_time + diff)/(total_deliveries + 1)
        vendor.average_response_time = new_avg_time
        vendor.save()
    except HistoricPerformanceModel.DoesNotExist:
        print("Vendor doesn't exists")

def fulfillment_rate(vendor_id):
    total_vendor_po = PurchaseOrderModel.objects.filter(vendor_id = vendor_id).count()
    total_completed_po = PurchaseOrderModel.objects.filter(vendor_id = vendor_id, status="completed").count() + 1
    vendor = HistoricPerformanceModel.objects.get(vendor_id = vendor_id)
    f_rate = float("{:.2f}".format(total_completed_po/total_vendor_po))
    vendor.fulfillment_rate = f_rate
    vendor.save()

        




