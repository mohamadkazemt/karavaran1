from django.db import models
from django_jalali.db import models as jmodels
from datetime import datetime
from django.conf import settings


class FailureReason(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Operator(models.Model):
    GROUP_CHOICES = [
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
    ]

    personnel_code = models.CharField("کد پرسنلی", max_length=10, unique=True)
    first_name = models.CharField("نام", max_length=30)
    last_name = models.CharField("نام خانوادگی", max_length=30)
    group = models.CharField("گروه", max_length=1, choices=GROUP_CHOICES)
    phone_number = models.CharField("شماره تماس", max_length=15, blank=True, null=True)
    position = models.CharField("سمت", max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "اپراتور"
        verbose_name_plural = "اپراتورها"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.personnel_code})"

class DumpTruck(models.Model):
    code = models.CharField("کد دستگاه", max_length=10, unique=True)
    model = models.CharField("مدل", max_length=30)
    is_active = models.BooleanField("فعال", default=True)
    type = models.CharField("نوع دستگاه", max_length=20, choices=[
        ('shovel', 'شاول'),
        ('dump_truck', 'دامپتراک'),
        ('excavator', 'بیل مکانیکی'),
        ('drilling_machine', 'دستگاه حفاری'),
    ])

    class Meta:
        verbose_name = "دامپ تراک"
        verbose_name_plural = "دامپ تراک‌ها"

    def __str__(self):
        return self.code


class Downtime(models.Model):
    operator = models.ForeignKey(Operator, verbose_name="اپراتور", on_delete=models.CASCADE)
    dump_truck = models.ForeignKey(DumpTruck, verbose_name="دامپ تراک", on_delete=models.CASCADE)
    start_date = jmodels.jDateField("تاریخ شروع")
    start_time = models.TimeField("زمان شروع")
    end_date = jmodels.jDateField("تاریخ پایان")
    end_time = models.TimeField("زمان پایان")
    reason = models.ForeignKey(FailureReason, verbose_name="علت خرابی", on_delete=models.CASCADE)
    description = models.TextField("توضیحات", blank=True, null=True)
    is_active = models.BooleanField("فعال", default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="ثبت کننده", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "خرابی"
        verbose_name_plural = "خرابی‌ها"

    def __str__(self):
        return f"خرابی برای {self.dump_truck.code} توسط {self.operator.personnel_code}"

    def calculate_duration(self):
        start_datetime = datetime.combine(self.start_date.togregorian(), self.start_time)
        end_datetime = datetime.combine(self.end_date.togregorian(), self.end_time)
        duration = end_datetime - start_datetime
        return duration
