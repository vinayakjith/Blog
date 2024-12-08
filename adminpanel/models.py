from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Check if OTP is within the 10-minute validity
        expiration_time = self.created_at + timedelta(minutes=300)
        print(f"OTP Created At: {self.created_at}, Expiration Time: {expiration_time}, Current Time: {now()}")
        return now() <= expiration_time

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_description=models.TextField()
    phone=models.CharField(max_length=20)
    profile_image=models.ImageField(upload_to='profile_images/')
    id_proof=models.ImageField(upload_to='proofs/')
    
    def __str__(self):
        return self.user.username


class Blog(models.Model):

    STATUS_CHOICES = (
    ('publish', 'Publish'),
    ('draft', 'Draft'),
    ('hidden', 'Hidden'),
)


    title=models.CharField(max_length=200)
    content=models.TextField()
    blog_image=models.ImageField(upload_to='blog_images/')
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='draft')


    def __str__(self):
        return self.title



class Comment(models.Model):

    STATUS_CHOICES = (
        ('show', 'Show'),
        ('hide', 'Hide'),
    )


    comment=models.TextField(max_length=300)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='show')

    def __str__(self):
        return self.user.username