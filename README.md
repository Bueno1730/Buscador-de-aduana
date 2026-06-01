# SISARM - Buscador de Aduana 🇧🇴

Sistema integral diseñado para optimizar las consultas y la gestión de Nomenclatura Arancelaria, facilitando el trabajo de los despachantes de aduana.

##  Características Principales

* **Buscador Especializado:** Consulta rápida de partidas arancelarias, incluyendo Gravamen Arancelario (GA), impuestos adicionales (ICE - IEHD) y requisitos de despacho (SENASAG, disp. legales).
* **Gestión Administrativa:** Panel protegido para la creación, edición y eliminación de aranceles.
* **Importación Masiva:** Capacidad de cargar cientos de partidas arancelarias simultáneamente mediante archivos `.xlsx` o `.csv` respetando las normativas oficiales.
* **Auditoría Inalterable:** Registro automático de trazabilidad que documenta qué usuario realiza cada búsqueda y en qué momento.
* **Sistema de Roles:** Vistas y permisos separados para Administradores y Despachantes.

##  Tecnologías Utilizadas

* **Backend:** Python / Django
* **Base de Datos:** SQLite (Desarrollo)
* **Frontend:** HTML5 / Tailwind CSS
* **Herramientas Extra:** `django-import-export`

##  Instalación y Configuración Local

Sigue estos pasos para ejecutar el proyecto en tu entorno local:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/Bueno1730/Buscador-de-aduana.git](https://github.com/Bueno1730/Buscador-de-aduana.git)
   cd Buscador-de-aduana

2. **Crear y activar el entorno virtual:**
   python -m venv venv
    # En Windows:
    venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate

3. **Instalar dependencias:**
   pip install -r requirements.txt

4. **Aplicar migraciones a la base de datos:**
   python manage.py migrate

5. **Iniciar el servidor de desarrollo:**
   python manage.py runserver

Desarrollado por Bueno17, SiroCarv, Kwyxzel.
