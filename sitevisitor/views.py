from django.shortcuts import render
from adminpanel.models import Blog, Comment,Profile
# Create your views here.

def site_home(request):

    profiles=Profile.objects.all()
    blogs=Blog.objects.filter(author__is_active=True,status='publish').order_by("-updated_at")
    comments=Comment.objects.filter(user__is_active=True)
    context={
        'blogs':blogs,
        'comments':comments,
        'profiles':profiles
    }
    return render(request,'sitevisitor/site_home.html',context)


def forgot_password(request):
    return render(request,'sitevisitor/forgot_password.html')
    
def login(request):
    return render(request,'sitevisitor/login.html')

def otp(request):
    return render(request,'sitevisitor/otp.html')

def registration(request):
    return render(request,'sitevisitor/registration.html')

def reset_password(request):
    return render(request,'sitevisitor/reset_password.html')