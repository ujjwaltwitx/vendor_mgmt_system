from .models import VendorModel, PurchaseOrderModel, HistoricPerformanceModel

from rest_framework import serializers

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorModel
        fields = ['name', 'contact_details', 'address', 'vendor_id']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderModel
        # fields = ['po_id', 'order_date', 'quantity', 'items', 'status', 'quality_rating', 'issue_date', 'acknowledgement_date']
        fields = '__all__'


class HistoricPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricPerformanceModel
        fields = ['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
