from tkinter import Button, Text,Tk, ttk,filedialog,messagebox,Label,Scrollbar
from tkinter import *
from os import startfile
from Token import Token
from Error import Error
from Clave import clave


#variables globales
Errores=[]
Tokens=[]
Claves=[]
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
    b3=Button(ventana,text="Reporte de Errores",command=ReporteHtmlErrores,font=("Verdana",10),borderwidth=3,background="beige").place(x=20,y=300,height=40,width=150)
    b4=Button(ventana,text="Reporte de Tokens",command=ReporteHtmlTokens,font=("Verdana",10),borderwidth=3,background="beige").place(x=20,y=360,height=40,width=150)
    
    
    #Labels
    Label(ventana,bg="#008080",fg="white",relief="flat" ,text="Entrada:", font=("arial italic", 18) ).place(x=200,y=40)
    Label(ventana,bg="#008080",fg="white",relief="flat" ,text="Salida:", font=("arial italic", 18) ).place(x=900,y=40)


    ventana.mainloop()

def cargarArchivo():
    global texto,textE
    archivo=filedialog.askopenfilename(
        title="Por favor seleccine un archivo",
        initialdir="./",
        filetypes=(
            ("Archivo LFP","*.lfp"),("Todos los archivos","*.*")
        )
    )
    print(archivo)
    if archivo=="":
        messagebox.showerror(message="No selecciono ningun archivo, por favor vuelva a intentarlo",title="Error")
        texto=""
        print("No selecciono ningun archivo, por favor vuelva a intentarlo")
    else:
        contenido=open(archivo,"r",encoding='UTF-8')
        temp=contenido.read()
        textE.delete('1.0', END)
        textE.insert(END,temp)
        contenido.close()

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
            elif ord(c)==40: #parentecis abierto
                Tokens.append(Token("parentesis_a",c,fila,columna))
                LexemaActual=""
                estado=0
            elif ord(c)==41: #parentecis cerrado
                Tokens.append(Token("parentesis_c",c,fila,columna))
                LexemaActual=""
                estado=0
            elif ord(c)==91: #corchete abierto
                Tokens.append(Token("Corchete_a",c,fila,columna))
                LexemaActual=""
                estado=0
            elif ord(c)==93: #corchete cerrado
                Tokens.append(Token("Corchete_c",c,fila,columna))
                LexemaActual=""
                estado=0
            elif ord(c)==44:# coma
                Tokens.append(Token("coma",c,fila,columna))
                LexemaActual=""
                estado=0
            elif ord(c)==59:# punto y coma
                Tokens.append(Token("punto_coma",c,fila,columna))
                LexemaActual=""
                estado=0
            elif ord(c)==123:# llave abierta
                Tokens.append(Token("llave_abierta",c,fila,columna))
                LexemaActual=""
                estado=0
            elif ord(c)==125:# llave cerrada
                Tokens.append(Token("llave_cerrada",c,fila,columna))
                LexemaActual=""
                estado=0
            elif ord(c)==35:
                estado=5
            elif isNumero(c):
                LexemaActual+=c
                estado=8
            elif ord(c)==39:#3 comillas simples
                if conteo==2:
                    conteo=0
                    estado=6
                else:
                    conteo+=1
            elif ord(c)==43 or ord(c)==45:#signo mas e igual
                LexemaActual+=c
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
        
        
        
        elif estado==1 and not isEspacio(c):
            if isLetra(c):
                LexemaActual+=c
                estado=1
            elif ord(c)==61:#signo =
                if LexemaActual=="Claves":
                    Tokens.append(Token("claves",LexemaActual,fila,columna-len(LexemaActual)))
                    Tokens.append(Token("igual",c,fila,columna))
                elif LexemaActual=="Registros":
                    Tokens.append(Token("registros",LexemaActual,fila,columna-len(LexemaActual)))
                    Tokens.append(Token("igual",c,fila,columna))
                else:
                    Errores.append(Error(fila,columna,LexemaActual,"Palabra reservada mal escrita"))
                    error=True
                    LexemaActual=""
                    estado=0
                
                LexemaActual=""
                estado=0
            elif ord(c)==40:#parentesis
                if LexemaActual=="imprimir":
                    Tokens.append(Token("imprimir",LexemaActual,fila,columna-len(LexemaActual)))
                    Tokens.append(Token("parentesis_a",c,fila,columna))
                    LexemaActual=""
                    estado=0
                elif LexemaActual=="imprimirln":
                    Tokens.append(Token("imprimirln",LexemaActual,fila,columna-len(LexemaActual)))
                    Tokens.append(Token("parentesis_a",c,fila,columna))
                    LexemaActual=""
                    estado=0
                elif LexemaActual=="conteo":
                    Tokens.append(Token("conteo",LexemaActual,fila,columna-len(LexemaActual)))
                    Tokens.append(Token("parentesis_a",c,fila,columna))
                    LexemaActual=""
                    estado=0
                elif LexemaActual=="promedio":
                    Tokens.append(Token("promedio",LexemaActual,fila,columna-len(LexemaActual)))
                    Tokens.append(Token("parentesis_a",c,fila,columna))
                    LexemaActual=""
                    estado=0
                elif LexemaActual=="contarsi":
                    Tokens.append(Token("contarsi",LexemaActual,fila,columna-len(LexemaActual)))
                    Tokens.append(Token("parentesis_a",c,fila,columna))
                    LexemaActual=""
                    estado=0
                elif LexemaActual=="datos":
                    Tokens.append(Token("datos",LexemaActual,fila,columna-len(LexemaActual)))
                    Tokens.append(Token("parentesis_a",c,fila,columna))
                    LexemaActual=""
                    estado=0
                elif LexemaActual=="sumar":
                    Tokens.append(Token("sumar",LexemaActual,fila,columna-len(LexemaActual)))
                    Tokens.append(Token("parentesis_a",c,fila,columna))
                    LexemaActual=""
                    estado=0
                elif LexemaActual=="max":
                    Tokens.append(Token("max",LexemaActual,fila,columna-len(LexemaActual)))
                    Tokens.append(Token("parentesis_a",c,fila,columna))
                    LexemaActual=""
                    estado=0
                elif LexemaActual=="min":
                    Tokens.append(Token("min",LexemaActual,fila,columna-len(LexemaActual)))
                    Tokens.append(Token("parentesis_a",c,fila,columna))
                    LexemaActual=""
                    estado=0
                elif LexemaActual=="exportarReporte":
                    Tokens.append(Token("exportarReporte",LexemaActual,fila,columna-len(LexemaActual)))
                    Tokens.append(Token("parentesis_a",c,fila,columna))
                    LexemaActual=""
                    estado=0
                else:
                    Errores.append(Error(fila,columna,LexemaActual,"Palabra reservada mal escrita"))
                    error=True
                    LexemaActual=""
                    estado=0

                LexemaActual=""
                estado=0
            else:
                if isEspacio(c):
                    pass
                else:
                    Errores.append(Error(fila,columna,c,"Caracter no valido")) 
                    error=True
                    LexemaActual=""
                    estado=0
                
        
        
        
        
        elif estado==2:
            if ord(c)==34:
                Tokens.append(Token("cadena",LexemaActual,fila,columna-len(LexemaActual)))
                estado=0
                LexemaActual=""
            else:
                LexemaActual+=c
        
        
        
        elif estado==5:
            if ord(c)==10:
                estado=0
                LexemaActual=""
               
        
        
        
        elif estado==6:
            if conteo==2 and ord(c)==39:
                conteo=0
                estado=0
            elif ord(c)==39:
                conteo+=1
            


        
        
        
        elif estado==7 and not isEspacio(c):
            if isNumero(c):
                LexemaActual+=c
                estado=8
            else:
                Errores.append(Error(fila,columna,c,"Caracter no valido"))
                error=True
                estado=0
                LexemaActual=""
        
        
        
        elif estado==8:
            if isNumero(c):
                LexemaActual+=c
                estado=8
            elif isEspacio(c):
                Tokens.append(Token("num",LexemaActual,fila,columna-len(LexemaActual)))
                estado=0
                LexemaActual=""
            elif ord(c)==44:
                Tokens.append(Token("num",LexemaActual,fila,columna-len(LexemaActual)))
                Tokens.append(Token("coma",c,fila,columna))
                LexemaActual=""
                estado=0
            elif ord(c)==125:# llave cerrada
                Tokens.append(Token("num",LexemaActual,fila,columna-len(LexemaActual)))
                Tokens.append(Token("llave_cerrada",c,fila,columna))
                LexemaActual=""
                estado=0
            elif ord(c)==41: #parentecis cerrado
                Tokens.append(Token("num",LexemaActual,fila,columna-len(LexemaActual)))
                Tokens.append(Token("parentesis_c",c,fila,columna))
                LexemaActual=""
                estado=0
            elif ord(c)==46:
                LexemaActual+=c
                estado=9
            else:
                Errores.append(Error(fila,columna,c,"Caracter no valido"))
                error=True
                estado=0
                LexemaActual=""
                
        elif estado==9 and not isEspacio(c):
            if isNumero(c):
                LexemaActual+=c
                estado=10
            else:
                Errores.append(Error(fila,columna,c,"se esperaba numero"))
                error=True
                estado=0
                LexemaActual=""
        
        
        
        elif estado==10:
            if isNumero(c):
                LexemaActual+=c
                estado=8
            elif isEspacio(c):
                Tokens.append(Token("num",LexemaActual,fila,columna-len(LexemaActual)))
                estado=0
                LexemaActual=""
            elif ord(c)==44:
                Tokens.append(Token("coma",c,fila,columna))
                LexemaActual=""
                estado=0
            elif ord(c)==125:# llave cerrada
                Tokens.append(Token("llave_cerrada",c,fila,columna))
                LexemaActual=""
                estado=0
            elif ord(c)==41: #parentecis cerrado
                Tokens.append(Token("parentesis_a",c,fila,columna))
                LexemaActual=""
                estado=0
            else:
                Errores.append(Error(fila,columna,c,"Caracter no valido"))
                error=True
                estado=0
                LexemaActual=""

        
        




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
    
    #for e in Errores:
        #print("fila:",e.fila,"columna",e.columna,"caracter:",e.caracter,e.observacion)

    #for t in Tokens:
        #print(t.token,t.lexema,t.fila,t.columna)
    if error:
        print("Si hubo error")
        messagebox.showinfo(message="Se reportaron errores en el analisis por favor vea los reportes",title="Aviso")
    else:
        print("No hubo error")
        analisisSintactico()


