-- ================================================================
--  Biblioteca Universidad Ducky  –  Schema MySQL
-- ================================================================

CREATE DATABASE IF NOT EXISTS biblioteca_ducky
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE biblioteca_ducky;

-- ── Tabla Libros ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS libros (
    isbn              VARCHAR(20)      NOT NULL,
    titulo            VARCHAR(255)     NOT NULL,
    autor             VARCHAR(255)     NOT NULL,
    editorial         VARCHAR(150),
    sinopsis          TEXT,
    anio_publicacion  YEAR,
    num_paginas       INT,
    precio            DECIMAL(10,2),
    ubicacion         VARCHAR(100),
    num_copias        INT              DEFAULT 1,
    categoria         VARCHAR(100),
    fecha_registro    DATETIME         DEFAULT CURRENT_TIMESTAMP,
    estado            ENUM('disponible','prestado','mantenimiento','perdido')
                                       DEFAULT 'disponible',
    PRIMARY KEY (isbn),
    INDEX idx_titulo (titulo),
    INDEX idx_autor  (autor)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ── Tabla Usuarios ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS usuarios (
    usuario    VARCHAR(50)   NOT NULL,
    contrasena VARCHAR(255)  NOT NULL  COMMENT 'Valor cifrado',
    nombre     VARCHAR(50)   NOT NULL,
    email      VARCHAR(150)  NOT NULL,
    PRIMARY KEY (usuario),
    UNIQUE KEY uq_nombre (nombre),
    UNIQUE KEY uq_email  (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ── Datos de prueba ──────────────────────────────────────────────
-- Contraseña: "admin123"  (hash bcrypt generado con werkzeug)
INSERT IGNORE INTO usuarios (usuario, contrasena, nombre, email) VALUES
('admin',
 'pbkdf2:sha256:600000$ducky2024$a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2',
 'Administrador',
 'admin@ducky.edu');

-- NOTA: regenera el hash real con:
--   from werkzeug.security import generate_password_hash
--   print(generate_password_hash('admin123'))
-- y reemplaza el valor anterior.

INSERT IGNORE INTO libros
  (isbn, titulo, autor, editorial, sinopsis,
   anio_publicacion, num_paginas, precio,
   ubicacion, num_copias, categoria, estado)
VALUES
('978-0-06-112008-4',
 'To Kill a Mockingbird', 'Harper Lee', 'J. B. Lippincott & Co.',
 'Una novela sobre la injusticia racial en el sur de Estados Unidos narrada por una niña.',
 1960, 281, 350.00,
 'Sección: Literatura Americana\nPasillo: 3-A\nEstantería: Nivel 2, Baida Derecha',
 2, 'Ficción', 'disponible'),

('978-84-16408-23-9',
 'El Eco de los Relojes de Arena', 'Elena Villarreal Solís', 'Nexo Arcano Editores',
 'En un pueblo donde el tiempo no transcurre de forma lineal, Julián descubre que sus recuerdos pertenecen a un hombre que aún no ha nacido.',
 2024, 342, 400.00,
 'Sección: Narrativa Hispanoamericana Contemporánea\nPasillo: 12-B (Planta Alta)\nEstantería: Nivel 4, Baida Izquierda',
 3, 'Ficción', 'disponible'),

('978-0-06-088328-7',
 'Cien Años de Soledad', 'Gabriel García Márquez', 'Editorial Sudamericana',
 'La historia mítica de la familia Buendía a lo largo de siete generaciones.',
 1967, 417, 280.00,
 'Sección: Literatura Latinoamericana\nPasillo: 5-C\nEstantería: Nivel 1, Baida Izquierda',
 5, 'Ficción', 'disponible');
