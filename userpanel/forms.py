from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm,PasswordChangeForm
from django import forms
from adminpanel.models import Profile,Blog,Comment

class Registrationform(UserCreationForm):
    first_name=forms.CharField(
        max_length=30,
        required=True,
        label='First Name',
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    last_name=forms.CharField(
        max_length=30,
        required=True,
        label='Last Name',
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    email=forms.EmailField(
        max_length=30,
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'class':'form-control'})
    )
    username=forms.CharField(
        max_length=30,
        required=True,
        label='User Name',
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    password1=forms.CharField(
        max_length=30,
        required=True,
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control'})

    )
    password2=forms.CharField(
        max_length=30,
        required=True,
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )


    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password1','password2']

class Loginform(forms.Form):
    username=forms.CharField(
        required=True,
        label='User Name',
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    password=forms.CharField(
        required=True,
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )

class Profileform(forms.ModelForm):

    first_name=forms.CharField(
        required=True,
        label="First Name",
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    
    last_name=forms.CharField(
        required=True,
        label="Last Name",
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    profile_description=forms.CharField(
        required=True,
        label="Description",
        widget=forms.TextInput(attrs={'class':'form-control'})
    )

    phone=forms.CharField(
        required=True,
        label="Phone",
        widget=forms.TextInput(attrs={'class':'form-control'})
    )

    profile_image=forms.ImageField(
        required=True,
        label='Profile Image',
        widget=forms.ClearableFileInput(attrs={'class':'form-control'})    
    )


    proof_image=forms.ImageField(
        label='Proof Image',
        widget=forms.ClearableFileInput(attrs={'class':'form-control'})     
    )

    class Meta:
        model=Profile
        fields='first_name','last_name','profile_description','phone','profile_image','proof_image'
class Blogform(forms.ModelForm):
    title=forms.CharField(
        required=True,
        label="Title",
        widget=forms.TextInput(attrs={'class':'form-control'})
    )

    content=forms.CharField(
        required=True,
        label="Content",
        widget=forms.Textarea(attrs={'class':'form-control'})
    )
    
    blog_image=forms.ImageField(
        required=True,
        label='Blog Image',
        widget=forms.ClearableFileInput(attrs={'class':'form-control'})    
    )

    class Meta:
        model=Blog
        fields=['title','content','blog_image','status']
class Commentform(forms.ModelForm):
    comment=forms.CharField(
        label='Comment',
        widget=forms.TextInput(attrs={'class':'form-control'})          
    )
    class Meta:
        model=Comment
        fields=['comment']
        
class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(label="New Password", widget=forms.PasswordInput)

class Change(PasswordChangeForm):
    
    class Meta:
        model=User
        fields='__all__'
