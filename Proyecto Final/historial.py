from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox, Frame, ttk
import tkinter as tk
import json
import os
import pyodbc
import perfiles, chat
from db_connection import connection_string

CONFIG_FILE = "window_position.json"

class HistorialWindow(Tk):
    def __init__(self, perfil):
        super().__init__()
        self.geometry("505x786")
        self.configure(bg="#FFFFFF")
        self.load_geometry()
        self.resizable(False, False)
        self.IDPerfil = perfil
        self.idCuenta = 0
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(r"assets_Historial\frame0")

        self.build_ui()
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

        # Imágenes de fondo
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(252.0, 393.0, image=self.image_image_1)

        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(252.3, 393.58, image=self.image_image_2)

        self.image_image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.canvas.create_image(255.08, 71.27, image=self.image_image_3)

        # Botón 1
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_start_chatbot_button_clicked(),
            relief="flat"
        )
        self.button_1.place(x=345.0, y=588.0, width=112.0, height=98.0)

        # Rectángulos y texto
        self.canvas.create_rectangle(290.36, 251.0, 494.36, 552.0, fill="#00A935", outline="")
        self.canvas.create_rectangle(333.36, 310.0, 494.36, 544.0, fill="#B3FFB5", outline="")

        self.image_image_4 = PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.canvas.create_image(311.26, 393.20, image=self.image_image_4)

        self.image_image_5 = PhotoImage(file=self.relative_to_assets("image_5.png"))
        self.canvas.create_image(306.36, 286.0, image=self.image_image_5)

        # Botones extra con la misma estructura que button_1
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        self.button_2.place(x=338.36, y=485.0, width=151.63, height=47.0)

        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_3 = Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        self.button_3.place(x=338.36, y=428.0, width=151.63, height=47.0)

        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_4.png"))
        self.button_4 = Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_4 clicked"),
            relief="flat"
        )
        self.button_4.place(x=338.0, y=378.0, width=152.0, height=39.0)

        self.button_image_5 = PhotoImage(file=self.relative_to_assets("button_5.png"))
        self.button_5 = Button(
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_5 clicked"),
            relief="flat"
        )
        self.button_5.place(x=338.36, y=323.0, width=151.63, height=48.0)

        self.canvas.create_text(338.0, 272.0, anchor="nw", text="Nutriólogo", fill="#FFFFFF", font=("PaytoneOne Regular", 20 * -1))

        self.canvas.create_rectangle(22.0, 253.0, 272.0, 290.0, fill="#A75050", outline="")
        self.canvas.create_text(92.0, 253.0, anchor="nw", text="Historial", fill="#000000", font=("PaytoneOne Regular", 24 * -1))

        self.image_image_6 = PhotoImage(file=self.relative_to_assets("image_6.png"))
        self.canvas.create_image(72.0, 271.0, image=self.image_image_6)

        # Obtener perfil e historial
        perfil = str(self.IDPerfil)
        cnxn = pyodbc.connect(connection_string)
        cursor = cnxn.cursor()

        sql_query = "Select Nombre From Perfil Where IDPerfil =" + perfil + ";"
        cursor.execute(sql_query)
        perfil_name = cursor.fetchall().pop()[0]

        sql_query = "Select IDCuenta From Perfil Where IDPerfil =" + perfil + ";"
        cursor.execute(sql_query)
        self.idCuenta = cursor.fetchall().pop()[0]

        self.canvas.create_text(22.0, 173.0, anchor="nw", text="Perfil: " + perfil_name, fill="#000000", font=("Fredoka Regular", 36 * -1))

        # Botones superiores
        self.button_image_6 = PhotoImage(file=self.relative_to_assets("button_6.png"))
        self.button_6 = Button(
            image=self.button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.mostrar(),
            relief="flat"
        )
        self.button_6.place(x=385.0, y=67.0, width=57.0, height=48.0)

        self.button_image_9 = PhotoImage(file=self.relative_to_assets("button_9.png"))
        self.button_9 = Button(
            image=self.button_image_9,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_back_button_clicked,
            relief="flat"
        )
        self.button_9.place(x=83.0, y=81.0, width=30.38, height=30.37)

        sql_query = "Select Historial, FechaHora From Historial Where IDPerfil =" + perfil + ";"
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        if rows:
            self.acumulador = []
            for row in rows:
                row[0] = row[0].replace("\\n", "\n")
                self.acumulador.append({"nombre": "Chat de " + str(row[1]), "info": row[0]})

            container = Frame(self, bg="#FFFFFF")
            container.place(x=25, y=300, width=244, height=380)

            self.scroll_canvas = Canvas(container, bg="#FFFFFF", highlightthickness=0)
            self.scroll_canvas.pack(fill="both", expand=True)

            self.buttons_frame = Frame(self.scroll_canvas, bg="#FFFFFF")
            self.scroll_canvas.create_window((0, 0), window=self.buttons_frame, anchor="nw")

            self.buttons_frame.bind(
                "<Configure>",
                lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
            )
            self.scroll_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

            self.generate_dynamic_buttons(self.acumulador)
        else:
            self.canvas.create_text(55.0, 310.0, anchor="nw", text="No hay Historial", fill="#000000", font=("Fredoka Regular", 26 * -1))

        cursor.close()
        cnxn.close()

    def generate_dynamic_buttons(self, items):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        def mostrar_info(nombre, info):
            messagebox.showinfo(title=nombre, message=info)

        for item in items:
            b = Button(
                self.buttons_frame,
                text=item["nombre"],
                width=20,
                height=2,
                bg="#AADAFF",
                fg="black",
                font=("Arial", 14, "bold"),
                relief="flat",
                command=lambda n=item["nombre"], i=item["info"]: mostrar_info(n, i)
            )
            b.pack(pady=5)

    def _on_mousewheel(self, event):
        self.scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def save_geometry(self):
        geometry = self.winfo_geometry()
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"geometry": geometry}, f)

    def load_geometry(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    geometry = config.get("geometry")
                    if geometry:
                        self.geometry(geometry)
            except json.JSONDecodeError:
                pass

    def on_closing(self):
        self.save_geometry()
        self.destroy()

    def on_back_button_clicked(self):
        self.save_geometry()
        self.destroy()
        new_root = perfiles.PerfilWindow(self.idCuenta)
        new_root.mainloop()

    def custom_messagebox_with_combobox(self):
    # Ventana modal personalizada
        top = tk.Toplevel(self)
        top.title("Seleccion de Perfil")
        top.geometry("300x150")
        top.resizable(False, False)

        # Evita interactuar con la ventana principal
        top.transient(self)
        top.grab_set()

        # Etiqueta
        tk.Label(top, text="Selecciona un Perfil:", font=("Arial", 11)).pack(pady=10)

        cnxn = pyodbc.connect(connection_string)
        cursor = cnxn.cursor()
        sql_query = "Select Nombre From Perfil Where IDCuenta = "+str(self.idCuenta)+";"
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        cursor.close()
        cnxn.close()
        opciones = []
        for row in rows:
            opciones.append(row[0])

        # Combobox
        combo = ttk.Combobox(top, values=opciones, state="readonly")
        combo.current(0)
        combo.pack(pady=5)

        # Variable para almacenar selección
        seleccion = tk.StringVar()

        def confirmar():
            seleccion.set(combo.get())
            top.destroy()

        # Botón aceptar
        ttk.Button(top, text="Aceptar", command=confirmar).pack(pady=10)

        top.wait_window()  # Espera a que se cierre la ventana
        return seleccion.get()
    
    def mostrar(self):
        try:
            valor = self.custom_messagebox_with_combobox()
            cnxn = pyodbc.connect(connection_string)
            cursor = cnxn.cursor()
            sql_query = "Select IDPerfil From Perfil Where Nombre = '"+valor+"';"
            cursor.execute(sql_query)
            id = cursor.fetchall().pop()[0]
            if id == self.IDPerfil:
                messagebox.showinfo("Information","Ya se encuentra en el perfil seleccionado")
            else:
                messagebox.showinfo("Information","Cambiando de perfil")
                self.IDPerfil = id
                self.build_ui()
        except IndexError:
            messagebox.showerror("Error","Seleccione un Perfil")

    def on_start_chatbot_button_clicked(self):
        messagebox.showinfo("Information","Ingresando al Chatbot")
        self.save_geometry()
        self.destroy()
        API_KEY = ""
        bot = chat.Chatbot(api_key=API_KEY)
        new_root = chat.InterfazChatbot(self.IDPerfil,chatbot=bot)
        new_root.mainloop()

if __name__ == "__main__":
    app = HistorialWindow(1)
    app.mainloop()
