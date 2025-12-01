import requests
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Autenticación de Usuarios")
        self.resize(300, 200)

        # Endpoint del servicio de identidad
        self.api_url = "https://059dfecdc33f.ngrok-free.app/api/Login"

        # Elementos de UI
        self.usuario_Label = QLabel("Usuario:", self)
        self.usuario_Label.setFont(QFont('serif', 10))
        self.usuario_Label.setGeometry(10, 20, 100, 30)

        self.usuario = QLineEdit(self)
        self.usuario.setGeometry(120, 20, 150, 25)

        self.pass_Label = QLabel("Contraseña:", self)
        self.pass_Label.setFont(QFont('serif', 10))
        self.pass_Label.setGeometry(10, 60, 100, 30)

        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setGeometry(120, 60, 150, 25)

        self.btn_login = QPushButton("Entrar", self)
        self.btn_login.setGeometry(40, 120, 100, 30)

        self.btn_registrar = QPushButton("Registrar", self)
        self.btn_registrar.setGeometry(160, 120, 100, 30)

        self.btn_registrar.clicked.connect(self.registrar_usuario)

    # Validación de credenciales contra servidor remoto
    def verificar_login(self):
        user = self.usuario.text()
        pwd = self.password.text()

        if user == "" or pwd == "":
            QMessageBox.warning(self, "Validación", "Campos requeridos vacíos")
            return False

        datos = {"nombreUsuario": user, "password": pwd, "rol": ""}

        try:
            # Envío sincrónico de credenciales
            respuesta = requests.post(self.api_url, json=datos)
            if respuesta.status_code == 200:
                return True
            else:
                QMessageBox.warning(self, "Error", "Credenciales inválidas")
                return False
        except Exception as e:
            QMessageBox.critical(self, "Error de Red", f"Servidor no alcanzable.\n{e}")
            return False

    # Registro de nuevos usuarios en la base de datos central
    def registrar_usuario(self):
        user = self.usuario.text()
        pwd = self.password.text()

        if user == "" or pwd == "":
            return

        datos = {"nombreUsuario": user, "password": pwd, "rol": "Vendedor"}

        try:
            url_registro = f"{self.api_url}/Registrar"
            respuesta = requests.post(url_registro, json=datos)

            if respuesta.status_code == 200:
                QMessageBox.information(self, "Registro", "Usuario creado exitosamente.")
            else:
                QMessageBox.warning(self, "Error", f"Fallo al registrar: {respuesta.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error de comunicación: {e}")