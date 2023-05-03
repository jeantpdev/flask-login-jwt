from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS, cross_origin
import supabase

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret' # Clave secreta para firmar los JWT
CORS(app)
jwt = JWTManager(app)

SUPABASE_URL = 'https://mmphzayxvvhdtrtcvjsq.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1tcGh6YXl4dnZoZHRydGN2anNxIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODI2MDY3NDYsImV4cCI6MTk5ODE4Mjc0Nn0.QZWfmiw-KMFgHOTSyxNGFlcOZvDRa305OkZH-YHTzDI'

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Conectamos con Supabase
    client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

    # Buscamos el usuario en la tabla 'usuario'
    query = client.table('usuario').select('*').eq('usuario', username).eq('contrasena', password)
    res = query.execute()

    # Si el usuario existe y la contraseña es correcta, se devuelve un token JWT
    if len(res.data) == 1:
        access_token = create_access_token(identity=username)
        print(access_token)
        return jsonify(access_token=access_token), 200

    # Si no se encontró el usuario o la contraseña es incorrecta, se devuelve un error 401
    return jsonify({"msg": "Credenciales inválidas"}), 401

if __name__=="__main__":
    ##app.run(debug=True, host="0.0.0.0")
    app.run(port=5000, debug=True)