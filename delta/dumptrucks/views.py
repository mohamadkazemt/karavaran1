from django.shortcuts import render, get_object_or_404, redirect
from .models import Downtime, Operator, DumpTruck, FailureReason
from .forms import DowntimeForm, OperatorForm, OperatorImportForm, DumpTruckForm, DumpTruckImportForm, FailureReasonForm, FailureReasonImportForm
from django.http import HttpResponse
import pandas as pd
import jdatetime
import django_jalali.db.models as jmodels
import datetime as dt
from django.contrib import messages
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@login_required
def downtime_list(request):
    downtimes = Downtime.objects.all()
    operators = Operator.objects.all()
    dump_trucks = DumpTruck.objects.all()
    reasons = FailureReason.objects.all()
    form = DowntimeForm()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search_query = request.GET.get('q')

    if start_date and end_date:
        try:
            start_date_gregorian = jdatetime.datetime.strptime(start_date, '%Y-%m-%d').togregorian()
            end_date_gregorian = jdatetime.datetime.strptime(end_date, '%Y-%m-%d').togregorian()
            downtimes = downtimes.filter(
                start_date__gte=start_date_gregorian, 
                end_date__lte=end_date_gregorian
            )
        except ValueError:
            pass

    if search_query:
        downtimes = downtimes.filter(
            Q(operator__first_name__icontains=search_query) |
            Q(operator__last_name__icontains=search_query) |
            Q(dump_truck__code__icontains=search_query) |
            Q(reason__name__icontains=search_query)
        )

    for downtime in downtimes:
        start_datetime = dt.datetime.combine(downtime.start_date.togregorian(), downtime.start_time)
        end_datetime = dt.datetime.combine(downtime.end_date.togregorian(), downtime.end_time)
        
        downtime.start_time_jalali = jdatetime.datetime.fromgregorian(datetime=start_datetime).strftime('%Y-%m-%d %H:%M:%S')
        downtime.end_time_jalali = jdatetime.datetime.fromgregorian(datetime=end_datetime).strftime('%Y-%m-%d %H:%M:%S')
        downtime.duration = downtime.calculate_duration()

    return render(request, 'dumptrucks/downtime_list.html', {
        'downtimes': downtimes,
        'operators': operators,
        'dump_trucks': dump_trucks,
        'reasons': reasons,
        'form': form,
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date,
    })

@login_required
def downtime_create(request):
    if request.method == 'POST':
        form = DowntimeForm(request.POST)
        if form.is_valid():
            downtime = form.save(commit=False)
            downtime.created_by = request.user
            downtime.save()
            return redirect('downtime_list')
    return redirect('downtime_list')

@login_required
def downtime_edit(request, id):
    downtime = get_object_or_404(Downtime, id=id)
    if request.method == 'POST':
        form = DowntimeForm(request.POST, instance=downtime)
        if form.is_valid():
            form.save()
            return redirect('downtime_list')
    else:
        form = DowntimeForm(instance=downtime)
    return render(request, 'dumptrucks/downtime_form.html', {'form': form})

