import logging
import os
from flask import Flask, render_template, request, redirect
import mysql.connector
import json_log_formatter
import time

app = Flask(__name__)

time.sleep(5)

# Configuración del logger
log = logging.getLogger()
log.setLevel(logging.INFO)

# Configuramos el formatter para que los logs sean en formato JSON
formatter = json_log_formatter.JSONFormatter()

# Configuramos el manejador de archivos de logs en formato JSON
log_handler = logging.FileHandler(os.path.join(os.getcwd(), 'logs', 'app.json'))
log_handler.setFormatter(formatter)
log.addHandler(log_handler)

# Configuración de la conexión a la base de datos
configuracion_bd = {
    'host': os.environ.get('DATABASE_HOST'),
    'user': os.environ.get('DATABASE_USER'),
    'password': os.environ.get('DATABASE_PASSWORD'),
    'database': os.environ.get('DATABASE_NAME'),
    'port': int(os.environ.get('DATABASE_PORT')),
}

def crear_tabla():
    try:
        conexion = mysql.connector.connect(**configuracion_bd)
        cursor = conexion.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS practicas (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255), correo VARCHAR(255), categoria VARCHAR(255), link VARCHAR(255))")
        conexion.commit()
        log.info("Tabla creada correctamente")
    except Exception as e:
        log.error({"message": f"Error al crear la tabla: {e}"})
    finally:
        if 'conexion' in locals():
            conexion.close()

def agregar_practica(nombre, correo, categoria, link):
    try:
        conexion = mysql.connector.connect(**configuracion_bd)
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO practicas (nombre, correo, categoria, link) VALUES (%s, %s, %s, %s)", (nombre, correo, categoria, link))
        conexion.commit()
        log.info({"message": "Práctica agregada correctamente", "nombre": nombre, "correo": correo, "categoria": categoria, "link": link})
    except Exception as e:
        log.error({"message": f"Error al agregar práctica: {e}"})
    finally:
        if 'conexion' in locals():
            conexion.close()

def obtener_practicas():
    try:
        conexion = mysql.connector.connect(**configuracion_bd)
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM practicas")
        practicas = cursor.fetchall()
        return practicas
    except Exception as e:
        log.error({"message": f"Error al obtener prácticas: {e}"})
        return []
    finally:
        if 'conexion' in locals():
            conexion.close()

def eliminar_practica(practica_id):
    try:
        conexion = mysql.connector.connect(**configuracion_bd)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM practicas WHERE id = %s", (practica_id,))
        conexion.commit()
        log.info({"message": "Práctica eliminada correctamente", "id": practica_id})
    except Exception as e:
        log.error({"message": f"Error al eliminar práctica: {e}"})
    finally:
        if 'conexion' in locals():
            conexion.close()

# Crear la tabla en la base de datos
crear_tabla()

@app.route('/')
def index():
    practicas = obtener_practicas()
    return render_template('index.html', practicas=practicas)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    correo = request.form['correo']
    categoria = request.form['categoria']
    link = request.form['link']
    agregar_practica(nombre, correo, categoria, link)
    return redirect('/')

@app.route('/eliminar/<int:practica_id>', methods=['POST'])
def eliminar(practica_id):
    eliminar_practica(practica_id)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
