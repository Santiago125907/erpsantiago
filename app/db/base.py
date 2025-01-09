"""
app/db/base.py

Código Python (psycopg2) para:
 - Conectarse a PostgreSQL.
 - Crear tablas 'usuarios' (con la columna password_hash) y 'empresas' si no existen.
 - Funciones de validación de usuarios y CRUD de empresas.
"""

import psycopg2
from psycopg2 import sql

# -------------------------------------------------------------------
# DATOS DE CONEXIÓN (ajusta a tu servidor PostgreSQL)
# -------------------------------------------------------------------
DB_HOST = "database-1.cd4u8i8ymfwu.us-east-1.rds.amazonaws.com"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "Xago5547"

# -------------------------------------------------------------------
# 1) FUNCIÓN DE CONEXIÓN
# -------------------------------------------------------------------
def get_db_connection():
    """
    Crea y retorna una conexión (psycopg2) a la base de datos PostgreSQL.
    """
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

# -------------------------------------------------------------------
# 2) CREAR TABLAS (usuarios y empresas) SI NO EXISTEN
# -------------------------------------------------------------------
def create_tables():
    """
    Crea las tablas 'usuarios' y 'empresas' si no existen,
    usando la columna 'password_hash' para la contraseña de los usuarios.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # Tabla usuarios con password_hash
    create_usuarios = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        nombre_completo VARCHAR(200),
        rol VARCHAR(50) DEFAULT 'user'
    );
    """

    # Tabla empresas
    create_empresas = """
    CREATE TABLE IF NOT EXISTS empresas (
        id_empresa SERIAL PRIMARY KEY,
        nombre_legal VARCHAR(200) NOT NULL,
        rut VARCHAR(50),
        direccion VARCHAR(300)
    );
    """

    cur.execute(create_usuarios)
    cur.execute(create_empresas)

    conn.commit()
    cur.close()
    conn.close()

# -------------------------------------------------------------------
# 3) VALIDAR USUARIO
# -------------------------------------------------------------------
def validate_user(username: str, password: str):
    """
    Valida que 'username' exista en la tabla 'usuarios'
    y que su 'password_hash' coincida con 'password' (texto plano por ahora).

    Retorna (True, id_usuario) si ok, o (False, None) si falla.

    En producción, se recomienda usar bcrypt o similar para verificar hashes:
      if bcrypt.checkpw(password.encode("utf-8"), db_password_hash.encode("utf-8")):
          return (True, db_id_usuario)
    """
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
    SELECT id_usuario, password_hash
    FROM usuarios
    WHERE username = %s
    """
    cur.execute(query, (username,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        # Usuario no existe
        return (False, None)

    db_id_usuario, db_password_hash = row

    # Comparación simple si tu password_hash en DB es solo texto plano.
    if password == db_password_hash:
        return (True, db_id_usuario)
    else:
        return (False, None)

# -------------------------------------------------------------------
# 4) CRUD DE EMPRESAS
# -------------------------------------------------------------------
def list_companies():
    """
    Retorna una lista de diccionarios con la información de cada empresa.
    Estructura: [ { 'id_empresa': X, 'nombre_legal': '...', 'rut': '...' }, ... ]
    """
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
    SELECT id_empresa, nombre_legal, rut
    FROM empresas
    ORDER BY id_empresa
    """
    cur.execute(query)
    rows = cur.fetchall()

    companies = []
    for row in rows:
        companies.append({
            "id_empresa": row[0],
            "nombre_legal": row[1],
            "rut": row[2]
        })

    cur.close()
    conn.close()
    return companies

def create_company(nombre_legal: str, rut: str, direccion: str = None):
    """
    Inserta una nueva empresa en la tabla 'empresas'.
    Retorna el id_empresa (SERIAL) generado.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
    INSERT INTO empresas (nombre_legal, rut, direccion)
    VALUES (%s, %s, %s)
    RETURNING id_empresa
    """
    cur.execute(query, (nombre_legal, rut, direccion))
    new_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return new_id

def update_company(id_empresa: int, nombre_legal: str, rut: str, direccion: str = None):
    """
    Actualiza los datos de una empresa existente por su ID.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
    UPDATE empresas
    SET nombre_legal = %s,
        rut = %s,
        direccion = %s
    WHERE id_empresa = %s
    """
    cur.execute(query, (nombre_legal, rut, direccion, id_empresa))

    conn.commit()
    cur.close()
    conn.close()

def delete_company(id_empresa: int):
    """
    Elimina una empresa por su ID.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
    DELETE FROM empresas
    WHERE id_empresa = %s
    """
    cur.execute(query, (id_empresa,))

    conn.commit()
    cur.close()
    conn.close()

# -------------------------------------------------------------------
# 5) PRUEBAS DIRECTAS (Opcional)
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Si ejecutas este archivo, crea/verifica tablas y
    # podrías hacer pruebas directas de funciones.
    create_tables()
    print("Tablas 'usuarios' y 'empresas' creadas/verificadas con éxito.")

    # Ejemplo de crear un usuario manual (texto plano en password_hash)
    # Para producción, usar hashing real.
    conn = get_db_connection()
    cur = conn.cursor()

    # Este INSERT es solo de ejemplo. Ajusta a tu caso.
    # Si ya tienes un usuario, coméntalo.
    try:
        cur.execute("""
            INSERT INTO usuarios (username, password_hash, nombre_completo, rol)
            VALUES (%s, %s, %s, %s)
        """, ("admin", "123", "Administrador", "admin"))
        conn.commit()
        print("Usuario 'admin' creado con password_hash='123'.")
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        print("El usuario 'admin' ya existe.")

    cur.close()
    conn.close()

    # Prueba de validación
    ok, user_id = validate_user("admin", "123")
    if ok:
        print(f"Validación exitosa, user_id={user_id}")
    else:
        print("Fallo en la validación.")

# -------------------------------------------------------------------
if __name__ == "__main__":
    # Si ejecutas este archivo directamente, se crearán las tablas
    # y podrías hacer pruebas.
    create_tables()
    print("Tablas creadas/verificadas con éxito.")
