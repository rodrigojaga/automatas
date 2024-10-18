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

class automata:
    def __init__(self, estados, alfabeto, transiciones, estado_inicial, estados_aceptacion):
        self.estados = estados  # Lista de todos los estados
        self.alfabeto = alfabeto  # Lista del alfabeto
        self.transiciones = transiciones  # Diccionario de transiciones {(estado_actual, simbolo): estado_siguiente}
        self.estado_inicial = estado_inicial  # Estado inicial
        self.estados_aceptacion = estados_aceptacion  # Lista de estados de aceptación

    def procesar_cadena(self, cadena):
        estado_actual = self.estado_inicial
        for simbolo in cadena:
            if (estado_actual, simbolo) in self.transiciones:
                estado_actual = self.transiciones[(estado_actual, simbolo)]
            else:
                return False
        return estado_actual in self.estados_aceptacion