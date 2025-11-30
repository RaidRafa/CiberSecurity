from flask import Flask, send_from_directory
import os
from Controller.usuario_controller import usuario_bp
from limiter_config import limiter
from flask import jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax" # Reduz o risco de CSRF

# Inicia o limiter com o app
limiter.init_app(app)

# === MVC ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIEW_DIR = os.path.join(BASE_DIR, "Visual")
MODEL_DIR = os.path.join(BASE_DIR, "Model")

# Blueprint da API
app.register_blueprint(usuario_bp, url_prefix="/api")

# --- Rota principal ---
@app.route("/")
def index():
    return send_from_directory(VIEW_DIR, "teladelogin.html")

# --- Tela de cadastro ---
@app.route("/registrar")
def registrar_page():
    return send_from_directory(VIEW_DIR, "cadastro.html")

# --- Rota para arquivos JS dentro de Model ---
@app.route("/Model/<path:arquivo>")
def servir_model(arquivo):
    return send_from_directory(MODEL_DIR, arquivo)

# --- Rota padrão para arquivos em Visual ---
@app.route("/<path:arquivo>")
def servir_arquivo(arquivo):
    return send_from_directory(VIEW_DIR, arquivo)

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "ok": False,
        "erro": "Muitas tentativas de login. Tente novamente mais tarde."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 8000, debug=False)
