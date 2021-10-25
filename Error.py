class Error:
    def __init__(self,fila,columna,caracter,observacion=""):
        self.fila=fila
        self.columna=columna
        self.caracter=caracter
        self.observacion=observacion    