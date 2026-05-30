# Instrucciones de Ejecución Local (Terminal Antigravity)

Este documento detalla los pasos para configurar y ejecutar la aplicación **SIG-UTCUTS Chile** utilizando la terminal de Antigravity.

---

## Opción 1: Ejecución Completa con Docker Compose (Recomendado)

Esta es la forma más rápida y sencilla de levantar todos los servicios (Base de Datos PostGIS, Backend FastAPI y Frontend Vite) simultáneamente.

### Inicio Rápido

Una vez que ya lo construiste por primera vez, **no necesitas volver a construir (`--build`) ni a copiar el archivo `.env`**. Para arrancar el proyecto en segundos, solo debes hacer:

1. Asegurarte de que **Docker Desktop** esté abierto.
2. Ejecutar el comando rápido:
   ```powershell
   docker compose up
   ```

### Configuración Inicial (Solo la primera vez)

1. **Configurar Variables de Entorno**: Crea el archivo `.env` copiando la plantilla de ejemplo (solo se hace una vez):
   ```powershell
   cp .env.example .env
   ```

2. **Abrir Docker Desktop**: Asegúrate de tener la aplicación **Docker Desktop** abierta y ejecutándose en tu equipo.

3. **Construir e Iniciar**: Descarga las imágenes iniciales y construye los contenedores (este paso tardará unos minutos la primera vez):
   ```powershell
   docker compose up --build
   ```

---

### Ejecuciones Siguientes (Inicio Rápido)

Una vez que ya lo construiste por primera vez, **no necesitas volver a construir (`--build`) ni a copiar el archivo `.env`**. Para arrancar el proyecto en segundos, solo debes hacer:

1. Asegurarte de que **Docker Desktop** esté abierto.
2. Ejecutar el comando rápido:
   ```powershell
   docker compose up
   ```

> [!TIP]
> Dado que los archivos locales del backend y frontend están enlazados con Docker (volúmenes), **cualquier cambio que hagas en el código se reflejará automáticamente en el navegador (hot-reload)** sin necesidad de reiniciar Docker ni usar `--build`.

---

## Opción 2: Ejecución Local en Desarrollo (Sin Docker / Con SQLite)

Si no tienes Docker Desktop iniciado o prefieres ejecutar el Backend y Frontend de manera local e independiente, puedes usar **SQLite** (que está soportado nativamente por la aplicación).

### 1. Configurar Base de Datos SQLite en `.env`
Abre el archivo `.env` que copiaste anteriormente y modifica la línea de `DATABASE_URL` para que use SQLite en lugar de PostgreSQL:

```env
# Comenta o reemplaza la línea original de PostgreSQL:
# DATABASE_URL=postgresql://sigutcuts:sigutcuts_dev_2024@db:5432/sigutcuts

# Y usa esta línea para SQLite:
DATABASE_URL=sqlite:///./sigutcuts.db
```

### 2. Configurar y Correr Backend (FastAPI)

1. Ve a la carpeta del backend y crea el entorno virtual de Python:
   ```powershell
   cd backend
   python -m venv venv
   ```

2. Activa el entorno virtual:
   ```powershell
   venv\Scripts\activate
   ```

3. Instala las dependencias necesarias:
   ```powershell
   pip install -r requirements.txt
   ```

4. Inicia el servidor del backend:
   ```powershell
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### 3. Configurar y Correr Frontend (React + Vite)

1. Navega al directorio del frontend:
   ```powershell
   cd frontend
   ```

2. Instala las dependencias de Node.js:
   ```powershell
   npm install
   ```

3. Arranca el servidor de desarrollo de Vite:
   ```powershell
   npm run dev
   ```

---

## Solución de Problemas

### Error: `open //./pipe/dockerDesktopLinuxEngine: El sistema no puede encontrar el archivo especificado`
Este error ocurre porque **Docker Desktop no está iniciado** en tu máquina de Windows.
- **Solución 1**: Abre la aplicación **Docker Desktop** en tu computadora, espera a que el servicio se inicie por completo, y vuelve a intentar ejecutar `docker compose up --build`.
- **Solución 2**: Utiliza la **Opción 2** (ejecución sin Docker usando SQLite) detallada arriba.

---

## Direcciones de Acceso

Una vez levantados los servicios, puedes acceder a ellos en tu navegador web:

- **Frontend**: [http://localhost:5173](http://localhost:5173)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **Documentación de la API (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)

> [!NOTE]
> Al ejecutar comandos de servidores de desarrollo en la terminal de Antigravity (como `docker compose up` o `npm run dev`), estos se iniciarán de forma asíncrona permitiendo seguir utilizando el asistente de programación.
