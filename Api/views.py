from rest_framework import generics
from .models import Vendor,PurchaseOrder
from .serializers import (
    VendorSerializer,
    PurchaseOrderSerializer,
    VendorPerformanceSerializer,
    UserSerializer,
    AcknowledgePurchaseOrderSerializer
)
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User



# user registration
class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer




class VendorListCreateView(generics.ListCreateAPIView):
    queryset=Vendor.objects.all()
    serializer_class=VendorSerializer
    permission_classes=[IsAuthenticated]


class VendorListUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Vendor.objects.all()
    serializer_class=VendorSerializer
    permission_classes=[IsAuthenticated]



# PurchaseOrder
class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset=PurchaseOrder.objects.all()
    serializer_class=PurchaseOrderSerializer
    permission_classes=[IsAuthenticated]


class PurchaseOrderListUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset=PurchaseOrder.objects.all()
    serializer_class=PurchaseOrderSerializer
    permission_classes=[IsAuthenticated]



class VendorPerformanceView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer
    lookup_field = 'id'
    permission_classes=[IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    


class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = AcknowledgePurchaseOrderSerializer
    lookup_field = 'id'  # Assuming 'id' is the primary key field in your PurchaseOrder model
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Trigger the recalculation of average_response_time (replace this with your actual logic)
        instance.calculate_average_response_time()
        
        return Response({"detail": "Purchase Order acknowledged successfully."})