def analisisSintactico():
    global Tokens,Errores,Claves,textS
    Claves=[]
    errorS=False
    reg=False
    cla=False
    textS.config(state=NORMAL)
    textS.delete('1.0', END)
    textS.config(state=DISABLED)
    
    for c,token in enumerate(Tokens):
        if Tokens[c].token=="claves":
            if Tokens[c+1].token=="igual":
                if Tokens[c+2].token=="Corchete_a":
                    iterador=c+3
                    nocla=0
                    while Tokens[iterador].token!="Corchete_c":
                        if Tokens[iterador].token=="cadena":
                            if Tokens[iterador+1].token=="coma":
                                Claves.append(clave(Tokens[iterador].lexema,nocla))
                            elif Tokens[iterador+1].token=="Corchete_c":
                                Claves.append(clave(Tokens[iterador].lexema,nocla))
                            else:
                                Errores.append(Error(Tokens[iterador+1].fila,Tokens[c+1].columna,Tokens[iterador+1].token,"se esperaba token coma o corchete_c"))
                                errorS=True
                        elif Tokens[iterador].token=="coma":
                            pass

                        iterador+=1
                        nocla+=1
                    cla=True
                else:
                    Errores.append(Error(Tokens[c+2].fila,Tokens[c+2].columna,Tokens[c+2].token,"se esperaba token Corchete_a"))
                    errorS=True
            else:
                Errores.append(Error(Tokens[c+1].fila,Tokens[c+1].columna,Tokens[c+1].token,"se esperaba token igual"))
                errorS=True
        
        
        
        elif Tokens[c].token=="registros":
            comp=False
            if Tokens[c+1].token=="igual":
                if Tokens[c+2].token=="Corchete_a":
                    iterador=c+3
                    llave=False
                    noreg=0
                    while Tokens[iterador+1].token!="Corchete_c":
                        if Tokens[iterador].token=="llave_abierta":
                            llave=True
                        elif Tokens[iterador].token=="num" and llave:
                            if Tokens[iterador+1].token=="coma" or Tokens[iterador+1].token=="llave_cerrada":
                                if noreg<len(Claves):
                                    Claves[noreg].insertar(Tokens[iterador].lexema)
                                    noreg+=1
                                else:
                                    comp=True
                        elif Tokens[iterador].token=="cadena" and llave:
                            if Tokens[iterador+1].token=="coma" or Tokens[iterador+1].token=="llave_cerrada":
                                if noreg<len(Claves):
                                    Claves[noreg].insertar(Tokens[iterador].lexema)
                                    noreg+=1
                                else:
                                    comp=True
                        elif Tokens[iterador].token=="llave_cerrada" and llave:
                            noreg=0
                            llave=False

                        iterador+=1
                    reg=True
                
                else:
                    Errores.append(Error(Tokens[c+2].fila,Tokens[c+2].columna,Tokens[c+2].token,"se esperaba token Corchete_a"))
                    errorS=True
            else:
                Errores.append(Error(Tokens[c+1].fila,Tokens[c+1].columna,Tokens[c+1].token,"se esperaba token igual"))
                errorS=True
            if comp:
                reg=False
                textS.config(state=NORMAL)
                textS.insert(END,"Vinieron mas registros que claves en alguna fila\n")
                textS.config(state=DISABLED)
        

        elif Tokens[c].token=="imprimir":
            if Tokens[c+1].token=="parentesis_a":
                if Tokens[c+2].token=="cadena":
                    if Tokens[c+3].token=="parentesis_c":
                        if Tokens[c+4].token=="punto_coma":
                            textS.config(state=NORMAL)
                            textS.insert(END,Tokens[c+2].lexema)
                            textS.config(state=DISABLED)
                        else:
                            Errores.append(Error(Tokens[c+4].fila,Tokens[c+4].columna,Tokens[c+4].token,"se esperaba token punto_coma"))
                            errorS=True
                    else:
                        Errores.append(Error(Tokens[c+3].fila,Tokens[c+3].columna,Tokens[c+3].token,"se esperaba token parentesis_c"))
                        errorS=True
                else:
                    Errores.append(Error(Tokens[c+2].fila,Tokens[c+2].columna,Tokens[c+2].token,"se esperaba token cadena"))
                    errorS=True
            else:
                Errores.append(Error(Tokens[c+1].fila,Tokens[c+1].columna,Tokens[c+1].token,"se esperaba token parentesis_a"))
                errorS=True

        elif Tokens[c].token=="imprimirln":
            if Tokens[c+1].token=="parentesis_a":
                if Tokens[c+2].token=="cadena":
                    if Tokens[c+3].token=="parentesis_c":
                        if Tokens[c+4].token=="punto_coma":
                            textS.config(state=NORMAL)
                            textS.insert(END,Tokens[c+2].lexema+"\n")
                            textS.config(state=DISABLED)
                        else:
                            Errores.append(Error(Tokens[c+4].fila,Tokens[c+4].columna,Tokens[c+4].token,"se esperaba token punto_coma"))
                            errorS=True
                    else:
                        Errores.append(Error(Tokens[c+3].fila,Tokens[c+3].columna,Tokens[c+3].token,"se esperaba token parentesis_c"))
                        errorS=True
                else:
                    Errores.append(Error(Tokens[c+2].fila,Tokens[c+2].columna,Tokens[c+2].token,"se esperaba token cadena"))
                    errorS=True
            else:
                Errores.append(Error(Tokens[c+1].fila,Tokens[c+1].columna,Tokens[c+1].token,"se esperaba token parentesis_a"))
                errorS=True

        elif Tokens[c].token=="conteo":
            if reg and cla:
                if Tokens[c+1].token=="parentesis_a":
                    if Tokens[c+2].token=="parentesis_c":
                        if Tokens[c+3].token=="punto_coma":
                            largo=len(Claves[0].registros)
                            textS.config(state=NORMAL)
                            textS.insert(END,str(largo)+"\n")
                            textS.config(state=DISABLED)
                        else:
                            Errores.append(Error(Tokens[c+3].fila,Tokens[c+3].columna,Tokens[c+3].token,"se esperaba token punto_coma"))
                            errorS=True
                    else:
                        Errores.append(Error(Tokens[c+2].fila,Tokens[c+2].columna,Tokens[c+2].token,"se esperaba token parentesis_c"))
                        errorS=True
                else:
                    Errores.append(Error(Tokens[c+1].fila,Tokens[c+1].columna,Tokens[c+1].token,"se esperaba token parentesis_a"))
                    errorS=True
            
            else:
                textS.config(state=NORMAL)
                textS.insert(END,"no se puede ejecutar conteo, los datos son incorrectos")
                textS.config(state=DISABLED)

        elif Tokens[c].token=="promedio":
            if reg and cla:
                if Tokens[c+1].token=="parentesis_a":
                    if Tokens[c+2].token=="cadena":
                        if Tokens[c+3].token=="parentesis_c":
                            if Tokens[c+4].token=="punto_coma":
                                for cla in Claves:
                                    if cla.clave==Tokens[c+2].lexema:
                                        try:
                                            columna=cla.registros
                                            recuento=len(columna)
                                            promedio=0
                                            for valor in columna:
                                                promedio+=float(valor)
                                            textS.config(state=NORMAL)
                                            textS.insert(END,str(promedio/recuento))
                                            textS.config(state=DISABLED)
                                        except:
                                            textS.config(state=NORMAL)
                                            textS.insert(END,"comando promedio, encontro una cadena")
                                            textS.config(state=DISABLED)
                            else:
                                Errores.append(Error(Tokens[c+4].fila,Tokens[c+4].columna,Tokens[c+4].token,"se esperaba token punto_coma"))
                                errorS=True
                        else:
                            Errores.append(Error(Tokens[c+3].fila,Tokens[c+3].columna,Tokens[c+3].token,"se esperaba token parentesis_c"))
                            errorS=True
                    else:
                        Errores.append(Error(Tokens[c+2].fila,Tokens[c+2].columna,Tokens[c+2].token,"se esperaba token cadena"))
                        errorS=True
                else:
                    Errores.append(Error(Tokens[c+1].fila,Tokens[c+1].columna,Tokens[c+1].token,"se esperaba token parentesis_a"))
                    errorS=True
            
            else:
                textS.config(state=NORMAL)
                textS.insert(END,"no se puede ejecutar promedio, los datos son incorrectos")
                textS.config(state=DISABLED)

        elif Tokens[c].token=="contarsi":
            if reg and cla:
                if Tokens[c+1].token=="parentesis_a":
                    if Tokens[c+2].token=="cadena":
                        if Tokens[c+3].token=="coma":
                            if Tokens[c+4].token=="cadena" or Tokens[c+4].token=="num":
                                if Tokens[c+5].token=="parentesis_c":
                                    if Tokens[c+6].token=="punto_coma":
                                        for cla in Claves:
                                            if cla.clave==Tokens[c+2].lexema:
                                                try:
                                                    columna=cla.registros
                                                    recuento=len(columna)
                                                    conteo=0
                                                    for valor in columna:
                                                        if valor==Tokens[c+4].lexema:
                                                            conteo+=1
                                                    textS.config(state=NORMAL)
                                                    textS.insert(END,str(conteo))
                                                    textS.config(state=DISABLED)
                                                except:
                                                    textS.config(state=NORMAL)
                                                    textS.insert(END,"comando contarsi, encontro una cadena")
                                                    textS.config(state=DISABLED)
                                    else:
                                        Errores.append(Error(Tokens[c+6].fila,Tokens[c+6].columna,Tokens[c+6].token,"se esperaba token punto_coma"))
                                        errorS=True
                                else:
                                    Errores.append(Error(Tokens[c+5].fila,Tokens[c+5].columna,Tokens[c+5].token,"se esperaba token parentesis_c"))
                                    errorS=True
                            else:
                                Errores.append(Error(Tokens[c+4].fila,Tokens[c+4].columna,Tokens[c+4].token,"se esperaba token cadena o num"))
                                errorS=True
                        else:
                            Errores.append(Error(Tokens[c+3].fila,Tokens[c+3].columna,Tokens[c+3].token,"se esperaba token coma"))
                            errorS=True
                    else:
                        Errores.append(Error(Tokens[c+2].fila,Tokens[c+2].columna,Tokens[c+2].token,"se esperaba token cadena"))
                        errorS=True
                else:
                    Errores.append(Error(Tokens[c+1].fila,Tokens[c+1].columna,Tokens[c+1].token,"se esperaba token parentesis_a"))
                    errorS=True
            
            else:
                textS.config(state=NORMAL)
                textS.insert(END,"no se puede ejecutar contarsi, los datos son incorrectos")
                textS.config(state=DISABLED)

        elif Tokens[c].token=="sumar":
            if reg and cla:
                if Tokens[c+1].token=="parentesis_a":
                    if Tokens[c+2].token=="cadena":
                        if Tokens[c+3].token=="parentesis_c":
                            if Tokens[c+4].token=="punto_coma":
                                for cla in Claves:
                                    if cla.clave==Tokens[c+2].lexema:
                                        try:
                                            columna=cla.registros
                                            recuento=len(columna)
                                            promedio=0
                                            for valor in columna:
                                                promedio+=float(valor)
                                            textS.config(state=NORMAL)
                                            print(promedio)
                                            textS.insert(END,str(promedio))
                                            textS.config(state=DISABLED)
                                        except:
                                            textS.config(state=NORMAL)
                                            textS.insert(END,"comando sumar, encontro una cadena")
                                            textS.config(state=DISABLED)
                            else:
                                Errores.append(Error(Tokens[c+4].fila,Tokens[c+4].columna,Tokens[c+4].token,"se esperaba token punto_coma"))
                                errorS=True
                        else:
                            Errores.append(Error(Tokens[c+3].fila,Tokens[c+3].columna,Tokens[c+3].token,"se esperaba token parentesis_c"))
                            errorS=True
                    else:
                        Errores.append(Error(Tokens[c+2].fila,Tokens[c+2].columna,Tokens[c+2].token,"se esperaba token cadena"))
                        errorS=True
                else:
                    Errores.append(Error(Tokens[c+1].fila,Tokens[c+1].columna,Tokens[c+1].token,"se esperaba token parentesis_a"))
                    errorS=True
            
            else:
                textS.config(state=NORMAL)
                textS.insert(END,"no se puede ejecutar sumar, los datos son incorrectos")
                textS.config(state=DISABLED)

        elif Tokens[c].token=="datos":
            if reg and cla:
                if Tokens[c+1].token=="parentesis_a":
                    if Tokens[c+2].token=="parentesis_c":
                        if Tokens[c+3].token=="punto_coma":
                            for cla in Claves:
                                textS.config(state=NORMAL)
                                textS.insert(END,cla.clave+"\t\t")
                                textS.config(state=DISABLED)
                            textS.config(state=NORMAL)
                            textS.insert(END,"\n")
                            textS.config(state=DISABLED)
                            cant=len(Claves[0].registros)
                            for i in range(cant):
                                for c in Claves:
                                    textS.config(state=NORMAL)
                                    textS.insert(END,c.registros[i]+"\t\t")
                                    textS.config(state=DISABLED)
                                textS.config(state=NORMAL)
                                textS.insert(END,"\n")
                                textS.config(state=DISABLED)
                        else:
                            Errores.append(Error(Tokens[c+3].fila,Tokens[c+3].columna,Tokens[c+3].token,"se esperaba token punto_coma"))
                            errorS=True
                    else:
                        Errores.append(Error(Tokens[c+2].fila,Tokens[c+2].columna,Tokens[c+2].token,"se esperaba token parentesis_c"))
                        errorS=True
                else:
                    Errores.append(Error(Tokens[c+1].fila,Tokens[c+1].columna,Tokens[c+1].token,"se esperaba token parentesis_a"))
                    errorS=True
            
            else:
                textS.config(state=NORMAL)
                textS.insert(END,"no se puede ejecutar datos, los datos son incorrectos")
                textS.config(state=DISABLED)
            
            
            
            # for cla in Claves:
            #     for g in cla.registros:
            #         print(g)
            #     print("otra columna")

        elif Tokens[c].token=="max":
            if reg and cla:
                if Tokens[c+1].token=="parentesis_a":
                    if Tokens[c+2].token=="cadena":
                        if Tokens[c+3].token=="parentesis_c":
                            if Tokens[c+4].token=="punto_coma":
                                for cla in Claves:
                                    if cla.clave==Tokens[c+2].lexema:
                                        try:
                                            columna=cla.registros
                                            for i in range(1,len(columna)):
                                                for j in range(0,len(columna)-i):
                                                    if(float(columna[j+1])>float(columna[j])):
                                                        aux1=columna[j]
                                                        columna[j]=columna[j+1]
                                                        columna[j+1]=aux1
                                            textS.config(state=NORMAL)
                                            #print(columna)
                                            textS.insert(END,str(columna[0]))
                                            textS.config(state=DISABLED)
                                        except:
                                            textS.config(state=NORMAL)
                                            textS.insert(END,"comando max, encontro una cadena")
                                            textS.config(state=DISABLED)
                            else:
                                Errores.append(Error(Tokens[c+4].fila,Tokens[c+4].columna,Tokens[c+4].token,"se esperaba token punto_coma"))
                                errorS=True
                        else:
                            Errores.append(Error(Tokens[c+3].fila,Tokens[c+3].columna,Tokens[c+3].token,"se esperaba token parentesis_c"))
                            errorS=True
                    else:
                        Errores.append(Error(Tokens[c+2].fila,Tokens[c+2].columna,Tokens[c+2].token,"se esperaba token cadena"))
                        errorS=True
                else:
                    Errores.append(Error(Tokens[c+1].fila,Tokens[c+1].columna,Tokens[c+1].token,"se esperaba token parentesis_a"))
                    errorS=True
            
            else:
                textS.config(state=NORMAL)
                textS.insert(END,"no se puede ejecutar max, los datos son incorrectos")
                textS.config(state=DISABLED)

        elif Tokens[c].token=="min":
            if reg and cla:
                if Tokens[c+1].token=="parentesis_a":
                    if Tokens[c+2].token=="cadena":
                        if Tokens[c+3].token=="parentesis_c":
                            if Tokens[c+4].token=="punto_coma":
                                for cla in Claves:
                                    if cla.clave==Tokens[c+2].lexema:
                                        try:
                                            columna=cla.registros
                                            for i in range(1,len(columna)):
                                                for j in range(0,len(columna)-i):
                                                    if(float(columna[j+1])<float(columna[j])):
                                                        aux1=columna[j]
                                                        columna[j]=columna[j+1]
                                                        columna[j+1]=aux1
                                            textS.config(state=NORMAL)
                                            #print(columna)
                                            textS.insert(END,str(columna[0]))
                                            textS.config(state=DISABLED)
                                        except:
                                            textS.config(state=NORMAL)
                                            textS.insert(END,"comando min, encontro una cadena")
                                            textS.config(state=DISABLED)
                            else:
                                Errores.append(Error(Tokens[c+4].fila,Tokens[c+4].columna,Tokens[c+4].token,"se esperaba token punto_coma"))
                                errorS=True
                        else:
                            Errores.append(Error(Tokens[c+3].fila,Tokens[c+3].columna,Tokens[c+3].token,"se esperaba token parentesis_c"))
                            errorS=True
                    else:
                        Errores.append(Error(Tokens[c+2].fila,Tokens[c+2].columna,Tokens[c+2].token,"se esperaba token cadena"))
                        errorS=True
                else:
                    Errores.append(Error(Tokens[c+1].fila,Tokens[c+1].columna,Tokens[c+1].token,"se esperaba token parentesis_a"))
                    errorS=True
            
            else:
                textS.config(state=NORMAL)
                textS.insert(END,"no se puede ejecutar min, los datos son incorrectos")
                textS.config(state=DISABLED)

        elif Tokens[c].token=="exportarReporte":
            if reg and cla:
                if Tokens[c+1].token=="parentesis_a":
                    if Tokens[c+2].token=="cadena":
                        if Tokens[c+3].token=="parentesis_c":
                            if Tokens[c+4].token=="punto_coma":
                                try:
                                    tablaHTML(Tokens[c+2].lexema)
                                except:
                                    textS.config(state=NORMAL)
                                    textS.insert(END,"Ocurrio un error al ejecutar exportarReporte")
                                    textS.config(state=DISABLED)
                            else:
                                Errores.append(Error(Tokens[c+4].fila,Tokens[c+4].columna,Tokens[c+4].token,"se esperaba token punto_coma"))
                                errorS=True
                        else:
                            Errores.append(Error(Tokens[c+3].fila,Tokens[c+3].columna,Tokens[c+3].token,"se esperaba token parentesis_c"))
                            errorS=True
                    else:
                        Errores.append(Error(Tokens[c+2].fila,Tokens[c+2].columna,Tokens[c+2].token,"se esperaba token cadena"))
                        errorS=True
                else:
                    Errores.append(Error(Tokens[c+1].fila,Tokens[c+1].columna,Tokens[c+1].token,"se esperaba token parentesis_a"))
                    errorS=True
            
            else:
                textS.config(state=NORMAL)
                textS.insert(END,"no se puede ejecutar exportarReporte, los datos son incorrectos")
                textS.config(state=DISABLED)

    if errorS:
        print("Si hubo error")
        messagebox.showinfo(message="Se reportaron errores en el analisis Sintactico por favor vea el reporte de errores",title="Aviso")
    else:
        print("No hubo error")
        messagebox.showinfo(message="Analisis realizado con exito y sin errores",title="Aviso")




