from tkinter import *
import subprocess
import time


class Contenido(Toplevel):
    """En esta clase crearemos las ventanas para manejar cada item NO SON ROOT"""
    def __init__(self, parent, logo):
        Toplevel.__init__(self)
        Toplevel.config(self, bg="#18152C")
        self.icon = logo
        self.__content()

    def __content(self):
        """Este método se encarga de crear un Frame en el cual se aloja el resto de Widgets"""
        self.frameP = Frame(self, bg="#18152C")
        self.frameP.pack(fill=X, expand=1)
        # Aquí insertamos la imagen que se nos pasa para cada nueva ventana
        img = PhotoImage(file=self.icon)
        photo = Label(self.frameP, image=img, bg="#18152C")
        photo.img = img
        photo.pack(pady=10)

    def properties(self, titulo, dimensions=None):
        """Definimos las propiedades que tendran tanto fijas como opcionales las ventanas que se crearán"""
        self.title(titulo)  # Nombre
        self.geometry(dimensions)  # Dimensiones que tendrá la ventana al iniciarse si se especifica
        icon = PhotoImage(file="icon.png")  # Icono de la ventana, todas tiene el mismo
        self.wm_iconphoto(False, icon)

    def comando(self, array, idout, cmd):
        """Nos permitira visualizar la salida del comando para ver los items que deseemos"""
        self.posId = idout  # idOut pasa a ser una propiedad de la clase
        lb = Listbox(self.frameP, selectmode='single', selectbackground="#4585C2", height="5", bg="#18152C",
                     fg="white")  # Listbox-1
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)  # Comando que se ejecuta
        self.Items = Listbox(self.frameP, selectmode='single', selectbackground="#4585C2", height="5", bg="#18152C",
                             fg="white")  # Listbox-2
        p = True  # Primera linea
        for line in proc.stdout.readlines():
            if p:
                Label(self.frameP, text=line, bg="#18152C", fg="white").pack(padx=10)  # Label para la primera linea,
                # suele ser la cabecera
                p = False
            else:
                # Una vez se inserte la cabecera el resto de Items se añadira al Listbox-1
                line = line.decode("utf-8")  # Linea pasa de binario a string
                lb.insert(END, str(line))  # Se inserta al final del Listbox
        self.array = array  # Array pasado como parametro pasa a ser una propiedad de la clase
        lb.bind("<<ListboxSelect>>", self.__on_selected)  # Asignamos un evento al Listbox-1
        lb.pack(side="top", fill="both", expand=True, ipadx=10, padx=10, pady=10)
        Label(self.frameP, text="ITEMS ELEGIDOS :", bg="#18152C", fg="white").pack()
        self.Items.pack(side="bottom", fill="both", expand=True, ipadx=10, padx=10, pady=10)

    def __on_selected(self, event):
        """Metodo llamado en caso de que un Items haya sido elegido"""
        widget = event.widget  # Almacenamos el evento
        selection = widget.curselection()  # Almacenamos Item elegido
        try:
            # Se almacena el valor de la seleccion
            value = widget.get(selection[0 - 1])
            if len(value) != 0:
                id = value.split()[self.posId]  # Sacamos el ID dentro de valor
                self.__val_to_array(id)
        except:
            # En caso de que value no tenga item elegido, se limpiará el array
            for i in self.array:
                self.array.remove(i)
                # También se borra del Listbox-2
                idIndex = self.Items.get(0, END).index(i)  # Sacamos indice
                self.Items.delete(idIndex)  # Con ese indice se borra del Listbox-2
            print(self.array)  # Los prints son solo para depurar

    def __val_to_array(self, identifier):
        """Miramos si el ID esta en el array o no para añadirse o borrarse"""
        if identifier not in self.array:
            self.array.append(identifier)
            self.Items.insert(END, str(identifier))

        else:
            self.array.remove(identifier)
            idIndex = self.Items.get(0, END).index(identifier)
            self.Items.delete(idIndex)

    def reload(self, array, idOut, cmd):
        """Actualiza el contenido en caso de sufrir cambios"""
        self.frameP.destroy()  # Destruye frame de contenido
        time.sleep(3)  # Pausa de 3 segundos
        self.__content()  # Vuelve a generar el frame de contenido
        self.comando(array, idOut, cmd)  # Volvemos a ejecutar cmd
        array.clear()  # Se limpia el array

    def toJson(self, array):
        """Damos salida a un fichero JSON a los Items elegidos"""
        for ID in array:
            raw = ID + ".json"
            cmd = "docker inspect " + ID + " > jsons/" + raw
            subprocess.run(cmd, shell=True)

    def des_boton(self, *botones):
        """Desahabilita los botones especificados"""
        for boton in botones:
            boton['state'] = DISABLED

    def hab_boton(self, *botones):
        """Habilita los botones especificados"""
        for boton in botones:
            boton['state'] = NORMAL

    def chckArray(self, array):
        """Revisa que el array no este vacio para ejecutar ciertas tareas"""
        self.empty = True  #Propiedad con valor True
        if len(array) != 0:
            self.empty = False
            return self.empty
        else:
            self.advertArray()

    def advertArray(self):
        """Alerta para array vacío"""
        advert = Toplevel(self, bg="#18152C")
        Label(advert, bg="#18152C", fg="white", text="Asegúrese de haber seleccionado un elemento").pack(padx=20,
                                                                                                         pady=10,
                                                                                                         fill=X,
                                                                                                         side=RIGHT)
        img = PhotoImage(file="img/advert.png")
        photo = Label(advert, image=img, bg="#18152C")
        photo.img = img
        photo.pack(side=LEFT, pady=10, padx=10)
