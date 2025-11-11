from flask import Flask
from controller.usuario_controller import usuario_bp

app = Flask(__name__, static_folder="Visual", template_folder="Visual")

app.register_blueprint(usuario_bp, url_prefix="/api")

# Rota principal
@app.route("/")
def index():
    return send_from_directory("Visual", "teladelogin.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("Visual", path)

if __name__ == "__main__":
    app.run(debug=True)