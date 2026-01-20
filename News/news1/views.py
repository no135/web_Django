from django.shortcuts import render
from .models import Artciels
# Create your views here.


def blog(request):
    articles = Artciels.objects.all()
    return render(request,'news.html',{'articles':articles})


def blog_detail(request):
    return render(request,'blog_detail.html')