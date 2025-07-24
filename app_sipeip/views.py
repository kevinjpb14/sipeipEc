from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Usuario
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import Instituciones,InstitucionSector,InstitucionSubsector,Roles,Usuario,Permisos,ObjetivoEstrategico,PlanNacionalDesarrollo,ObjetivosDesarrolloSostenible,ObjetivoEstrategicoHistory,AlineacionObjetivoOds
from django.http import JsonResponse
from datetime import datetime
from .models import Proyectos, ProyectoImpactoAmbiental, Programas,Planes,Provincias,Cantones,Parroquias,Metas,FinanciamientoProyecto,ActividadesProyecto,PeriodoActividad
from .models import ProyectoUbiGeografica
import json

@login_required(login_url='login')  # Redirige al login si no está autenticado
def registrar_usuario(request):
    usuario = request.user.usuario
    modulos = obtener_modulos_por_usuario(usuario)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        identificacion = request.POST.get('identificacion')

        if User.objects.filter(username=username).exists():
            return render(request, 'app_sipeip/registro.html', {'error': 'El usuario ya existe','modulos': modulos})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'app_sipeip/registro.html', {'error': 'El correo ya se encuentra registrado','modulos': modulos})
        
        if Usuario.objects.filter(identificacion=identificacion).exists():
            return render(request, 'app_sipeip/registro.html', {'error': 'La Cédula ya se encuentra registrada','modulos': modulos})
        # Generar contraseña temporal
        temp_password = get_random_string(length=10)

        # Crear usuario desactivado
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(temp_password),
            is_active=False
        )

        # Crear registro en tabla usuario
        Usuario.objects.create(
            user=user,
            username=username,
            identificacion=identificacion,
            nombres=nombres,
            apellidos=apellidos,
            mail=email,
            estado=False,
            fechacreacion=timezone.now()
        )

        # Generar token de activación válido por 2 días
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = request.build_absolute_uri(
            reverse('activar_cuenta', kwargs={'uidb64': uid, 'token': token})
        )

        # Enviar email
        send_mail(
            subject='Activación de cuenta SIPEIP+',
            message=f"Hola {nombres},\n\nTu usuario ha sido creado en el Sistema Integrado de Planificación e Inversión Pública (SIPeIP+).\n\nUsuario: {username}\nContraseña temporal: {temp_password}\n\nActiva tu cuenta aquí:\n{activation_link}\n\nEl enlace expirará en 2 días.",
            from_email="no-responder@sipeip.com",
            recipient_list=[email],
            fail_silently=False,
        )

        #return render(request, 'app_sipeip/registro_exitoso.html')
        return render(request, 'app_sipeip/registro.html', {'registro_exitoso': True,'modulos': modulos})
    if request.method == 'GET':
     return render(request, 'app_sipeip/registro.html',{'modulos': modulos})

