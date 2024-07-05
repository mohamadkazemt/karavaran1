from django.urls import path
from . import views

urlpatterns = [
    path('top-dump-truck-downtimes/', views.top_dump_truck_downtimes, name='top_dump_truck_downtimes'),
    path('top-operator-downtimes/', views.top_operator_downtimes, name='top_operator_downtimes'),
    path('top-failure-reasons/', views.top_failure_reasons, name='top_failure_reasons'),
]
