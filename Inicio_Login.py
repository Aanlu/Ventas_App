import pyodbc
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(300, 200)

        self.conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DAVID\\DAVID;'
            'DATABASE=Tienda;'
            "UID=sa;"
            "PWD=sqlSA%;"
        )
        self.cursor = self.conexion.cursor()

        # Usuario
        self.usuario_Label = QLabel("Usuario:", self)
        self.usuario_Label.setFont(QFont('serif', 10))
        self.usuario_Label.setGeometry(10, 20, 100, 30)

        self.usuario = QLineEdit(self)
        self.usuario.setGeometry(120, 20, 150, 25)

        # Contraseña
        self.pass_Label = QLabel("Contraseña:", self)
        self.pass_Label.setFont(QFont('serif', 10))
        self.pass_Label.setGeometry(10, 60, 100, 30)

        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setGeometry(120, 60, 150, 25)

        # Botones
        self.btn_login = QPushButton("Entrar", self)
        self.btn_login.setGeometry(40, 120, 100, 30)

        self.btn_registrar = QPushButton("Registrar", self)
        self.btn_registrar.setGeometry(160, 120, 100, 30)

    # --------------------------------
    #     FUNCION: Iniciar Sesión
    # --------------------------------
    def verificar_login(self):
        user = self.usuario.text()
        pwd = self.password.text()

        if user == "" or pwd == "":
            QMessageBox.warning(self, "Error", "Ingrese usuario y contraseña")
            return False

        query = "SELECT * FROM Usuarios WHERE usuario = ? AND password = ?"
        self.cursor.execute(query, (user, pwd))
        resultado = self.cursor.fetchone()

        if resultado:
            return True
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")
            return False

