from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu de Opciones")
        self.resize(300, 300)

        # ----- Botón Carnes -----
        self.btn_carne = QPushButton("Carnes", self)
        self.btn_carne.setFont(QFont('serif', 10))
        self.btn_carne.setGeometry(80, 30, 140, 40)

        # ----- Botón Verduras -----
        self.btn_verduras = QPushButton("Verduras", self)
        self.btn_verduras.setFont(QFont('serif', 10))
        self.btn_verduras.setGeometry(80, 100, 140, 40)

        # ----- Botón Frutas -----
        self.btn_frutas = QPushButton("Frutas", self)
        self.btn_frutas.setFont(QFont('serif', 10))
        self.btn_frutas.setGeometry(80, 170, 140, 40)