@login_required
def export_downtimes_to_excel(request):
    downtimes = Downtime.objects.all()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search_query = request.GET.get('q')

    if start_date and end_date:
        try:
            start_date_gregorian = jdatetime.datetime.strptime(start_date, '%Y-%m-%d').togregorian()
            end_date_gregorian = jdatetime.datetime.strptime(end_date, '%Y-%m-%d').togregorian()
            downtimes = downtimes.filter(
                start_date__gte=start_date_gregorian, 
                end_date__lte=end_date_gregorian
            )
        except ValueError:
            pass

    if search_query:
        downtimes = downtimes.filter(
            Q(operator__first_name__icontains=search_query) |
            Q(operator__last_name__icontains=search_query) |
            Q(dump_truck__code__icontains=search_query) |
            Q(reason__name__icontains=search_query)
        )

    data = []
    total_duration = dt.timedelta()

    for downtime in downtimes:
        start_datetime = dt.datetime.combine(downtime.start_date.togregorian(), downtime.start_time)
        end_datetime = dt.datetime.combine(downtime.end_date.togregorian(), downtime.end_time)
        duration = end_datetime - start_datetime
        total_duration += duration

        data.append({
            'کد پرسنلی': downtime.operator.personnel_code,
            'نام اپراتور': f"{downtime.operator.first_name} {downtime.operator.last_name}",
            'دامپ تراک': downtime.dump_truck.code,
            'علت خرابی': downtime.reason.name,
            'زمان شروع': jdatetime.datetime.fromgregorian(datetime=start_datetime).strftime('%Y-%m-%d %H:%M:%S'),
            'زمان پایان': jdatetime.datetime.fromgregorian(datetime=end_datetime).strftime('%Y-%m-%d %H:%M:%S'),
            'مدت زمان خرابی': str(duration)
        })

    df = pd.DataFrame(data)
    df.loc[len(df)] = {
        'کد پرسنلی': 'مجموع',
        'نام اپراتور': '',
        'دامپ تراک': '',
        'علت خرابی': '',
        'زمان شروع': '',
        'زمان پایان': '',
        'مدت زمان خرابی': str(total_duration)
    }

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Downtimes.xlsx'
    df.to_excel(response, index=False)

    return response



@login_required
def operator_list(request):
    operators = Operator.objects.all().order_by('group')
    form = OperatorForm()
    import_form = OperatorImportForm()

    if request.method == 'POST':
        if 'add_operator' in request.POST:
            form = OperatorForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'اپراتور با موفقیت اضافه شد.')
                return redirect('operator_list')
            else:
                messages.error(request, 'خطا در افزودن اپراتور. لطفاً فرم را بررسی کنید.')
                print(form.errors)
        elif 'import_operators' in request.POST:
            import_form = OperatorImportForm(request.POST, request.FILES)
            if import_form.is_valid():
                file = request.FILES['file']
                df = pd.read_excel(file)
                for index, row in df.iterrows():
                    Operator.objects.create(
                        personnel_code=row['کد پرسنلی'],
                        first_name=row['نام'],
                        last_name=row['نام خانوادگی'],
                        group=row['گروه'],
                        phone_number=row['شماره تماس'],
                        position=row['سمت']
                    )
                messages.success(request, 'اپراتورها با موفقیت ایمپورت شدند.')
                return redirect('operator_list')
            else:
                messages.error(request, 'خطا در ایمپورت اپراتورها. لطفاً فایل اکسل را بررسی کنید.')

    return render(request, 'dumptrucks/operator_list.html', {
        'operators': operators,
        'form': form,
        'import_form': import_form
    })

@login_required
def edit_operator(request, id):
    operator = get_object_or_404(Operator, id=id)
    if request.method == 'POST':
        form = OperatorForm(request.POST, instance=operator)
        if form.is_valid():
            form.save()
            messages.success(request, 'اپراتور با موفقیت ویرایش شد.')
            return redirect('operator_list')
    else:
        form = OperatorForm(instance=operator)
    return render(request, 'dumptrucks/operator_edit.html', {'form': form, 'operator': operator})

@login_required
def delete_operator(request, id):
    operator = get_object_or_404(Operator, id=id)
    operator.delete()
    messages.success(request, 'اپراتور با موفقیت حذف شد.')
    return redirect('operator_list')

@login_required
def download_excel_template(request):
    data = {
        'کد پرسنلی': ['12345', '67890'],
        'نام': ['علی', 'حسین'],
        'نام خانوادگی': ['رضایی', 'احمدی'],
        'گروه': ['a', 'b'],
        'شماره تماس': ['09121234567', '09351234567'],
        'سمت': ['راننده', 'کمک راننده']
    }
    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=operator_template.xlsx'
    df.to_excel(response, index=False)
    return response

