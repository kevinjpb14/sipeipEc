from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class RegistroUsuarioTest(TestCase):
    def test_registro_usuario_post(self):
        response = self.client.post(reverse('registrar_usuario'), {
            'username': 'prueba',
            'email': 'prueba@test.com',
            'nombres': 'Kevin',
            'apellidos': 'Paz',
            'identificacion': '0101010101',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='prueba').exists())
