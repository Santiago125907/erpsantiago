import psycopg2

# Configuración de la base de datos
DB_HOST = "database-1.cd4u8i8ymfwu.us-east-1.rds.amazonaws.com"
DB_PORT = 5432  # Cambiado a 5432
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "Xago5547"

def probar_conexion():
    try:
        print("Intentando conectarse a la base de datos...")
        conexion = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Conexión exitosa.")
        cursor = conexion.cursor()
        cursor.execute("SELECT version();")
        print("Versión de PostgreSQL:", cursor.fetchone())
        cursor.close()
        conexion.close()
    except Exception as e:
        print("Error en la conexión:", e)

if __name__ == "__main__":
    probar_conexion()
