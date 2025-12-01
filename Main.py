import sys
import socket
import time
import json
import os
import requests
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal

from Inicio_Login import LoginWindow
from Menu_Crud import MenuWindow
from Carnes import Carne
from Verduras import Verduras
from Frutas import Frutas


# Hilo dedicado a la comunicación TCP en tiempo real.
# Mantiene una conexión persistente con el servidor para recibir notificaciones push
# sin bloquear el hilo principal de la interfaz gráfica.
class HiloSocket(QThread):
    senal_actualizar = pyqtSignal(str)  # Señal para enviar datos a la UI de forma segura

    def run(self):
        host = 'localhost'
        port = 6000  # Puerto TCP configurado en el servidor C# para notificaciones

        while True:
            try:
                # Establece conexión de stream (TCP)
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((host, port))
                    print("Conexión establecida con el servicio de notificaciones")

                    while True:
                        # Lectura bloqueante del buffer de red
                        data = s.recv(1024)
                        if not data: break

                        # Decodificación y emisión del evento a la capa de presentación
                        self.senal_actualizar.emit(data.decode('utf-8'))
            except:
                # Estrategia de reconexión automática en caso de caída del servidor
                time.sleep(3)


# Hilo de sincronización para tolerancia a fallos (Store & Forward).
# Revisa periódicamente el almacenamiento local en busca de transacciones fallidas
# para reintentar su envío al servidor central.
class HiloSync(QThread):
    def run(self):
        # Endpoint base del Web Service (Túnel Ngrok)
        base_url = "https://059dfecdc33f.ngrok-free.app/api"

        while True:
            time.sleep(10)  # Ciclo de verificación (polling)

            if os.path.exists("pendientes.json"):
                self.procesar_pendientes(base_url)

    def procesar_pendientes(self, base_url):
        try:
            with open("pendientes.json", "r") as f:
                lineas = f.readlines()
            if not lineas: return

            pendientes = []

            # Procesa cada transacción almacenada localmente
            for linea in lineas:
                try:
                    obj = json.loads(linea)
                    url = f"{base_url}/{obj['tabla']}"

                    # Reconstruye y ejecuta la petición HTTP original
                    if obj['metodo'] == "POST":
                        r = requests.post(url, json=obj['datos'])
                    elif obj['metodo'] == "PUT":
                        r = requests.put(url, json=obj['datos'])
                    elif obj['metodo'] == "DELETE":
                        r = requests.delete(f"{url}/{obj['datos']['nombre']}")

                    # Si la petición falla nuevamente, se conserva para el siguiente ciclo
                    if r.status_code != 200:
                        pendientes.append(linea)
                except:
                    pendientes.append(linea)

            # Actualiza el archivo de persistencia local
            with open("pendientes.json", "w") as f:
                for p in pendientes: f.write(p)

            if not pendientes: os.remove("pendientes.json")
        except:
            pass


# Controlador principal que gestiona el ciclo de vida de las ventanas y la lógica de navegación
class Controlador:
    def __init__(self):
        # Inicialización de vistas
        self.login = LoginWindow()
        self.menu = MenuWindow()
        self.carn = Carne()
        self.verd = Verduras()
        self.frut = Frutas()

        # Vinculación de eventos de interfaz (Signals & Slots)
        self.login.btn_login.clicked.connect(self.abrir_menu)

        self.menu.btn_carne.clicked.connect(self.abrir_carne)
        self.menu.btn_verduras.clicked.connect(self.abrir_verdura)
        self.menu.btn_frutas.clicked.connect(self.abrir_fruta)

        # Vinculación de señales de retorno para navegación jerárquica
        self.carn.senal_volver.connect(self.mostrar_menu)
        self.verd.senal_volver.connect(self.mostrar_menu)
        self.frut.senal_volver.connect(self.mostrar_menu)

        # Inicialización de servicios en segundo plano (Hilos)
        self.hilo_socket = HiloSocket()
        self.hilo_socket.senal_actualizar.connect(self.procesar_actualizacion)
        self.hilo_socket.start()

        self.hilo_sync = HiloSync()
        self.hilo_sync.start()

        self.login.show()

    def abrir_menu(self):
        if self.login.verificar_login():
            self.menu.show()
            self.login.close()

    def mostrar_menu(self):
        self.menu.show()

    def abrir_carne(self):
        self.carn.show()
        self.menu.hide()

    def abrir_verdura(self):
        self.verd.show()
        self.menu.hide()

    def abrir_fruta(self):
        self.frut.show()
        self.menu.hide()

    # Manejador de eventos del Socket: Actualiza la vista específica que fue modificada
    # Garantiza la consistencia de datos entre múltiples clientes conectados
    def procesar_actualizacion(self, mensaje):
        if "FRUTAS" in mensaje:
            self.frut.loadData()
        elif "CARNES" in mensaje:
            self.carn.loadData()
        elif "VERDURAS" in mensaje:
            self.verd.loadData()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        controlador = Controlador()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error en ejecución: {e}")