def ReporteHtmlTokens():
    global Tokens,Errores,analizado
    if analizado:
        f=open("ReporteTokens.html","w",encoding='UTF-8')
        inicio="""
        <!doctype html>
        <html lang="en">
        <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We" crossorigin="anonymous">

        <title>Reporte Proyecto 1</title>
        </head>
        <style>
        .titulo{
            text-align: center;
            background-color: aqua;
            padding: 8px;
        }
        .cuerpo{
            background-color: white;
        }
        .contenido{
            color: white;
        }
        .inscritos{
            color:white;
            background-color: teal;
            padding: 8px;
        }
        .tabla{
            width:80%; 
            text-align: center; 
            margin-right: auto; 
            margin-left: auto;
            padding: 15px;
        }
        h1,h2{
            text-align:center;
            padding:8px;
        }
        </style>
        <body class="cuerpo">
        <div class="titulo">
        <h1>Reportes</h1></div>"""

        inicio+="<div><h2>Tabla de Tokens</h2>"

        inicio+="<div class=\"tabla\"><table class=\"table table-dark table-hover\">"
        inicio+="""<thead><tr>
        <th scope="col">No.</th>
        <th scope="col">TOKEN</th>
        <th scope="col">LEXEMA</th>
        <th scope="col">FILA</th>
        <th scope="col">COLUMNA</th>
        </tr></thead><tbody>"""
                
        for i in range(len(Tokens)):
            inicio+="<tr>"
            inicio+="<th scope=\"row\">"+str(i+1)+"</th>"
            inicio+="<td>"+Tokens[i].token+"</td>"
            inicio+="<td>"+Tokens[i].lexema+"</td>"
            inicio+="<td>"+str(Tokens[i].fila)+"</td>"
            inicio+="<td>"+str(Tokens[i].columna)+"</td>"
            inicio+="</tr>"
                
        inicio+="</tbody></table></div></div>"
        #------------------------------------------------------------------------------------------------
        




        fin="""
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-U1DAWAznBHeqEIlVSCgzq+c9gqGAJn5c/t99JyeKa9xxaYpSvHU5awsuZVVFIhvj" crossorigin="anonymous"></script>
        </body>
        </html>"""
        f.write(inicio+fin)
        f.close()
        startfile("ReporteTokens.html")
    else:
        messagebox.showerror(message="No se ha analizado ningun archivo",title="Error")

