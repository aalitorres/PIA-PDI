import customtkinter as ctk

from procesamiento import ProcesadorDICOM
from PIL import Image, ImageTk
import cv2
from tkinter import filedialog

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Aplicacion(ctk.CTk):

    def __init__(self):
        super().__init__()
        
        # Procesador DICOM
        self.procesador = ProcesadorDICOM("imagenes")

        self.indice = 0

        self.imagen_actual = self.procesador.leer_corte(self.indice)

        # Ventana
        self.title("Procesamiento de Imágenes Médicas")
        self.geometry("1200x700")
        self.minsize(1100,650)

         # Panel izquierdo
        self.panel = ctk.CTkFrame(
            self,
            width=260
        )

        self.panel.pack(
            side="left",
            fill="y",
            padx=10,
            pady=10
        )

        # Título 
        titulo = ctk.CTkLabel(
            self.panel,
            text="Procesamiento\nDICOM",
            font=("Arial",22,"bold")
        )

        titulo.pack(pady=(20,20))

        # Botón abrir
        self.boton_abrir = ctk.CTkButton(
            self.panel,
            text="Abrir estudio",
            command=self.abrir_estudio
        )

        self.boton_abrir.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # Navegación
        self.frame_nav = ctk.CTkFrame(
            self.panel
        )

        self.frame_nav.pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.boton_anterior = ctk.CTkButton(
            self.frame_nav,
            text="◀",
            width=35,
            command=self.corte_anterior
        )

        self.boton_anterior.pack(
            side="left",
            padx=5,
            pady=5
        )

        self.label_corte = ctk.CTkLabel(
            self.frame_nav,
            text=f"1 / {self.procesador.numero_cortes()}",
            font=("Arial",15)
        )

        self.label_corte.pack(
            side="left",
            expand=True
        )
        
        self.label_info = ctk.CTkLabel(
            self.panel,
            text="512 × 512 px\nEscala de grises uint8",
            font=("Arial",12),
            justify="center"
        )

        self.label_info.pack(
            pady=(0,15)
        )

        self.boton_siguiente = ctk.CTkButton(
            self.frame_nav,
            text="▶",
            width=35,
            command=self.corte_siguiente
        )

        self.boton_siguiente.pack(
            side="right",
            padx=5,
            pady=5
        )

        # Procesamiento
        titulo_proc = ctk.CTkLabel(
            self.panel,
            text="Procesamiento",
            font=("Arial",16,"bold")
        )

        titulo_proc.pack(
            pady=(15,5)
        )

        self.combo = ctk.CTkComboBox(

            self.panel,

            values=[
                "Original",
                "Ecualización",
                "Media",
                "Gaussiano",
                "Original - Gaussiano",
                "Sobel",
                "Laplaciano",
                "Segmentación",
                "AND",
                "OR",
                "Fourier"
            ],
            command=self.cambiar_procesamiento
        )

        self.combo.pack(
            fill="x",
            padx=20
        )

        self.combo.set("Original")
        
        self.invertir = ctk.CTkCheckBox(
            self.panel,
            text="Invertir imagen",
            command=self.mostrar_imagen
        )

        self.invertir.pack(
            anchor="w",
            padx=20,
            pady=(8,15)
        )

        # Umbral
        self.titulo_umbral = ctk.CTkLabel(
            self.panel,
            text="Umbral",
            font=("Arial",16,"bold")
        )

        self.titulo_umbral.pack(
            pady=(25,5)
        )

        self.slider = ctk.CTkSlider(
            self.panel,
            from_=0,
            to=255,
            number_of_steps=255,
            command=self.cambiar_umbral
        )

        self.slider.pack(
            fill="x",
            padx=20
        )

        self.slider.set(120)
        self.slider.configure(state="disabled")

        self.label_umbral = ctk.CTkLabel(
            self.panel,
            text="120/255"
        )

        self.label_umbral.pack()

        # Guardar
        self.boton_guardar = ctk.CTkButton(
            self.panel,
            text="Guardar imagen",
            command=self.guardar_imagen
        )

        self.boton_guardar.pack(
            fill="x",
            padx=20,
            pady=35
        )
        
        self.footer = ctk.CTkLabel(
            self.panel,
            text="Procesamiento Digital de Imágenes\nEquipo 2 - UANL",
            font=("Arial",11),
            text_color="gray70"
        )

        self.footer.pack(
            side="bottom",
            pady=15
        )

        # Área principal
        self.area = ctk.CTkFrame(
            self
        )

        self.area.pack(
            side="right",
            expand=True,
            fill="both",
            padx=10,
            pady=10
        )

        # Configurar cuadrícula
        self.area.grid_columnconfigure((0,1), weight=1)
        self.area.grid_rowconfigure((0,1), weight=1)

       # Imagen original
        self.label_original = ctk.CTkLabel(
            self.area,
            text="Imagen Original",
            font=("Arial",16,"bold")
        )

        self.label_original.grid(
            row=0,
            column=0,
            pady=(10,5)
        )

        self.canvas_original = ctk.CTkLabel(
            self.area,
            text=""
        )

        self.canvas_original.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0,20)
        )

        # Histograma original
        self.label_hist_original = ctk.CTkLabel(
            self.area,
            text="Histograma Original",
            font=("Arial",16,"bold")
        )

        self.label_hist_original.grid(
            row=0,
            column=1,
            pady=(10,5)
        )

        self.canvas_hist_original = ctk.CTkLabel(
            self.area,
            text=""
        )

        self.canvas_hist_original.grid(
            row=1,
            column=1,
            padx=20,
            pady=(0,20)
        )

        # Imagen procesada 
        self.label_procesada = ctk.CTkLabel(
            self.area,
            text="Imagen Procesada",
            font=("Arial",16,"bold")
        )

        self.label_procesada.grid(
            row=2,
            column=0,
            pady=(10,5)
        )

        self.canvas_procesada = ctk.CTkLabel(
            self.area,
            text=""
        )

        self.canvas_procesada.grid(
            row=3,
            column=0,
            padx=20,
            pady=(0,20)
        )

        # Histograma procesado
        self.label_hist_procesada = ctk.CTkLabel(
            self.area,
            text="Histograma Procesado",
            font=("Arial",16,"bold")
        )

        self.label_hist_procesada.grid(
            row=2,
            column=1,
            pady=(10,5)
        )

        self.canvas_hist_procesada = ctk.CTkLabel(
            self.area,
            text=""
        )

        self.canvas_hist_procesada.grid(
            row=3,
            column=1,
            padx=20,
            pady=(0,20)
        )

        # Mostrar la primera imagen al iniciar
        self.mostrar_imagen()

        
    def mostrar_imagen(self):

        # Imagen original
        imagen_original = self.imagen_actual
        alto, ancho = imagen_original.shape

        self.label_info.configure(
            text=f"{ancho} × {alto} px\n{imagen_original.dtype}"
        )

        # Imagen procesada
        opcion = self.combo.get()

        if opcion == "Original":
            imagen_procesada = imagen_original

        elif opcion == "Ecualización":
            imagen_procesada = self.procesador.ecualizar(imagen_original)
       
        elif opcion == "Media":

            imagen_procesada = self.procesador.media(
                imagen_original
            )

        elif opcion == "Gaussiano":
            imagen_procesada = self.procesador.gaussiano(imagen_original)
            
        elif opcion == "Original - Gaussiano":
            imagen_procesada = self.procesador.resta(imagen_original)

        elif opcion == "Sobel":
            imagen_procesada = self.procesador.sobel(imagen_original)

        elif opcion == "Laplaciano":
            imagen_procesada = self.procesador.laplaciano(imagen_original)
            
        elif opcion == "Segmentación":
            
            imagen_procesada = self.procesador.binaria(
                imagen_original,
                int(self.slider.get())
            )
            
        elif opcion == "AND":

            imagen_procesada = self.procesador.and_logico(
                imagen_original,
                int(self.slider.get())
            )
           
        elif opcion == "OR":

            imagen_procesada = self.procesador.or_logico(
                imagen_original,
                int(self.slider.get())
            )    
                        
        elif opcion == "Fourier":

            imagen_procesada = self.procesador.fourier(
                imagen_original
            )

        else:
            imagen_procesada = imagen_original
            
        # Invertir imagen si el CheckBox está activado
        if self.invertir.get():

            imagen_procesada = cv2.bitwise_not(imagen_procesada)

        color = "#3FA9F5"   

        if opcion == "Original":
            color = "#3FA9F5"     

        elif opcion == "Ecualización":
            color = "#00E676"     
        
        elif opcion == "Media":
            color = "#D22E7E"   

        elif opcion == "Gaussiano":
            color = "#FFD54F"      

        elif opcion == "Original - Gaussiano":
            color = "#FF80AB"    

        elif opcion == "Sobel":
            color = "#FF9800"     

        elif opcion == "Laplaciano":
            color = "#F44336"      

        elif opcion == "Segmentación":
            color = "#FFFFFF"     

        elif opcion == "AND":
            color = "#BA68C8"    

        elif opcion == "OR":
            color = "#FF80AB"    

        elif opcion == "Fourier":
            color = "#00BCD4"      

        hist_original = self.procesador.histograma(
            imagen_original,
            "#3FA9F5"
        )

        hist_procesado = self.procesador.histograma(
            imagen_procesada,
            color
        )
        # Preparar imagen original
        img_original = cv2.resize(imagen_original, (350, 350))
        img_original = Image.fromarray(img_original)
        img_original = ImageTk.PhotoImage(img_original)
        # Preparar imagen procesar
        img_procesada = cv2.resize(imagen_procesada, (350, 350))
        img_procesada = Image.fromarray(img_procesada)
        img_procesada = ImageTk.PhotoImage(img_procesada)
        
        # Redimensionar histogramas
        hist_original = hist_original.resize((540, 350))
        hist_procesado = hist_procesado.resize((540, 350))

        # Convertir a formato para Tkinter
        hist_original = ImageTk.PhotoImage(hist_original)
        hist_procesado = ImageTk.PhotoImage(hist_procesado)

        # Mostrar original
        self.canvas_original.configure(image=img_original)
        self.canvas_original.image = img_original

        # Mostrar procesada
        self.canvas_procesada.configure(image=img_procesada)
        self.canvas_procesada.image = img_procesada
        
        # Mostrar histograma original
        self.canvas_hist_original.configure(image=hist_original)
        self.canvas_hist_original.image = hist_original

        # Mostrar histograma procesado
        self.canvas_hist_procesada.configure(image=hist_procesado)
        self.canvas_hist_procesada.image = hist_procesado
        
    def corte_siguiente(self):

        if self.indice < self.procesador.numero_cortes() - 1:
            
            self.indice += 1

            self.imagen_actual = self.procesador.leer_corte(self.indice)

            self.label_corte.configure(
                 text=f"{self.indice + 1} / {self.procesador.numero_cortes()}"
            )

            self.mostrar_imagen()

    def corte_anterior(self):

        if self.indice > 0:

            self.indice -= 1

            self.imagen_actual = self.procesador.leer_corte(self.indice)

            self.label_corte.configure(
                text=f"{self.indice + 1} / {self.procesador.numero_cortes()}"
            )

            self.mostrar_imagen()
    
    def cambiar_umbral(self, valor):

        self.label_umbral.configure(
            text=f"{int(valor)} / 255"
        )

        if self.combo.get() in ["Segmentación", "AND", "OR"]:
            self.mostrar_imagen()
            

    def cambiar_procesamiento(self, opcion):

        if opcion in ["Segmentación", "AND", "OR"]:

            self.slider.configure(state="normal")

            self.label_umbral.configure(
                text_color="white"
            )

            self.titulo_umbral.configure(
                text_color="white"
            )

        else:

            self.slider.configure(state="disabled")

            self.label_umbral.configure(
                text_color="gray60"
            )

            self.titulo_umbral.configure(
                text_color="gray60"
            )

        self.mostrar_imagen()
        
    def guardar_imagen(self):

        opcion = self.combo.get()

        imagen = self.imagen_actual

        if opcion == "Ecualización":
            imagen = self.procesador.ecualizar(imagen)

        elif opcion == "Gaussiano":
            imagen = self.procesador.gaussiano(imagen)

        elif opcion == "Original - Gaussiano":
            imagen = self.procesador.resta(imagen)

        elif opcion == "Sobel":
            imagen = self.procesador.sobel(imagen)

        elif opcion == "Laplaciano":
            imagen = self.procesador.laplaciano(imagen)

        elif opcion == "Segmentación":
            imagen = self.procesador.binaria(
                imagen,
                int(self.slider.get())
            )

        elif opcion == "AND":
            imagen = self.procesador.and_logico(
                imagen,
                int(self.slider.get())
            )

        elif opcion == "OR":
            imagen = self.procesador.or_logico(
                imagen,
                int(self.slider.get())
            )

        elif opcion == "Fourier":
            imagen = self.procesador.fourier(imagen)

        ruta = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG","*.png"),
                ("JPEG","*.jpg")
            ]
        )

        if ruta:
            cv2.imwrite(ruta, imagen)
    def abrir_estudio(self):

        carpeta = filedialog.askdirectory(
            title="Seleccionar carpeta DICOM"
        )

        if not carpeta:
            return

        self.procesador = ProcesadorDICOM(carpeta)

        if self.procesador.numero_cortes() == 0:
            return

        self.indice = 0

        self.imagen_actual = self.procesador.leer_corte(0)

        self.label_corte.configure(
            text=f"1 / {self.procesador.numero_cortes()}"
        )

        self.mostrar_imagen()
        
        