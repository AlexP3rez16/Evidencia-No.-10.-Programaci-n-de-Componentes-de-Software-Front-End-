# Biblioteca Universidad Ducky

Aplicación web Flask + MySQL con arquitectura MVC que replica los wireframes de la librería universitaria.

---

## Estructura del proyecto

```
Act10/
├── app.py                      # Punto de entrada Flask, registro de blueprints
├── db.py                       # Conexión a MySQL
├── schema.sql                  # Script de base de datos (tablas + datos de prueba)
├── requirements.txt
├── .env                        # Variables de entorno (no se sube al repo)
├── controllers/
│   ├── auth.py                 # Rutas de autenticación (login / logout)
│   └── libros.py               # Rutas CRUD de libros
├── models/
│   ├── libro.py                # Modelo Libro
│   └── usuario.py              # Modelo Usuario
├── static/
│   ├── css/style.css
│   └── js/main.js
└── templates/
    ├── base.html               # Layout base (sidebar + topbar)
    ├── login.html              # Pantalla de inicio de sesión
    ├── libros.html             # Catálogo de libros
    ├── libro_detalle.html      # Detalle de un libro
    └── libro_form.html         # Formulario nuevo / edición
```

---

## Instalación paso a paso

### 1. Requisitos previos

- Python 3.10+
- MySQL 8.0+ o MariaDB 10.6+
- (Opcional) Entorno virtual: `python -m venv .venv && source .venv/bin/activate`

### 2. Instalar dependencias Python

```bash
pip install -r requirements.txt
```

> En macOS/Linux puede necesitar: `brew install mysql` o `sudo apt install libmysqlclient-dev`

### 3. Crear la base de datos

```bash
mysql -u root -p < schema.sql
```

Esto crea:
- Base de datos `biblioteca_arqui`
- Tabla `libros` con los campos del wireframe
- Tabla `usuarios`
- Registros de ejemplo

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
DB_HOST=localhost
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=biblioteca_arqui
```

### 5. Generar contraseña de admin

Abre Python y ejecuta:

```python
from werkzeug.security import generate_password_hash
print(generate_password_hash('admin123'))
```

Copia el hash y actualiza en MySQL:

```sql
USE biblioteca_arqui;
UPDATE usuarios SET contrasena = 'HASH_AQUI' WHERE usuario = 'admin';
```

### 6. Ejecutar la aplicación

```bash
python app.py
```

Abre el navegador en: **http://localhost:5000**

**Credenciales de prueba:**
- Usuario: `admin`
- Contraseña: `admin123` (después de actualizar el hash)

---

## Pantallas implementadas

| Pantalla | Ruta |
|----------|------|
| Inicio de sesión | `GET/POST /login` |
| Catálogo de libros | `GET /libros` |
| Detalle de libro | `GET /libros/<isbn>` |
| Nuevo libro | `GET/POST /libros/nuevo` |
| Editar libro | `GET/POST /libros/<isbn>/editar` |
| Eliminar libro | `POST /libros/<isbn>/eliminar` |
| Cerrar sesión | `GET /logout` |
