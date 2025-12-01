import requests
import json
import os
from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal


# Clase base abstracta para la gestión de entidades CRUD.
# Implementa la lógica de comunicación con la API REST y el manejo de errores de red.
class CrudPadre(QWidget):
    # Señal para notificar al controlador la solicitud de cambio de vista
    senal_volver = pyqtSignal()

    def __init__(self, table_name):
        super().__init__()
        self.table_name = table_name  # Identificador de la entidad (Tabla)
        self.setWindowTitle(f"Gestión de {self.table_name}")
        self.setGeometry(200, 200, 600, 400)

        # Configuración del endpoint remoto (Ngrok)
        self.base_url = "https://54d872b30336.ngrok-free.app/api"

        self.initUI()
        self.loadData()

    def initUI(self):
        # Construcción dinámica de la interfaz de usuario
        self.lblTitulo = QLabel("Sistema de Inventario", self)
        self.lblTitulo.setFont(QFont("Arial", 14))
        self.lblTitulo.setAlignment(Qt.AlignCenter)
        self.lblTitulo.setGeometry(200, 10, 200, 40)

        self.tabla = QTableWidget(self)
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Precio"])
        self.tabla.setGeometry(20, 60, 350, 300)

        # Campos de entrada
        self.lblNombre = QLabel("Nombre:", self)
        self.lblNombre.setGeometry(400, 80, 150, 30)
        self.txtNombre = QLineEdit(self)
        self.txtNombre.setGeometry(400, 110, 150, 30)

        self.lblPrecio = QLabel("Precio:", self)
        self.lblPrecio.setGeometry(400, 150, 150, 30)
        self.txtPrecio = QLineEdit(self)
        self.txtPrecio.setGeometry(400, 180, 150, 30)

        # Botones de acción CRUD
        self.btnAgregar = QPushButton("Agregar", self)
        self.btnAgregar.setGeometry(400, 230, 150, 35)
        self.btnAgregar.clicked.connect(self.agregar)

        self.btnActualizar = QPushButton("Actualizar", self)
        self.btnActualizar.setGeometry(400, 275, 150, 35)
        self.btnActualizar.clicked.connect(self.actualizar)

        self.btnEliminar = QPushButton("Eliminar", self)
        self.btnEliminar.setGeometry(400, 320, 150, 35)
        self.btnEliminar.clicked.connect(self.eliminar)

        self.btnVolver = QPushButton("Volver al Menú", self)
        self.btnVolver.setGeometry(20, 10, 120, 30)
        self.btnVolver.clicked.connect(self.emitir_volver)

    def emitir_volver(self):
        self.senal_volver.emit()
        self.close()

    # Recuperación de datos mediante petición HTTP GET
    def loadData(self):
        url = f"{self.base_url}/{self.table_name}"
        try:
            # Timeout configurado para evitar congelamiento de UI en redes inestables
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                datos = response.json()
                self.tabla.setRowCount(len(datos))
                # Poblado de la tabla visual con datos remotos
                for row, item in enumerate(datos):
                    self.tabla.setItem(row, 0, QTableWidgetItem(str(item["id"])))
                    self.tabla.setItem(row, 1, QTableWidgetItem(item["nombre"]))
                    self.tabla.setItem(row, 2, QTableWidgetItem(str(item["precio"])))
        except Exception:
            # Manejo silencioso de error de conexión para no interrumpir el flujo
            pass

    # Creación de registros mediante HTTP POST
    def agregar(self):
        nombre = self.txtNombre.text()
        precio = self.txtPrecio.text()
        if not nombre or not precio: return

        datos = {"nombre": nombre, "precio": float(precio), "stock": 0}
        endpoint = self.table_name

        try:
            r = requests.post(f"{self.base_url}/{endpoint}", json=datos, timeout=2)
            if r.status_code == 200: self.loadData()
        except:
            # Fallback a modo offline en caso de error de red
            self.guardar_offline(endpoint, "POST", datos)
            QMessageBox.information(self, "Offline", "Operación guardada localmente.")

        self.txtNombre.clear();
        self.txtPrecio.clear()

    # Actualización mediante HTTP PUT
    def actualizar(self):
        nombre = self.txtNombre.text()
        precio = self.txtPrecio.text()
        datos = {"nombre": nombre, "precio": float(precio)}
        endpoint = self.table_name
        try:
            r = requests.put(f"{self.base_url}/{endpoint}", json=datos, timeout=2)
            if r.status_code == 200: self.loadData()
        except:
            self.guardar_offline(endpoint, "PUT", datos)
            QMessageBox.information(self, "Offline", "Actualización en cola de sincronización.")

        self.txtNombre.clear();
        self.txtPrecio.clear()

    # Eliminación mediante HTTP DELETE
    def eliminar(self):
        nombre = self.txtNombre.text()
        endpoint = self.table_name
        try:
            r = requests.delete(f"{self.base_url}/{endpoint}/{nombre}", timeout=2)
            if r.status_code == 200: self.loadData()
        except:
            self.guardar_offline(endpoint, "DELETE", {"nombre": nombre})
            QMessageBox.information(self, "Offline", "Eliminación en cola de sincronización.")
        self.txtNombre.clear()

    # Serialización de la operación en JSON local para persistencia temporal
    def guardar_offline(self, endpoint, metodo, datos):
        registro = {"tabla": endpoint, "metodo": metodo, "datos": datos, "fecha": str(datetime.now())}
        with open("pendientes.json", "a") as f:
            json.dump(registro, f)
            f.write("\n")