from django.urls import path
from .views import site_home,forgot_password,login,otp,reset_password,registration

app_name='sitevisitor'
urlpatterns=[
    path('',site_home, name='site_home'),
    path('forgot_password/',forgot_password,name='forgot_password'),
    path('login/',login,name='login'),
    path('otp/',otp,name='otp'),
    path('registration/',registration,name='registration'),
    path('reset_password/',reset_password,name='reset_password'),

]

