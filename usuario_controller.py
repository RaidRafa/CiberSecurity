import mysql.connector

class UsuarioModel:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="28092004",
            database="usuarios"
        )
        self.cursor = self.conexao.cursor(dictionary=True)

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
        sql = "INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)"
        valores = (usuario, senha)
        self.cursor.execute(sql, valores)
        self.conexao.commit()

    def login(self, usuario, senha):
        sql = "SELECT * FROM usuarios WHERE usuario = %s and senha = %s"
        valores = (usuario, senha)
        self.cursor.execute(sql, valores)
        return self.cursor.fetchone()

usuario_Model = UsuarioModel()
UsuarioModel.criar_tabela()
    

