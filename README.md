# Biblioteca Universidad Ducky 🎓

Aplicación web Flask + MySQL que replica los wireframes de la librería universitaria.

---

## Estructura del proyecto

```
biblioteca_ducky/
├── app.py                   # Aplicación Flask principal
├── schema.sql               # Script de base de datos (tablas + datos de prueba)
├── requirements.txt
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── img/logo.png         # Logo de universidad
└── templates/
    ├── base.html            # Layout base (sidebar + topbar)
    ├── login.html           # Pantalla de inicio de sesión
    ├── libros.html          # Catálogo de libros
    ├── libro_detalle.html   # Detalle de un libro
    └── libro_form.html      # Formulario nuevo / edición
```

---

## Instalación paso a paso

### 1. Requisitos previos
- Python 3.10+
- MySQL 8.0+ o MariaDB 10.6+
- (Opcional) Entorno virtual: `python -m venv venv && source venv/bin/activate`

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
- Base de datos `biblioteca_ducky`
- Tabla `libros` con los campos del wireframe
- Tabla `usuarios`
- 3 libros de ejemplo

### 4. Generar contraseña de admin real

Abre Python y ejecuta:

```python
from werkzeug.security import generate_password_hash
print(generate_password_hash('admin123'))
```

Copia el hash y actualiza en MySQL:

```sql
USE biblioteca_ducky;
UPDATE usuarios SET contrasena = 'HASH_AQUI' WHERE usuario = 'admin';
```

### 5. Configurar conexión MySQL en `app.py`

```python
app.config['MYSQL_HOST']     = 'localhost'
app.config['MYSQL_USER']     = 'root'
app.config['MYSQL_PASSWORD'] = 'tu_contraseña'
app.config['MYSQL_DB']       = 'biblioteca_ducky'
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

---

## Logo

logo de la universidad en:  
`static/img/logo.png`  

