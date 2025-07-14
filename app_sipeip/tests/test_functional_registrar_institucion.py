from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from django.contrib.auth.models import User
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app_sipeip.models import Usuario, Roles, InstitucionSector,InstitucionSubsector

class RegistrarInstitucionFuncionalTest(LiveServerTestCase):
    def setUp(self):
        # Usa Chrome WebDriver con WebDriverManager
        self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        # Si tu vista requiere login, crea usuario de prueba y loguea aquí
        self.user = User.objects.create_user(username='kevin', password='admin')
        # Rol requerido para el usuario
        self.rol = Roles.objects.create(nombre="Administrador", estado=True)
            # Usuario personalizado vinculado al user de Django
        self.usuario = Usuario.objects.create(
        user=self.user,
        username='kevin',
        nombres="Test",
        apellidos="User",
        estado=True,
        idrol=self.rol
    )

        # Sector requerido por la vista
        self.sector = InstitucionSector.objects.create(nombre="Sector Test", estado=True)
        self.subsector = InstitucionSubsector.objects.create(idsector=self.sector,nombre="SubSector Test", estado=True)

        self.client.login(username='kevin', password='admin')

    def tearDown(self):
        self.browser.quit()

    def test_registrar_institucion(self):
        # 1. Ir a login
        self.browser.get(self.live_server_url + '/login/')  # Cambia la URL si tu login es diferente

        # 2. Completamos el formulario de login
        self.browser.find_element(By.NAME, "username").send_keys('kevin')
        self.browser.find_element(By.NAME, "password").send_keys('admin')
        self.browser.find_element(By.CSS_SELECTOR, "form button[type=submit]").click()
        


        # 1. Esperamos y hacemos click en "Configuración Institucional" para desplegar el submenú
        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@data-bs-toggle="collapse" and @href="#submenu2"]'))
        )
        configuracion_link = self.browser.find_element(By.XPATH, '//a[@data-bs-toggle="collapse" and @href="#submenu2"]')
        configuracion_link.click()

        # 2. Esperamos y hacemos click en "Instituciones" dentro del submenú
        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Instituciones"))
        )
        instituciones_link = self.browser.find_element(By.LINK_TEXT, "Instituciones")
        instituciones_link.click()

        # 3. Esperamos el botón de agregar institución y continuamos con el flujo normal
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-bs-target="#modalAgregarInstitucion"]'))
        )
        #print(self.browser.current_url)
        #print(self.browser.page_source)
        # clic en el botón que abre el modal
        agregar_btn = self.browser.find_element(By.CSS_SELECTOR, 'button[data-bs-target="#modalAgregarInstitucion"]')
        agregar_btn.click()

        # Esperamos que el modal aparezca y el campo 'nombre' esté visible
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.ID, "agregar-nombre"))
        )

        # Completamos el formulario
        self.browser.find_element(By.NAME, "nombre").send_keys("Instituto Nacional de Prueba")
        # Selecciona 'NACIONAL' en el select
        select_nivel = self.browser.find_element(By.NAME, "nivelgobierno")
        for option in select_nivel.find_elements(By.TAG_NAME, "option"):
            if option.text == "NACIONAL":
                option.click()
                break
       
        
        # Selecciona 'Sector Test' en el select
        select_sector = self.browser.find_element(By.NAME, "sector")
        for option in select_sector.find_elements(By.TAG_NAME, "option"):
            if option.text == "SECTOR TEST":
                option.click()
                break     
        time.sleep(2)   
            # Selecciona 'SubSector Test' en el select
        select_subsector = self.browser.find_element(By.NAME, "subsector")
        for option in select_subsector.find_elements(By.TAG_NAME, "option"):
            if option.text == "SUBSECTOR TEST":
                option.click()
                break     
        # clic en el botón de guardar dentro del modal
        # Ajustamos el selector según tu HTML (por ejemplo, botón type="submit" dentro del modal)
        guardar_btn = self.browser.find_element(By.CSS_SELECTOR, '#modalAgregarInstitucion button[type="submit"]')
        time.sleep(2)   
        guardar_btn.click()

        # Esperamos un momento a que la tabla/listado se actualice
        time.sleep(3)

        # Verificamos que la institución aparece en la página 
        page_source = self.browser.page_source
        self.assertIn("instituto nacional de prueba", page_source.lower())
