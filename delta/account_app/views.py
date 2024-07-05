from django.shortcuts import render

def account(request):
    return render(request, 'account_app/account_app.html')