def ReporteHtmlErrores():
    global Tokens,Errores,analizado
    if analizado:
        f=open("ReporteErrores.html","w",encoding='UTF-8')
        inicio="""
        <!doctype html>
        <html lang="en">
        <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We" crossorigin="anonymous">

        <title>Reporte Proyecto 1</title>
        </head>
        <style>
        .titulo{
            text-align: center;
            background-color: aqua;
            padding: 8px;
        }
        .cuerpo{
            background-color: white;
        }
        .contenido{
            color: white;
        }
        .inscritos{
            color:white;
            background-color: teal;
            padding: 8px;
        }
        .tabla{
            width:80%; 
            text-align: center; 
            margin-right: auto; 
            margin-left: auto;
            padding: 15px;
        }
        h1,h2{
            text-align:center;
            padding:8px;
        }
        </style>
        <body class="cuerpo">
        <div class="titulo">
        <h1>Reportes</h1></div>"""

        inicio+="<div><h2>Tabla de Errores</h2>"

        inicio+="<div class=\"tabla\"><table class=\"table table-dark table-hover\">"
        inicio+="""<thead><tr>
        <th scope="col">No.</th>
        <th scope="col">FILA</th>
        <th scope="col">COLUMNA</th>
        <th scope="col">CARACTER</th>
        <th scope="col">OBSERVACION</th>
        </tr></thead><tbody>"""
                
        for i in range(len(Errores)):
            inicio+="<tr>"
            inicio+="<th scope=\"row\">"+str(i+1)+"</th>"
            inicio+="<td>"+str(Errores[i].fila)+"</td>"
            inicio+="<td>"+str(Errores[i].columna)+"</td>"
            inicio+="<td>"+Errores[i].caracter+"</td>"
            inicio+="<td>"+Errores[i].observacion+"</td>"
            inicio+="</tr>"
                
        inicio+="</tbody></table></div></div>"
        




        fin="""
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-U1DAWAznBHeqEIlVSCgzq+c9gqGAJn5c/t99JyeKa9xxaYpSvHU5awsuZVVFIhvj" crossorigin="anonymous"></script>
        </body>
        </html>"""
        f.write(inicio+fin)
        f.close()
        startfile("ReporteErrores.html")
    else:
        messagebox.showerror(message="No se ha analizado ningun archivo",title="Error")

