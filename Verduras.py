from PyQt5.QtWidgets import QTableWidgetItem

from App_Ventas.Ventana_Padre import CrudPadre

class Verduras(CrudPadre):
    def __init__(self):
        super().__init__("Verduras")
        self.table_nam = "Verduras"

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

    def agregar(self):
        nombre = self.txtNombre.text()
        precio = self.txtPrecio.text()

        if nombre == "" or precio == "":
            print("Falta nombre o precio.")
            return

        query = f"INSERT INTO {self.table_name} (nombre, precio) VALUES (?, ?)"
        self.cursor.execute(query, (nombre, precio))
        self.conexion.commit()

        self.loadData()
        self.txtNombre.clear()
        self.txtPrecio.clear()

    def actualizar(self):
        nombre = self.txtNombre.text()
        precio = self.txtPrecio.text()

        if nombre == "" or precio == "":
            print("Falta nombre o precio.")
            return

        query = f"UPDATE {self.table_name} SET precio = ? WHERE nombre = ?"
        self.cursor.execute(query, (precio, nombre))
        self.conexion.commit()

        self.loadData()
        self.txtNombre.clear()
        self.txtPrecio.clear()

    def eliminar(self):
        nombre = self.txtNombre.text()

        if nombre == "":
            print("Escribe el nombre para eliminar.")
            return

        query = f"DELETE FROM {self.table_name} WHERE nombre = ?"
        self.cursor.execute(query, (nombre,))
        self.conexion.commit()

        self.loadData()
        self.txtNombre.clear()
