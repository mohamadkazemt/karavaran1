from django.contrib import admin
from .models import Operator, DumpTruck, Downtime

admin.site.register(Operator)
admin.site.register(DumpTruck)
admin.site.register(Downtime)
