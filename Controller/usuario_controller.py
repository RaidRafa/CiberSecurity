from flask import Blueprint, request, jsonify
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from limiter_config import limiter
from dotenv import load_dotenv
import os

load_dotenv()

class UsuarioModel:
    def __init__(self):
        print("DB_HOST:", os.getenv("DB_HOST"))
        print("DB_USER:", os.getenv("DB_USER"))
        print("DB_NAME:", os.getenv("DB_NAME"))

        self.conexao = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            cursorclass=pymysql.cursors.DictCursor, 
        )
        self.cursor = self.conexao.cursor()

    def criar_tabela(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario VARCHAR(100) UNIQUE NOT NULL,
                senha VARCHAR(255) NOT NULL
            )
        """)
        self.conexao.commit()

    def registrar(self, usuario, senha):
        senha_hash = generate_password_hash(senha)
        sql = "INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)"
        valores = (usuario, senha_hash)
        self.cursor.execute(sql, valores)
        self.conexao.commit()

    def login(self, usuario, senha):
        sql = "SELECT * FROM usuarios WHERE usuario = %s"
        self.cursor.execute(sql, (usuario,))
        user = self.cursor.fetchone()

        if user and check_password_hash(user["senha"], senha):
            return user
        return None
        

usuario_model = UsuarioModel()
usuario_model.criar_tabela()

usuario_bp = Blueprint("usuario_bp", __name__)

# --- LOGIN ---
@usuario_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")  # se não quiser rate limit, pode remover essa linha
def login():
    try:
        data = request.get_json(force=True) or {}
        usuario = data.get("usuario", "").strip()
        senha   = data.get("senha", "").strip()

        if not usuario or not senha:
            return jsonify({"ok": False, "erro": "Usuário e senha são obrigatórios."}), 400

        user = usuario_model.login(usuario, senha)
        if user:
            return jsonify({
                "ok": True,
                "usuario": {
                    "id": user["id"],
                    "usuario": user["usuario"]
                }
            }), 200

        return jsonify({"ok": False, "erro": "Usuário ou senha incorretos."}), 401

    except Exception as e:
        print("Erro no /api/login:", repr(e))
        return jsonify({"ok": False, "erro": "Erro interno no servidor."}), 500


# --- REGISTRAR ---
@usuario_bp.route("/registrar", methods=["POST"])
def registrar():
    data = request.get_json()
    usuario = data.get("usuario")
    senha = data.get("senha")

    if not usuario or not senha:
        return jsonify({"ok": False, "erro": "Campos obrigatórios"}), 400

    try:
        usuario_model.registrar(usuario, senha)
        return jsonify({"ok": True, "mensagem": "Usuário registrado com sucesso!"})
    except pymysql.MySQLError as e:
        if e.errno == 1062:  # código de erro para entrada duplicada
            return jsonify({"ok": False, "erro": "Usuário já existe"}), 400
        else:
            return jsonify({"ok": False, "erro": str(e)}), 500
