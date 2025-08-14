import openai
from openai import OpenAI
from pathlib import Path
from tkinter import Tk, Canvas, Text, Button, PhotoImage, END, Frame, Label
import json, os
import pyodbc
import historial
from db_connection import connection_string

CONFIG_FILE = "window_position.json"

# ----- Clase Chatbot -----
class Chatbot:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.historial = []
        self.personalidad = "Eres un chatbot amigable que da consejos de nutrición a niños de 8 a 12 años."
        self.client = OpenAI(api_key=self.api_key)

    def obtener_respuesta(self, mensaje_usuario):
        self.historial.append({"role": "user", "content": mensaje_usuario})
        mensajes = [{"role": "system", "content": self.personalidad}] + self.historial
        try:
            respuesta = self.client.chat.completions.create(
                model=self.model,
                messages=mensajes
            )
            contenido = respuesta.choices[0].message.content
            self.historial.append({"role": "assistant", "content": contenido})
            return contenido
        except Exception as e:
            return f"[Error al conectar con IA]"

# ----- Clase InterfazChatbot -----
class InterfazChatbot(Tk):  # Ahora hereda directamente de Tk
    def __init__(self, idperfil, chatbot):
        super().__init__()
        self.chatbot = chatbot
        self.IDPerfil = idperfil
        self.historial = ""
        self.geometry("505x786")
        self.configure(bg="#FFFFFF")
        self.load_geometry()
        self.title("RoboNutri - Chat")
        self.resizable(False, False)

        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(r"assets_Chat\frame0")

        self.build_ui()
        #self.after(250, self.saludo_inicial)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def build_ui(self):
        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=786,
            width=505,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Imágenes y botones
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(252.0, 393.0, image=self.image_image_1)

        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(252.24, 392.54, image=self.image_image_2)

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        Button(self, image=self.button_image_1, borderwidth=0, highlightthickness=0,
               command=lambda: self.on_back_button_clicked(), relief="flat").place(x=47.88, y=51.14, width=40.55, height=30.21)

        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        Button(self, image=self.button_image_2, borderwidth=0, highlightthickness=0,
               command=lambda: print("Perfil"), relief="flat").place(x=421.13, y=38.78, width=55.02, height=57.41)

        self.image_image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.canvas.create_image(253.84, 711.69, image=self.image_image_3)

        self.image_image_4 = PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.canvas.create_image(80.93, 711.28, image=self.image_image_4)

        self.image_image_5 = PhotoImage(file=self.relative_to_assets("image_5.png"))
        self.canvas.create_image(268.0, 713.0, image=self.image_image_5)

        self.image_image_6 = PhotoImage(file=self.relative_to_assets("image_6.png"))
        self.canvas.create_image(259.86, 100.74, image=self.image_image_6)

        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_4.png"))
        Button(self, image=self.button_image_4, borderwidth=0, highlightthickness=0,
               command=lambda: print("Panel"), relief="flat").place(x=436.33, y=251.16, width=57.99, height=300.80)
        
        # ======== Área de mensajes con Canvas + Frame ========
        self.chat_canvas = Canvas(self, bg="#FFFFFF", bd=0, highlightthickness=0)
        self.scrollable_frame = Frame(self.chat_canvas, bg="#FFFFFF")
        self.chat_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        )

        self.chat_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.chat_canvas.place(x=20, y=200, width=355, height=460)

        # ======== Entrada de texto ========
        self.entrada = Text(self, bd=0, bg="#FFFEEF", fg="#000716", highlightthickness=0)
        self.entrada.place(x=129.24, y=679.79, width=276.59, height=64.88)

        # Botón enviar
        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        Button(self, image=self.button_image_3, borderwidth=0, highlightthickness=0,
               command=self.enviar_mensaje, relief="flat").place(x=418.0, y=681.0, width=56.0, height=66.0)
        
        cnxn = pyodbc.connect(connection_string)
        cursor = cnxn.cursor()
        sql_query = "Select Nombre From Perfil Where IDPerfil ="+str(self.IDPerfil)+";"
        cursor.execute(sql_query)
        nombre = cursor.fetchall().pop()[0].split()[0]
        self.after(300, self.saludo_inicial(nombre))
        
    def _on_mousewheel(self, event):
        """Desplazar con la rueda del mouse."""
        self.chat_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def save_geometry(self):
        """Saves the current window's geometry to a file."""
        geometry = self.winfo_geometry()
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"geometry": geometry}, f)

    def load_geometry(self):
        """Loads the window's geometry from a file and applies it."""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    geometry = config.get("geometry")
                    if geometry:
                        self.geometry(geometry)
                    else:
                        self.geometry("400x300+150+150") # Default if no geometry in file
            except json.JSONDecodeError:
                self.geometry("400x300+150+150") # Default if file is corrupted
        else:
            self.geometry("400x300+150+150") # Default if no file exists

    def on_closing(self):
        """Called when the window is closed. Saves geometry and destroys the window."""
        self.guardar_historial_sql()
        self.save_geometry()
        self.destroy()

    def mostrar_mensaje(self, remitente, mensaje):
        # Configuración visual según remitente
        if remitente == "Tú":
            color_fondo = "#BEE3F8"
            anclaje = "e"
            just = "right"
            margen_x = 20
        else:
            color_fondo = "#C6F6D5"
            anclaje = "w"
            just = "left"
            margen_x = 20

        # Crear contenedor de burbuja
        burbuja = Label(
            self.scrollable_frame,
            text=mensaje,
            bg=color_fondo,
            fg="#000000",
            wraplength=300,
            justify=just,
            padx=10,
            pady=5
        )
        burbuja.pack(anchor=anclaje, pady=5, padx=margen_x)

        # Desplazar al final
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)

    def enviar_mensaje(self):
        print(self.historial)
        mensaje = self.entrada.get("1.0", END).strip()
        if mensaje:
            self.mostrar_mensaje("Tú", mensaje)
            self.entrada.delete("1.0", END)
            respuesta = self.chatbot.obtener_respuesta(mensaje)
            self.mostrar_mensaje("RoboNutri", respuesta)

    def saludo_inicial(self, nombre):
        saludo = "¡Hola "+nombre+"! Soy RoboNutri. Estoy aquí para ayudarte con tus preguntas sobre alimentación saludable."
        self.mostrar_mensaje("RoboNutri", saludo)

    def guardar_historial_sql(self):
        """
        Guarda el historial completo en la base de datos.
        idperfil: ID del niño
        historial: lista de diccionarios con 'role' y 'content' del chat
        """
        if not self.chatbot.historial:
            # No hay mensajes, no guardamos nada
            print("No hay historial para guardar.")
            return
        # Convertir lista de mensajes a texto plano con formato "Tú: ...\nRoboNutri: ..."
        texto_historial = ""
        for msg in self.chatbot.historial:
            remitente = "Tú" if msg["role"] == "user" else "RoboNutri"
            texto_historial += f"{remitente}: {msg['content']}\n"
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        try:
            #sql_query = "Insert Into Historial Values(?,?, GETDATE())",(self.IDPerfil, texto_historial)
            cursor.execute("INSERT INTO Historial (IDPerfil, Historial, FechaHora) VALUES (?, ?, CONVERT(date, GETDATE()))",(self.IDPerfil, texto_historial))
            conn.commit()
            print("Historial guardado correctamente")
        except Exception as e:
            print("Error al guardar historial:", e)
        finally:
            cursor.close()
            conn.close()

    def on_back_button_clicked(self):
        self.save_geometry()
        self.destroy()
        new_root = historial.HistorialWindow(self.IDPerfil)
        new_root.mainloop()

# ----- Ejecución principal -----
if __name__ == "__main__":
    API_KEY = ""
    bot = Chatbot(api_key=API_KEY)
    app = InterfazChatbot(1,chatbot=bot)
    app.mainloop()
