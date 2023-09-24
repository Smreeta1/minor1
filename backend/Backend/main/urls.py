"""
URL configuration for djangobackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from api import views
from django.contrib import admin
from django.urls import path,include


 
admin.site.site_header = "Garbage Tracking System Admin"
admin.site.site_title = "Garbage Tracking System Admin Portal"
admin.site.index_title = "Welcome to Garbage Tracking System Portal"

urlpatterns =[
    #path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('',include('api.urls')),
    path('api/', include('api.urls')),
]
"""path('api/', include('api.urls')),
   
     
    path('signup/public/', views.signup_public, name='signup_public'),
    path('signup/staff/', views.signup_staff, name='signup_staff'),
    path('signup/officer/', views.signup_officer, name='signup_officer'),
    
    path('signin/public/', views.signin_public, name='signin_public'),
    path('signin/staff/', views.signin_staff, name='signin_staff'),
    path('signin/officer/', views.signin_officer, name='signin_officer'),
"""




