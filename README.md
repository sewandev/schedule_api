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