from django.test import TestCase
from app_sipeip.models import Instituciones, InstitucionSubsector

class InstitucionesModelTest(TestCase):
    def setUp(self):
        self.subsector = InstitucionSubsector.objects.create(nombre="subsector", estado=True)

    def test_nombre_se_guarda_en_mayusculas(self):
        inst = Instituciones(
            idsector=1,
            idsubsector=self.subsector,
            nombre="ministerio de cultura",
            nivelgobierno="nacional",
            estado=True,
            fechacreacion="2024-01-01"
        )
        inst.save()
        self.assertEqual(inst.nombre, "MINISTERIO DE CULTURA")
        self.assertEqual(inst.nivelgobierno, "NACIONAL")
