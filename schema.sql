--CREATE DATABASE IF NOT EXISTS biblioteca_ducky CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

--USE biblioteca_ducky;

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
    estado            ENUM('disponible','prestado','mantenimiento','perdido') DEFAULT 'disponible',
    PRIMARY KEY (isbn)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS usuarios (
    usuario    VARCHAR(50)   NOT NULL,
    contrasena VARCHAR(255)  NOT NULL,
    nombre     VARCHAR(50)   NOT NULL,
    email      VARCHAR(150)  NOT NULL,
    PRIMARY KEY (usuario),
    UNIQUE KEY uq_nombre (nombre),
    UNIQUE KEY uq_email  (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── Usuario admin (contraseña: admin123) ─────────────────────────
INSERT IGNORE INTO usuarios (usuario, contrasena, nombre, email) VALUES
('admin', 'pbkdf2:sha256:600000$pSK617XS7u8y94In$4cae02f163f8acb79be5ee441b38ece65371e8de83dc38d71f4c96bc204ef1e3', 'Administrador', 'admin@ducky.edu');

-- ── Libros de prueba ─────────────────────────────────────────────
INSERT IGNORE INTO libros (isbn, titulo, autor, editorial, sinopsis, anio_publicacion, num_paginas, precio, ubicacion, num_copias, categoria, estado) VALUES
('978-0-06-112008-4', 'To Kill a Mockingbird', 'Harper Lee', 'J. B. Lippincott', 'Una novela sobre la injusticia racial en el sur de Estados Unidos.', 1960, 281, 350.00, 'Sección: Literatura Americana\nPasillo: 3-A\nEstantería: Nivel 2', 2, 'Ficción', 'disponible'),
('978-84-16408-23-9', 'El Eco de los Relojes de Arena', 'Elena Villarreal Solís', 'Nexo Arcano Editores', 'En un pueblo donde el tiempo no transcurre de forma lineal, Julián descubre que sus recuerdos pertenecen a un hombre que aún no ha nacido.', 2024, 342, 400.00, 'Sección: Narrativa Hispanoamericana\nPasillo: 12-B\nEstantería: Nivel 4', 3, 'Ficción', 'disponible'),
('978-0-06-088328-7', 'Cien Años de Soledad', 'Gabriel García Márquez', 'Editorial Sudamericana', 'La historia mítica de la familia Buendía a lo largo de siete generaciones.', 1967, 417, 280.00, 'Sección: Literatura Latinoamericana\nPasillo: 5-C\nEstantería: Nivel 1', 5, 'Ficción', 'disponible');