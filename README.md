# Instrucciones para Configurar el Proyecto

## Clonar el Repositorio

1. Abre una terminal.
2. Ejecuta el siguiente comando para clonar el repositorio:

   ```bash
   git clone https://github.com/sewandev/reserva-hora-api.git
   cd reserva-hora-api
   python -m venv venv
   venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

3. Levantar el servidor de la API desde el terminal.

    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

4. Documentación una vez iniciado el servidor

   ```bash
   http://127.0.0.1:8000/docs # Swagger
   http://127.0.0.1:8000/redoc # Redoc
   ```

## Para realizar pruebas iniciales con [Postman](https://www.postman.com/downloads/) o [HTTPie](https://httpie.io/desktop)

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
         "0.0.0.0",
         "--port",
         "8000",
         "--reload"
      ],
      "jinja": true
      }
   ]
}
```