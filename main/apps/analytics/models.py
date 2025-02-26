from django.db import models

class Report(models.Model):
    TRADING = 'trading'
    REVENUE = 'revenue'
    PROFIT_LOSS = 'profit_loss'
    
    REPORT_TYPES = [
        (TRADING, "Trading Volume"),
        (REVENUE, "Revenue Tracking"),
        (PROFIT_LOSS, "Profit/Loss"),
    ]

    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    generated_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()  # Storing insights as JSON data
    csv_file = models.FileField(upload_to="analytics_reports/", blank=True, null=True)

    def __str__(self):
        return f"{self.report_type} Report - {self.generated_at}"
