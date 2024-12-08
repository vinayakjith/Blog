from django.urls import path

from .views import view_comments,admin_home,blog_list,blog_view,reset_password,user_list,view_user,dashboard,user_status,hide_blog,hide_comment


app_name='adminpanel'
urlpatterns=[
    path('',admin_home, name='admin_home'),
    path('blog_list/',blog_list,name='blog_list'),
    path('blog/<int:blog_id>/',blog_view,name='blog_view'),
    path('reset_password/',reset_password,name='reset_password'),
    path('user_list/',user_list,name='user_list'),
    path('user/<int:user_id>/',view_user, name='view_user'),
    path('blog_view/<int:blog_id>/',blog_view, name='blog_view'),
    path('dashboard/',dashboard,name='dashboard'),
    path('user_status/<int:user_id>/',user_status,name='user_status'),
    path('hide_blog/<int:blog_id>/',hide_blog,name='hide_blog'),
    path('hide_comment/<int:comment_id>/',hide_comment,name='hide_comment'),
    path('view_comments/<int:blog_id>/',view_comments,name='view_comments')
    
]

