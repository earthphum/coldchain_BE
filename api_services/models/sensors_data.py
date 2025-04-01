from django.db import models
from datetime import datetime 
from django.utils.timezone import localtime, now

class SensorData(models.Model):
    sensor_type = models.CharField(max_length=50)  # ประเภทเซ็นเซอร์
    temperature = models.FloatField(null=True, blank=True)  # อุณหภูมิ
    humidity = models.FloatField(null=True, blank=True)  # ความชื้น
    latitude = models.FloatField(null=True, blank=True)  # ละติจูด
    longitude = models.FloatField(null=True, blank=True)  # ลองจิจูด
    wake_source = models.CharField(max_length=50, null=True, blank=True)  # แหล่งที่มาของ wake-up
    box_status = models.CharField(max_length=50, null=True, blank=True)  # สถานะของกล่อง
    received_at = models.DateTimeField(default=now)  # เวลาที่รับข้อมูล

    def __str__(self):
        return f"{self.sensor_type} - Temp: {self.temperature}°C, Humidity: {self.humidity}%"