def activar_cuenta(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and default_token_generator.check_token(user, token):
        request.session['activar_usuario_id'] = user.id
        return redirect('cambio_clave')
    else:
        return render(request, 'app_sipeip/activacion_invalida.html')

def cambio_clave(request):
    user_id = request.session.get('activar_usuario_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        nueva = request.POST.get('nueva')
        confirmar = request.POST.get('confirmar')

        if nueva != confirmar:
            return render(request, 'app_sipeip/cambio_clave.html', {'error': 'Las contraseñas no coinciden'})

        # 1. Cambiar contraseña y activar en auth_user
        user.set_password(nueva)
        user.is_active = True
        user.save()

        # 2. Actualizar también el estado en la tabla usuario
        usuario = Usuario.objects.get(user=user)
        usuario.estado = True
        #instancia de Foreign Key para guardar nuevo valor de id de llave foranea
        usuario.idrol =  Roles.objects.get(pk=4)#instancia de Foreign Key para guardar nuevo valor de id de llave foranea
        usuario.save()

        # Mantener sesión activa
        update_session_auth_hash(request, user)#Esta función actualiza la sesión activa del usuario después de que se cambie su contraseña, sin desconectarlo.
        login(request, user)
        return render(request, 'app_sipeip/activacion_exitosa.html')

    return render(request, 'app_sipeip/cambio_clave.html')

#Funcion que me obtiene todos los modulos que cada rol tiene acceso, para mostrar en el menú lateral
def obtener_modulos_por_usuario(usuario):
  # Aquí defines los módulos según el rol/permiso del usuario
    modulos = []
    if usuario.idrol.nombre == 'Administrador':
        modulos = [
            {
                'nombre': 'Usuarios', 
                'icono': 'fa-user',
                'submenu': [
                    {'nombre': 'Consultar', 'url': '/usuarios/'},
                    {'nombre': 'Registrar', 'url': '/registro/'},
                ]
            },
            {
             'nombre': 'Configuración Institucional', 
             'icono': 'fa-building-columns',
             'submenu': [
                    {'nombre': 'Instituciones', 'url': '/conf_institucional/'},
                    {'nombre': 'Sectores', 'url': '/conf_institucional/sectores/'},
                    {'nombre': 'Subsectores', 'url': '/conf_institucional/subsectores/'},
                ]
            },
            {
                'nombre': 'Objetivos estratégicos',
                'icono': 'fa-bullseye',
                'submenu': [
                    {'nombre': 'PND', 'url': '/objetivos/pnd/'},
                    {'nombre': 'ODS', 'url': '/objetivos/ods/'},
                    {'nombre': 'Objetivos estratégicos', 'url': '/objetivos/estrategicos/'},
                    #{'nombre': 'Alinear objetivos', 'url': '/objetivos/alinear/'},
                ]
            },
            {'nombre': 'Proyectos', 'url': '/proyectos/', 'icono': 'fa-diagram-project'},
            {'nombre': 'Reportes', 'url': '/reportes/', 'icono': 'fa-file-excel'},
            
        ]
    elif usuario.idrol.nombre == 'Tecnico':
        modulos = [
            {'nombre': 'Proyectos', 'url': '/proyectos/'},
        ]
    elif usuario.idrol.nombre == 'Reportador':
        modulos = [
            {'nombre': 'Proyectos', 'url': '/proyectos/', 'icono': 'fa-diagram-project'},
            {'nombre': 'Reportes', 'url': '/reportes/', 'icono': 'fa-file-excel'},
        ]    
    return modulos

@login_required(login_url='login')  # Redirige al login si no está autenticado
def inicio(request):
    usuario = request.user.usuario
    modulos = obtener_modulos_por_usuario(usuario)
    return render(request, 'app_sipeip/inicio.html', {'modulos': modulos})

#CRUD GESTION DE USUARIOS-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
#vista de configuracion institucional principal, donde muestra el datatable con las consultas 
@login_required
def usuarios(request):
    if request.method== 'GET':
        usuario = request.user.usuario
        modulos = obtener_modulos_por_usuario(usuario)
        usuarios = Usuario.objects.filter(estado=True)
        roles = Roles.objects.filter(estado=True)
        permisos = Permisos.objects.filter(estado=True)
        return render(request,'app_sipeip/usuarios/usuarios.html',{'usuarios': usuarios,'modulos': modulos,'roles': roles,'permisos':permisos})


#vista para modal de edicion de institucion, donde mediante el id obtiene los campos para editar
@login_required
def usuario_modi(request,idusuario):
   usuario=get_object_or_404(Usuario,pk=idusuario)
   roles = Roles.objects.filter(estado=True)
   permisos = Permisos.objects.filter(estado=True)
   
   return render(request,'app_sipeip/usuarios/modi_usuario.html',{'usuario':usuario,'roles': roles,'permisos': permisos})

#vista para post de edicion de institucion, donde mediante el id actualiza
@login_required
def usuario_modificar(request,idusuario):
     if request.method == 'POST':
        valor_deseado = request.POST.get('valor_deseado', None)
        valor_deseado2 = request.POST.get('valor_deseado2', None)
    
        if valor_deseado:
         # Realiza la verificación en la base de datos
            registro_existe = Usuario.objects.filter(identificacion=valor_deseado).exists()
            if Usuario.objects.filter(identificacion=valor_deseado,idusuario = valor_deseado2).exists():
                registro_existe= False
            return JsonResponse({'existe': registro_existe})
        else:
            print(request.POST)
            inst= get_object_or_404(Usuario,pk=idusuario)
            cedula = request.POST.get('input-cedula')
            nombres = request.POST.get('input-nombres')
            apellidos = request.POST.get('input-apellidos')
            username = request.POST.get('input-username')
            mail = request.POST.get('input-mail')
            idrol= request.POST.get('select-rol')
            idpermiso= request.POST.get('select-permisos')
            inst.identificacion = cedula
            inst.nombres = nombres
            inst.apellidos = apellidos
            #instancia de Foreign Key para guardar nuevo valor de id de llave foranea
            inst.idrol =  Roles.objects.get(pk=idrol)#instancia de Foreign Key para guardar nuevo valor de id de llave foranea
            inst.idpermiso =  Permisos.objects.get(pk=idpermiso)#instancia de Foreign Key para guardar nuevo valor de id de llave foranea
            #fin instancia
            inst.username=username
            inst.mail = mail
            inst.save()
            #hago lo mismo para la otra tabla de auth user de django
            inst2= get_object_or_404(Usuario,pk=idusuario)

            user = User.objects.get(id=inst2.user.id)
            user.username = username
            user.first_name = nombres
            user.last_name = apellidos
            user.email=mail
            user.save()
            messages.success(request, 'Los datos se han Modificado exitosamente.')
            return redirect('usuarios')

@login_required
def eliminar_usuario(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        inst = Usuario.objects.get(idusuario=id)
        inst.estado = False
        inst.save()
        inst2= get_object_or_404(Usuario,pk=id)

        user = User.objects.get(id=inst2.user.id)
        user.is_active= False
        user.save()

        messages.success(request, 'Los datos se ha eliminado exitosamente.')
        return JsonResponse({'success': True})
#FIN CRUD USUARIOS-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

#*-*-*-*-*-*-*-*-*-*-*-*CRUD CONFIGURACION INSTITUCIONAL-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
#vista de consulta de sectores
@login_required
def sectores(request):
    if request.method== 'GET':
        usuario = request.user.usuario
        modulos = obtener_modulos_por_usuario(usuario)
        sectores = InstitucionSector.objects.filter(estado=True)
        return render(request,'app_sipeip/institucional/sectores.html',{'modulos': modulos,'sectores': sectores})
    
#vista para modal de edicion de sector, donde mediante el id obtiene los campos para editar
@login_required
def sector_modi(request,idsector):
   sector=get_object_or_404(InstitucionSector,pk=idsector)
   
   return render(request,'app_sipeip/institucional/modi_sector.html',{'sector': sector})

#vista para post de edicion de Sector, donde mediante el id actualiza
@login_required
def sector_modificar(request,idsector):
     if request.method == 'POST':
        valor_deseado = request.POST.get('valor_deseado', None)
        valor_deseado2 = request.POST.get('valor_deseado2', None)
    
        if valor_deseado:
         # Realiza la verificación en la base de datos
            registro_existe = InstitucionSector.objects.filter(nombre=valor_deseado).exists()
            if InstitucionSector.objects.filter(nombre=valor_deseado,idinstitucion = valor_deseado2).exists():
                registro_existe= False
            return JsonResponse({'existe': registro_existe})
        else:
            print(request.POST)
            inst= get_object_or_404(InstitucionSector,pk=idsector)
            nombre = request.POST.get('input-nombre')
            
            inst.nombre = nombre
            inst.save()
            messages.success(request, 'Los datos se han Modificado exitosamente.')
            return redirect('sectores')

#AGREGAR NUEVO SECTOR 
@login_required
def sector_agregar(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')

        if not (nombre):
            return JsonResponse({'success': False, 'error': 'Todos los campos son requeridos.'})

        try:
            
            nueva = InstitucionSector(
               
                nombre=nombre.upper(),
                estado=True,
            )
            nueva.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

#elimina el sector seleccionado, lo cambia aestado false
@login_required
def eliminar_sector(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        inst = InstitucionSector.objects.get(idsector=id)
        inst.estado = False
        inst.save()
        messages.success(request, 'Los datos se ha eliminado exitosamente.')
        return JsonResponse({'success': True})

#vista de Subsectores principal, donde muestra el datatable con las consultas 
@login_required
def subsectores(request):
    if request.method== 'GET':
        usuario = request.user.usuario
        modulos = obtener_modulos_por_usuario(usuario)
        subsectores = InstitucionSubsector.objects.filter(estado=True)
        sectores = InstitucionSector.objects.filter(estado=True)
        return render(request,'app_sipeip/institucional/subsectores.html',{'subsectores': subsectores,'modulos': modulos,'sectores': sectores})


#vista para modal de edicion de Subsector, donde mediante el id obtiene los campos para editar
@login_required
def subsector_modi(request,idsubsector):
   subsector=get_object_or_404(InstitucionSubsector,pk=idsubsector)
   sectores = InstitucionSector.objects.filter(estado=True)
   
   return render(request,'app_sipeip/institucional/modi_subsector.html',{'subsector':subsector,'sectores': sectores})

#vista para post de edicion de subsectores, donde mediante el id actualiza
@login_required
def subsector_modificar(request,idsubsector):
     if request.method == 'POST':
        valor_deseado = request.POST.get('valor_deseado', None)
        valor_deseado2 = request.POST.get('valor_deseado2', None)
    
        if valor_deseado:
         # Realiza la verificación en la base de datos
            registro_existe = InstitucionSubsector.objects.filter(nombre=valor_deseado).exists()
            if InstitucionSubsector.objects.filter(nombre=valor_deseado,idsubsector = valor_deseado2).exists():
                registro_existe= False
            return JsonResponse({'existe': registro_existe})
        else:
            print(request.POST)
            inst= get_object_or_404(InstitucionSubsector,pk=idsubsector)
            nombre = request.POST.get('input-nombre')
            idsect= request.POST.get('select-sect')
            inst.nombre = nombre
            #instancia de Foreign Key para guardar nuevo valor de id de llave foranea
            inst.idsector =  InstitucionSector.objects.get(pk=idsect)#instancia de Foreign Key para guardar nuevo valor de id de llave foranea
            #fin instancia
            inst.save()
            messages.success(request, 'Los datos se han Modificado exitosamente.')
            return redirect('subsectores')
@login_required
def eliminar_subsector(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        inst = InstitucionSubsector.objects.get(idsubsector=id)
        inst.estado = False
        inst.save()
        messages.success(request, 'Los datos se ha eliminado exitosamente.')
        return JsonResponse({'success': True})

#AGREGAR NUEVO SUBSECTOR  
@login_required
def subsector_agregar(request):
    if request.method == 'POST':
        idsector = request.POST.get('sector')
        nombre = request.POST.get('nombre')
        if not (idsector and nombre):
            return JsonResponse({'success': False, 'error': 'Todos los campos son requeridos.'})

        try:
            #instancia de Foreign Key para guardar nuevo valor de id de llave foranea
            sector_obj = InstitucionSector.objects.get(pk=idsector)
            #Fin Instancia
            nueva = InstitucionSubsector(
                idsector=sector_obj,
                nombre=nombre.upper(),
                estado=True,
            )
            nueva.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

#vista de configuracion institucional principal, donde muestra el datatable con las consultas 
@login_required
def conf_institucional(request):
    if request.method== 'GET':
        usuario = request.user.usuario
        modulos = obtener_modulos_por_usuario(usuario)
        instituciones = Instituciones.objects.filter(estado=True)
        sectores = InstitucionSector.objects.filter(estado=True)
        return render(request,'app_sipeip/institucional/conf_institucional.html',{'instituciones': instituciones,'modulos': modulos,'sectores': sectores})


#vista para modal de edicion de institucion, donde mediante el id obtiene los campos para editar
@login_required
def institucion_modi(request,idinstitucion):
   institucion=get_object_or_404(Instituciones,pk=idinstitucion)
   print(institucion.idsubsector.idsubsector)
   sectores = InstitucionSector.objects.filter(estado=True)
   subsectores = InstitucionSubsector.objects.filter(estado=True)
   
   return render(request,'app_sipeip/institucional/modi_institucion.html',{'institucion':institucion,'sectores': sectores,'subsectores': subsectores})

#vista para post de edicion de institucion, donde mediante el id actualiza
@login_required
def institucion_modificar(request,idinstitucion):
     if request.method == 'POST':
        valor_deseado = request.POST.get('valor_deseado', None)
        valor_deseado2 = request.POST.get('valor_deseado2', None)
    
        if valor_deseado:
         # Realiza la verificación en la base de datos
            registro_existe = Instituciones.objects.filter(nombre=valor_deseado).exists()
            if Instituciones.objects.filter(nombre=valor_deseado,idinstitucion = valor_deseado2).exists():
                registro_existe= False
            return JsonResponse({'existe': registro_existe})
        else:
            print(request.POST)
            inst= get_object_or_404(Instituciones,pk=idinstitucion)
            nombre = request.POST.get('input-nombre')
            idsect= request.POST.get('hselect-sect')
            idsubsect= request.POST.get('hselect-subsect')
            nivelGob= request.POST.get('hselect-nivelgobierno').upper()
            inst.nombre = nombre
            inst.idsector = idsect
            #instancia de Foreign Key para guardar nuevo valor de id de llave foranea
            inst.idsubsector =  InstitucionSubsector.objects.get(pk=idsubsect)#instancia de Foreign Key para guardar nuevo valor de id de llave foranea
            #fin instancia
            inst.nivelgobierno=nivelGob
            inst.fechaactualizacion = datetime.now()
            inst.save()
            messages.success(request, 'Los datos se han Modificado exitosamente.')
            return redirect('conf_institucional')

#vista que me consulta los subsectores relacionados al sector seleccionado.
@login_required
def obtener_subsectores(request):
    idsector = request.GET.get('idsector')
    subsectores = InstitucionSubsector.objects.filter(idsector=idsector, estado=True).values('idsubsector', 'nombre')
    return JsonResponse(list(subsectores), safe=False)

@login_required
def eliminar_institucion(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        inst = Instituciones.objects.get(idinstitucion=id)
        inst.estado = False
        inst.save()
        messages.success(request, 'Los datos se ha eliminado exitosamente.')
        return JsonResponse({'success': True})

#AGREGAR NUEVA INSTITUCION  
@login_required
def institucion_agregar(request):
    if request.method == 'POST':
        idsector = request.POST.get('sector')
        idsubsector = request.POST.get('subsector')
        nombre = request.POST.get('nombre')
        nivelgobierno = request.POST.get('nivelgobierno')

        if not (idsector and idsubsector and nombre and nivelgobierno):
            return JsonResponse({'success': False, 'error': 'Todos los campos son requeridos.'})

        try:
            #instancia de Foreign Key para guardar nuevo valor de id de llave foranea
            subsector_obj = InstitucionSubsector.objects.get(pk=idsubsector)
            #Fin Instancia
            nueva = Instituciones(
                idsector=idsector,
                idsubsector=subsector_obj,
                nombre=nombre.upper(),
                nivelgobierno=nivelgobierno.upper(),
                estado=True,
                fechacreacion=timezone.now()
            )
            nueva.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})
#*-*-*-*-*-*-*-*-*-*-*-*FIN CRUD CONFIGURACION INSTITUCIONAL-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

#*-*-*-*-*-*-*-*-*-*-*-*OBJETIVOS ESTRATEGICOS-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
@login_required
def objetivo_estrategico_list(request):
    usuario = request.user.usuario
    modulos = obtener_modulos_por_usuario(usuario)
    objetivos = ObjetivoEstrategico.objects.select_related('idpnd').all()
    pn_desarrollos = PlanNacionalDesarrollo.objects.filter(estado=True)
    ods_list = ObjetivosDesarrolloSostenible.objects.filter(estado=True).order_by('numeroods')
    return render(request, 'app_sipeip/objetivos/estrategico_list.html', {'modulos': modulos,'objetivos': objetivos,'pn_desarrollos': pn_desarrollos,'ods_list': ods_list})

#AGREGAR OBJETIVOS ESTRATEGICOS
@login_required
def objetivo_estrategico_agregar(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').upper()
        descripcion = request.POST.get('descripcion', '').upper()
        idpnd = request.POST.get('idpnd')
        ods_list = request.POST.getlist('ods[]')  # JS enviará como array
        user = request.user

        if not nombre or not descripcion or not idpnd or not ods_list:
            return JsonResponse({'success': False, 'error': 'Todos los campos son requeridos.'})

        try:
            pnd = PlanNacionalDesarrollo.objects.get(pk=idpnd)
            objetivo = ObjetivoEstrategico.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                idpnd=pnd,
                fecharegistro=timezone.now(),
                estado=True
            )
            # Guardar alineación ODS
            for idods in ods_list:
                ods_obj = ObjetivosDesarrolloSostenible.objects.get(pk=idods)
                AlineacionObjetivoOds.objects.create(idobjest=objetivo, idods=ods_obj)
            # Guardar historial
            ObjetivoEstrategicoHistory.objects.create(
                idobjest=objetivo,
                nombre=nombre,
                descripcion=descripcion,
                fechainicio=timezone.now(),
                numversion=1,
                cambiadoporusr=user.usuario.idusuario if hasattr(user, 'usuario') else None,
                fechacambio=timezone.now(),
                idpnd=idpnd
            )
            return JsonResponse({'success': True})
        except Exception as e:
            print('Error '+str(e))
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})
#obtener ODS alineados Al objetivo estrategico seleccionado
@login_required
def objetivo_estrategico_ods(request):
    idobjest = request.GET.get('idobjest')
    ods_ids = list(AlineacionObjetivoOds.objects.filter(idobjest=idobjest).values_list('idods', flat=True))
    return JsonResponse({'ods': ods_ids})
#OBTENER TODOS LOS ODS ACTIVOS 
@login_required
def objetivo_ods_list(request):
    usuario = request.user.usuario
    modulos = obtener_modulos_por_usuario(usuario)
    ods = ObjetivosDesarrolloSostenible.objects.filter(estado=True).order_by('numeroods')

    return render(request, 'app_sipeip/objetivos/ods_list.html', {'modulos': modulos,'odss': ods})

#AGREGAR NUEVO ODS
def ods_agregar(request):
    if request.method == 'POST':
        numeroods = request.POST.get('numeroods')
        nombre = request.POST.get('nombre', '').upper()
        estado = request.POST.get('estado') == 'True'
        imagen = request.FILES.get('imagen')

        ods = ObjetivosDesarrolloSostenible(
            numeroods=numeroods,
            nombre=nombre,
            estado=estado
        )
        if imagen:
            ods.imagen = imagen  # Si usas ImageField, asegúrate de tener configurado MEDIA_ROOT y MEDIA_URL

        ods.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

#Eliminar ods
def ods_eliminar(request):
    if request.method == 'POST':
        idods = request.POST.get('idods')
        try:
            ods = ObjetivosDesarrolloSostenible.objects.get(pk=idods)
            ods.estado = False
            ods.save()
            return JsonResponse({'success': True})
        except ObjetivosDesarrolloSostenible.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'ODS no encontrado'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})
#editar ods
def ods_editar(request):
    if request.method == 'POST':
        idods = request.POST.get('idods')
        numeroods = request.POST.get('numeroods')
        nombre = request.POST.get('nombre', '').upper()
        imagen = request.POST.get('imagen', '')  # Aquí se guarda la URL
        estado = request.POST.get('estado') == 'True'

        try:
            ods = ObjetivosDesarrolloSostenible.objects.get(pk=idods)
            ods.numeroods = numeroods
            ods.nombre = nombre
            ods.imagen = imagen
            ods.estado = estado
            ods.save()
            return JsonResponse({'success': True})
        except ObjetivosDesarrolloSostenible.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'ODS no encontrado'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})




