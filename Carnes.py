from Ventana_Padre import CrudPadre

class Carne(CrudPadre):
    def __init__(self):
        # Al pasar "Carnes", el padre ya sabe a qué API llamar (/api/Carnes)
        super().__init__("Carnes")