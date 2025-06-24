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

        # 1. Generar contraseña temporal
        temp_password = get_random_string(length=10)

        # 2. Crear usuario desactivado
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(temp_password),
            is_active=False
        )

        # 3. Crear registro en tabla usuario
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

        # 4. Generar token de activación válido por 2 días
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = request.build_absolute_uri(
            reverse('activar_cuenta', kwargs={'uidb64': uid, 'token': token})
        )

        # 5. Enviar email
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

def hello(request):
    return HttpResponse("Hola Mundo")

@never_cache
def login_view(request):
    

    if request.method== 'GET':

     return render(request, 'app_sipeip/login.html')
    #return render(request,'login.html',{'form': UserCreationForm})
    else:
        user = authenticate(request, username= request.POST['username'], password= request.POST['password'])
        if user is None:
            return render(request,'app_sipeip/login.html',{'error': 'Username o password incorrecto'})
        else:
            logout(request)
            login(request, user) #Aquí guarda la sesión en la cookie del navegador
           
            return redirect('cons_arch')