#OBTENER TODOS LOS PND ACTIVOS 
@login_required
def objetivo_pnd_list(request):
    usuario = request.user.usuario
    modulos = obtener_modulos_por_usuario(usuario)
    pnd = PlanNacionalDesarrollo.objects.filter(estado=True)

    return render(request, 'app_sipeip/objetivos/pnd_list.html', {'modulos': modulos,'pnds': pnd})

#AGREGAR NUEVO pnd
def pnd_agregar(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').upper()
        estado = request.POST.get('estado') == 'True'

        pnd = PlanNacionalDesarrollo(
            nombreeje=nombre,
            estado=estado
        )
        pnd.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

#Eliminar pnd
def pnd_eliminar(request):
    if request.method == 'POST':
        idpnd = request.POST.get('idpnd')
        try:
            pnd = PlanNacionalDesarrollo.objects.get(pk=idpnd)
            pnd.estado = False
            pnd.save()
            return JsonResponse({'success': True})
        except PlanNacionalDesarrollo.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'PND no encontrado'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})
#editar pnd
def pnd_editar(request):
    if request.method == 'POST':
        idpnd = request.POST.get('idpnd')
        nombre = request.POST.get('nombre', '').upper()
        estado = request.POST.get('estado') == 'True'

        try:
            ods = PlanNacionalDesarrollo.objects.get(pk=idpnd)
            ods.nombreeje = nombre
            ods.estado = estado
            ods.save()
            return JsonResponse({'success': True})
        except PlanNacionalDesarrollo.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'PND no encontrado'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})
