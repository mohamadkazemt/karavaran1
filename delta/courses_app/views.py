from django.shortcuts import render
from .models import course


def courses(request):
    courses = course.objects.all()
    context = {'courses': courses}
    return render(request, 'courses_app/courses_app.html', context)

def courses_detail(request, course_id):
    course = course.objects.get(id=course_id)
    context = {'course': course}
    return render(request, 'courses_app/courses_detail.html', context)