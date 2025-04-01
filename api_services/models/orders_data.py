from django.db import models
from datetime import datetime
from django.utils.timezone import localtime, now
class OrdersData(models.Model):
    order_number = models.CharField(max_length=20,unique=True,blank=True)
    customer_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    product = models.CharField(max_length=255)
    delivery_date = models.DateField(null=True,blank=True)
    def save(self, *args, **kwargs):
        if not self.order_number :
            today = localtime(now()).strftime('%Y%m%d')
            last_order = OrdersData.objects.filter(order_number__startswith=f"ORD{today}").order_by('id').last()
            if last_order:
                last_number = int(last_order.order_number.split("-")[-1])
                self.order_number = f'ORD{today}-{last_number + 1:04d}'
            else:
                self.order_number =f'ORD{today}-0001'
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Order for {self.customer_name} , {self.product}"