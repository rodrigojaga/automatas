class transicion:
    def __init__(self, estadoOrigen, simboloTransicion, estadoDestino):
        self.estadoOrigen = estadoOrigen
        self.estadoDestino = estadoDestino
        self.simboloTransicion = simboloTransicion

class estado:
    def __init__(self, nombreEstado, isAceptacion, isInicio):
        self.nombreEstado = nombreEstado
        self.isAceptacion = isAceptacion
        self.isInicio = isInicio