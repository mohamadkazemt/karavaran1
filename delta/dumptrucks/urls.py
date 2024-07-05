from django.urls import path
from .views import (
    downtime_list, downtime_create, downtime_edit, export_downtimes_to_excel, 
    operator_list, edit_operator, delete_operator, download_excel_template, 
    failure_reason_list, delete_reason, dump_truck_list, delete_dump_truck, 
    edit_dump_truck, download_dump_truck_template
)

urlpatterns = [
    path('', downtime_list, name='downtime_list'),
    path('create/', downtime_create, name='downtime_create'),
    path('edit/<int:id>/', downtime_edit, name='downtime_edit'),
    path('export/', export_downtimes_to_excel, name='export_downtimes_to_excel'),
    path('operators/', operator_list, name='operator_list'),
    path('edit_operator/<int:id>/', edit_operator, name='edit_operator'),
    path('delete_operator/<int:id>/', delete_operator, name='delete_operator'),
    path('download_excel_template/', download_excel_template, name='download_excel_template'),
    path('failure_reasons/', failure_reason_list, name='failure_reason_list'),
    path('delete_reason/<int:id>/', delete_reason, name='delete_reason'),
    path('dump_trucks/', dump_truck_list, name='dump_truck_list'),
    path('edit_dump_truck/<int:id>/', edit_dump_truck, name='edit_dump_truck'),
    path('delete_dump_truck/<int:id>/', delete_dump_truck, name='delete_dump_truck'),
    path('download_dump_truck_template/', download_dump_truck_template, name='download_dump_truck_template'),
]
