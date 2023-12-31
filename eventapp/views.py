from django.shortcuts import render

def home(request):
    return render(request,'eventapp/home.html')