@login_required
def failure_reason_list(request):
    reasons = FailureReason.objects.all()
    form = FailureReasonForm()
    import_form = FailureReasonImportForm()

    if request.method == 'POST':
        if 'add_reason' in request.POST:
            form = FailureReasonForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'علت خرابی با موفقیت اضافه شد.')
                return redirect('failure_reason_list')
            else:
                messages.error(request, 'خطا در افزودن علت خرابی. لطفاً فرم را بررسی کنید.')
        elif 'import_reasons' in request.POST:
            import_form = FailureReasonImportForm(request.POST, request.FILES)
            if import_form.is_valid():
                file = request.FILES['file']
                df = pd.read_excel(file)
                for index, row in df.iterrows():
                    FailureReason.objects.create(name=row['name'])
                messages.success(request, 'علت‌های خرابی با موفقیت ایمپورت شدند.')
                return redirect('failure_reason_list')
            else:
                messages.error(request, 'خطا در ایمپورت علت‌های خرابی. لطفاً فایل اکسل را بررسی کنید.')

    return render(request, 'dumptrucks/failure_reason_list.html', {
        'reasons': reasons,
        'form': form,
        'import_form': import_form
    })

@login_required
def delete_reason(request, id):
    reason = get_object_or_404(FailureReason, id=id)
    reason.delete()
    messages.success(request, 'علت خرابی با موفقیت حذف شد.')
    return redirect('failure_reason_list')

@login_required
def dump_truck_list(request):
    dump_trucks = DumpTruck.objects.all().order_by('type')
    form = DumpTruckForm()
    import_form = DumpTruckImportForm()

    if request.method == 'POST':
        if 'add_dump_truck' in request.POST:
            form = DumpTruckForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'دستگاه با موفقیت اضافه شد.')
                return redirect('dump_truck_list')
            else:
                messages.error(request, 'خطا در افزودن دستگاه. لطفاً فرم را بررسی کنید.')
                print(form.errors)
        elif 'import_dump_trucks' in request.POST:
            import_form = DumpTruckImportForm(request.POST, request.FILES)
            if import_form.is_valid():
                file = request.FILES['file']
                df = pd.read_excel(file)
                for index, row in df.iterrows():
                    DumpTruck.objects.create(
                        code=row['کد دستگاه'],
                        model=row['مدل'],
                        is_active=row['فعال'],
                        type=row['نوع']
                    )
                messages.success(request, 'دستگاه‌ها با موفقیت ایمپورت شدند.')
                return redirect('dump_truck_list')
            else:
                messages.error(request, 'خطا در ایمپورت دستگاه‌ها. لطفاً فایل اکسل را بررسی کنید.')

    active_counts = dump_trucks.values('type').annotate(active_count=Count('type', filter=Q(is_active=True)))

    return render(request, 'dumptrucks/dump_truck_list.html', {
        'dump_trucks': dump_trucks,
        'form': form,
        'import_form': import_form,
        'active_counts': active_counts
    })

@login_required
def edit_dump_truck(request, id):
    dump_truck = get_object_or_404(DumpTruck, id=id)
    if request.method == 'POST':
        form = DumpTruckForm(request.POST, instance=dump_truck)
        if form.is_valid():
            form.save()
            messages.success(request, 'دستگاه با موفقیت ویرایش شد.')
            return redirect('dump_truck_list')
    else:
        form = DumpTruckForm(instance=dump_truck)
    return render(request, 'dumptrucks/dump_truck_edit.html', {'form': form, 'dump_truck': dump_truck})

@login_required
def delete_dump_truck(request, id):
    dump_truck = get_object_or_404(DumpTruck, id=id)
    dump_truck.delete()
    messages.success(request, 'دستگاه با موفقیت حذف شد.')
    return redirect('dump_truck_list')

@login_required
def download_dump_truck_template(request):
    data = {
        'کد دستگاه': ['DT123', 'DT456'],
        'مدل': ['Komatsu', 'Caterpillar'],
        'فعال': [True, True],
        'نوع': ['شاول', 'دامپتراک']
    }
    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=dump_truck_template.xlsx'
    df.to_excel(response, index=False)
    return response
