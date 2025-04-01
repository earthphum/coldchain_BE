from django.db import models

class RoutePlanCache(models.Model):
    delivery_date = models.DateField()
    rider_names_hash = models.CharField(max_length=256)  # เก็บค่า hash ที่สร้างจาก delivery_date, rider_names และ orders
    result_json = models.JSONField()  # เก็บผลลัพธ์การคำนวณในรูปแบบ JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.delivery_date} - {self.rider_names_hash}"
