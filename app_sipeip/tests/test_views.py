from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from django.contrib.auth.models import User

class RegistroUsuarioTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='kevin14', password='admin')
        self.client.login(username='kevin14', password='admin')

    def test_registro_usuario_post(self):
        response = self.client.post(reverse('registro'), {
            'username': 'prueba',
            'email': 'prueba@test.com',
            'nombres': 'Kevin',
            'apellidos': 'Paz',
            'identificacion': '0101010101',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='prueba').exists())
