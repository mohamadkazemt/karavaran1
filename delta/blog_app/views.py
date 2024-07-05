from django.shortcuts import render
from django.http import Http404

users = [
    {
        'username': 'amir',
        'lastname': 'amiri',
        'age': '35'
    },
    {
        'username': 'mohamad',
        'lastname': 'kazem',
        'age': '44'
    },
    {
        'username': 'محمدکلظم',
        'lastname': 'kazem',
        'age': '55'
    },
]
def userlist(request):
    return render(request, 'blog_app/userlist.html', {'users': users})

def profile(request, username):
    for user in users:
        if user['username'] == username:
            context = {
                'username': user['username'],
                'lastname': user['lastname'],
                'age': user['age']
            }
            return render(request, 'blog_app/profile.html', context)
    raise Http404("این کاربر وجود ندارد")
