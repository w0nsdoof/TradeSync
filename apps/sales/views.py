from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django.db import transaction
from django.http import FileResponse

from .models import SalesOrder, Invoice, Discount
from .serializers import SalesOrderSerializer, InvoiceSerializer, DiscountSerializer
from apps.users.permissions import IsOwner, IsAdmin

class SalesOrderViewSet(viewsets.ModelViewSet):
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if IsAdmin().has_permission(self.request, self):
            return SalesOrder.objects.all() 
        return SalesOrder.objects.filter(user=self.request.user)  

    def perform_create(self, serializer):
        with transaction.atomic():
            sales_order = serializer.save(user=self.request.user)
            Invoice.objects.create(sales_order=sales_order)  # Auto-create invoice

class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if IsAdmin().has_permission(self.request, self):
            return Invoice.objects.all()  
        return Invoice.objects.filter(sales_order__customer=self.request.user)
    
    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        """API endpoint to download the PDF invoice"""
        invoice = self.get_object()
        return FileResponse(invoice.pdf_file.open(), as_attachment=True, filename=f"invoice_{invoice.sales_order.id}.pdf")

class DiscountViewSet(viewsets.ModelViewSet):
    serializer_class = DiscountSerializer
    permission_classes = [IsAdmin]  

    def get_queryset(self):
        return Discount.objects.filter(is_active=True)  
