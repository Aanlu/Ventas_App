import pyodbc
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QTableWidget,QTableWidgetItem)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class CrudPadre(QWidget):
    def __init__(self, table_name):
        super().__init__()
        self.table_name = table_name
        self.setWindowTitle(f"CRUD de {self.table_name}")
        self.setGeometry(200, 200, 600, 400)

        self.conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DAVID\\DAVID;'
            'DATABASE=Tienda;'
            "UID=sa;"
            "PWD=sqlSA%;"
            'Trusted_Connection=yes;'
        )
        self.cursor = self.conexion.cursor()

        self.initUI()
        self.loadData()

    # ------------------------
    # INTERFAZ GRAFICA
    # ------------------------
    def initUI(self):

        # ----- LABEL TITULO -----
        self.lblTitulo = QLabel("Tienda", self)
        self.lblTitulo.setFont(QFont("Arial", 14))
        self.lblTitulo.setAlignment(Qt.AlignCenter)
        self.lblTitulo.setGeometry(200, 10, 200, 40)

        # ----- TABLA -----
        self.tabla = QTableWidget(self)
        self.tabla.setColumnCount(2)
        self.tabla.setHorizontalHeaderLabels(["Nombre", "Precio"])
        self.tabla.setGeometry(20, 60, 350, 300)

        # ----- ENTRADA NOMBRE -----
        self.lblNombre = QLabel("Nombre:", self)
        self.lblNombre.setGeometry(400, 80, 150, 30)

        self.txtNombre = QLineEdit(self)
        self.txtNombre.setGeometry(400, 110, 150, 30)

        # ----- ENTRADA PRECIO -----
        self.lblPrecio = QLabel("Precio:", self)
        self.lblPrecio.setGeometry(400, 150, 150, 30)

        self.txtPrecio = QLineEdit(self)
        self.txtPrecio.setGeometry(400, 180, 150, 30)

        # ----- BOTON AGREGAR -----
        self.btnAgregar = QPushButton("Agregar", self)
        self.btnAgregar.setGeometry(400, 230, 150, 35)
        self.btnAgregar.clicked.connect(self.agregar)

        # ----- BOTON ACTUALIZAR -----
        self.btnActualizar = QPushButton("Actualizar", self)
        self.btnActualizar.setGeometry(400, 275, 150, 35)
        self.btnActualizar.clicked.connect(self.actualizar)

        # ----- BOTON ELIMINAR -----
        self.btnEliminar = QPushButton("Eliminar", self)
        self.btnEliminar.setGeometry(400, 320, 150, 35)
        self.btnEliminar.clicked.connect(self.eliminar)

    # ------------------------------------------
    # MÉTODOS POLIMÓRFICOS PARA REDEFINIR EN HIJOS
    # ------------------------------------------

    def loadData(self):
        query = f"SELECT id, nombre, precio FROM {self.table_name}"
        self.cursor.execute(query)
        datos = self.cursor.fetchall()

        self.tabla.setRowCount(len(datos))
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Precio"])

        for row, item in enumerate(datos):
            self.tabla.setItem(row, 0, QTableWidgetItem(str(item[0])))
            self.tabla.setItem(row, 1, QTableWidgetItem(item[1]))
            self.tabla.setItem(row, 2, QTableWidgetItem(str(item[2])))
        """
        Este método se sobrescribe en la clase hija.
        Se utiliza para cargar los datos desde la BD.
        """
        pass

    def agregar(self):
        nombre = self.txt_nombre.text()
        precio = self.txt_precio.text()

        query = f"INSERT INTO {self.table_name}(nombre, precio) VALUES(?, ?)"
        self.cursor.execute(query, (nombre, precio))
        self.conexion.commit()

        self.load_data()
        """
        Insertar en la BD.
        Se sobrescribe en la clase hija.
        """
        print("Agregar (padre): redefinir en la clase hija.")

    def actualizar(self):
        nombre = self.txt_nombre.text()
        precio = self.txt_precio.text()

        query = f"UPDATE {self.table_name} SET precio = ? WHERE nombre = ?"
        self.cursor.execute(query, (precio, nombre))
        self.conexion.commit()

        self.load_data()
        """
        Actualizar en la BD.
        Se sobrescribe en la clase hija.
        """
        print("Actualizar (padre): redefinir en la clase hija.")

    def eliminar(self):
        nombre = self.txt_nombre.text()

        query = f"DELETE FROM {self.table_name} WHERE nombre = ?"
        self.cursor.execute(query, (nombre,))
        self.conexion.commit()

        self.load_data()
        """
        Eliminar en la BD.
        Se sobrescribe en la clase hija.
        """
        print("Eliminar (padre): redefinir en la clase hija.")
