"""
URL configuration for sipeip project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from app_sipeip import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.hello),
    path('inicio/',views.hello,name='inicio'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registrar_usuario, name='registro'),
    path('activar/<uidb64>/<token>/', views.activar_cuenta, name='activar_cuenta'),
    path('cambio-clave/', views.cambio_clave, name='cambio_clave'),
    #vistas de recuperacion de clave por Django
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='app_sipeip/recuperar_clave/password_reset.html',
        email_template_name='app_sipeip/recuperar_clave/password_reset_email.txt',  # Backup texto plano
        html_email_template_name='app_sipeip/recuperar_clave/password_reset_email.html',
        subject_template_name='app_sipeip/recuperar_clave/password_reset_subject.txt',
        success_url='/password_reset_enviado/',
    ), name='password_reset'),

    path('password_reset_enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='app_sipeip/recuperar_clave/password_reset_enviado.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='app_sipeip/recuperar_clave/password_reset_confirm.html',
        success_url='/password_reset_completo/'
    ), name='password_reset_confirm'),

    path('password_reset_completo/', auth_views.PasswordResetCompleteView.as_view(
        template_name='app_sipeip/recuperar_clave/password_reset_completo.html'
    ), name='password_reset_complete'),
    #fin de vistas de recuperacion de clave por Django
]
