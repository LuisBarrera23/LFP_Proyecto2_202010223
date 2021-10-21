from tkinter import Button,Tk, ttk,filedialog,messagebox,Label

#variables globales
ventana=Tk()
def generarVentana():
    global ventana,canvas,combo,label
    label=Label(ventana, width=135, height=40)
    label.place(x=220,y=80)
    ventana.configure(background="#008080")
    ancho=1200
    alto=700
    x=ventana.winfo_screenwidth()
    #calculamos la coordenada X donde se posicionara la ventana
    x=(x-ancho)/2
    y=ventana.winfo_screenheight()
    #calculamos la coordenada Y donde se posicionara la ventana
    y=(y-alto)/2
    ventana.geometry('%dx%d+%d+%d' % (ancho, alto, x, y))
    ventana.title("Proyecto 2")

    ventana.mainloop()

if __name__=='__main__':
    generarVentana()