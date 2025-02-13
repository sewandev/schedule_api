# Instrucciones para Configurar el Proyecto

## Clonar el Repositorio

1. Abre una terminal.
2. Ejecuta el siguiente comando para clonar el repositorio:

   ```bash
   git clone https://github.com/sewandev/reserva-hora-api.git
   cd reserva-hora-api
   python -m venv venv # Opcional para crear un entorno virutal
   venv\\Scripts\\activate  # Si se crea el entorno virtual, se debe activar
   pip install -r requirements.txt
   ```

3. Levantar el servidor de la API desde el terminal.

    ```bash
    uvicorn main:app --reload
    ```

4. Documentación una vez iniciado el servidor

   ```bash
   http://127.0.0.1:8000/docs # Swagger
   http://127.0.0.1:8000/redoc # Redoc
   ```

## Arbol de carpetas actual

```bash
├── 📁 app                        # Carpeta principal de la aplicación.
│   ├── 📁 api                    # Contiene la lógica relacionada con la API.
│   │   ├── 📁 endpoints           # Define los puntos de entrada (endpoints) de la API.
│   │   │   ├── 📄 appointments.py # Endpoints específicos para gestionar citas (appointments).
│   │   ├── 📄 routes.py           # Configura las rutas de la API.
│   ├── 📁 core                   # Contiene configuraciones y componentes centrales de la aplicación.
│   │   ├── 📄 config.py           # Archivo de configuración (variables de entorno, settings, etc.).
│   │   ├── 📄 database.py         # Configuración y conexión a la base de datos.
│   ├── 📁 models                 # Define los modelos de datos (entidades) de la aplicación.
│   │   ├── 📄 models.py           # Modelos de la base de datos (por ejemplo, la tabla "appointments").
│   ├── 📁 repositories           # Contiene la lógica para interactuar con la base de datos (CRUD).
│   │   ├── 📄 appointments.py     # Operaciones específicas para la tabla de citas (appointments).
│   ├── 📁 schemas                # Define esquemas de validación de datos (por ejemplo, con Pydantic).
│   │   ├── 📄 appointments.py     # Esquemas para validar datos relacionados con citas.
│   ├── 📁 services               # Contiene la lógica de negocio de la aplicación.
│   │   ├── 📄 appointments.py     # Servicios relacionados con la gestión de citas.
├── 📄 .env                       # Archivo de variables de entorno (credenciales, configuraciones sensibles).
├── 📄 appointments.db            # Base de datos SQLite (o similar) para almacenar datos de citas.
├── 📄 main.py                    # Punto de entrada de la aplicación (inicia el servidor o la app).
```

## Para realizar pruebas iniciales con [Postman](https://www.postman.com/downloads/) o [HTTPie](https://httpie.io/desktop)

```bash
Ruta: http://localhost:8000/api/v1/appointments/
Tipo: POST
Headers: Content-Type: application/json
JSON:

{
  "patient_id": 1,
  "medic_id": 1,
  "start_time": "2023-10-10T09:00:00",
  "end_time": "2023-10-10T10:30:00"
}

```

## Relizar debug de API

1. Crear un launch.son en vscode

```bash
{
   "version": "0.2.0",
   "configurations": [
      {
         "name": "Reserva Hora",
         "type": "debugpy",
         "request": "launch",
         "module": "uvicorn",
         "args": [
         "main:app",
         "--host",
         "127.0.0.1",
         "--port",
         "8000",
         "--reload"
      ],
      "jinja": true
      }
   ]
}
```