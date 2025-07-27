import openai
from openai import OpenAI
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, END

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
            return f"[Error al conectar con IA: {e}]"


# ----- Clase InterfazChatbot con diseño de TkDesigner -----
class InterfazChatbot:
    def __init__(self, chatbot):
        self.chatbot = chatbot

        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path("") #Directorio

        def relative_to_assets(path: str) -> Path:
            return self.ASSETS_PATH / Path(path)

        self.window = Tk()
        self.window.geometry("505x786")
        self.window.configure(bg="#FFFFFF")
        self.window.title("RoboNutri - Chat")

        self.canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=786,
            width=505,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        #Imágenes y botones de TkDesigner
        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.create_image(252.0, 393.0, image=self.image_image_1)

        self.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        self.canvas.create_image(252.24, 392.54, image=self.image_image_2)

        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        Button(image=self.button_image_1, borderwidth=0, highlightthickness=0, command=lambda: print("Menu"), relief="flat").place(x=47.88, y=51.14, width=40.55, height=30.21)

        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        Button(image=self.button_image_2, borderwidth=0, highlightthickness=0, command=lambda: print("Perfil"), relief="flat").place(x=421.13, y=38.78, width=55.02, height=57.41)

        self.image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        self.canvas.create_image(253.84, 711.69, image=self.image_image_3)

        self.image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
        self.canvas.create_image(80.93, 711.28, image=self.image_image_4)

        self.image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
        self.canvas.create_image(268.0, 713.0, image=self.image_image_5)

        self.image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
        self.canvas.create_image(259.86, 100.74, image=self.image_image_6)

        self.button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
        Button(image=self.button_image_4, borderwidth=0, highlightthickness=0, command=lambda: print("Panel"), relief="flat").place(x=436.33, y=251.16, width=57.99, height=300.80)

        #Campo de entrada del mensaje
        self.entrada = Text(self.window, bd=0, bg="#FFFEEF", fg="#000716", highlightthickness=0)
        self.entrada.place(x=129.24, y=679.79, width=276.59, height=64.88)

        #Botón de enviar mensaje
        self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.enviar_mensaje,
            relief="flat"
        ).place(x=418.0, y=681.0, width=56.0, height=66.0)

        #Área de chat arriba de la entrada
        self.area_chat = Text(self.window, bg="#FFFEEF", fg="#000000", wrap="word")
        self.area_chat.place(x=40, y=210, width=380, height=440)
        self.area_chat.config(state="disabled")

        #Estilos de mensajes
        self.area_chat.tag_configure("usuario", justify="right", background="#D0F0FF", foreground="#000000", lmargin1=50, rmargin=10, spacing3=5)
        self.area_chat.tag_configure("bot", justify="left", background="#E0FFE0", foreground="#000000", lmargin1=10, rmargin=50, spacing3=5)

        self.window.resizable(False, False)
        self.window.mainloop()

    def enviar_mensaje(self):
        mensaje = self.entrada.get("1.0", END).strip()
        if mensaje:
            self.mostrar_mensaje("Tú", mensaje)
            self.entrada.delete("1.0", END)
            respuesta = self.chatbot.obtener_respuesta(mensaje)
            self.mostrar_mensaje("RoboNutri", respuesta)

    def mostrar_mensaje(self, remitente, mensaje):
        self.area_chat.config(state="normal")

        if remitente == "Tú":
            self.area_chat.insert(END, f"{remitente}: {mensaje}\n", "usuario")
        else:
            self.area_chat.insert(END, f"{remitente}: {mensaje}\n", "bot")

        self.area_chat.config(state="disabled")
        self.area_chat.see(END)  #Auto-scroll al final
"""
    def mostrar_mensaje(self, remitente, mensaje):
        self.area_chat.config(state="normal")
        self.area_chat.insert(END, f"{remitente}: {mensaje}\n\n")
        self.area_chat.see(END)
        self.area_chat.config(state="disabled")
"""

# ----- Ejecución principal -----
if __name__ == "__main__":
    API_KEY = ""
    bot = Chatbot(api_key=API_KEY)
    InterfazChatbot(chatbot=bot)
