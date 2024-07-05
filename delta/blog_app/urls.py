import django.urls
from django.urls import path
import blog_app.views

urlpatterns = [
    path('<username>', blog_app.views.profile, name='profile'),  
    path('', blog_app.views.userlist, name='userlist'),

]