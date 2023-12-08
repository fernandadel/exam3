from modelo.Coneccion import conexion2023
from flask import jsonify, request

def buscar_estu(codigo):
    try:
        conn = conexion2023()
        cur = conn.cursor()
        cur.execute("""select * FROM clientes WHERE id = %s""", (codigo,))
        datos = cur.fetchone()
        conn.close()

        if datos != None:
            estu = {'id': datos[0], 'nombre': datos[1],
                       'apellido': datos[2], 'email': datos[3],
                       'telefono': datos[4]}
            return estu
        else:
            return None
    except Exception as ex:
            raise ex
    

class ModeloClientes:
    @classmethod
    def listar_Estudiante(self):
        try:
            conn = conexion2023()
            cursor=conn.cursor()
            cursor.execute("SELECT * FROM clientes")
            datos = cursor.fetchall()
            estudiantes = []

            for fila in datos:
                estu = {'id': fila[0],
                       'nombre': fila[1],
                       'apelllido': fila[2],
                       'email': fila[3],
                       'telefono': fila[4]}
                estudiantes.append(estu)

            conn.close()

            return jsonify({'estudiante': estudiantes, 'mensaje': "estudiantes listados.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Errorr", 'exito': False,"estu":estudiantes})
    
    @classmethod
    def lista_Estudiante(self,codigo):
        try:
            usuario = buscar_estu(codigo)
            if usuario != None:
                return jsonify({'usuarios': usuario, 'mensaje': "usuario encontrado.", 'exito': True})
            else:
                return jsonify({'mensaje': "Usuario no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})

    @classmethod
    def registrar_estudiante(self):
        try:
            usuario = buscar_estu(request.json['ci_e'])
            if usuario != None:
                return jsonify({'mensaje': "Cedula de identidad  ya existe, no se puede duplicar.", 'exito': False})
            else:
                conn = conexion2023()
                cur = conn.cursor()
                cur.execute('INSERT INTO clientes values(%s,%s,%s,%s,%s)', (request.json['id_e'], request.json['nombre_e'], request.json['apellido_e'],
                                                                            request.json['email_e'], request.json['telefono_e']))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "Usuario registrado.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    
    @classmethod
    def actualizar_estudiante(self,codigo):
        try:
            usuario = buscar_estu(codigo)
            if usuario != None:
                conn = conexion2023()
                cur = conn.cursor()
                cur.execute("""UPDATE clientes SET nombre=%s, apellido=%s, email=%s,
                telefono=%s WHERE id=%s""",
                        (request.json['nombre_e'], request.json['apellido_e'], request.json['email_e'], request.json['telefono_e'], codigo))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "estudiante actualizado.", 'exito': True})
            else:
                return jsonify({'mensaje': "estudiante  no encontrado.", 'exito': False})
        except Exception as ex:
                return jsonify({'mensaje': "Error", 'exito': False})
        
    @classmethod
    def eliminar_estuy(self,codigo):
        try:
            usuario = buscar_estu(codigo)
            if usuario != None:
                conn = conexion2023()
                cur = conn.cursor()
                cur.execute("DELETE FROM clientes WHERE ci = %s", (codigo,))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "estudiantes eliminado.", 'exito': True})
            else:
                return jsonify({'mensaje': "estudiante no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})