from tkinter import Button, Text,Tk, ttk,filedialog,messagebox,Label,Scrollbar
from tkinter import *
from os import startfile
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
    b3=Button(ventana,text="Reporte de Errores",command=ReporteHtmlErrores,font=("Verdana",10),borderwidth=3,background="beige").place(x=20,y=300,height=40,width=150)
    b4=Button(ventana,text="Reporte de Tokens",command=ReporteHtmlTokens,font=("Verdana",10),borderwidth=3,background="beige").place(x=20,y=360,height=40,width=150)
    
    
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
                Tokens.append(Token("parentesis_a",c,fila,columna))
                if LexemaActual=="imprimir":
                    Tokens.append(Token("imprimir",LexemaActual,fila,columna-len(LexemaActual)))
                    LexemaActual=""
                    estado=0
                elif LexemaActual=="imprimirln":
                    Tokens.append(Token("imprimirln",LexemaActual,fila,columna-len(LexemaActual)))
                    LexemaActual=""
                    estado=0
                elif LexemaActual=="conteo":
                    Tokens.append(Token("conteo",LexemaActual,fila,columna-len(LexemaActual)))
                    LexemaActual=""
                    estado=0
                elif LexemaActual=="promedio":
                    Tokens.append(Token("promedio",LexemaActual,fila,columna-len(LexemaActual)))
                    LexemaActual=""
                    estado=0
                elif LexemaActual=="contarsi":
                    Tokens.append(Token("contarsi",LexemaActual,fila,columna-len(LexemaActual)))
                    LexemaActual=""
                    estado=0
                elif LexemaActual=="datos":
                    Tokens.append(Token("datos",LexemaActual,fila,columna-len(LexemaActual)))
                    LexemaActual=""
                    estado=0
                elif LexemaActual=="leidos.sumar" or LexemaActual=="leídos.sumar":
                    Tokens.append(Token("leidossumar",LexemaActual,fila,columna-len(LexemaActual)))
                    LexemaActual=""
                    estado=0
                elif LexemaActual=="max":
                    Tokens.append(Token("max",LexemaActual,fila,columna-len(LexemaActual)))
                    LexemaActual=""
                    estado=0
                elif LexemaActual=="min":
                    Tokens.append(Token("min",LexemaActual,fila,columna-len(LexemaActual)))
                    LexemaActual=""
                    estado=0
                elif LexemaActual=="exportarReporte":
                    Tokens.append(Token("min",LexemaActual,fila,columna-len(LexemaActual)))
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
            comilla=False
            if conteo==2 and ord(c)==39 and comilla:
                conteo=0
                estado=0
            elif ord(c)==39:
                conteo+=1
                comilla=True
            else:
                Errores.append(Error(fila,columna,c,"Se esperaba comilla")) 
                error=True
                LexemaActual=""
                estado=0


        
        
        
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
        messagebox.showinfo(message="Se realizo el analisis con exito y sin errores",title="Aviso")

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
        startfile("Reporte.html")
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
        startfile("Reporte.html")
    else:
        messagebox.showerror(message="No se ha analizado ningun archivo",title="Error")

if __name__=='__main__':
    generarVentana()