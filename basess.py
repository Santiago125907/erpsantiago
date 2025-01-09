import psycopg2
from tabulate import tabulate

# Configuración de la base de datos
DB_HOST = "database-1.cd4u8i8ymfwu.us-east-1.rds.amazonaws.com"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "Xago5547"  # Considera usar variables de entorno para mayor seguridad


def obtener_estructura():
    try:
        # Conexión a la base de datos
        conexion = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conexion.cursor()

        # Archivo para guardar la salida
        with open("estructura_db.txt", "w") as archivo:
            # Consulta para obtener tablas y columnas
            consulta_tablas = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
            """
            cursor.execute(consulta_tablas)
            tablas = cursor.fetchall()

            archivo.write("=== Tablas en la base de datos ===\n\n")
            for tabla in tablas:
                archivo.write(f"Tabla: {tabla[0]}\n")

                # Consulta para obtener columnas
                consulta_columnas = f"""
                SELECT column_name, data_type, character_maximum_length, is_nullable
                FROM information_schema.columns
                WHERE table_name = '{tabla[0]}'
                ORDER BY ordinal_position;
                """
                cursor.execute(consulta_columnas)
                columnas = cursor.fetchall()
                archivo.write(tabulate(columnas, headers=["Columna", "Tipo de Dato", "Longitud Máxima", "Nullable"],
                                       tablefmt="grid"))
                archivo.write("\n")

                # Claves primarias
                consulta_pk = f"""
                SELECT kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
                WHERE tc.table_name = '{tabla[0]}' AND tc.constraint_type = 'PRIMARY KEY';
                """
                cursor.execute(consulta_pk)
                pks = cursor.fetchall()
                archivo.write(f"Clave primaria: {[pk[0] for pk in pks]}\n")

                # Claves foráneas
                consulta_fk = f"""
                SELECT
                    kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name='{tabla[0]}';
                """
                cursor.execute(consulta_fk)
                fks = cursor.fetchall()
                if fks:
                    archivo.write("Claves foráneas:\n")
                    archivo.write(tabulate(fks, headers=["Columna", "Tabla Referenciada", "Columna Referenciada"],
                                           tablefmt="grid"))
                    archivo.write("\n")
                else:
                    archivo.write("Claves foráneas: Ninguna\n")

                # Índices
                consulta_indices = f"""
                SELECT indexname, indexdef
                FROM pg_indexes
                WHERE schemaname = 'public' AND tablename = '{tabla[0]}';
                """
                cursor.execute(consulta_indices)
                indices = cursor.fetchall()
                if indices:
                    archivo.write("Índices:\n")
                    archivo.write(
                        tabulate(indices, headers=["Nombre del Índice", "Definición del Índice"], tablefmt="grid"))
                    archivo.write("\n")
                else:
                    archivo.write("Índices: Ninguno\n")

                archivo.write("\n")

        # Cerrar conexión
        cursor.close()
        conexion.close()
        print("Estructura de la base de datos guardada en 'estructura_db.txt'")
    except Exception as e:
        print("Error al obtener la estructura de la base de datos:", e)


if __name__ == "__main__":
    obtener_estructura()
