# SISARM - Buscador de Aduana 🇧🇴

Sistema integral diseñado para optimizar las consultas y la gestión de Nomenclatura Arancelaria, facilitando el trabajo de los despachantes de aduana.

## 🚀 Características Principales

* **Buscador Especializado:** Consulta rápida de partidas arancelarias, incluyendo Gravamen Arancelario (GA), impuestos adicionales (ICE - IEHD) y requisitos de despacho (SENASAG, disp. legales).
* **Gestión Administrativa:** Panel protegido para la creación, edición y eliminación de aranceles.
* **Importación Masiva:** Capacidad de cargar cientos de partidas arancelarias simultáneamente mediante archivos `.xlsx` o `.csv` respetando las normativas oficiales.
* **Auditoría Inalterable:** Registro automático de trazabilidad que documenta qué usuario realiza cada búsqueda y en qué momento.
* **Sistema de Roles:** Vistas y permisos separados para Administradores y Despachantes.

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python / Django
* **Base de Datos:** SQLite (Desarrollo)
* **Frontend:** HTML5 / Tailwind CSS
* **Herramientas Extra:** `django-import-export`

## 📦 Instalación y Configuración Local

Sigue estos pasos para ejecutar el proyecto en tu entorno local:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/Bueno1730/Buscador-de-aduana.git](https://github.com/Bueno1730/Buscador-de-aduana.git)
   cd Buscador-de-aduana
Crear y activar el entorno virtual:

python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
Instalar dependencias:

pip install -r requirements.txt
Aplicar migraciones a la base de datos:

python manage.py migrate
Iniciar el servidor de desarrollo:

python manage.py runserver
🔐 Acceso al Sistema (Cuentas de Prueba)
Para evaluar el sistema rápidamente una vez levantado el servidor, puedes iniciar sesión utilizando las siguientes credenciales preconfiguradas:

👑 Cuenta de Administrador (Privilegios de edición):

Usuario: Bueno17

Contraseña: Pablobueno_17

👤 Cuenta de Despachante (Solo lectura y búsqueda):

Usuario: Bueno

Contraseña: Pablobueno_30

👥 Creación de Nuevos Usuarios
Si necesitas generar cuentas adicionales para pruebas o evaluación, puedes usar cualquiera de los siguientes métodos:

1. Crear un nuevo Administrador (Superusuario)
Desde la terminal con el entorno virtual activo, ejecuta:

python manage.py createsuperuser
Sigue las instrucciones en pantalla para asignar el nombre de usuario y la contraseña.

2. Crear un nuevo Despachante (Usuario Regular)
Opción A: Desde la Consola (Recomendado para desarrollo rápido)
Puedes crear un despachante directamente abriendo la consola interactiva de Django:

python manage.py shell
Dentro del entorno interactivo, ejecuta el siguiente código reemplazando el usuario y contraseña deseados:

from django.contrib.auth.models import User
User.objects.create_user(username='nuevo_despachante', password='Contraseña_123')
exit()

Opción B: Desde el Panel de Administración Web
Inicia sesión como Administrador.

Entra a http://127.0.0.1:8000/admin/cuentas/arancel/.

En la sección Usuarios, haz clic en Añadir.

Define el usuario, la contraseña y guarda.

Asegúrate de que la casilla "Estado de staff" (Staff status) permanezca DESMARCADA para mantenerlo con el rol de solo lectura.

Desarrollado por Bueno17, SiroCarv, Kwyxzel.