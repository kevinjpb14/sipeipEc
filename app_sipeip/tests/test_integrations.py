from django.test import TestCase
from django.urls import reverse
from django.core import mail

class RegistroIntegracionTest(TestCase):
    def test_flujo_completo_registro_envio_email(self):
        response = self.client.post(reverse('registrar_usuario'), {
            'username': 'kevinp',
            'email': 'kevin@ejemplo.com',
            'nombres': 'Kevin',
            'apellidos': 'Paz',
            'identificacion': '1234567890',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Activación de cuenta SIPEIP+', mail.outbox[0].subject)
