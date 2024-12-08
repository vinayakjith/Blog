from django.urls import path
from .views import user_logout,passchange,del_blogs, password_reset_done,reset_password,user_login,blog, user_profile,user_home,add_blog,blog_lists,edit_blog,edit_profile,my_blogs,view_profile,view_blog,register_user,blog_edit,forgot_password,validate_otp


app_name='userpanel'
urlpatterns=[
    path('',user_home,name='user_home'),
    path('add_blog/',add_blog,name='add_blog'),
    path('blog_lists/',blog_lists,name='blog_lists'),
    path('edit_blog/<int:blog_id>/',edit_blog,name='edit_blog'),
    path('edit_profile/<int:profile_id>/',edit_profile, name='edit_profile'),  
    path('my_blogs/<int:user_id>/',my_blogs,name='my_blogs'),
    path('view_profile/',view_profile,name='view_profile'),
    path('view_blog/<int:blog_id>/',view_blog,name='view_blog'),
    path('register/',register_user,name='register_user'),
    path('user_login/',user_login,name='user_login'),
    path('user_profile/<int:user_id>/',user_profile,name='user_profile'),
    path('blog/<int:user_id>/',blog,name='blog'),
    path('blog_edit/<int:blog_id>/',blog_edit,name='blog_edit'),
    path('reset_password/',reset_password,name='reset_password'),
    path('password_reset_done/', password_reset_done, name='password_reset_done'),  
    path('del_blogs/<int:blog_id>/',del_blogs,name='del_blogs'),
    path('passchange/', passchange, name='passchange'),
    path('user_logout/',user_logout,name='user_logout'),
    path('forgot_password/',forgot_password, name='forgot_password'),
    path('validate-otp/',validate_otp, name='validate_otp'),

]