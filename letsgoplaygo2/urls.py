"""
URL configuration for letsgoplaygo2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='home'),
    path('auth', views.auth, name='auth'),
    path('login', views.login_user, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('movie/<int:page>', views.save_create_movie, name='save_create_movie'),
    path('raw/<str:str_model>/add', views.create_model, name='CreateModel'),
    path('update/movie/<int:movie_id>/', views.update_movie, name='UpdateMovie'),
    path('delete/', views.delete_model, name='delete'),
    path('update/session/<int:session_id>/', views.update_session, name='update_session'),
]