def tablaHTML(titulo):
    global Claves
    f=open("ReporteTabla.html","w",encoding='UTF-8')
    inicio="""
    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We" crossorigin="anonymous">

    <title>Tabla de registros</title>
    </head>
    <style>
    .titulo{
        text-align: center;
        background-color: aqua;
        padding: 8px;
    }
    .cuerpo{
        background-color: white;
    }
    .contenido{
        color: white;
    }
    .inscritos{
        color:white;
        background-color: teal;
        padding: 8px;
    }
    .tabla{
        width:80%; 
        text-align: center; 
        margin-right: auto; 
        margin-left: auto;
        padding: 15px;
    }
    h1,h2{
        text-align:center;
        padding:8px;
    }
    </style>
    <body class="cuerpo">
    <div class="titulo">
    <h1>Reporte Registro</h1></div>"""

    inicio+=f"<div><h2>{titulo}</h2>"

    inicio+="<div class=\"tabla\"><table class=\"table table-dark table-hover\">"
    
    inicio+="<thead><tr>"
    for cla in Claves:
        inicio+=f"<th scope=\"col\">{cla.clave}</th>"
    inicio+="</tr></thead><tbody>"
    cant=len(Claves[0].registros)
    for i in range(cant):
        inicio+="<tr>"
        for c in Claves:
            inicio+="<td>"+str(c.registros[i])+"</td>"
        inicio+="</tr>"
    
            
    inicio+="</tbody></table></div></div>"
    




    fin="""
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-U1DAWAznBHeqEIlVSCgzq+c9gqGAJn5c/t99JyeKa9xxaYpSvHU5awsuZVVFIhvj" crossorigin="anonymous"></script>
    </body>
    </html>"""
    f.write(inicio+fin)
    f.close()
    startfile("ReporteTabla.html")

if __name__=='__main__':
    generarVentana()