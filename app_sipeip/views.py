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
from .models import Instituciones,InstitucionSector,InstitucionSubsector
from django.http import JsonResponse
from datetime import datetime

@login_required(login_url='login')  # Redirige al login si no está autenticado
def registrar_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        identificacion = request.POST.get('identificacion')

        if User.objects.filter(username=username).exists():
            return render(request, 'app_sipeip/registro.html', {'error': 'El usuario ya existe'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'app_sipeip/registro.html', {'error': 'El correo ya se encuentra registrado'})

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

        return render(request, 'app_sipeip/registro_exitoso.html')

    return render(request, 'app_sipeip/registro.html')

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
        usuario.save(update_fields=['estado'])

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
            {'nombre': 'Usuarios', 'url': '/usuarios/', 'icono': 'fa-user'},
            {
             'nombre': 'Configuración Institucional', 
             'icono': 'fa-building-columns',
             'submenu': [
                    {'nombre': 'Instituciones', 'url': '/conf_institucional/'},
                    {'nombre': 'Sectores', 'url': '/conf_institucional/sectores/'},
                    {'nombre': 'Subsectores', 'url': '/conf_institucional/subsectores/'},
                ]
            },
            {'nombre': 'Proyectos', 'url': '/proyectos/', 'icono': 'fa-diagram-project'},
            {'nombre': 'Reportes', 'url': '/reportes/', 'icono': 'fa-file-excel'},
            {
                'nombre': 'Objetivos estratégicos',
                'icono': 'fa-bullseye',
                'submenu': [
                    {'nombre': 'PND', 'url': '/objetivos/pnd/'},
                    {'nombre': 'ODS', 'url': '/objetivos/ods/'},
                    {'nombre': 'Objetivos estratégicos', 'url': '/objetivos/estrategicos/'},
                    {'nombre': 'Alinear objetivos', 'url': '/objetivos/alinear/'},
                ]
            },
        ]
    elif usuario.idrol.nombre == 'Tecnico':
        modulos = [
            {'nombre': 'Proyectos', 'url': '/proyectos/'},
        ]
    return modulos

@login_required(login_url='login')  # Redirige al login si no está autenticado
def inicio(request):
    usuario = request.user.usuario
    modulos = obtener_modulos_por_usuario(usuario)
    return render(request, 'app_sipeip/inicio.html', {'modulos': modulos})

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

#vista para post de edicion de institucion, donde mediante el id actualiza
@login_required
def sector_modificar(request,idsector):
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
            inst= get_object_or_404(InstitucionSector,pk=idsector)
            nombre = request.POST.get('input-nombre')
            
            inst.nombre = nombre
            inst.save()
            messages.success(request, 'Los datos se han Modificado exitosamente.')
            return redirect('sectores')

#AGREGAR NUEVA INSTITUCION  
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
   sectores = InstitucionSector.objects.all()
   subsectores = InstitucionSubsector.objects.all()
   
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