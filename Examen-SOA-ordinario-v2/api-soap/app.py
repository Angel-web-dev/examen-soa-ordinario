from flask import Flask, request, Response, jsonify
from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
load_dotenv()

import os

app = Flask(__name__)

DB_URL = os.getenv('DB_URL', 'mysql+pymysql://root:password@db:3306/examen_db')
engine = create_engine(DB_URL, future=True)

class AlumnoService(ServiceBase):

    @rpc(Unicode, Unicode, Unicode, _returns=Unicode)
    def registrar(ctx, matricula, nombre, apellido):
        if not matricula or not nombre or not apellido:
            return "ERROR: Datos incompletos"
        try:
            with engine.begin() as conn:
                conn.execute(text(
                    "INSERT INTO alumno (matricula, nombre, apellido) VALUES (:m, :n, :a)"
                ), {"m": matricula, "n": nombre, "a": apellido})
            return "OK"
        except Exception as e:
            return f"ERROR: {str(e)}"

    @rpc(Unicode, _returns=Unicode)
    def consultar(ctx, matricula):
        if not matricula:
            return "ERROR: matricula vacía"
        try:
            with engine.connect() as conn:
                result = conn.execute(text(
                    "SELECT matricula, nombre, apellido FROM alumno WHERE matricula = :m"
                ), {"m": matricula}).fetchone()
            if not result:
                return "NO_ENCONTRADO"
            xml = f"""
            <alumno>
                <matricula>{result.matricula}</matricula>
                <nombre>{result.nombre}</nombre>
                <apellido>{result.apellido}</apellido>
            </alumno>
            """.strip()
            return xml
        except Exception as e:
            return f"ERROR: {str(e)}"

    @rpc(Unicode, _returns=Unicode)
    def eliminar(ctx, matricula):
        if not matricula:
            return "ERROR: matricula vacía"
        try:
            with engine.connect() as conn:
                result = conn.execute(text(
                    "SELECT matricula FROM alumno WHERE matricula = :m"
                ), {"m": matricula}).fetchone()
            if not result:
                return "NO_ENCONTRADO"
            with engine.begin() as conn:
                conn.execute(text(
                    "DELETE FROM alumno WHERE matricula = :m"
                ), {"m": matricula})
            return "OK"
        except Exception as e:
            return f"ERROR: {str(e)}"


soap_app = Application(
    [AlumnoService],
    tns='spyne.alumno',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(soap_app)


@app.route('/soap', methods=['POST', 'OPTIONS'])
def soap_http():
    # Preflight CORS
    if request.method == "OPTIONS":
        response = Response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        return response

    # SOAP normal
    response = wsgi_app(request.environ, start_response=lambda s, h: None)
    resp = Response(b''.join(response), mimetype='text/xml')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/health')
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
