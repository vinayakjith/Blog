from django.shortcuts import render,redirect,get_object_or_404
from adminpanel.models import Blog, Comment,Profile,User
from django.contrib import messages
from django.contrib.auth import authenticate,login,update_session_auth_hash,logout
from .forms import Registrationform,Loginform,Profileform,Blogform,Commentform,PasswordResetForm,PasswordChangeForm,ResetPasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from adminpanel.models import OTP
from userpanel.tasks import send_otp_email,register
from .utils import generate_otp
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

# Create your views here.



@login_required(login_url='userpanel:user_login')
def user_home(request):
    profiles=Profile.objects.all()
    blogs=Blog.objects.filter(author__is_active=True,status='publish').order_by("-updated_at")
    comments=Comment.objects.filter(user__is_active=True)
    context={
        'blogs':blogs,
        'comments':comments,
        'profiles':profiles
    }
    return render(request,'userpanel/user_home.html',context)

@login_required(login_url='userpanel:user_login')
def add_blog(request):
    users=User.objects.all()
    if request.method=='POST':
        title=request.POST.get('blog_title')
        content=request.POST.get('blog_content')
        image=request.FILES.get('blog_image')
        user_id=request.POST.get('blog_author')
        user=get_object_or_404(User,id=user_id)
        Blog.objects.create(
            title=title,
            content=content,
            blog_image=image,
            author=user

        )  
        messages.success(request,'A new blog is added successfully')
        if user.is_staff():
            return redirect("adminpanel:admin_home")
        else:
            return redirect("userpanel:user_home")

     
    context={
        'users':users
    }
    return render(request,'userpanel/add_blog.html',context)

@login_required(login_url='userpanel:user_login')
def edit_blog(request, blog_id):
    blog=get_object_or_404(Blog, id=blog_id)
    users=User.objects.all()
    if request.method=='POST':
        blog.title=request.POST.get('blog_title')
        blog.content=request.POST.get('blog_content')
        blog.blog_image=request.FILES.get('blog_image')
        user_id=request.POST.get('blog_author')
        user=get_object_or_404(User,id=user_id)

        if request.FILES.get('blog_image'):
            blog.blog_image=request.FILES.get('blog_image')
        blog.save()
        if user.is_staff():
            return redirect("adminpanel:admin_home")
        else:
            return redirect("userpanel:user_home")

     
    
    context={
        "users":users,
        "blog":blog

    }
    return render(request,'userpanel/edit_blog.html',context)

@login_required(login_url='userpanel:user_login')
def blog_lists(request):
    blog=Blog.objects.all().order_by("-updated_at")
    context={
        'blog':blog
    }
    return render(request,'userpanel/blog_lists.html',context)
@login_required(login_url='userpanel:user_login')
def edit_profile(request, profile_id):
    profile=get_object_or_404(Profile,id=profile_id)
    if request.method=='POST':
        profile.user.username=request.POST.get('profile_name')
        profile.profile_description=request.POST.get('profile_description')
        profile.phone=request.POST.get('profile_phone')
        profile.user.email=request.POST.get('profile_email')
        profile.profile_image=request.FILES.get('profile_image')
        profile.id_proof=request.FILES.get('proof_image')
        if request.FILES.get('profile_image'):
            profile.profile_image = request.FILES.get('profile_image')
        if request.FILES.get('proof_image'):
            profile.id_proof = request.FILES.get('proof_image')

        profile.save()
        return redirect('userpanel:view_profile')
    context={
        'profile':profile
    
    }

    return render(request,'userpanel/edit_profile.html',context)

@login_required(login_url='userpanel:user_login')
def my_blogs(request, user_id):
    user=get_object_or_404(User, id=user_id)
    blog=Blog.objects.filter(author=user).order_by('-updated_at')
    context={
        'user':user,
        'blog':blog
    }


    return render(request,'userpanel/my_blogs.html',context)

    

@login_required(login_url='userpanel:user_login')
def view_profile(request):
    user=request.user
    profile=Profile.objects.filter(user=user)
    
    context={
        'profile':profile,
        'user':user
    }
    return render(request,'userpanel/view_profile.html',context)


def register_user(request):
    if request.method=='POST':
        email=request.POST.get('email')
        form=Registrationform(request.POST)
        if form.is_valid():
            form.save()
            register.delay(email)
            messages.success(request,'User registered successfully')
            return redirect('userpanel:user_login')
    else:
        form=Registrationform()
    context={
        'form':form
    }
    return render(request,'userpanel/register.html',context)



