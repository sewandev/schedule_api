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
📁 reserva-hora-api
├── 📁 app
│   ├── 📁 api
│   │   ├── 📁 endpoints
│   │   │   ├── 📄 appointments.py        # Controlador para gestionar las rutas relacionadas con las citas.
│   │   │   ├── 📄 upload_schedules.py    # Controlador para gestionar las rutas relacionadas con la carga de horarios.
│   │   ├── 📄 routes.py                  # Registro centralizado de las rutas de la API.
│   ├── 📁 core
│   │   ├── 📄 config.py                  # Configuración principal de la aplicación, incluidas variables de entorno.
│   │   ├── 📄 database.py                # Configuración de la conexión a la base de datos usando SQLAlchemy.
│   ├── 📁 models
│   │   ├── 📄 models.py                  # Definición de los modelos de datos con SQLAlchemy.
│   ├── 📁 repositories
│   │   ├── 📄 appointments.py            # Repositorio para la lógica de acceso y manipulación de datos de citas.
│   │   ├── 📄 upload_schedules.py        # Repositorio para la lógica de acceso y manipulación de horarios.
│   ├── 📁 schemas
│   │   ├── 📄 appointments.py            # Esquemas de validación y serialización de datos relacionados con las citas (usando Pydantic).
│   ├── 📁 services
│   │   ├── 📄 appointments.py            # Lógica de negocio relacionada con las citas.
│   │   ├── 📄 upload_schedules.py        # Lógica de negocio relacionada con la carga de horarios.
├── 📄 .env                               # Archivo para variables de entorno (configuración de base de datos, claves secretas).
├── 📄 appointments.db                    # Base de datos SQLite para desarrollo (migrable a PostgreSQL en producción).
├── 📄 main.py                            # Punto de entrada principal de la aplicación, inicia el servidor FastAPI y carga las rutas.
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