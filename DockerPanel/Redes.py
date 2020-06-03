#################################################################################################################
#       Autor: Cristhian Bonilla Meruvia                                                                        #
#       Año: 2020                                                                                               #
#################################################################################################################
from tkinter import *
from contenido import Contenido
import subprocess


class Redes(Contenido):
    """Subclase de contenido para el Item Redes"""
    def __init__(self):
        icon = "img/red.png"
        Contenido.__init__(self, None, icon)
        self.properties("Redes")
        self.entry = "docker network ls"
        self.netId = []
        self.chckout = StringVar()
        self.comando(self.netId, 0, self.entry)
        self.acciones()

# ######## A partir de aquí se crean métodos para la propia subclase ############
    def __bfconect(self):
        """Ventana emergente para elegir contenedor"""
        self.chckArray(self.netId)
        if self.empty is False:
            conLf = Toplevel(self, bg="#18152C")
            self.des_boton(self.coBtn)
            vsb = Scrollbar(conLf, orient="vertical")
            text = Text(conLf, bg="#18152C", yscrollcommand=vsb.set, height="10")
            text.config(state="disabled")
            vsb.config(command=text.yview)
            vsb.pack(side="right", fill=Y, padx=5)
            text.pack(fill=X)
            self.idCon = StringVar()  # Para almacenar el ID del contenedor elegido
            proc = subprocess.Popen("docker container ls -a", stdout=subprocess.PIPE)
            p = True
            for line in proc.stdout.readlines():
                if p:
                    head = Label(conLf, text=line, font=("Helvetica", "10", "bold"), fg="white", bg="#18152C")
                    text.window_create("end", window=head)
                    text.insert("end", "\n")
                    p = False
                else:
                    line = line.decode("utf-8")
                    ID = line.split()[0]
                    Nid = "None " + ID  # Esto nos servira para quitarlo del array
                    cb = Checkbutton(conLf, text=line, fg="white", bg="#18152C", onvalue=ID, offvalue=Nid,
                                     variable=self.idCon, )
                    cb.deselect()
                    text.window_create("end", window=cb)
                    text.insert("end", "\n")

            Button(conLf, relief="groove", cursor="hand2", fg="blue", bg="white", text="Ok",
                   command=lambda: [self.__confirm_net(), conLf.destroy()]).pack(fill=X)
            Button(conLf, relief="groove", cursor="hand2", fg="blue", bg="white", text="Cancelar",
                   command=lambda: [conLf.destroy(), self.hab_boton(self.coBtn)]).pack(fill=X)

    def __confirm_net(self):
        """Ventana emergente para confirmar nuestra elección"""
        confirm = Toplevel(self,bg="#18152C")
        self.isSelect = False
        Label(confirm, bg="#18152C", fg="white", text="¿Desea conectar el contenedor con ID" +
                                                      self.idCon.get() + " a la red con ID " + self.netId[0] + "?").pack(fill=X)
        Button(confirm, relief="groove", cursor="hand2", fg="blue", bg="white", text="Si",
               command=lambda: [self.__container_sel(), confirm.destroy()]).pack(padx=5, pady=5, fill=X)
        Button(confirm, relief="groove", cursor="hand2", fg="blue", bg="white", text="No",
               command=lambda: confirm.destroy()).pack(padx=5, pady=5, fill=X)

    def __container_sel(self):
        """Una vez elegido el contenedor se procederá a realizar la conexión"""
        self.isSelect = True
        if self.isSelect:
            cmd = "docker network connect " + self.netId[0] + " " + self.idCon.get()
            subprocess.Popen(cmd, shell=TRUE)
            self.hab_boton(self.coBtn)
            self.reload(self.netId, 0, self.entry)

    def __bfcreate_net(self):
        """Sección para crear una nueva red"""
        createLb = LabelFrame(self, text="Crear nueva red", bg="#18152C", fg="white")
        createLb.pack(fill=X, ipadx=10, ipady=10)
        self.des_boton(self.crBtn)  # Almacenar nombre de red
        Label(createLb, text="Nombre de la red:", bg="#18152C", fg="white").pack()
        self.nNet = StringVar()  # Almacenar el nombre de la red
        Entry(createLb, textvariable=self.nNet).pack(fill=X)
        Label(createLb, text="Ámbito de la red:", bg="#18152C",fg="white").pack()
        self.scope = StringVar()  # Almacenar el ámbito de la red
        Entry(createLb, textvariable=self.scope).pack(fill=X)
        Label(createLb, text="Driver:", bg="#18152C", fg="white").pack(side="left")
        # Loop para crear los radiobuttons, NO FUNCIONA BIEN CON CUALQUIER WIDGET!
        opdrv = ["bridge", "host"]
        self.dvr = StringVar()
        for i in opdrv:
            radio = Radiobutton(createLb, text=i, variable=self.dvr, value=i, bg="#18152C", fg="white")
            radio.pack(side="left")
            radio.deselect()
        Button(createLb, relief="groove", cursor="hand2", fg="blue", bg="white", text="Crear",
               command=lambda: [self.__create_net(), createLb.destroy()]).pack(pady=2, fill=X)
        Button(createLb, relief="groove", cursor="hand2", fg="blue", bg="white", text="Cancelar",
               command=lambda: [createLb.destroy(), self.hab_boton(self.crBtn)]).pack(pady=2, fill=X)

    def __create_net(self):
        """Tras completar los campos necesarios, se procederá a confirmar la creación"""
        if len(self.nNet.get()) == 0 or len(self.scope.get()) == 0:
            aviso = Toplevel(self)
            aviso.config(padx=10, pady=10)
            Label(aviso, text="Asegurese de tener rellenos los campos de Nombre y ámbito").pack(fill=X)
            Button(aviso, relief="groove", cursor="hand2", fg="blue", bg="white", text="Aceptar",
                   command=lambda: aviso.destroy()).pack()
        else:
            cmd = "docker network create " + self.nNet.get() + " --scope " + self.scope.get() + " --driver " + self.dvr.get()
            subprocess.Popen(cmd, shell=TRUE)
            self.reload(self.netId, 0, self.entry)

    def __rm_net(self):
        """Borrar red"""
        for i in self.netId :
            cmd = "docker network rm " + i
            subprocess.Popen(cmd, shell=TRUE)
        self.reload(self.netId, 0, self.entry)

    def __bfrmall_net(self):
        """Confirmación para borrar todas las redes (CRITICO)"""
        aviso = Toplevel(self)
        aviso.config(padx=10, pady=10)
        Label(aviso, text="¿Esta seguro que desea borrar todas las redes?").pack(fill=X)
        Button(aviso, relief="groove", cursor="hand2", fg="blue", bg="white", text="Si", command=lambda: self.__rmall()).pack()
        Button(aviso, relief="groove", cursor="hand2", fg="blue", bg="white", text="No", command=lambda: aviso.destroy()).pack()

    def __rmall(self):
        """Borrar todas las redes"""
        cmd = "docker network prune -f "
        subprocess.Popen(cmd, shell=TRUE)
        self.reload(self.netId, 0, self.entry)

    def acciones(self):
        """Este método nos crea los botones con sus debidas acciones"""
        botones = Frame(self, bg="#18152C")
        botones.pack(side=BOTTOM, pady=10)

        self.coBtn = Button(botones, relief="groove", cursor="hand2", fg="blue", bg="white",
                            text="CONNECT", command=lambda :self.__bfconect())
        self.coBtn.pack(side=LEFT, padx=5)
        self.crBtn = Button(botones, relief="groove", cursor="hand2", fg="blue", bg="white",
                            text="CREATE", command=lambda: self.__bfcreate_net())
        self.crBtn.pack(side=LEFT, padx=5)
        Button(botones, relief="groove", cursor="hand2", fg="blue", bg="white", text="REMOVE",
               command=lambda: self.__rm_net()).pack(side=LEFT, padx=5)
        Button(botones, relief="groove", cursor="hand2", fg="blue", bg="white", text="PRUNE",
               command=lambda: self.__bfrmall_net()).pack(side=LEFT, padx=5)
        Button(botones, text="INSPECT", relief="groove", cursor="hand2", fg="blue", bg="white",
               command=lambda: self.toJson(self.netId)).pack(side=LEFT, padx=5)
        Button(botones, text="RELOAD", relief="groove", cursor="hand2", fg="blue", bg="white",
               command=lambda: self.reload(self.netId, 0, self.entry)).pack(side=LEFT, padx=5)

