from django.shortcuts import render
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
from pytz import timezone

from .models import VendorModel, PurchaseOrderModel, HistoricPerformanceModel
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricPerformanceSerializer

#API's for vendor profile management


class VendorView(APIView):
    def get(self, request, vendor_id=None):
        if vendor_id is None:
            return self.get_all_vendors()
        return self.get_vendor_by_id(vendor_id);
    
    def get_all_vendors(self):
        queryset = VendorModel.objects.all()
        serializer = VendorSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_vendor_by_id(self, vendor_id):
        try:
            vendor = VendorModel.objects.get(vendor_id = vendor_id)
            serializer = VendorSerializer(vendor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except VendorModel.DoesNotExist:
            return Response("Vendor Not Found", status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            vendor_instance = serializer.save()
            historic_performance_model = HistoricPerformanceModel.objects.create(vendor=vendor_instance)
            historic_performance_model.save()
            return Response("Object Saved", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, vendor_id):
        try:
            VendorModel.objects.get(vendor_id = vendor_id).delete()
            return Response("Object Deleted", status=status.HTTP_200_OK)
        except VendorModel.DoesNotExist:
            return Response("Vendor Not found", status=status.HTTP_404_NOT_FOUND)

    
    def put(self, request, vendor_id):
        try:
            object = VendorModel.objects.get(vendor_id=vendor_id)
            serializer = VendorSerializer(object, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("Object Updated", status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except VendorModel.DoesNotExist:
            return Response("Vendor does not exist", status=status.HTTP_404_NOT_FOUND)
            
        
class PurchaseOrderView(APIView):
    def get_all_po(self):
        queryset = PurchaseOrderModel.objects.all()
        serializer = PurchaseOrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_po_by_id(self, po_id):
        try:
            object = PurchaseOrderModel.objects.get(po_id = po_id)
            serializer = PurchaseOrderSerializer(object)
            return Response(serializer.data)
        except PurchaseOrderModel.DoesNotExist:
            return Response("Purchase Order not found", status=status.HTTP_204_NO_CONTENT)
        
    def get(self, request, po_id=None):
        if po_id is None:
            return self.get_all_po()
        return self.get_po_by_id(po_id)

    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Object created", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, po_id):
        object = PurchaseOrderModel.objects.get(po_id = po_id)
        serializer = PurchaseOrderSerializer(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Object updated", status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, po_id):
        try:
            PurchaseOrderModel.objects.get(po_id = po_id).delete()
            return Response("Purcahse Order deleted")
        except PurchaseOrderModel.DoesNotExist:
            return Response("Purchase Order not found", status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_performance(request, vendor_id):
    performace = HistoricPerformanceModel.objects.get(vendor_id=vendor_id)
    serializer = HistoricPerformanceSerializer(performace)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_ack(request, po_id):
    tz = timezone("UTC")
    try:
        po = PurchaseOrderModel.objects.get(po_id = po_id)
        po.acknowledgement_date = datetime.now(tz=tz);
        po.save()
        return Response("Acknowledgement updated successfully")
    except PurchaseOrderModel.DoesNotExist:
        return Response("Purchase Order Not found", status=status.HTTP_400_BAD_REQUEST)
