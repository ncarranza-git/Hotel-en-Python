import tkinter 
from tkinter import *

#Paleta de colores
FONDO_PRINCIPAL = "#36393F"

class HotelGUI():
    def __init__(self, hotel):
        self.cochera = hotel # Creo el objeto 
        self.top = tkinter.Tk() # Crea la ventana principal

        # Configurar el grid de la ventana principal 
        self.top.grid_rowconfigure(0, weight=1)   # Espacio arriba
        self.top.grid_rowconfigure(6, weight=1)   # Espacio abajo
        self.top.grid_columnconfigure(0, weight=1)  # Centrar horizontalmente

        self.top.title("Las Vegas Hotel") # Define el titulo de la ventana

        self.top.configure(background = FONDO_PRINCIPAL) # Define el color de fondo de la ventana (Antes era #003976)

        # Titulo de la Ventana Principal
        self.titulo = Label(self.top, text="¡Bienvenidos a Las Vegas Hotel!", font=("Broadway", 36, "bold"), bg="#36393F", fg="white")
        self.titulo.grid(row=1, column=0, pady=40)

        # Botones del Menu
        self.boton1 = Button(self.top, text="Realizar Reserva", width=40, height=2, bg="#6c757d", fg="white", 
                             font=("Arial", 14, "bold"), command= self.ventana_realizar_reserva)
        self.boton1.grid(row=2, column=0, pady=15)

        self.boton2 = Button(self.top, text="Mostrar Habitaciones Disponibles", width=40, height=2, bg="#6c757d", fg="white", 
                             font=("Arial", 14, "bold"), command=self.ventana_mostrar_reservas)
        self.boton2.grid(row=3, column=0, pady=15)

        self.boton3 = Button(self.top, text="Cancelar Reserva", width=40, height=2, bg="#6c757d", fg="white", font=("Arial", 14, "bold"))
        self.boton3.grid(row=4, column=0, pady=15)

        self.boton3 = Button(self.top, text="IA Gemini", width=40, height=2, bg="#6c757d", fg="white", font=("Arial", 14, "bold"))
        self.boton3.grid(row=5, column=0, pady=15, )

        self.boton3 = Button(self.top, text="API Clima", width=40, height=2, bg="#6c757d", fg="white", font=("Arial", 14, "bold"))
        self.boton3.grid(row=6, column=0, pady=15)

        self.boton4 = Button(self.top, text="Salir", width=40, height=2, bg="#6c757d", fg="white", font=("Arial", 14, "bold"), command=self.top.destroy)
        self.boton4.grid(row=7, column=0, pady=30)

        self.top.mainloop()

    # Ventana Secundaria para Registrar Reserva
    def ventana_realizar_reserva(self):
        self.ventana_reservar = tkinter.Toplevel() # Ventana secundaria
        # self.ventana_reservar.grid_rowconfigure(0, weight=1)   # Espacio arriba
        # self.ventana_reservar.grid_rowconfigure(6, weight=1)   # Espacio abajo
        # self.ventana_reservar.grid_columnconfigure(0, weight=1)  # Centrar horizontalmente
        self.ventana_reservar.title("Ventana Registrar Habitación")
        self.ventana_reservar.geometry("1000x1000")
        self.ventana_reservar.configure(background = FONDO_PRINCIPAL) # Define el color de fondo de la ventana

        # Titulo de la Ventana Reservar
        self.titulo = tkinter.Label(self.ventana_reservar, text="Complete los datos solicitados", font=("Arial", 36, "bold"), bg=FONDO_PRINCIPAL, fg="black", justify="center")
        self.titulo.grid(row=0, column=2, pady=40)

        # Defino la etiqueta donde indica el campo a completar
        self.texto1 = tkinter.Label(self.ventana_reservar, text='Cantidad de Personas:', font=("Arial", 20, "bold"))
        self.texto1.grid(row=1, column=0, padx=15, pady=15)

        # Campo para ingresar la cantidad de personas a hospedar
        self.entry_cant_personas = tkinter.Entry(self.ventana_reservar)
        self.entry_cant_personas.grid(row=1, column= 1, padx=35, pady=35)

        self.btn_confirmar = Button(self.ventana_reservar, text="Confirmar", font=("Arial", 15, "bold"))
        self.btn_confirmar.grid(row=4, column=1, padx=20, pady=20)
        self.btn_salir = Button(self.ventana_reservar, text="Salir", font=("Arial", 15, "bold"), command=self.ventana_reservar.destroy)
        self.btn_salir.grid(row=4, column=3, padx=20, pady=20)


        # tkinter.Label(self.ventana_reservar, text='Tipo de vehiculo').grid(row=1, column=0)
        # tkinter.Label(self.ventana_reservar, text='Ubicación').grid(row=2, column=0)

    # Ventana Secundaria para Mostrar Reservas
    def ventana_mostrar_reservas(self):
        self.ventana_mostrarR = tkinter.Toplevel() # Ventana secundaria
        # self.ventana_reservar.grid_rowconfigure(0, weight=1)   # Espacio arriba
        # self.ventana_reservar.grid_rowconfigure(6, weight=1)   # Espacio abajo
        # self.ventana_reservar.grid_columnconfigure(0, weight=1)  # Centrar horizontalmente
        self.ventana_mostrar_reservas.tittle
        self.ventana_mostrarR.geometry("1000x1000")
        self.ventana_mostrarR.configure(background = FONDO_PRINCIPAL) # Define el color de fondo de la ventana

app = HotelGUI(None)