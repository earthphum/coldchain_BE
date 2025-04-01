from django.db import models
class RiderHistoryData(models.Model):
    rider_name = models.CharField(max_length=100, unique=True)  # ชื่อไรเดอร์ (ต้องไม่ซ้ำกัน)
    total_distance = models.FloatField(default=0.0)  # ระยะทางที่เคยวิ่งทั้งหมด (เมตร)

    def __str__(self):
        return f"{self.rider_name} - {self.total_distance} meters"