def user_login(request):
    if request.method=="POST":
        form=Loginform(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                if user.is_staff:
                    messages.success(request,'User Login successfull')
                    return redirect('adminpanel:admin_home')
                else:
                    messages.success(request,'User Login successfull')
                    return redirect('userpanel:user_home')
    else:
        form=Loginform()
    context={
        'form':form,
        'user':request.user
    }
    return render(request,'userpanel/user_login.html',context)


@login_required(login_url='userpanel:user_login')
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = Profile.objects.filter(user=user).first()
    
    if request.method == 'POST':
        form = Profileform(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Profile updated successfully')
            if user.is_staff:
                return redirect('adminpanel:admin_home')
            else:
                return redirect('userpanel:user_home')
    else:
        form = Profileform(instance=profile)

    context = {
        'form': form
    }
    return render(request, 'userpanel/user_profile.html', context)


@login_required(login_url='userpanel:user_login')
def blog(request,user_id):
    user=get_object_or_404(User, id=user_id)
    if request.method=='POST':
        form=Blogform(request.POST,request.FILES)  
        if form.is_valid():
            blog=form.save(commit=False)
            blog.author=request.user
            blog.save()
            messages.success(request,'Blog added Successfully')
            if user.is_staff:
                return redirect('adminpanel:admin_home') 
            else:
                return redirect('userpanel:user_home')
    else:
        form=Blogform()
    context={
        'form':form
    }
    return render(request,'userpanel/blog.html',context)

@login_required(login_url='userpanel:user_login')
def blog_edit(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id) 
    user=request.user

    if blog.author==request.user:
        user_id=request.session.get('user_id',0)
        if request.method=='POST':
            form=Blogform(request.POST,request.FILES,instance=blog)
            if form.is_valid():
                form.save()
                messages.success(request,'Blog edited successfully')
                if user.is_staff:
                    return redirect('adminpanel:admin_home')  
                else:
                    return redirect('userpanel:user_home')
        else:
            form=Blogform(instance=blog)
    else:
        messages.error(request, 'You are not authorized to edit this blog')
        if user.is_staff:
            return redirect('adminpanel:admin_home')  
        else:
            return redirect('userpanel:user_home')


    context={
        'form':form
    }
    return render(request,'userpanel/blog_edit.html',context)

@login_required(login_url='userpanel:user_login')
def del_blogs(request, blog_id):
    blog=get_object_or_404(Blog, id=blog_id)
    user=request.user
    if blog.author==request.user:
        blog.delete()
        messages.success(request,'Blog deleted successfully')
        if user.is_staff:
            return redirect('adminpanel:admin_home')  
        else:
            return redirect('userpanel:user_home')
    else:
        messages.error(request, 'You are not authorized to delete this blog')
        if user.is_staff:
            return redirect('adminpanel:admin_home')  
        else:
            return redirect('userpanel:user_home')
   
        
@login_required(login_url='userpanel:user_login')
def view_blog(request, blog_id):
    blog=get_object_or_404(Blog,id=blog_id) 
    comment=Comment.objects.filter(blog=blog,status='show')
    if request.method=="POST":
        form=Commentform(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.blog=blog
            comment.user=request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('userpanel:view_blog', blog_id=blog.id)
    else:
        form=Commentform()
    context={
        'form':form,
        'blog':blog,
        'comments':comment
    }
    return render(request,'userpanel/view_blog.html',context)




@login_required(login_url='userpanel:user_login')
def password_reset_done(request):
    return render(request, 'userpanel/password_reset_done.html')

@login_required(login_url='userpanel:user_login')
def passchange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Change Password successful')
            return redirect('userpanel:user_login')
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form
    }
    return render(request, 'userpanel/passchange.html', context)


@login_required(login_url='userpanel:user_login')
def user_logout(request):
    logout(request)
    return redirect('sitevisitor:site_home')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.filter(email=email).first()
            otp = generate_otp()
            OTP.objects.update_or_create(user=user, defaults={'otp': otp})
            send_otp_email.delay(email, otp)  # Send email using Celery
            messages.success(request, "OTP sent to your email.")
            return redirect('userpanel:validate_otp')  # Redirect to OTP validation page
        except User.DoesNotExist:
            messages.error(request, "No user found with this email.")
    return render(request, 'userpanel/forgot_password.html')



def validate_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')

        # Fetch all users with the given email
        users = User.objects.filter(email=email)

        if not users.exists():
            messages.error(request, "No account found with this email.")
            return render(request, 'userpanel/validate_otp.html')

        if users.count() > 1:
            messages.error(request, "Multiple accounts found with this email. Please contact support.")
            return render(request, 'userpanel/validate_otp.html')
        user = users.first()

        try:
            # Ensure that 'user' is a singular object
            otp_record = OTP.objects.get(user=user, otp=otp)

            if otp_record.is_valid():
                messages.success(request, "OTP validated. You can now reset your password.")
                return redirect('userpanel:reset_password')
            else:
                messages.error(request, "OTP has expired.")
        except OTP.DoesNotExist:
            messages.error(request, "Invalid OTP.")
    
    return render(request, 'userpanel/validate_otp.html')



def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successfully.")
            return redirect('userpanel:user_login')  # Redirect to login page
        except User.DoesNotExist:
            messages.error(request, "An error occurred while resetting the password.")
    return render(request, 'userpanel/reset_password.html')