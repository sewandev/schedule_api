# Instrucciones para Configurar el Proyecto

## Clonar el Repositorio

1. Abre una terminal.
2. Ejecuta el siguiente comando para clonar el repositorio:

   ```bash
   git clone https://github.com/sewandev/reserva-hora-api.git
   cd reserva-hora-api
   pip install -r requirements.txt
   ```

3. Levantar el servidor de la API desde el terminal.

    ```bash
    uvicorn main:app --reload
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

## Arbol de carpetas actual

```bash
├── 📁 app
│   ├── 📁 api
│   │   ├── 📁 endpoints
│   │   │   ├── 📄 appointments.py
│   │   ├── 📄 routes.py
│   ├── 📁 core
│   │   ├── 📄 config.py
│   │   ├── 📄 database.py
│   ├── 📁 models
│   │   ├── 📄 models.py
│   ├── 📁 repositories
│   │   ├── 📄 appointments.py
│   ├── 📁 schemas
│   │   ├── 📄 appointments.py
│   ├── 📁 services
│   │   ├── 📄 appointments.py
├── 📄 .env
├── 📄 appointments.db
├── 📄 main.py
```