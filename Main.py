import sys
from PyQt5.QtWidgets import QApplication



from Inicio_Login import LoginWindow
from Menu_Crud import MenuWindow
from Carnes import Carne
from Verduras import Verduras
from Frutas import Frutas


class Controlador:
    def __init__(self):
        self.login = LoginWindow()
        self.menu = MenuWindow()

        self.carn = Carne()
        self.verd = Verduras()
        self.frut = Frutas()

        # Eventos
        self.login.btn_login.clicked.connect(self.abrir_menu)
        self.menu.btn_carne.clicked.connect(self.abrir_carne)
        self.menu.btn_verduras.clicked.connect(self.abrir_verdura)
        self.menu.btn_frutas.clicked.connect(self.abrir_fruta)

        self.login.show()

    def abrir_menu(self):
        if self.login.verificar_login():
            self.menu.show()
            self.login.close()

    def abrir_carne(self):
        self.carn.show()

    def abrir_verdura(self):
        self.verd.show()

    def abrir_fruta(self):
        self.frut.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controlador = Controlador()
    sys.exit(app.exec_())