from django.contrib import admin
from django.urls import path ,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account_app.urls')),
    path('userlist/', include('blog_app.urls')),
    path('dumptrucks/', include('dumptrucks.urls')),
    path('courses/', include('courses_app.urls')),
    path('reports/', include('reports.urls')),
    
]
