from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)
conexion = MySQL(app)

#  /////////(GET)
@app.route('/Department', methods=['GET'])
def obtener_departamentos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM Human_resources.Departments_2;"
        cursor.execute(sql)
        datos = cursor.fetchall()

        # Convertir los datos a formato JSON
        departamentos = []
        for fila in datos:
            departamento = {
                'DEPARTMENT_ID': fila[0],
                'DEPARTMENT_NAME': fila[1],
                'DEPARTMENT_ABREV': fila[2],
                'MANAGER_ID': fila[3],
                'LAST_UPDATED': str(fila[4]),  # Convertir datetime astring
                'LOCATION': fila[5]
            }
            departamentos.append(departamento)

        return jsonify({'Departamentos': departamentos})  # Respuesta en formato JSON

    except Exception as ex:
        return jsonify({'error': 'Error en la consulta'}), 500  

# Registrar uno nuevo (POST)
@app.route('/Department', methods=['POST'])
def registrar_departamento():
    try:
        # request
        datos = request.json
        if not datos:
            return jsonify({'error': 'No se enviaron datos'}), 400  

        # Extraer  JSON
        department_id = datos.get('DEPARTMENT_ID')
        department_name = datos.get('DEPARTMENT_NAME')
        department_abrev = datos.get('DEPARTMENT_ABREV')
        manager_id = datos.get('MANAGER_ID')
        last_updated = datos.get('LAST_UPDATED', None)  
        location = datos.get('LOCATION', None)  

        if not department_id or not department_name or not department_abrev or not manager_id:
            return jsonify({'error': 'Faltan datos obligatorios'}), 400

        # inserta en la base de datos
        cursor = conexion.connection.cursor()
        sql = "INSERT INTO Human_resources.Departments_2 (DEPARTMENT_ID, DEPARTMENT_NAME, DEPARTMENT_ABREV, MANAGER_ID, LAST_UPDATED, LOCATION) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (department_id, department_name, department_abrev, manager_id, last_updated, location)
        cursor.execute(sql, valores)
        conexion.connection.commit()

        return jsonify({'mensaje': 'Departamento registrado correctamente'}), 201  

    except Exception as ex:
        return jsonify({'error': 'Error al registrar el departamento'}), 500  

def pagina_no_encontrada(error):
    return "<h1>La página no fue encontrada</h1>", 404



##/////ELIMINAR
## ELIMINAR
@app.route('/Department/<int:id>', methods=['DELETE'])
def eliminar_departamento(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM Human_resources.Departments_2 WHERE DEPARTMENT_ID = %s;"
        cursor.execute(sql, (id,))
        conexion.connection.commit()
        return jsonify({'mensaje': f'Departamento con ID {id} eliminado correctamente'}), 200  # Código 200 = OK
    except Exception as ex:
        return jsonify({'error': 'Error al eliminar el departamento', 'detalle': str(ex)}), 500  # Código 500 = Internal Server Error



## ACTUALIZAR
@app.route('/Department/<int:id>', methods=['PUT'])
def actualizar_departamento(id):
    try: 
        cursor = conexion.connection.cursor()
        datos = request.json

        campos = []
        valores = []

        if "nombre" in datos:
            campos.append("DEPARTMENT_NAME = %s")
            valores.append(datos["nombre"])
        if "ubicacion" in datos:
            campos.append("LOCATION = %s")
            valores.append(datos["ubicacion"])
        if "abreviatura" in datos:
            campos.append("DEPARTMENT_ABREV = %s")
            valores.append(datos["abreviatura"])


        sql = f"UPDATE Human_resources.Departments_2 SET {', '.join(campos)} WHERE DEPARTMENT_ID = %s;"
        valores.append(id)
        cursor.execute(sql, tuple(valores))
        conexion.connection.commit()
        
        return jsonify({'mensaje': f'Departamento con ID {id} actualizado correctamente'}), 200

    except Exception as ex:
        return jsonify({'error': 'Error al actualizar el departamento', 'detalle': str(ex)}), 500




if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True)
