class clave:
    def __init__(self,clave,numero):
        self.clave=clave
        self.registros=[]
        #self.numero=numero
    def insertar(self,valor):
        self.registros.append(valor)