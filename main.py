from tkinter import Button, Text,Tk, ttk,filedialog,messagebox,Label,Scrollbar
from tkinter import *
from Token import Token
from Error import Error

#variables globales
Errores=[]
Tokens=[]
ventana=Tk()
textE=Text()
textS=Text()
texto=""
analizado=False
def generarVentana():
    global ventana,textE,textS
    ventana.configure(background="#008080")
    ancho=1400
    alto=700
    x=ventana.winfo_screenwidth()
    #calculamos la coordenada X donde se posicionara la ventana
    x=(x-ancho)/2
    y=ventana.winfo_screenheight()
    #calculamos la coordenada Y donde se posicionara la ventana
    y=(y-alto)/2
    ventana.geometry('%dx%d+%d+%d' % (ancho, alto, x, y))
    ventana.title("Proyecto 2")

    #para el text area de entrada
    frameEntrada=Frame(ventana)
    frameEntrada.place(x=200,y=80)
    scrollbar1=Scrollbar(frameEntrada, orient='horizontal')
    scrollbar1.pack(side=BOTTOM, fill='x')
    textE=Text(frameEntrada, font=("Calibri, 14"), wrap="none", xscrollcommand=scrollbar1.set,width=58,height=25)
    textE.pack()
    scrollbar1.config(command=textE.xview)

    #para el text area de salida
    frameSalida=Frame(ventana)
    frameSalida.place(x=900,y=80)
    scrollbar2=Scrollbar(frameSalida, orient='horizontal')
    scrollbar2.pack(side=BOTTOM, fill='x')
    textS=Text(frameSalida, font=("Calibri, 14"),background="#696969", wrap="none", xscrollcommand=scrollbar2.set,width=43,height=25,state=DISABLED)
    textS.pack()
    scrollbar2.config(command=textS.xview)


    #botones
    b1=Button(ventana,text="Cargar",command=cargarArchivo,font=("Verdana",10),borderwidth=3,background="beige").place(x=300,y=35,height=40,width=100)
    b2=Button(ventana,text="Analizar",command=Solicitaranalisis,font=("Verdana",10),borderwidth=3,background="beige").place(x=980,y=35,height=40,width=100)
    b3=Button(ventana,text="Reporte de Errores",font=("Verdana",10),borderwidth=3,background="beige").place(x=20,y=300,height=40,width=150)
    b4=Button(ventana,text="Reporte de Tokens",font=("Verdana",10),borderwidth=3,background="beige").place(x=20,y=360,height=40,width=150)
    
    
    #Labels
    Label(ventana,bg="#008080",fg="white",relief="flat" ,text="Entrada:", font=("arial italic", 18) ).place(x=200,y=40)
    Label(ventana,bg="#008080",fg="white",relief="flat" ,text="Salida:", font=("arial italic", 18) ).place(x=900,y=40)


    ventana.mainloop()

def cargarArchivo():
    global texto,textE
    archivo=filedialog.askopenfile(
        title="Por favor seleccine un archivo",
        initialdir="./",
        filetypes=(
            ("Archivo LFP","*.lfp"),("Todos los archivos","*.*")
        )
    )

    if archivo is None:
        messagebox.showerror(message="No selecciono ningun archivo, por favor vuelva a intentarlo",title="Error")
        texto=""
        print("No selecciono ningun archivo, por favor vuelva a intentarlo")
    else:
        temp=archivo.read()
        textE.delete('1.0', END)
        textE.insert(END,temp)
        archivo.close()

def Solicitaranalisis():
    global texto,analizado,textE
    texto=textE.get("1.0", "end-1c")
    if texto=="":
        print("texto vacio")
        messagebox.showerror(message="No hay archivo por analizar, Por favor primero cargue un archivo",title="Error")
        analizado=False
    else:
        print(texto)
        analizar(texto)
        analizado=True


#metodos para el analizador lexico-------------------------------------
def isLetra(C):
    if((ord(C) >= 65 and ord(C) <= 90) or (ord(C) >= 97 and ord(C) <= 122) or ord(C) == 164 or ord(C) == 165):
        return True
    else:
        return False

def isNumero(C):
    if ((ord(C) >= 48 and ord(C) <= 57)):
        return True
    else:
        return False

def isEspacio(C):
    if (ord(C)==32 or ord(C)==9 or ord(C)==10):
        return True
    else:
        return False

def analizar(txt):
    global Tokens,Errores
    Errores=[]
    Tokens=[]
    fila=1
    columna=1
    estado=0
    error=False
    LexemaActual=""

    conteo=0
    for c in txt:
        if estado==0 and not isEspacio(c):
            if isLetra(c):
                LexemaActual+=c
                estado=1
            #seccion de simbolos---------------------------------------
            elif ord(c)==61:#signo =
                Tokens.append(Token("igual",c,fila,columna))
                LexemaActual=""
                estado=0
            elif ord(c)==40:
                Tokens.append(Token("parentesis_a",c,fila,columna))
                LexemaActual=""
                estado=0
            elif ord(c)==35:
                estado=5
            elif isNumero(c):
                estado=8
            elif ord(c)==39:#3 comillas simples
                if conteo==2:
                    conteo=0
                    estado=6
                else:
                    conteo+=1
            elif ord(c)==43 or ord(c)==45:#signo mas e igual
                Tokens.append(Token("signo",c,fila,columna))
                estado=7
            #-------------------------------------------------------
            elif ord(c)==34:#comillas
                LexemaActual=""
                estado=2
            else:
                Errores.append(Error(fila,columna,c,"Caracter no valido"))
                error=True
                LexemaActual=""
                estado=0
        elif estado==1:
            if isLetra(c):
                LexemaActual+=c
                estado=1
            elif ord(c)==61:#signo =
                Tokens.append(Token("Reservada",LexemaActual,fila,columna-len(LexemaActual)))
                Tokens.append(Token("igual",c,fila,columna))
                LexemaActual=""
                estado=0
            elif ord(c)==40:
                Tokens.append(Token("Reservada",LexemaActual,fila,columna-len(LexemaActual)))
                Tokens.append(Token("parentesis_a",c,fila,columna))
                LexemaActual=""
                estado=0
            else:
                if isEspacio(c):
                    pass
                
        elif estado==2:
            pass
        elif estado==3:
            pass
        elif estado==4:
            pass
        elif estado==5:
            pass
               
        elif estado==6 and not isEspacio(c):
            pass

        elif estado==7 and not isEspacio(c):
            pass
        elif estado==8:
            pass
        elif estado==9 and not isEspacio(c):
            pass
        elif estado==10:
            pass
        
        




        # controlador de filas y columnas
        if ord(c) == 10:
            columna=1
            fila+=1
            continue
        elif(ord(c) == 9): #para tabulación
            columna+=4
            continue
        elif(ord(c)==32):
            columna+=1
            continue
        columna+=1
    
    for e in Errores:
        print("fila:",e.fila,"columna",e.columna,"caracter:",e.caracter,e.observacion)

    for t in Tokens:
        print(t.token,t.lexema,t.fila,t.columna)
    if error:
        print("Si hubo error")
        messagebox.showinfo(message="Se reportaron errores en el analisis por favor vea los reportes",title="Aviso")
    else:
        print("No hubo error")
        messagebox.showinfo(message="Se realizo el analisis con exito y sin errores",title="Aviso")

if __name__=='__main__':
    generarVentana()