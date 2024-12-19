
# Despliegue de la Aplicación

## Requisitos previos

1. **Base de datos**: Crear una base de datos en **Postgres**.
2. **Archivo `.env`**: Copiar el archivo `envexample` y crear un nuevo archivo llamado `.env`.
3. **Configurar la base de datos**:
   - Cambiar la cadena de conexión de **Postgres** con la base de datos que tenemos en la variable de entorno `DATABASE_URL`.

## Configuración Opcional

Puedes modificar las siguientes variables en el archivo `.env` si deseas configurar el envío de correos electrónicos:

- `EMAIL_HOST_USER`: Tu dirección de correo electrónico de Gmail.
- `EMAIL_HOST_PASSWORD`: La contraseña de tu cuenta de Gmail (con aplicaciones poco seguras habilitadas).

## Pasos Obligatorios

### 1. Crear un entorno virtual

- En **Windows**:
    ```bash
    python -m venv venv
    ```

- En **Linux**:
    ```bash
    python3 -m venv venv
    ```

### 2. Activar el entorno virtual

- En **Windows**:
    ```bash
    venv\Scripts\activate
    ```

- En **Linux**:
    ```bash
    source venv/bin/activate
    ```

### 3. Instalar las dependencias

- En **Windows**:
    ```bash
    pip install -r requirements.txt
    ```

- En **Linux**:
    ```bash
    pip install -r requirements.txt
    ```

### 4. Ejecutar las migraciones

- En **Windows**:
    ```bash
    python manage.py migrate
    ```

- En **Linux**:
    ```bash
    python3 manage.py migrate
    ```

Con estos pasos, la aplicación estará lista para desplegarse en un entorno local.

## Ejecutar la Aplicación

### 1. Iniciar el servidor

- En **Windows**:
    ```bash
    python manage.py runserver 0.0.0.0:8000
    ```

- En **Linux**:
    ```bash
    python3 manage.py runserver 0.0.0.0:8000
    ```

### 2. Acceder a la aplicación

- Abre tu navegador y accede a: [http://localhost:8000](http://localhost:8000).

### 3. Usuario y Contraseña

- Usuario: `joubmaja.69@gmail.com`
- Contraseña: `Cambiame123`

Con estos pasos, la aplicación debería estar funcionando correctamente en tu entorno local.
