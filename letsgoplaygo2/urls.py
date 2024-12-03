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
    path('update/<str:model>/0/', views.create),
    path('admin/', admin.site.urls),
    path('', views.main, name='home'),
    path('auth', views.auth, name='auth'),
    path('login', views.login_user, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('raw/<str:str_model>/add', views.create_model, name='CreateModel'),
    path('<str:model>/<int:page>', views.read_model, name='view_some_table'),
    path('update/session/<int:session_id>/', views.update_session, name='update_session'),
    path('update/movie/<int:movie_id>/', views.update_movie, name='UpdateMovie'),
    path('update/ticket/<int:ticket_id>/', views.update_ticket, name='update_ticket'),
    path('update/hall/<int:hall_id>/', views.update_hall, name='update_hall'),
    path('update/row/<int:row_id>/', views.update_row, name='update_row'),
    path('update/client/<int:client_id>/', views.update_client, name='update_row'),
    path('delete/', views.delete_model, name='delete'),
    path('create/ticket/<int:session>/<int:row>/<int:seat>', views.create_ticket, name="create_ticket"),
    path('first', views.first_otchet),
    path('second', views.second_otchet),
    path('third', views.third_otchet)


]
