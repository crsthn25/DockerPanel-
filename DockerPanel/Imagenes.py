#################################################################################################################
#       Autor: Cristhian Bonilla Meruvia                                                                        #
#       Año: 2020                                                                                               #
#################################################################################################################
from tkinter import *
from contenido import Contenido
import subprocess
import time


class Imagenes(Contenido):
    """Subclase de contenido para el Item Redes"""
    def __init__(self):
        self.icon = "img/image.png"
        Contenido.__init__(self, None, self.icon)
        self.properties("Imagenes")
        self.idIm = []  # Array para ID
        self.ntIm = []  # Array para NAME:TAG
        self.__imgcomando("docker image ls")
        self.acciones()

# ######## A partir de aquí se crean métodos para la propia subclase ############
# ######## Imagenes es una subclase especial al tener que trabajar con 2 arrays #

    def __reload(self):
        """Recarga contenido"""
        self.destroy()  # Destruye frame de Imagenes
        time.sleep(3)  # Pausa de 3 segundos
        self.__init__()  # Vuelve a generar el frame de Imagenes

    def __imgcomando(self, cmd):
        """Muestra la salida del comando"""
        outFrame = Frame(self, bg="#18152C")
        outFrame.pack(fill=X)
        lb = Listbox(outFrame, selectmode='single', selectbackground="#4585C2", height="5", bg="#18152C", fg="white")
        self.ItemsId = Listbox(outFrame, selectmode='single', selectbackground="#4585C2", height="5", bg="#18152C",
                               fg="white")
        self.ItemsNT = Listbox(outFrame, selectmode='single', selectbackground="#4585C2", height="5", bg="#18152C",
                               fg="white")
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p = True
        for line in proc.stdout.readlines():
            if p:
                Label(outFrame, text=line, bg="#18152C", fg="white").pack(padx=10)
                p = False
            else:
                line = line.decode("utf-8")
                lb.insert("end", str(line))

        lb.bind("<<ListboxSelect>>", self.__on_sending)
        lb.pack(side=TOP, fill="both", expand=True, ipadx=10, padx=10, pady=10)
        LabelFrame(outFrame, text="ITEMS ELEGIDOS (ID) :", bg="#18152C", fg="white").pack()
        self.ItemsId.pack(side=LEFT, fill="both", expand=True, ipadx=10, padx=10, pady=10)
        LabelFrame(outFrame, text="ITEMS ELEGIDOS(NAME:TAG) :", bg="#18152C", fg="white").pack()
        self.ItemsNT.pack(side=LEFT, fill="both", expand=True, ipadx=10, padx=10, pady=10)

    def __on_sending(self, event):
        """Se saca el ID y N:T para pasarlo al siguiente metodo"""
        widget = event.widget
        selection = widget.curselection()
        try:
            value = widget.get(selection[0 - 1])
            if len(value) != 0:
                ID = value.split()[2]
                nameTag = value.split()[0] + ":" + value.split()[1]
                self.__to_array(ID, nameTag)
        except:
            self.idIm.clear()
            self.ntIm.clear()
            self.ItemsId.delete(0, END)
            self.ItemsNT.delete(0, END)
            print(self.idIm)
            print(self.ntIm)

    def __to_array(self, ID, nameTag):
        """Cuando hemos elegido un Item se almacenan ID y N:T de este en los respectivos arrays"""
        if ID not in self.idIm:
            self.idIm.append(ID)  # ID -> idIm
            self.ItemsId.insert(END, str(ID))  # ID -> Listbox
            print(self.idIm)
        if nameTag not in self.ntIm:
            self.ntIm.append(nameTag)  # N:T -> ntIm
            self.ItemsNT.insert(END, str(nameTag))  # N:T -> Listbox
            print(self.ntIm)
        else:
            self.idIm.remove(ID)  # ID X idIm
            idIndex = self.ItemsId.get(0, END).index(ID)
            self.ItemsId.delete(idIndex)  # ID X Listbox
            self.ntIm.remove(nameTag)  # N:T X ntIm
            ntIndex = self.ItemsNT.get(0, END).index(nameTag)
            self.ItemsNT.delete(ntIndex)  # N:T X Listbox
            print(self.idIm)
            print(self.ntIm)

    def __login(self):
        """Con esto iniciamos sesión con los parametros adecuados"""
        cmd = "docker login -u " + self.user.get() + " -p " + self.passw.get()
        sh = subprocess.run(cmd, shell=True)
        if sh.returncode == 0:
            self.login = 0
            Label(self.wlogin, text="Has iniciado Sesión", fg="green").pack()
            time.sleep(5)
            self.wlogin.destroy()
            self.__push()

    def __bfpush(self):
        """Realizará la comprobacion de un usuario que haya iniciado sesión y en caso contrario se lo pedirá"""
        self.des_boton(self.btPush)
        self.login = subprocess.run("docker login", stderr=subprocess.DEVNULL, shell=True)
        if self.login.returncode == 0:
            self.__push()

        else:  # Lanzamos una nueva ventana para el inicio de sesión
            self.wlogin = Toplevel(self, padx=20, pady=20, bg="#18152C")
            Label(self.wlogin, bg="#18152C", fg="white", text="INICIO SESIÓN").pack()
            Label(self.wlogin, bg="#18152C", fg="white", text="Usuario").pack()
            self.user = StringVar()
            Entry(self.wlogin, textvariable=self.user).pack()
            Label(self.wlogin, bg="#18152C", fg="white", text="Contraseña").pack()
            self.passw = StringVar()
            Entry(self.wlogin, textvariable=self.passw, show="·").pack()
            Button(self.wlogin, relief="groove", cursor="hand2", fg="blue", bg="white", text="OK",
                   command=lambda: self.__login()).pack(pady=5, fill=X)
            Button(self.wlogin, relief="groove", cursor="hand2", fg="blue", bg="white", text="Cerrar",
                   command=lambda: self.wlogin.destroy()).pack(pady=5, fill=X)

    def __push(self):
        """Realizamo el push de una o varias imagenes comprobando que el usuario tenga una sesion iniciada """
        print(self.idIm)
        print(self.ntIm)
        for i in self.ntIm:
            cmd = "docker image push  --disable-content-trust " + i
            print(cmd)
            subprocess.Popen(cmd, shell=TRUE)
            self.hab_boton(self.btPush)
        self.__reload()

    def __rm_img(self):
        """Borrar imagen"""
        for i in self.idIm:
            cmd = "docker image rm " + i + " -f"
            print(cmd)
            subprocess.Popen(cmd, shell=TRUE)
        self.__reload()

    def __delall_img(self):
        """Borrar todas las imagenes"""
        cmd = "docker image prune -f"
        subprocess.Popen(cmd, shell=TRUE)
        self.__reload()

    def __bfbuild(self):
        """Seccion para crear nueva imagen"""
        self.des_boton(self.btBuild)
        subprocess.run("explorer.exe", shell=True)
        pushLf = LabelFrame(self, text="Build de imagen", bg="#18152C", fg="white")
        pushLf.pack(fill=X)
        Label(pushLf, bg="#18152C", fg="white", text="Ruta de Dockerfile:").pack()
        dckrfile = StringVar()
        Entry(pushLf, textvariable=dckrfile).pack(fill=X)
        Label(pushLf, bg="#18152C", fg="white", text="NOMBRE:TAG para imagen:").pack()
        nametag = StringVar()
        Entry(pushLf, bg="#18152C", fg="white", textvariable=nametag).pack(fill=X)
        self.ok = Button(pushLf, relief="groove", cursor="hand2", fg="blue", bg="white", text="OK",
                         command=lambda: self.__build(dckrfile, nametag)).pack(
            pady=5, fill=X)
        Button(pushLf, relief="groove", cursor="hand2", fg="blue", bg="white", text="Cancelar",
               command=lambda: [pushLf.destroy(), self.hab_boton(self.btBuild)]).pack(pady=5, fill=X)

    def __build(self, file, nt):
        """Crear nueva imagen"""
        if len(file.get()) != 0 and len(nt.get()) != 0:
            cmd = "docker build " + file.get() + " -t " + nt.get().lower()
            print(cmd)
            subprocess.Popen(cmd, shell=True)
            self.hab_boton(self.btBuild)

    def acciones(self):
        """Este método nos crea los botones con sus debidas acciones"""
        botones = Frame(self, bg="#18152C")
        botones.pack(side=BOTTOM, pady=10)
        self.btPush = Button(botones, relief="groove", cursor="hand2", fg="blue", bg="white", text="PUSH",
               command=lambda: self.__bfpush())
        self.btPush.pack(side=LEFT, padx=5)
        self.btBuild = Button(botones, relief="groove", cursor="hand2", fg="blue", bg="white", text="BUILD",
               command=lambda: self.__bfbuild())
        self.btBuild.pack(side=LEFT, padx=5)
        Button(botones, relief="groove", cursor="hand2", fg="blue", bg="white", text="REMOVE",
               command=lambda: self.__rm_img()).pack(side=LEFT, padx=5)
        Button(botones, relief="groove", cursor="hand2", fg="blue", bg="white", text="PRUNE",
               command=lambda: self.__delall_img()).pack(side=LEFT, padx=5)
        Button(botones, text="INSPECT", relief="groove", cursor="hand2", fg="blue", bg="white",
               command=lambda: self.toJson(self.idIm)).pack(side=LEFT, padx=5)
