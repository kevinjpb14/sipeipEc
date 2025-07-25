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
    path('',views.inicio),
    path('inicio/',views.inicio,name='inicio'),
    path('login/', views.login_view, name='login'),
    #URLS DE CRUD CONFIGURACIÓN INSTITUCIONAL*-*-*-**-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
    path('conf_institucional/',views.conf_institucional,name='conf_institucional'),
    path('modifica-institucion/<int:idinstitucion>/',views.institucion_modi, name="modi_inst"),#vista para modal de edicion institucional
    path('modificar-institucion/<int:idinstitucion>/',views.institucion_modificar, name="modificar_inst"), #aqui se envia el post para editar la institucion
    path('ajax/obtener_subsectores/', views.obtener_subsectores, name='obtener_subsectores'),#url que me consulta los subsectores relacionados al sector seleccionado.
    path('instituciones/eliminar/', views.eliminar_institucion, name='eliminar_institucion'),#url que enlaza eliminar instituciones y cambia estado a flase de las mismas
    path('instituciones/agregar/', views.institucion_agregar, name='institucion_agregar'),#url que permite agregar nuevas instituciones
    #SECTORES*-*-*-*-*-*-*
    path('conf_institucional/sectores/', views.sectores, name='sectores'),#url que consulta todos los sectores
    path('modifica-sector/<int:idsector>/',views.sector_modi, name="modi_sect"),#vista para modal de edicion sector
    path('modificar-sector/<int:idsector>/',views.sector_modificar, name="modificar_sect"), #aqui se envia el post para editar el sector
    path('sector/agregar/', views.sector_agregar, name='sector_agregar'),#url que permite agregar nuevas sectores
    path('sector/eliminar/', views.eliminar_sector, name='eliminar_sector'),#url que enlaza eliminar sector y cambia estado a false de las mismas
    #FIN SECTORES *-*-*-*-*-*
    #SUBSECTORES*-*-*-*-*-*-*
    path('conf_institucional/subsectores/', views.subsectores, name='subsectores'),#url que consulta todos los subsectores
    path('modifica-subsector/<int:idsubsector>/',views.subsector_modi, name="modi_subsect"),#vista para modal de edicion subsector
    path('modificar-subsector/<int:idsubsector>/',views.subsector_modificar, name="modificar_subsect"), #aqui se envia el post para editar el subsector
    path('subsector/agregar/', views.subsector_agregar, name='subsector_agregar'),#url que permite agregar nuevas subsectores
    path('subsector/eliminar/', views.eliminar_subsector, name='eliminar_subsector'),#url que enlaza eliminar subsector y cambia estado a false de las mismas
    #FIN SUBSECTORES *-*-*-*-*-*
    #FIN URLS DE CRUD CONFIGURACIÓN INSTITUCIONAL*-*-*-**-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
    
    #URLS CRUD GESTION DE USUARIOS*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
    path('usuarios/',views.usuarios,name='usuarios'),
    path('modifica-usuario/<int:idusuario>/',views.usuario_modi, name="modi_usu"),#vista para modal de edicion usuarios
    path('modificar-usuario/<int:idusuario>/',views.usuario_modificar, name="modificar_usu"), #aqui se envia el post para editar al usuario
    path('usuarios/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),#url que enlaza eliminar usuarios y cambia estado a false de las mismas
    #FIN DE URLS CRUD GESTION DE USUARIOS*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
    # URLS OBJETIVOS ESTRATEGICOS-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
    path('objetivos/estrategicos/', views.objetivo_estrategico_list, name='objetivo_estrategico_list'),
    path('objetivos/estrategicos/agregar/', views.objetivo_estrategico_agregar, name='objetivo_estrategico_agregar'),
    path('objetivos/estrategicos/ods/', views.objetivo_estrategico_ods, name='objetivo_estrategico_ods'),
    path('objetivos/estrategicos/editar/', views.objetivo_estrategico_edit, name='objetivo_estrategico_edit'),
    path('objetivos/estrategicos/history/', views.objetivo_estrategico_history, name='objetivo_estrategico_history'),
    path('objetivos/estrategicos/eliminar/', views.objetivo_estrategico_delete, name='objetivo_estrategico_delete'),
    path('objetivos/ods/', views.objetivo_ods_list, name='objetivo_ods_list'),
    path('ods/agregar/', views.ods_agregar, name='ods_agregar'),
    path('ods/eliminar/', views.ods_eliminar, name='ods_eliminar'),
    path('ods/editar/', views.ods_editar, name='ods_editar'),
    path('objetivos/pnd/', views.objetivo_pnd_list, name='objetivo_pnd_list'),
    path('pnd/agregar/', views.pnd_agregar, name='pnd_agregar'),
    path('pnd/eliminar/', views.pnd_eliminar, name='pnd_eliminar'),
    path('pnd/editar/', views.pnd_editar, name='pnd_editar'),

    #FIN DE URLS OBJETIVOS ESTRATEGICOS-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
    #URLS PROYECTOS-*-*-**-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
    path('proyectos/', views.proyectos_list, name='proyectos_list'),
    path('proyectos/registrar/', views.proyecto_registrar, name='proyecto_registrar'),
    path('ajax/programas_por_plan/', views.programas_por_plan, name='programas_por_plan'),#URL para la vista AJAX de programas por plan
    path('ajax/cantones_por_provincia/', views.cantones_por_provincia, name='cantones_por_provincia'),#URL para la vista AJAX de cantones por provincia
    path('ajax/parroquias_por_canton/', views.parroquias_por_canton, name='parroquias_por_canton'),#URL para la vista AJAX de parroquias por canton
    path('ajax/info_objetivo_estrategico/', views.info_objetivo_estrategico, name='info_objetivo_estrategico'),#URL para la vista AJAX para enviar info del objetivo seleccionado
    path('ajax/info_meta/', views.info_meta, name='info_meta'),#URL para la vista AJAX para enviar indicadores asociados a meta seleccionada
    path('ajax/info_impacto_ambiental/', views.info_impacto_ambiental, name='info_impacto_ambiental'),#URL para la vista AJAX para enviar info del impacto ambiental seleccionado
    path('ajax/proyecto_detalle/', views.proyecto_detalle, name='proyecto_detalle'),#AJAX en Django para traer todo el detalle del producto


    #FIN URLS PROYECTOS-*-*-**-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
    path('logout/', views.logout_view, name='logout'),
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
