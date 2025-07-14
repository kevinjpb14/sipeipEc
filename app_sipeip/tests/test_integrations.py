from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User

class RegistroIntegracionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='kevin14', password='admin')
        self.client.login(username='kevin14', password='admin')
    def test_flujo_completo_registro_envio_email(self):
        response = self.client.post(reverse('registro'), {
            'username': 'kevinp',
            'email': 'kevin@ejemplo.com',
            'nombres': 'Kevin',
            'apellidos': 'Paz',
            'identificacion': '1234567890',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Activación de cuenta SIPEIP+', mail.outbox[0].subject)
