from django.shortcuts import render,get_object_or_404,redirect
from .models import Blog, Comment,Profile,User
from django.contrib import messages
from  .tasks import userstatus
# Create your views here.


# Admin Home View
def admin_home(request):
    profiles=Profile.objects.all()
    blogs=Blog.objects.filter(author__is_active=True, status='publish').order_by("-updated_at")
    comments=Comment.objects.filter(user__is_active=True, status='show')
    context={
        'blogs':blogs,
        'comments':comments,
        'profiles':profiles
    }
    return render(request,'adminpanel/admin_home.html',context)


# Dashboard View
def dashboard(request):
    count_published=Blog.objects.filter(status='publish').count()
    count_hidden=Blog.objects.filter(status='hidden').count()
    count_draft=Blog.objects.filter(status='draft').count()
    count_active=User.objects.filter(is_active=True).count()
    count_admin=User.objects.filter(is_staff=True).count()
    count_inactive=User.objects.filter(is_active=False).count()
    context={
        'count_published':count_published,
        'count_hidden': count_hidden,
        'count_draft':count_draft,
        'count_active':count_active,
        'count_admin':count_admin,
        'count_inactive':count_inactive
        
    }

    return render(request,'adminpanel/dashboard.html',context)


# Blog List View
def blog_list(request):
    blog=Blog.objects.all().order_by("-updated_at")
    context={
        'blog':blog
    }
    return render(request,'adminpanel/blog_list.html',context)

# Blog View
def blog_view(request,blog_id):
    blog=get_object_or_404(Blog,id=blog_id)
    context={
        'blog':blog
    }

    return render(request,'adminpanel/blog_view.html',context)

# Reset Password View
def reset_password(request):
    return render(request,'adminpanel/reset_password.html')


# User List View
def user_list(request):
    user=User.objects.all()
    context={
        'users':user
    }
    return render(request,'adminpanel/user_list.html',context)


# View User Details
def view_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context={
        'user':user
    }
    return render(request, 'adminpanel/view_user.html', context)

# Toggle User Status
def user_status(request,user_id):
    user=get_object_or_404(User, id=user_id)
    email= user.email
    if request.user != user:
        user.is_active=not user.is_active
        user.save()

        if user.is_active:
            status='Activated'
            userstatus.delay(email, status)
            messages.success(request,'User Activated')

        else:
            status='Deactivated'
            userstatus.delay(email, status)
            messages.success(request,'User Deactivated')
        
        return redirect('adminpanel:user_list')
    else:
        messages.error(request, 'You cannot deactivate your own account.')
        return redirect('adminpanel:user_list')


# Toggle Blog Visibility
def hide_blog(request, blog_id):
    blog=get_object_or_404(Blog, id=blog_id)
    if blog.status=='hidden':
        blog.status='publish'
        messages.success(request,'Blog is visible now')

    else:
        blog.status='hidden'
        messages.success(request,'Blog is hidden now')

    blog.save()
    return redirect('adminpanel:blog_list')


# View Comments
def view_comments(request, blog_id):
    comments=Comment.objects.filter(blog_id=blog_id)
    context={
        'comments':comments
    }
    return render(request,'adminpanel/view_comments.html',context)


# Toggle Comment Visibility
def hide_comment(request,comment_id):
    comments=get_object_or_404(Comment,id=comment_id)
    if comments.status=='hide':
        comments.status='show'
        messages.success(request,'Comment is visible now')
    else:
        comments.status='hide'
        messages.success(request,'Comment hidden')


    comments.save()
    return redirect('adminpanel:view_comments', blog_id=comments.blog.id)

