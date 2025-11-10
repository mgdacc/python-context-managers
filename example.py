import time
from contextlib import contextmanager

# ==============================================================================
# EJEMPLO 1: Creación de un Context Manager usando una CLASE
# Objetivo: Crear un temporizador para medir cuánto tarda un bloque de código.
# ==============================================================================

print("--- Ejemplo 1: Context Manager con Clase (Temporizador) ---")

class Timer:
    """
    Un Context Manager que mide el tiempo de ejecución de un bloque de código.
    """
    def __enter__(self):
        """
        Este método se ejecuta al inicio del bloque 'with'.
        Guardamos el tiempo de inicio.
        """
        print("Iniciando temporizador...")
        self.start_time = time.time()
        # No necesitamos devolver nada en particular, así que devolvemos None implícitamente.
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Este método se ejecuta al final del bloque 'with', sin importar cómo termine.
        Calculamos el tiempo transcurrido y lo mostramos.
        
        Los argumentos exc_type, exc_val, exc_tb contienen información de la excepción
        si ocurrió un error dentro del bloque 'with'. Si no hubo error, son None.
        """
        self.end_time = time.time()
        elapsed_time = self.end_time - self.start_time
        print(f"Bloque de código finalizado en {elapsed_time:.4f} segundos.")
        
        # Si devolvemos True, la excepción se suprime (no se propaga).
        # Si devolvemos False o None, la excepción continúa su curso normal.
        return False

# --- Uso del Temporizador ---
with Timer():
    print("Realizando una tarea que tarda un poco...")
    # Simulamos una operación que tarda 1.5 segundos
    time.sleep(1.5)
    print("Tarea completada.")

print("\n")


# ==============================================================================
# EJEMPLO 2: Creación de un Context Manager usando un DECORADOR
# Objetivo: Simular la conexión y desconexión segura de una base de datos.
# ==============================================================================

print("--- Ejemplo 2: Context Manager con @contextmanager (Base de Datos) ---")

@contextmanager
def database_connection(db_name):
    """
    Un Context Manager que simula la conexión a una base de datos.
    Garantiza que la conexión siempre se cierre.
    """
    print(f"Conectando a la base de datos '{db_name}'...")
    # --- Esto es el equivalente a __enter__ ---
    # Simulamos un objeto de conexión que se podría usar para hacer consultas.
    connection = {"db": db_name, "status": "conectado"}
    
    try:
        # 'yield' pasa el control al bloque 'with'. El valor cedido ('connection')
        # es lo que se asigna a la variable después de 'as'.
        yield connection
    finally:
        # --- Esto es el equivalente a __exit__ ---
        # Este bloque se ejecuta siempre al salir del 'with',
        # garantizando la limpieza del recurso.
        print(f"Cerrando la conexión a la base de datos '{db_name}'...")
        connection["status"] = "desconectado"

# --- Uso del gestor de conexión (caso exitoso) ---
print("-> Caso 1: Operación exitosa")
with database_connection("produccion_db") as db:
    print(f"   Dentro del 'with': Realizando consultas en la base de datos.")
    print(f"   Estado de la conexión: {db['status']}")
    # Simulamos trabajo en la base de datos
    time.sleep(1)
print("Operación terminada.\n")


# --- Uso del gestor de conexión (caso con error) ---
print("-> Caso 2: Operación con error")
try:
    with database_connection("reportes_db") as db:
        print(f"   Dentro del 'with': Realizando una consulta compleja.")
        print(f"   Estado de la conexión: {db['status']}")
        # Simulamos un error durante la operación
        raise ValueError("Error: La consulta SQL es inválida.")
        print("   Esta línea nunca se ejecutará.")
except ValueError as e:
    print(f"Se ha capturado un error fuera del 'with': {e}")

print("A pesar del error, el programa continúa y la conexión fue cerrada.")

"""

Output esperado:

--- Ejemplo 1: Context Manager con Clase (Temporizador) ---
Iniciando temporizador...
Realizando una tarea que tarda un poco...
Tarea completada.
Bloque de código finalizado en 1.50XX segundos.


--- Ejemplo 2: Context Manager con @contextmanager (Base de Datos) ---
-> Caso 1: Operación exitosa
Conectando a la base de datos 'produccion_db'...
   Dentro del 'with': Realizando consultas en la base de datos.
   Estado de la conexión: conectado
Cerrando la conexión a la base de datos 'produccion_db'...
Operación terminada.

-> Caso 2: Operación con error
Conectando a la base de datos 'reportes_db'...
   Dentro del 'with': Realizando una consulta compleja.
   Estado de la conexión: conectado
Cerrando la conexión a la base de datos 'reportes_db'...
Se ha capturado un error fuera del 'with': Error: La consulta SQL es inválida.
A pesar del error, el programa continúa y la conexión fue cerrada.

"""
