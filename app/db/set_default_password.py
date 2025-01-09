"""
set_default_password.py

Script para establecer una contraseña por defecto ("123") a todos los usuarios
en la tabla 'usuarios'. Uso provisional, mientras se implementa un sistema
de contraseñas más seguro con hashing.
"""

from app.db.base import get_db_connection


def set_default_password_for_all(default_pwd="123"):
    """
    Establece el password = default_pwd para todos los registros de la tabla 'usuarios'.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # Ajusta el nombre de la columna si fuera distinto (p. ej. 'clave' o 'pass').
    query = "UPDATE usuarios SET password = %s"
    cur.execute(query, (default_pwd,))

    conn.commit()
    cur.close()
    conn.close()

    print(f"Todas las contraseñas se han actualizado a: '{default_pwd}'")


if __name__ == "__main__":
    # Aquí definimos la contraseña por defecto (puedes cambiarla).
    set_default_password_for_all("123")
