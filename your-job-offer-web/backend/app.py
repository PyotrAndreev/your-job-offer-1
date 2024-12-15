import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config.from_object(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)

CORS(app, resources={r"/*":{'origins':'*'}})

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello!!"


@app.route('/registration', methods=['POST'])
def registration():
    return "registered"

@app.route('/form', methods=['POST'])
def form():
    name = request.form['name']
    resume = request.files.get('resume')
    print(resume.filename)
    return name

@app.route('/userData', methods=['POST'])
def userData():
    name = request.form['name']
    resume = request.files.get('resume')
    print(resume.filename)
    return name

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    #find user data in db
    if username != "test" or password != "test":
        return jsonify({"msg": "Invalid username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)
    
@app.route('/dashboard', methods=["GET"])
@jwt_required
def dashboard():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == "__main__":
    app.run(debug=True)