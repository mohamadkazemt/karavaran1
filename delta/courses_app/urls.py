from django.urls import path
from . import views

urlpatterns = [
    path('', views.courses, name='courses_app'),
    path('detail/<int:course_id>', views.courses_detail, name='courses_detail'),
]