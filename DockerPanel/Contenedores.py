from tkinter import *
from contenido import Contenido
import subprocess


class Contenedores(Contenido):
    """Subclase de contenido para el Item Contenedores"""
    def __init__(self):
        self.icon = "img/container.png"
        Contenido.__init__(self, None, self.icon)
        self.properties("Contenedores")
        self.entry = "docker container ls -a"
        self.contId = []
        self.chckout = StringVar()
        self.comando(self.contId, 0, self.entry)
        self.acciones()
# ######## A partir de aquí se crean métodos para la propia subclase ############
    def __run_cont(self):
        """Incializar contenedor"""
        self.chckArray(self.contId)
        if self.empty is False:
            for i in self.contId:
                cmd = "docker container start " + i  # Comando a ejecutar con cada Item del array
                print(cmd)
                subprocess.Popen(cmd, shell=TRUE)
            self.reload(self.contId, 0, self.entry)

    def __stop_cont(self):
        """Para un contenedor"""
        self.chckArray(self.contId)
        if self.empty is False:
            for i in self.contId:
                cmd = "docker container stop " + i
                print(cmd)
                subprocess.Popen(cmd, shell=TRUE)
            self.reload(self.contId, 0, self.entry)

    def __pause_cont(self):
        """Pausar contenedor"""
        self.chckArray(self.contId)
        if self.empty is False:
            for i in self.contId:
                cmd = "docker container pause " + i
                print(cmd)
                subprocess.Popen(cmd, shell=TRUE)
            self.reload(self.contId, 0, self.entry)

    def __restart_cont(self):
        """Reiniciar contenedor"""
        self.chckArray(self.contId)
        if self.empty is False:
            for i in self.contId:
                cmd = "docker container restart " + i
                print(cmd)
                subprocess.Popen(cmd, shell=TRUE)
            self.reload(self.contId, 0, self.entry)

    def __rm_cont(self):
        """Borrar contenedor"""
        self.chckArray(self.contId)
        if self.empty is False:
            for i in self.contId:
                cmd = "docker container rm " + i
                print(cmd)
                subprocess.Popen(cmd, shell=TRUE)
            self.reload(self.contId, 0, self.entry)

    def __prune_cont(self):
        """Borrar todos los contenedores"""
        self.chckArray(self.contId)
        if self.empty is False:
            cmd = "docker container prune -f"
            print(cmd)
            subprocess.Popen(cmd, shell=TRUE)
            self.reload(self.contId, 0, self.entry)

    def __choose_img(self):
        """Ventana emergente para elegir imagen"""
        chooseW = Toplevel(self, bg="#18152C")
        self.des_boton(self.neBtn)
        chooseF = LabelFrame(chooseW, text="Seleccion de imagen", bg="#18152C", fg="white")
        chooseF.pack(fill=X)
        lbCont = Listbox(chooseW, selectmode='single', selectbackground="#4585C2", height="5", bg="#18152C", fg="white")
        self.selImg = StringVar()  # ID de imagen elegida
        self.sp = StringVar()  # Ejecución en segundo plano
        self.rm = StringVar()  # Borrar contenedor al terminar proceso
        self.nnCont = StringVar()  # Nombre del contenedor
        proc = subprocess.Popen("docker image ls", stdout=subprocess.PIPE)
        p = True
        for line in proc.stdout.readlines():
            if p:
                Label(self.frameP, text=line, bg="#18152C", fg="white").pack(padx=10)
                p = False
            else:
                line = line.decode("utf-8")
                lbCont.insert(END, str(line))
        lbCont.bind("<<ListboxSelect>>", self.__cont_choosed)
        lbCont.pack(side="top", fill="both", expand=True, ipadx=10, padx=10, pady=10)
        Label(chooseW, text="Nombre del Contenedor", padx=5, pady=5,fg="white", bg="#18152C").pack(side=LEFT, padx=5)
        Entry(chooseW, textvariable=self.nnCont).pack(side=LEFT, padx=5)
        Checkbutton(chooseW, text="Segundo Plano", onvalue=" -d ", offvalue="", variable=self.sp, fg="white",
                    bg="#18152C").pack()
        Checkbutton(chooseW, text="Borrar contenedor al dejar de ejecutarse", onvalue=" --rm ", offvalue="",
                    variable=self.rm, fg="white", bg="#18152C").pack()
        Button(chooseW, text="Ok", command=lambda: [self.__new_cont(), chooseW.destroy()]).pack(fill=X)
        # Hay botones que al ejecutarse cumplen varias funciones
        Button(chooseW, text="Cancelar", command=lambda: [chooseW.destroy(), self.hab_boton(self.neBtn)]).pack(fill=X)

    def __cont_choosed(self, event):
        """Para guardar ID de la imagen elegida"""
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        if len(value) != 0:
            self.selImg = value.split()[self.posId]

    def __new_cont(self):
        """Inicializa el nuevo contenedor"""
        self.chckArray(self.selImg)
        if self.empty is False:
            cmd = "docker run " + self.sp.get() + self.rm.get() + "--name " + self.nnCont.get() + " " + self.selImg
            print(cmd)
            subprocess.run(cmd, shell=True)
            self.hab_boton(self.neBtn)
            self.reload(self.contId, 0, self.entry)
        else:
            self.__choose_img()

    def acciones(self):
        """Este método nos crea los botones con sus debidas acciones"""
        botones = Frame(self, bg="#18152C")
        botones.pack(side=BOTTOM, pady=10)
        # Los botones que se tengan que deshabilitar en algun momento pasar a ser propiedades de la clase
        self.neBtn = Button(botones, text="NEW", relief="groove", cursor="hand2", fg="blue", bg="white", command=lambda : self.__choose_img())
        self.neBtn.pack(side=LEFT, padx=5)
        Button(botones, text="RUN", relief="groove", cursor="hand2", fg="blue", bg="white",
               command=lambda: self.__run_cont()).pack(side=LEFT, padx=5)
        Button(botones, text="STOP", relief="groove", cursor="hand2", fg="blue", bg="white",
               command=lambda: self.__stop_cont()).pack(side=LEFT, padx=5)
        Button(botones, text="RESTART", relief="groove", cursor="hand2", fg="blue", bg="white",
               command=lambda: self.__restart_cont()).pack(side=LEFT, padx=5)
        Button(botones, text="PAUSE", relief="groove", cursor="hand2", fg="blue", bg="white",
               command=lambda: self.__pause_cont()).pack(side=LEFT, padx=5)
        Button(botones, text="REMOVE", relief="groove", cursor="hand2", fg="blue",bg="white",
               command=lambda: self.__rm_cont()).pack(side=LEFT, padx=5)
        Button(botones, text="PRUNE", relief="groove", cursor="hand2", fg="blue", bg="white",
               command=lambda: self.__prune_cont()).pack(side=LEFT, padx=5)
        Button(botones, text="INSPECT", relief="groove", cursor="hand2", fg="blue", bg="white",
               command=lambda: self.toJson(self.contId)).pack(side=LEFT, padx=5)
        Button(botones, text="RELOAD", relief="groove", cursor="hand2", fg="blue", bg="white",
               command=lambda: self.reload(self.contId, 0, self.entry)).pack(side=LEFT, padx=5)
