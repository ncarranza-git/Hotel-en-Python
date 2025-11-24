import tkinter 
from tkinter import *
from tkinter import messagebox
from Clase_Habitacion import *
from Clase_Hotel import *

# Color principal de la ventana
FONDO_PRINCIPAL = "#36393F"

# Clase GUI
class HotelGUI():
    def __init__(self, hotel):
        self.hotel = hotel # Creo el objeto 
        self.top = tkinter.Tk() # Crea la ventana principal
        self.top.attributes('-fullscreen', True) # Tamaño de la pantalla - pantalla completa

        # Inicializamos la variable
        self.cantidad_personas_reserva = None 
        
        # Configuración de Centrado para la Ventana Principal  
        self.top.grid_columnconfigure(0, weight=1) 

        # Configuración de filas para centrado vertical (Espacio arriba y abajo)
        self.top.grid_rowconfigure(0, weight=1)
        self.top.grid_rowconfigure(8, weight=1)

        # Titulo de la ventana
        self.top.title("Menú principal") # Titulo de la ventana
        self.top.configure(background = FONDO_PRINCIPAL) 

        # Titulo de la Ventana Principal
        self.titulo = Label(self.top, text=f"¡Bienvenidos a {self.hotel.nombre}!", font=("Broadway", 36, "bold"), bg=FONDO_PRINCIPAL, fg="white")
        self.titulo.grid(row=1, column=0, pady=40) 

        # --- Botones del Menu ---

        # Boton Realizar una Reserva
        self.boton1 = Button(self.top, text="Realizar Reserva", width=40, height=2, bg="#6c757d", fg="white", 
                             font=("Arial", 14, "bold"), command= self.ventana_realizar_reserva)
        self.boton1.grid(row=2, column=0, pady=10)

        # Boton Mostrar Reservas Registradas 
        self.boton2 = Button(self.top, text="Mostrar Reservas Registradas", width=40, height=2, bg="#6c757d", fg="white", 
                             font=("Arial", 14, "bold"), command=self.ventana_mostrar_reservas)
        self.boton2.grid(row=6, column=0, pady=10)

        # Boton Cancelar Reserva
        self.boton3 = Button(self.top, text="Cancelar Reserva", width=40, height=2, bg="#6c757d", fg="white", 
                             font=("Arial", 14, "bold"), command=self.ventana_eliminar_reserva)
        self.boton3.grid(row=4, column=0, pady=10)
        
        # Boton IA de consulta
        self.boton4 = Button(self.top, text="IA Gemini", width=40, height=2, bg="#6c757d", fg="white", 
                             font=("Arial", 14, "bold"), command=self.ventana_api_gemini)
        self.boton4.grid(row=5, column=0, pady=10)

        # Boton Mostrar Habitaciones
        self.boton5 = Button(self.top, text="Mostrar Habitaciones", width=40, height=2, bg="#6c757d", fg="white", 
                             font=("Arial", 14, "bold"), command=self.ventana_mostrar_disponibles)
        self.boton5.grid(row=3, column=0, pady=10)

        
        # Boton Mostrar Historial de Reservas 
        self.boton6 = Button(self.top, text="Historial de Reservas", width=40, height=2, bg="#6c757d", fg="white", 
                             font=("Arial", 14, "bold"), command=self.ventana_mostrar_eliminados)
        self.boton6.grid(row=7, column=0, pady=10)

        # Boton Salir
        self.boton_salir = Button(self.top, text="Salir", width=40, height=2, bg="#dc3545", fg="white", # Color distinto para salir
                                  font=("Arial", 14, "bold"), command=self.top.destroy)
        self.boton_salir.grid(row=9, column=0, pady=30)
        
        self.top.mainloop()

    # --- VENTANAS SECUNDARIAS ---

    # Ventana Realizar Reserva 
    def ventana_realizar_reserva(self):
        self.ventana_reservar = tkinter.Toplevel() 
        self.ventana_reservar.title("1: Registrar Habitación - Paso 1")
        self.ventana_reservar.attributes('-fullscreen', True)
        self.ventana_reservar.configure(background = FONDO_PRINCIPAL) 
        
        # Configuración de Centrado con 3 Columnas
        self.ventana_reservar.grid_columnconfigure(0, weight=1) # Espacio Izquierdo
        self.ventana_reservar.grid_columnconfigure(1, weight=0) # Columna central
        self.ventana_reservar.grid_columnconfigure(2, weight=1) # Espacio Derecho
        self.ventana_reservar.grid_rowconfigure(0, weight=1) # Espacio Superior
        self.ventana_reservar.grid_rowconfigure(5, weight=1) # Espacio Inferior

        # Titulo de la Ventana
        self.titulo = tkinter.Label(self.ventana_reservar, text="Complete los datos solicitados", font=("Arial", 36, "bold"), bg=FONDO_PRINCIPAL, fg="white", justify="center")
        self.titulo.grid(row=1, column=1, pady=40)

        # Frame para agrupar etiqueta y entrada 
        self.frame_datos = tkinter.Frame(self.ventana_reservar, bg=FONDO_PRINCIPAL)
        self.frame_datos.grid(row=2, column=1, padx=10, pady=10)
        
        # Etiqueta Cantidad de Personas
        self.texto1 = tkinter.Label(self.frame_datos, text='Cantidad de Personas:', font=("Arial", 20, "bold"), bg=FONDO_PRINCIPAL, fg="white")
        self.texto1.grid(row=0, column=0, padx=15, pady=15, sticky='E')

        # Campo de Entrada - Cantidad de Personas
        self.entry_cant_personas = tkinter.Entry(self.frame_datos, font=("Arial", 20))
        self.entry_cant_personas.grid(row=0, column=1, padx=15, pady=15, sticky='W')

        # Botones 
        self.frame_botones = tkinter.Frame(self.ventana_reservar, bg=FONDO_PRINCIPAL)
        self.frame_botones.grid(row=3, column=1, pady=30)
        
        # Botón Confirmar
        self.btn_confirmar = Button(self.frame_botones, text="Confirmar", font=("Arial", 15, "bold"), command=self.procesar_cant_personas, width=20, height=2, bg="#28a745", fg="white")
        self.btn_confirmar.grid(row=0, column=0, padx=20)

        # Botón Salir
        self.btn_salir = Button(self.frame_botones, text="Volver al Menú", font=("Arial", 15, "bold"), command=self.ventana_reservar.destroy, width=20, height=2, bg="#6c757d", fg="white")
        self.btn_salir.grid(row=0, column=1, padx=20)

    # Funcion para Procesar la cantidad de personas para ver el tipo de habitacion
    def procesar_cant_personas(self):
        try:
            # Guarda la cantidad de personas como atributo de la clase
            cant_personas = int(self.entry_cant_personas.get())
            if cant_personas > 0:
                self.cantidad_personas_reserva = cant_personas
                # Lógica de Recomendación de Tipo de Habitación
                if cant_personas == 1:
                    tipo_recomendado = "Simple (1 persona)"
                elif cant_personas == 2:
                    tipo_recomendado = "Matrimonial (2 personas)"
                elif 3 <= cant_personas <= 5:
                    tipo_recomendado = "Familiar (3-5 personas)"
                
            
                # Informa la recomendación al usuario mediante un Message Box
                messagebox.showinfo(
                    "Sugerencia de Habitación", f"Para {cant_personas} persona(s), el sistema recomienda una habitación tipo{tipo_recomendado}.\n\nAhora ingrese los datos personales.")
                
                self.ventana_datos_personales() # Llama a la siguiente ventana
            else:
                messagebox.showerror("Error", "La cantidad de personas debe ser mayor a cero.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad de personas válida (número entero).")

    # Ventana de datos personales 
    def ventana_datos_personales(self):
        try:
            self.hotel.eliminacion_automatica()
        except:
            pass
        # Destruir la ventana anterior
        try:
            self.ventana_reservar.destroy()
        except AttributeError:
            pass # Si se llama directo, la ventana anterior no existe

        self.ventana_datos_personales_obj = tkinter.Toplevel() 
        self.ventana_datos_personales_obj.title("1: Registrar Habitación - Paso 2")
        self.ventana_datos_personales_obj.attributes('-fullscreen', True)
        self.ventana_datos_personales_obj.configure(background = FONDO_PRINCIPAL)
        
        # Configuración de Centrado con 3 Columnas
        self.ventana_datos_personales_obj.grid_columnconfigure(0, weight=1) # Espacio Izquierdo
        self.ventana_datos_personales_obj.grid_columnconfigure(1, weight=0) # Contenido (Columna central)
        self.ventana_datos_personales_obj.grid_columnconfigure(2, weight=1) # Espacio Derecho
        self.ventana_datos_personales_obj.grid_rowconfigure(0, weight=1) # Espacio Superior
        self.ventana_datos_personales_obj.grid_rowconfigure(10, weight=1) # Espacio Inferior

        # Titulo de la Ventana 
        self.titulo = tkinter.Label(self.ventana_datos_personales_obj, text="Ingrese los datos solicitados", font=("Arial", 40, "bold"), bg=FONDO_PRINCIPAL, fg="white", justify="center")
        self.titulo.grid(row=1, column=1, pady=40)
        
        # Frame para agrupar el formulario
        self.frame_form = tkinter.Frame(self.ventana_datos_personales_obj, bg=FONDO_PRINCIPAL)
        self.frame_form.grid(row=2, column=1, padx=10, pady=20)

        # Etiquetas (Dentro del Frame)
        self.texto1 = tkinter.Label(self.frame_form, text='Nombre y Apellido:', font=("Arial", 20, "bold"),bg=FONDO_PRINCIPAL, fg="white")
        self.texto1.grid(row=0, column=0, padx=15, pady=15, sticky='E')
        self.entry_nombre = tkinter.Entry(self.frame_form, font=("Arial", 20))
        self.entry_nombre.grid(row=0, column=1, padx=15, pady=15, sticky='W')

        self.texto2 = tkinter.Label(self.frame_form, text="DNI:", font=("Arial", 20, "bold"), bg=FONDO_PRINCIPAL, fg="white")
        self.texto2.grid(row=1, column=0, padx=15, pady=15, sticky='E')
        self.entry_dni = tkinter.Entry(self.frame_form, font=("Arial", 20))
        self.entry_dni.grid(row=1, column=1, padx=15, pady=15, sticky='W')

        self.texto3 = tkinter.Label(self.frame_form, text="Fecha de Ingreso (formato año-mes-día):",font=("Arial", 20, "bold"), bg=FONDO_PRINCIPAL, fg="white" )
        self.texto3.grid(row=2, column=0, padx=15, pady=15, sticky='E')
        self.entry_fecha_ingreso = tkinter.Entry(self.frame_form, font=("Arial", 20))
        self.entry_fecha_ingreso.grid(row=2, column=1, padx=15, pady=15, sticky='W')

        self.texto4 = tkinter.Label(self.frame_form, text="Fecha de Salida (formato año-mes-día):",font=("Arial", 20, "bold"), bg=FONDO_PRINCIPAL, fg="white" )
        self.texto4.grid(row=3, column=0, padx=15, pady=15, sticky='E')
        self.entry_fecha_salida = tkinter.Entry(self.frame_form, font=("Arial", 20))
        self.entry_fecha_salida.grid(row=3, column=1, padx=15, pady=15, sticky='W')


        # Frame Botones 
        self.frame_botones_dp = tkinter.Frame(self.ventana_datos_personales_obj, bg=FONDO_PRINCIPAL)
        self.frame_botones_dp.grid(row=3, column=1, pady=30)

        self.btn_guardar = Button(self.frame_botones_dp, text="Guardar Reserva", font=("Arial", 15, "bold"), width=20, height=2, bg="#28a745", fg="white", command= self.confirmar_datos)
        self.btn_guardar.grid(row=0, column=0, padx=20)

        self.btn_salir = Button(self.frame_botones_dp, text="Volver al Menú", font=("Arial", 15, "bold"), command=self.ventana_datos_personales_obj.destroy, width=20, height=2, bg="#6c757d", fg="white")
        self.btn_salir.grid(row=0, column=1, padx=20)


    # Creo una funcion confirmar para reemplazar los valores y vincular el GUI con clase hotel
    def confirmar_datos(self):
        # Obtener los datos de los campos de entrada
        try:
            cantidad_personas = self.cantidad_personas_reserva # Usamos el valor guardado
        except AttributeError:
            # Esto puede pasar si se llama a esta ventana directamente, manejamos el caso
            tkinter.messagebox.showerror("Error", "Falta ingresar la cantidad de personas.")
            return

        confirmar = True # Lo definimos como True ya que el botón de "Guardar Reserva" implica confirmación
        nombre_cliente = self.entry_nombre.get().upper()
        dni = self.entry_dni.get()
        # Obtener el TEXTO de los Entry, no el objeto Entry completo
        dia_ingreso = self.entry_fecha_ingreso.get()
        dia_salida = self.entry_fecha_salida.get()

        # Validaciones simples (pueden ser más robustas)
        if not all([nombre_cliente, dni, dia_ingreso, dia_salida]):
            tkinter.messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Llamar al método de la clase Hotel
        try:
            # Los nombres de los argumentos en el método de Hotel son:
            # (cantidad_personas, confirmacion, nombre_cliente, dni, dia_ingreso, dia_salida)
            self.hotel.eliminacion_automatica()
            resultado = self.hotel.reservar_habitacion(cantidad_personas, confirmar, nombre_cliente, dni, dia_ingreso, dia_salida)

            if resultado:
                tkinter.messagebox.showinfo("Reserva Exitosa", f"Reserva {resultado[2]} registrada para {resultado[0]} (DNI {resultado[1]}). Total: ${resultado[6]}.")
                self.ventana_datos_personales.destroy()
            else:
                 # El método reservar_habitacion puede no devolver nada si no encuentra habitación o falla internamente
                 tkinter.messagebox.showwarning("Advertencia", "No se pudo realizar la reserva. Revise si hay habitaciones disponibles para esa cantidad de personas.")
        except Exception as e:
            tkinter.messagebox.showerror("Error de Reserva", f"Ocurrió un error al procesar la reserva: {e}. Verifique el formato de las fechas (AAAA-MM-DD).")

    def formatear_lista_habitaciones(self, lista):
        if not lista:
            return "No hay habitaciones disponibles."
        texto = ""
        for h in lista:
            estado = "Ocupada" if h.ocupada else "Libre"
            texto += f"N°{h.numero} - {h.tipo} - ${h.precio} - Estado: {estado}\n"
        return texto


    # Ventana -  Mostrar Habitaciones en Cantidad y Tipo con sus Caracteristicas
    def ventana_mostrar_disponibles(self):
        self.ventana_mostrar_disp = tkinter.Toplevel()
        self.ventana_mostrar_disp.title("Habitaciones")
        self.ventana_mostrar_disp.attributes('-fullscreen', True)
        self.ventana_mostrar_disp.configure(background = FONDO_PRINCIPAL)

        # self.hotel.eliminacion_automatica()
        self.hotel.actualizar_estados()
        lista = self.hotel.habitaciones  # todas
        texto = self.formatear_lista_habitaciones(lista)

        # Configuración de Centrado con 3 Columnas
        self.ventana_mostrar_disp.grid_columnconfigure(0, weight=1) 
        self.ventana_mostrar_disp.grid_columnconfigure(1, weight=0) 
        self.ventana_mostrar_disp.grid_columnconfigure(2, weight=1)
        self.ventana_mostrar_disp.grid_rowconfigure(0, weight=1)
        self.ventana_mostrar_disp.grid_rowconfigure(3, weight=1)

        self.titulo = tkinter.Label(self.ventana_mostrar_disp, text="Habitaciones del Hotel - Estados Actuales", font=("Arial", 36, "bold"), bg=FONDO_PRINCIPAL, fg="white")
        self.titulo.grid(row=1, column=1, pady=40)
        # Guardo la consulta de los registros en una variable
        # Campo de texto
        self.mostrar = tkinter.Text(self.ventana_mostrar_disp, font=("Arial", 22), bg="#44475a",fg="white", padx=40, pady=40,width=50, height=10)
        self.mostrar.insert("1.0", texto)
        self.mostrar.config(state="disabled")
        self.mostrar.grid(row=2, column=1, pady=30)

        # Boton Salir 
        self.btn_salir = Button(self.ventana_mostrar_disp, text="Volver al Menú", font=("Arial", 15, "bold"), command=self.ventana_mostrar_disp.destroy, width=20, height=2, bg="#6c757d", fg="white")
        self.btn_salir.grid(row=4, column=1, pady=50)
        
    # Ventana - Cancelar reserva
    def ventana_eliminar_reserva(self):
        self.ventana_eliminar = tkinter.Toplevel()
        self.ventana_eliminar.title("Cancelar Reserva")
        self.ventana_eliminar.attributes('-fullscreen', True)
        self.ventana_eliminar.configure(background = FONDO_PRINCIPAL)

        # Configuración de Centrado con 3 Columnas
        self.ventana_eliminar.grid_columnconfigure(0, weight=1) 
        self.ventana_eliminar.grid_columnconfigure(1, weight=0) 
        self.ventana_eliminar.grid_columnconfigure(2, weight=1)
        self.ventana_eliminar.grid_rowconfigure(0, weight=1)
        self.ventana_eliminar.grid_rowconfigure(3, weight=1)

        self.titulo = tkinter.Label(self.ventana_eliminar, text="Ingrese DNI para Cancelar Reserva", font=("Arial", 36, "bold"), bg=FONDO_PRINCIPAL, fg="white")
        self.titulo.grid(row=1, column=1, pady=40)

        # Frame para formulario
        self.frame_dni = tkinter.Frame(self.ventana_eliminar, bg=FONDO_PRINCIPAL)
        self.frame_dni.grid(row=2, column=1, padx=10, pady=10)
        
        tkinter.Label(self.frame_dni, text='DNI del Titular:', font=("Arial", 20, "bold"), bg=FONDO_PRINCIPAL, fg="white").grid(row=0, column=0, padx=15, pady=15, sticky='E')
        self.entry_buscar_dni = tkinter.Entry(self.frame_dni, font=("Arial", 20))
        self.entry_buscar_dni.grid(row=0, column=1, padx=15, pady=15, sticky='W')

        # Frame Botones
        self.frame_botones = tkinter.Frame(self.ventana_eliminar, bg=FONDO_PRINCIPAL)
        self.frame_botones.grid(row=3, column=1, pady=30)

        self.btn_cancelar = Button(self.frame_botones, text="Confirmar Cancelación", font=("Arial", 15, "bold"), width=25, height=2, bg="#dc3545", fg="white", command=lambda:self.eliminar_datos())
        self.btn_cancelar.grid(row=0, column=0, padx=20)
        self.btn_salir = Button(self.frame_botones, text="Volver al Menú", font=("Arial", 15, "bold"), command=self.ventana_eliminar.destroy, width=25, height=2, bg="#6c757d", fg="white")
        self.btn_salir.grid(row=0, column=1, padx=20)

    # Creo una funcion eliminar para reemplazar los valores y vincular el GUI con clase hotel
    def eliminar_datos(self):
        dni_buscado = self.entry_buscar_dni.get() # Guardo el entry en la variable a buscar
        if not dni_buscado:
            messagebox.showwarning("Advertencia", "Debe ingresar un DNI para cancelar la reserva.")
            return
        self.hotel.eliminacion_automatica()
        self.hotel.eliminar_reserva(dni_buscado) # Ejecuto la funcion para cancelar la reserva
        messagebox.showinfo(f"Se canceló la reserva con DNI: {dni_buscado}.")
        self.ventana_eliminar.destroy()

    def datos_api(self):
        pregunta = self.entry_pregunta.get()

        if not pregunta:
            self.texto_rta.delete("1.0", "end")
            self.texto_rta.insert("end", "Por favor, ingrese una pregunta.")
            return

        respuesta = self.hotel.api_gemini(pregunta)

        self.texto_rta.delete("1.0", "end")
        self.texto_rta.insert("end", respuesta)

    # Ventana - IA de consulta
    def ventana_api_gemini(self):
        self.ventana_gemini = tkinter.Toplevel()
        self.ventana_gemini.title("Consulta IA Gemini")
        self.ventana_gemini.attributes('-fullscreen', True)
        self.ventana_gemini.configure(background = FONDO_PRINCIPAL)

        # Configuración de Centrado con 3 Columnas
        self.ventana_gemini.grid_columnconfigure(0, weight=1) 
        self.ventana_gemini.grid_columnconfigure(1, weight=0) 
        self.ventana_gemini.grid_columnconfigure(2, weight=1)
        self.ventana_gemini.grid_rowconfigure(0, weight=1)
        self.ventana_gemini.grid_rowconfigure(3, weight=1)

        # Titulo de la Ventana
        self.titulo = tkinter.Label(self.ventana_gemini, text="IA Gemini: Asistente de Hotel", font=("Arial", 36, "bold"), bg=FONDO_PRINCIPAL, fg="white")
        self.titulo.grid(row=1, column=1, pady=40)
        
        self.entry_pregunta = tkinter.Entry(self.ventana_gemini, font=("Arial", 20), width=50)
        self.entry_pregunta.grid(row=2, column=1, padx=30, pady=30, sticky='W')

        self.btn_preguntar = tkinter.Button(self.ventana_gemini, text="Preguntar", font=("Arial", 15, "bold"), command=self.datos_api, width=20, height=2, bg="#6c757d", fg="white")
        self.btn_preguntar.grid(row=3, column=1, pady=50)

        # self.hotel.response.text

        # Campo donde aparecerá el texto de respuesta
        self.texto_rta = tkinter.Text(self.ventana_gemini,font=("Arial", 18),bg="#44475a",fg="white",padx=40,pady=40,width=60,height=5,wrap="word")
        self.texto_rta.grid(row=4, column=1, pady=30)

        self.btn_salir = Button(self.ventana_gemini, text="Volver al Menú", font=("Arial", 15, "bold"), command=self.ventana_gemini.destroy, width=20, height=2, bg="#6c757d", fg="white")
        self.btn_salir.grid(row=5, column=1, pady=50)

    # Ventana - Mostrar reservas registradas
    def ventana_mostrar_reservas(self):
        self.ventana_mostrarR = tkinter.Toplevel() 
        self.ventana_mostrarR.title("5: Mostrar Reservas Registradas")
        self.ventana_mostrarR.attributes('-fullscreen', True)
        self.ventana_mostrarR.configure(background = FONDO_PRINCIPAL) 
        self.hotel.eliminacion_automatica()
        texto_reservas = self.hotel.mostrar_reservas() 

        # Configuración de Centrado con 3 Columnas
        self.ventana_mostrarR.grid_columnconfigure(0, weight=1) 
        self.ventana_mostrarR.grid_columnconfigure(1, weight=0) 
        self.ventana_mostrarR.grid_columnconfigure(2, weight=1)
        self.ventana_mostrarR.grid_rowconfigure(0, weight=1)
        self.ventana_mostrarR.grid_rowconfigure(3, weight=1)

        # Titulo de la Ventana
        self.titulo = tkinter.Label(self.ventana_mostrarR, text="Reservas Actualmente Registradas", font=("Arial", 36, "bold"), bg=FONDO_PRINCIPAL, fg="white")
        self.titulo.grid(row=1, column=1, pady=40)
        
        # Campo de texto de Respuestas
        self.texto_consultas = tkinter.Text(self.ventana_mostrarR, font=("Arial", 18), bg="#44475a", fg="white", padx=50, pady=50, width=100, height=15)
        # Insertar el texto
        self.texto_consultas.insert(tkinter.END, texto_reservas)
        # Hacer que sea solo lectura
        self.texto_consultas.config(state='disabled')
        # Ubicarlo en la ventana
        self.texto_consultas.grid(row=2, column=1, pady=30)

        self.btn_salir = Button(self.ventana_mostrarR, text="Volver al Menú", font=("Arial", 15, "bold"), command=self.ventana_mostrarR.destroy, width=20, height=2, bg="#6c757d", fg="white")
        self.btn_salir.grid(row=4, column=1, pady=50)

    # Ventana - Mostrar historial de reservas eliminadas
    def ventana_mostrar_eliminados(self):
        self.ventana_eliminados = tkinter.Toplevel()
        self.ventana_eliminados.title("6: Historial de Reservas Eliminadas")
        self.ventana_eliminados.attributes('-fullscreen', True)
        self.ventana_eliminados.configure(background = FONDO_PRINCIPAL)

        self.hotel.eliminacion_automatica()

        # Configuración de Centrado con 3 Columnas
        self.ventana_eliminados.grid_columnconfigure(0, weight=1) 
        self.ventana_eliminados.grid_columnconfigure(1, weight=0) 
        self.ventana_eliminados.grid_columnconfigure(2, weight=1)
        self.ventana_eliminados.grid_rowconfigure(0, weight=1)
        self.ventana_eliminados.grid_rowconfigure(3, weight=1)

        # Titulo de la Vetana 
        self.titulo = tkinter.Label(self.ventana_eliminados, text="Historial de Reservas Eliminadas", font=("Arial", 36, "bold"), bg=FONDO_PRINCIPAL, fg="white")
        self.titulo.grid(row=1, column=1, pady=40)

        # Frame para el texto con scroll
        frame_texto = tkinter.Frame(self.ventana_eliminados, bg=FONDO_PRINCIPAL)
        frame_texto.grid(row=2, column=1, pady=30)

        scrollbar = tkinter.Scrollbar(frame_texto)
        scrollbar.pack(side="right", fill="y")

        self.text_historial = tkinter.Text(frame_texto,width=100,height=5,font=("Arial", 16),bg="#44475a",fg="white",yscrollcommand=scrollbar.set,padx=20,pady=20)
        self.text_historial.pack()

        scrollbar.config(command=self.text_historial.yview)

        # Cargar el texto desde SQL
        texto_historial = self.hotel.mostrar_eliminados()
        self.text_historial.insert("end", texto_historial)
        

        self.btn_salir = Button(self.ventana_eliminados, text="Volver al Menú", font=("Arial", 15, "bold"), command=self.ventana_eliminados.destroy, width=20, height=2, bg="#6c757d", fg="white")
        self.btn_salir.grid(row=5, column=1, pady=50)
