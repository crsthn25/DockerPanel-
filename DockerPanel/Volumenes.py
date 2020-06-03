from tkinter import *
from contenido import Contenido
import subprocess


class Volumenes(Contenido):
    """Subclase de contenido para el Item Volumenes"""
    def __init__(self):
        self.icon = "img/volume.png"
        Contenido.__init__(self, None, self.icon)
        self.properties("Volumenes")
        self.entry = "docker volume ls"
        self.volId = []
        self.comando(self.volId, 1, self.entry)
        self.acciones()

# ######## A partir de aquí se crean métodos para la propia subclase ############
    def __create_vol(self):
        """Seccion para crear un nuevo volumen"""
        self.des_boton(self.btCreate)  # Desahbilitamos el boton de crear para no aparecer más secciones
        cLf = LabelFrame(self, text="Crear nuevo volumen", relief=GROOVE, bg="#18152C", fg="white")
        cLf.pack(side=BOTTOM, fill=X, padx=5, pady=10)
        Label(cLf, text="Nombre del Volumen", bg="#18152C", fg="white", font=("Helvetica", 10), padx=5, pady=5)\
            .pack(side=LEFT, padx=5)
        nnVol = StringVar()
        Entry(cLf, textvariable=nnVol).pack(side=LEFT, padx=5)
        Button(cLf, text="OK", relief="groove", cursor="hand2", fg="blue", bg="white",
               command=lambda: [subprocess.Popen(("docker volume create --name " + nnVol.get()), shell=TRUE),
                                cLf.destroy(), self.reload(self.volId, 1, self.entry),
                                self.hab_boton(self.btCreate)]).pack(side=LEFT, padx=5)
        Button(cLf, text="Cancelar", relief="groove", cursor="hand2", fg="blue", bg="white",
               command=lambda: [cLf.destroy(), self.hab_boton(self.btCreate)]).pack(side=LEFT, padx=5)

    def __del_vol(self):
        """Borrar un volumen"""
        self.chckArray(self.volId)
        if self.empty is False:
            for i in self.volId:
                cmd = "docker volume rm " + i
                subprocess.Popen(cmd, shell=TRUE)
            self.reload(self.volId, 1, self.entry)

    def __delall_vol(self):
        """Borrar todos los volumenes"""
        self.chckArray(self.volId)
        if self.empty is False:
            cmd = "docker volume prune -f"
            subprocess.Popen(cmd, shell=TRUE)
            self.reload(self.volId, 1, self.entry)

    def acciones(self):
        """Este método nos crea los botones con sus debidas acciones"""
        botones = Frame(self, bg="#18152C")
        botones.pack(side=BOTTOM, pady=10)
        self.btCreate = Button(botones, text="CREATE", relief="groove", cursor="hand2", fg="blue", bg="white",
                               command=lambda: self.__create_vol())
        self.btCreate.pack(side=LEFT, padx=5)
        Button(botones, text="REMOVE", relief="groove", cursor="hand2", fg="blue", bg="white",
               command=lambda: self.__del_vol()).pack(side=LEFT, padx=5)
        Button(botones, text="PRUNE",  relief="groove", cursor="hand2", fg="blue", bg="white",
               command=lambda: self.__delall_vol()).pack(side=LEFT, padx=5)
        Button(botones, text="INSPECT", relief="groove", cursor="hand2", fg="blue", bg="white",
               command=lambda: self.toJson(self.volId)).pack(side=LEFT, padx=5)
        Button(botones, text="RELOAD", relief="groove", cursor="hand2", fg="blue", bg="white",
               command=lambda: self.reload(self.volId, 0, self.entry)).pack(side=LEFT, padx=5)

