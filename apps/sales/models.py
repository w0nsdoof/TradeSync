from django.db import models
from django.conf import settings

from apps.products.models import Product


class SalesOrder(models.Model):
    PENDING = "pending"
    APPROVED = "approved"
    COMPLETED = "completed"
    
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (COMPLETED, "Completed"),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sales_orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sales_orders")
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sales Order {self.id} - {self.customer}"

class Invoice(models.Model):
    sales_order = models.OneToOneField(SalesOrder, on_delete=models.CASCADE, related_name="invoice")
    invoice_date = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to="invoices/", blank=True, null=True)

    def __str__(self):
        return f"Invoice for {self.sales_order.id}"
