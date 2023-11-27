from django.db import models
from django.utils import timezone

class Vendor(models.Model):
    name = models.CharField(max_length=50)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=20, unique=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()


    def calculate_on_time_delivery_rate(self):
        completed_orders = self.purchaseorder_set.filter(status='completed')
        on_time_delivered = completed_orders.filter(delivery_date__lte=models.F('acknowledgment_date'))
        on_time_delivery_rate = (on_time_delivered.count() / completed_orders.count()) * 100 if completed_orders.count() > 0 else 0
        self.on_time_delivery_rate = on_time_delivery_rate
        self.save()

    def calculate_quality_rating_avg(self):
        completed_orders = self.purchaseorder_set.filter(status='completed', quality_rating__isnull=False)
        quality_ratings = completed_orders.values_list('quality_rating', flat=True)
        quality_rating_avg = sum(quality_ratings) / len(quality_ratings) if len(quality_ratings) > 0 else 0
        self.quality_rating_avg = quality_rating_avg
        self.save()

    def calculate_average_response_time(self):
        completed_orders = self.purchaseorder_set.filter(status='completed', acknowledgment_date__isnull=False)
        response_times = completed_orders.annotate(
            response_time=models.F('acknowledgment_date') - models.F('issue_date')
        ).values_list('response_time', flat=True)
        average_response_time = sum(response_times, timezone.timedelta()) / len(response_times) if len(response_times) > 0 else 0
        self.average_response_time = average_response_time.total_seconds() / 60  # convert to minutes
        self.save()

    def calculate_fulfillment_rate(self):
        total_orders = self.purchaseorder_set.count()
        fulfilled_orders = self.purchaseorder_set.filter(status='completed', quality_rating__isnull=True).count()
        fulfillment_rate = (fulfilled_orders / total_orders) * 100 if total_orders > 0 else 0
        self.fulfillment_rate = fulfillment_rate
        self.save()

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=20, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 'completed':
            self.vendor.calculate_on_time_delivery_rate()
            self.vendor.calculate_quality_rating_avg()

        if self.acknowledgment_date:
            self.vendor.calculate_average_response_time()

        self.vendor.calculate_fulfillment_rate()

    def __str__(self):
        return self.po_number

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