#vista para enviar edicion de objetivo estrategico
@login_required
def objetivo_estrategico_edit(request):
    if request.method == 'POST':
        idobjest = request.POST.get('idobjest')
        nombre = request.POST.get('nombre', '').upper()
        descripcion = request.POST.get('descripcion', '').upper()
        idpnd = request.POST.get('idpnd')
        ods_list = request.POST.getlist('ods[]')
        user = request.user

        if not idobjest or not nombre or not descripcion or not idpnd or not ods_list:
            return JsonResponse({'success': False, 'error': 'Todos los campos son requeridos.'})

        try:
            objetivo = ObjetivoEstrategico.objects.get(pk=idobjest)
            pnd = PlanNacionalDesarrollo.objects.get(pk=idpnd)

            # Actualiza campos
            objetivo.nombre = nombre
            objetivo.descripcion = descripcion
            objetivo.idpnd = pnd
            objetivo.save()

            # Actualizar ODS alineados
            AlineacionObjetivoOds.objects.filter(idobjest=objetivo).delete()
            for idods in ods_list:
                ods_obj = ObjetivosDesarrolloSostenible.objects.get(pk=idods)
                AlineacionObjetivoOds.objects.create(idobjest=objetivo, idods=ods_obj)

            # Guardar versión en historial
            versiones = ObjetivoEstrategicoHistory.objects.filter(idobjest=objetivo).count()
            ObjetivoEstrategicoHistory.objects.create(
                idobjest=objetivo,
                nombre=nombre,
                descripcion=descripcion,
                fechainicio=timezone.now(),
                numversion=versiones + 1,
                cambiadoporusr=user.usuario.idusuario if hasattr(user, 'usuario') else None,
                fechacambio=timezone.now(),
                idpnd=idpnd
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

#historial de objetivos estrategicos
@login_required
def objetivo_estrategico_history(request):
    idobjest = request.GET.get('idobjest')
    historial = ObjetivoEstrategicoHistory.objects.filter(idobjest=idobjest).order_by('-numversion')
    history_list = []
    for h in historial:
        # Obtener usuario si existe
        usuario = Usuario.objects.filter(idusuario=h.cambiadoporusr).first()
        nombre_usuario = f"{usuario.nombres} {usuario.apellidos}" if usuario else ''
        # Obtener nombre PND si existe
        pnd = PlanNacionalDesarrollo.objects.filter(idpnd=h.idpnd).first()
        nombre_pnd = pnd.nombreeje if pnd else ''
        history_list.append({
            'numversion': h.numversion,
            'nombre': h.nombre,
            'descripcion': h.descripcion,
            'fechacambio': h.fechacambio.strftime('%d/%m/%Y %H:%M') if h.fechacambio else '',
            'usuario': nombre_usuario,
            'pnd': nombre_pnd
        })
    return JsonResponse({'success': True, 'historial': history_list})

#eliminar objetivos estrategicos

@login_required
def objetivo_estrategico_delete(request):
    if request.method == 'POST':
        idobjest = request.POST.get('idobjest')
        try:
            objetivo = ObjetivoEstrategico.objects.get(pk=idobjest)
            objetivo.estado = False
            objetivo.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

#*-*-*-*-*-*-*-*-*-*-*-*FIN OBJETIVOS ESTRATEGICOS-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

#*-*-*-*-*-*-*-*-*-*-*-*MODULOS PROYECTOS DE INVERSION-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
@login_required
def proyectos_list(request):
    usuario = request.user.usuario
    modulos = obtener_modulos_por_usuario(usuario)
    #La función select_related en Django es un método de optimización de consultas en el ORM. 
    #select_related hace una "JOIN" en la base de datos y trae todo junto en una sola consulta, para que no haga consultas extra después
    #esto Optimiza el acceso a relaciones y mejora el rendimiento en listados complejos.
    proyectos = Proyectos.objects.select_related('idinstitucion', 'idobjest', 'idug','idiambiental', 'idprograma','idmeta').filter(estado=True)

    return render(request, 'app_sipeip/proyectos/proyectos_list.html', {'modulos': modulos,'proyectos': proyectos})

@login_required
def proyecto_registrar(request):
    if request.method == 'POST':
        # Campos principales del proyecto
        nombre = request.POST.get('nombre').upper()
        impacto_ambiental = request.POST.get('impacto_ambiental')
        idinstitucion = request.POST.get('institucion')
        situacion_actual = request.POST.get('situacion_actual')
        justificacion = request.POST.get('justificacion')
        beneficiarios = request.POST.get('beneficiarios')
        proyectos_relacionados = request.POST.get('proyectos_relacionados')
        #idplan = request.POST.get('plan')
        idobjest = request.POST.get('objetivo')
        idmeta = request.POST.get('meta')
        # Calcular total inversión
        # Serializados
        actividades = json.loads(request.POST.get('actividades_json', '[]'))
        fuentes = json.loads(request.POST.get('fuentes_json', '[]'))
        total_inversion = sum(float(f['monto']) for f in fuentes) if fuentes else 0
        duracion_proyecto = request.POST.get('duracion_proyecto')
        autogestion = request.POST.get('autogestion')
        idprograma = request.POST.get('programa')
        sostenibilidad = request.POST.get('sostenibilidad')

        idusuario_resp = request.POST.get('usuario_responsable')
        provincia = request.POST.get('provincia')
        canton = request.POST.get('canton')
        parroquia = request.POST.get('parroquia')
        coordenadas = request.POST.get('coordenadas')

        
       
        # 1. Creamos UG
        ug=ProyectoUbiGeografica.objects.create(
            coordenadas=coordenadas,
            idparroquia_id=parroquia
        )
        # 1. Crear el proyecto principal
        proyecto = Proyectos.objects.create(
            nombre=nombre,
            idiambiental_id=impacto_ambiental,
            idinstitucion_id=idinstitucion,
            idug=ug,
            situacionactual=situacion_actual,
            justificacion=justificacion,
            beneficiarios=beneficiarios,
            proyectosrelacionados=proyectos_relacionados,
            idobjest_id=idobjest,
            idmeta_id=idmeta,
            inversion=total_inversion,
            duracionproyecto = duracion_proyecto,
            autogestion=autogestion,
            idprograma_id=idprograma,
            sostenibilidad=sostenibilidad,
            estado=True
        )

        # 2. Guardar fuentes de financiamiento
        for f in fuentes:
            FinanciamientoProyecto.objects.create(
                idproyecto=proyecto,
                fuente=f['fuenteTxt'],
                monto=f['monto'],
                observaciones=f['obs']
            )

        # 3. Guardar actividades y periodos
        for act in actividades:
            actividad = ActividadesProyecto.objects.create(
                nombre=act['nombre'],
                idproyecto=proyecto,
                estado=True
            )
            for periodo in act['periodos']:
                PeriodoActividad.objects.create(
                    nombre=periodo['nombre'],
                    valor=periodo['valor'],
                    idactividad=actividad,
                    estado=True
                )
        #actualizamos el responsable de la meta
        meta = Metas.objects.get(pk=idmeta)

        # Actualiza campos meta, asigna el responsable
        meta.nombre = nombre
        meta.idusuario =  Usuario.objects.get(pk=idusuario_resp)
        meta.save()
        # Aquí puedes agregar guardado de cronograma, etc.

        # Mensaje de éxito
        messages.success(request, "Proyecto registrado correctamente.")
        return redirect('proyectos_list')  # O donde prefieras
    if request.method == 'GET':
        usuario = request.user.usuario
        modulos = obtener_modulos_por_usuario(usuario)
        instituciones = Instituciones.objects.filter(estado=True)
        objetivos = ObjetivoEstrategico.objects.filter(estado=True)
        programas = Programas.objects.filter(estado=True)
        planes = Planes.objects.filter(estado=True)
        provincias = Provincias.objects.all()
        cantones = Cantones.objects.all()
        parroquias = Parroquias.objects.all()
        metas = Metas.objects.filter(estado=True)
        usuarios = Usuario.objects.filter(estado=True,idrol=2)
        # fuentes de financiamiento
        FUENTES_FINANCIAMIENTO = [
        {'id': 1, 'nombre': 'Gobierno Central'},
        {'id': 2, 'nombre': 'Gobiernos Autónomos Descentralizados'},
        {'id': 3, 'nombre': 'Cooperación Internacional'},
        {'id': 4, 'nombre': 'Autogestión'},
        {'id': 5, 'nombre': 'Otros'}
        ]
        impactos = ProyectoImpactoAmbiental.objects.filter(estado=True)
        return render(request, 'app_sipeip/proyectos/proyecto_registrar.html', {'modulos': modulos,'instituciones': instituciones,'objetivos': objetivos,
            'programas': programas,'planes': planes,'provincias': provincias,'cantones': cantones,'parroquias': parroquias,'metas': metas,
            'usuarios': usuarios,'fuentes': FUENTES_FINANCIAMIENTO,'impactos': impactos,})


#Vista AJAX para cargar programas por plan
@login_required
def programas_por_plan(request):
    idplan = request.GET.get('idplan')
    programas = Programas.objects.filter(idplan=idplan, estado=True).values('idprograma', 'nombre')
    return JsonResponse(list(programas), safe=False)

#AJAX para cascada de cantones y parroquias
@login_required
def cantones_por_provincia(request):
    idprovincia = request.GET.get('idprovincia')
    cantones = Cantones.objects.filter(idprovincia=idprovincia).values('idcanton', 'nombre')
    return JsonResponse(list(cantones), safe=False)

#AJAX para cascada de cantones y parroquias
@login_required
def parroquias_por_canton(request):
    idcanton = request.GET.get('idcanton')
    parroquias = Parroquias.objects.filter(idcanton=idcanton).values('idparroquia', 'nombre')
    return JsonResponse(list(parroquias), safe=False)

#Vista AJAX para descripción del impacto ambiental
@login_required
def info_impacto_ambiental(request):
    idambiental = request.GET.get('idambiental')
    try:
        impacto = ProyectoImpactoAmbiental.objects.get(pk=idambiental)
        descripcion = impacto.descripcion or "Sin descripción."
        return JsonResponse({'descripcion': descripcion})
    except ProyectoImpactoAmbiental.DoesNotExist:
        return JsonResponse({'descripcion': 'No encontrado'})
#Vista AJAX para enviar info del objetivo seleccionado
@login_required
def info_objetivo_estrategico(request):
    idobj = request.GET.get('idobjest')
    objetivo = ObjetivoEstrategico.objects.select_related('idpnd').get(pk=idobj)
    pnd = objetivo.idpnd

    # Define los colores según el ID del PND
    colores = {
        1: '#704e9a',
        2: '#008781',
        3: '#408ac9',
        4: '#3d2f6d',
        5: '#f9b43d'
    }
    color_pnd = colores.get(pnd.idpnd, '#704e9a')

    # Trae los ODS alineados
    ods_list = []
    for alineacion in AlineacionObjetivoOds.objects.filter(idobjest=idobj):
        ods = alineacion.idods
        ods_list.append({
            'numero': ods.numeroods,
            'nombre': ods.nombre,
            'imagen': ods.imagen 
        })

    return JsonResponse({
        'pnd': pnd.nombreeje,
        'color': color_pnd,
        'objetivo': objetivo.nombre,
        'descripcion': objetivo.descripcion,
        'ods': ods_list
    })
#Vista AJAX para obtener indicador de la meta
@login_required
def info_meta(request):
    idmeta = request.GET.get('idmeta')
    try:
        meta = Metas.objects.get(pk=idmeta)
        indicador = meta.idindicador.nombre +' '+meta.idindicador.formula if meta.idindicador else 'Sin indicador asociado'
        return JsonResponse({'indicador': indicador})
    except Metas.DoesNotExist:
        return JsonResponse({'indicador': 'No encontrado'})

#Vista AJAX en Django para traer todo el detalle del Proyecto
@login_required
def proyecto_detalle(request):
    idproyecto = request.GET.get('idproyecto')
    try:
        proyecto = Proyectos.objects.select_related('idprograma','idinstitucion','idiambiental','idobjest','idug').get(pk=idproyecto)
        ubicacion = proyecto.idug
        financiaciones = list(FinanciamientoProyecto.objects.filter(idproyecto=proyecto).values('fuente','monto','observaciones'))
        actividades = []
        for act in ActividadesProyecto.objects.filter(idproyecto=proyecto):
            periodos = list(PeriodoActividad.objects.filter(idactividad=act).values('nombre','valor'))
            actividades.append({'nombre': act.nombre, 'periodos': periodos})
        # Objetivo estratégico + PND + ODS alineados
        obj = proyecto.idobjest
        pnd = obj.idpnd
        colores = {1:'#704e9a',2:'#008781',3:'#408ac9',4:'#3d2f6d',5:'#f9b43d'}
        color_pnd = colores.get(pnd.idpnd, '#704e9a')
        ods_imgs = []
        for alineacion in AlineacionObjetivoOds.objects.filter(idobjest=obj.idobjest):
            ods = alineacion.idods
            ods_imgs.append({'numero': ods.numeroods, 'nombre': ods.nombre, 'imagen': ods.imagen})
        return JsonResponse({
            'success': True,
            'proyecto': {
                'nombre': proyecto.nombre,
                'institucion': proyecto.idinstitucion.nombre,
                'programa': proyecto.idprograma.nombre if proyecto.idprograma else '',
                'impacto': proyecto.idiambiental.nombre if proyecto.idiambiental else '',
                'autogestion': proyecto.autogestion,
                'sostenibilidad': proyecto.sostenibilidad,
                'objetivo': obj.nombre,
                'objetivo_desc': obj.descripcion,
                'pnd': pnd.nombreeje,
                'color_pnd': color_pnd,
                'ods_imgs': ods_imgs,
                'meta': proyecto.idmeta.nombre if proyecto.idmeta else '',
                'usuario_responsable': proyecto.idmeta.idusuario.nombres if proyecto.idmeta and proyecto.idmeta.idusuario else '',
                'provincia': ubicacion.idparroquia.idcanton.idprovincia.nombre if ubicacion and ubicacion.idparroquia.idcanton.idprovincia else '',
                'canton':  ubicacion.idparroquia.idcanton.nombre if ubicacion and ubicacion.idparroquia.idcanton else '',
                'parroquia': ubicacion.idparroquia.nombre if ubicacion and ubicacion.idparroquia else '',
                'coordenadas': ubicacion.coordenadas if ubicacion else '',
            },
            'financiaciones': financiaciones,
            'actividades': actividades,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

#*-*-*-*-*-*-*-*-*-*-*-*FIN MODULOS PROYECTOS DE INVERSION-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

@never_cache
def login_view(request):
    #si ya se encuentra autenticado, redirecciona al inicio
    if request.user.is_authenticated:
        return redirect('inicio')
    
    if request.method== 'GET':
     if 'next' in request.GET:
        messages.warning(request, 'Tu sesión ha expirado. Por favor, inicia sesión nuevamente.')
     return render(request, 'app_sipeip/login.html')
    #return render(request,'login.html',{'form': UserCreationForm})
    if request.method == 'POST':
        user = authenticate(request, username= request.POST['username'], password= request.POST['password'])
        if user is None:
            return render(request,'app_sipeip/login.html',{'error': 'Username o password incorrecto'})
        else:
            logout(request)
            login(request, user) #Aquí guarda la sesión en la cookie del navegador
           
            return redirect('inicio')
        
def logout_view(request):
    logout(request)    
    return redirect('login')       