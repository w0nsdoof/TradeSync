from io import BytesIO
import pdfkit

from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.utils import timezone
from django.db import models
from django.conf import settings

from apps.products.models import Product

class SalesOrder(models.Model):
    PENDING = "pending"
    APPROVED = "approved"
    COMPLETED = "completed"
    CANCELED = "canceled"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (COMPLETED, "Completed"),
        (CANCELED, "Canceled"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sales_orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sales_orders")
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == self.COMPLETED and not hasattr(self, "invoice"):
            invoice = Invoice.objects.create(sales_order=self)
            invoice.generate_invoice_pdf()
    
    def __str__(self):
        return f"Sales Order {self.id} - {self.customer}"

class Invoice(models.Model):
    sales_order = models.OneToOneField(SalesOrder, on_delete=models.CASCADE, related_name="invoice")
    invoice_date = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to="invoices/", blank=True, null=True)

    def generate_invoice_pdf(self):
        """Generates a PDF invoice for the sales order."""
        context = {"invoice": self}
        html_content = render_to_string("sales/invoice_template.html", context)  # Renders HTML template
        pdf_file = pdfkit.from_string(html_content, False)  # Generate PDF as bytes

        # Save PDF file
        filename = f"invoice_{self.sales_order.id}.pdf"
        self.pdf_file.save(filename, ContentFile(pdf_file), save=True)

    def __str__(self):
        return f"Invoice for Order {self.sales_order.id}"


class Discount(models.Model):
    code = models.CharField(max_length=50, unique=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Discount percentage (e.g., 10 for 10%)")
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    
    @property
    def is_active(self):
        return self.valid_from <= timezone.now() <= self.valid_to

    def __str__(self):
        return f"{self.code} - {self.percentage}% ({'Active' if self.is_active else 'Expired'})"
