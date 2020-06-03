from tkinter import *
from Contenedores import Contenedores
from Volumenes import Volumenes
from Redes import Redes
from Imagenes import Imagenes


class Inicio(Tk):
    """Esta clase crea la ventana ROOT para las siguientes, es la principal en la app"""
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.__parent = parent
        self.title("DockerPanel")
        self.config(bg="#18152C")
        icon = PhotoImage(file="icon.png")
        self.wm_iconphoto(False, icon)
        self.resizable(False, False)
        self.__menu()

        # Obtenemos las medidas de la pantalla.
        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()
        print("Width", windowWidth, "Height", windowHeight)

        # Ajustamos las medidas en comparación con la pantalla
        positionRight = int(self.winfo_screenwidth() / 2.5 - windowWidth / 1)
        positionDown = int(self.winfo_screenheight() / 3 - windowHeight / 1)

        # Posicionamos la ventana
        self.geometry("+{}+{}".format(positionRight, positionDown))

    def __menu(self):
        """Este método monta el contenido del menú principal"""
        menu = Frame(self, bg="#18152C")  # Creamos frame para el contenido
        menu.pack(side=BOTTOM, pady=10, padx=10)
        img = PhotoImage(file="img/Docker-Logo.png")  # Añadimos logo
        logo = Label(menu, image=img, bg="#18152C")
        logo.img = img
        logo.pack(pady=5)
        # Añadimos los botones que llamaran a la clase correspondiente
        Button(menu, text='Contenedores', relief="groove", cursor="hand2", fg="blue", bg="white",
               command=lambda: Contenedores()).pack(fill=X, pady=5)
        Button(menu, text='Volumenes', relief="groove", cursor="hand2", fg="blue", bg="white",
               command=lambda: Volumenes()).pack(fill=X, pady=5)
        Button(menu, text='Imagenes', relief="groove", cursor="hand2", fg="blue", bg="white",
               command=lambda: Imagenes()).pack(fill=X, pady=5)
        Button(menu, text='Redes', relief="groove", cursor="hand2", fg="blue", bg="white",
               command=lambda: Redes()).pack(fill=X, pady=5)
