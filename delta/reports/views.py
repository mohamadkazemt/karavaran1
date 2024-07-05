from django.shortcuts import render
from django.db.models import Sum, F
from dumptrucks.models import Downtime
import json

def top_dump_truck_downtimes(request):
    data = Downtime.objects.values('dump_truck__code').annotate(total_downtime=Sum(F('end_time') - F('start_time'))).order_by('-total_downtime')[:10]
    labels = json.dumps([item['dump_truck__code'] for item in data])
    values = json.dumps([item['total_downtime'].total_seconds() / 3600 for item in data])
    return render(request, 'reports/top_dump_truck_downtimes.html', {'labels': labels, 'values': values})

def top_operator_downtimes(request):
    data = Downtime.objects.values('operator__first_name', 'operator__last_name').annotate(total_downtime=Sum(F('end_time') - F('start_time'))).order_by('-total_downtime')[:10]
    labels = json.dumps([f"{item['operator__first_name']} {item['operator__last_name']}" for item in data])
    values = json.dumps([item['total_downtime'].total_seconds() / 3600 for item in data])
    return render(request, 'reports/top_operator_downtimes.html', {'labels': labels, 'values': values})

def top_failure_reasons(request):
    data = Downtime.objects.values('reason__name').annotate(total_downtime=Sum(F('end_time') - F('start_time'))).order_by('-total_downtime')[:10]
    labels = json.dumps([item['reason__name'] for item in data])
    values = json.dumps([item['total_downtime'].total_seconds() / 3600 for item in data])
    return render(request, 'reports/top_failure_reasons.html', {'labels': labels, 'values': values})
