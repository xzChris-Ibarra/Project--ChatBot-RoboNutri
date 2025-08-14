from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, messagebox
import inicio_sesion, historial
import json, os, pyodbc
from db_connection import connection_string

CONFIG_FILE = "window_position.json"

class PerfilWindow(Tk):
    def __init__(self,Cuenta):
        super().__init__()
        self.geometry("505x786")
        self.configure(bg="#FFFFFF")
        self.load_geometry()
        self.resizable(False, False)
        self.IDCuenta = Cuenta
        self.perfil_seleccionado = 0
        self.active_button = None
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(r"assets_Perfiles\frame0")

        self.setup_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def setup_ui(self):
        self.canvas = Canvas(self, bg="#FFFFFF", height=786, width=505, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        vcmd = (self.register(self.only_numbers), "%P")

        # Imágenes
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(252.0, 393.0, image=self.image_image_1)

        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(252.3, 393.58, image=self.image_image_2)

        self.image_image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.canvas.create_image(267.28, 63.43, image=self.image_image_3)

        self.image_image_4 = PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.canvas.create_image(229.0, 363.0, image=self.image_image_4)

        # Botones
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(image=self.button_image_1, borderwidth=0, highlightthickness=0,
                               command=lambda: print("button_1 clicked"), relief="flat")
        self.button_1.place(x=436.33, y=251.17, width=58.04, height=300.67)

        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_4.png"))
        self.button_4 = Button(image=self.button_image_4, borderwidth=0, highlightthickness=0,
                               command=lambda: self.on_back_button_clicked(), relief="flat")
        self.button_4.place(x=51.65, y=45.25, width=30.39, height=30.37)

        self.button_image_5 = PhotoImage(file=self.relative_to_assets("button_5.png"))
        self.button_5 = Button(image=self.button_image_5, borderwidth=0, highlightthickness=0,
                               command=lambda: self.on_create_perfil_button_clicked(), relief="flat")
        self.button_5.place(x=41.0, y=237.0, width=150.0, height=43.0)

        self.button_image_6 = PhotoImage(file=self.relative_to_assets("button_6.png"))
        self.button_6 = Button(image=self.button_image_6, borderwidth=0, highlightthickness=0,
                               command=lambda: self.on_erase_perfil_button_clicked(), relief="flat")
        self.button_6.place(x=253.0, y=237.0, width=164.0, height=43.0)

        self.button_image_7 = PhotoImage(file=self.relative_to_assets("button_7.png"))
        self.button_7 = Button(image=self.button_image_7, borderwidth=0, highlightthickness=0,
                               command=lambda: self.on_next_button_clicked(), relief="flat")
        self.button_7.place(x=163.0, y=664.0, width=175.0, height=48.0)

        # Rectángulo y texto
        self.canvas.create_rectangle(178.0, 154.0, 328.0, 200.0, fill="#9D97D4", outline="")
        self.canvas.create_text(191.37, 154.13, anchor="nw", text="Perfiles", fill="#FFFFFF",
                                font=("PaytoneOne Regular", -32))

        self.canvas.create_text(51.0, 304.0, anchor="nw", text="Nombre:", fill="#000000",
                                font=("Palanquin Regular", -16))
        self.canvas.create_text(234.0, 304.0, anchor="nw", text="Apellido:", fill="#000000",
                                font=("Palanquin Regular", -16))
        self.canvas.create_text(51.0, 357.0, anchor="nw", text="Edad:", fill="#000000",
                                font=("Palanquin Regular", -16))
        self.canvas.create_text(172.0, 357.0, anchor="nw", text="Alergias:", fill="#000000",
                                font=("Palanquin Regular", -16))

        # Entradas
        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.canvas.create_image(174.0, 318.5, image=self.entry_image_1)
        self.entry_1 = Entry(bd=0, bg="#AADAFF", fg="#000716", highlightthickness=0)
        self.entry_1.place(x=119.0, y=304.0, width=110.0, height=27.0)

        self.entry_image_2 = PhotoImage(file=self.relative_to_assets("entry_2.png"))
        self.canvas.create_image(326.0, 388.0, image=self.entry_image_2)
        self.entry_2 = Text(bd=0, bg="#A2DDFF", fg="#000716", highlightthickness=0)
        self.entry_2.place(x=240.0, y=357.0, width=172.0, height=60.0)

        self.entry_image_3 = PhotoImage(file=self.relative_to_assets("entry_3.png"))
        self.canvas.create_image(127.0, 371.5, image=self.entry_image_3)
        self.entry_3 = Entry(bd=0, bg="#AADAFF", fg="#000716", highlightthickness=0, validate="key", validatecommand=vcmd)
        self.entry_3.place(x=103.0, y=357.0, width=48.0, height=27.0)

        self.entry_image_4 = PhotoImage(file=self.relative_to_assets("entry_4.png"))
        self.canvas.create_image(357.0, 318.5, image=self.entry_image_4)
        self.entry_4 = Entry(bd=0, bg="#AADAFF", fg="#000716", highlightthickness=0)
        self.entry_4.place(x=302.0, y=304.0, width=110.0, height=27.0)


        container = Frame(self, bg="#FFFFFF")
        container.place(x=40, y=450, width=380, height=180)  # Área visible

        self.scroll_canvas = Canvas(container, bg="#FFFFFF", highlightthickness=0)
        self.scroll_canvas.pack(fill="both", expand=True)

        # Frame interno donde van los botones
        self.buttons_frame = Frame(self.scroll_canvas, bg="#FFFFFF")
        self.scroll_canvas.create_window((0, 0), window=self.buttons_frame, anchor="nw")

        # Ajusta el área de scroll cuando cambie el tamaño
        self.buttons_frame.bind(
            "<Configure>",
            lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        )

        # Vincular scroll con la rueda del mouse
        self.scroll_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Lista de ejemplo
        cnxn = pyodbc.connect(connection_string)
        cursor = cnxn.cursor()
        sql_query = "Select IDPerfil, Nombre FROM Perfil Where IDCuenta = "+str(self.IDCuenta)+";"
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        cursor.close()
        cnxn.close()
        self.generate_dynamic_buttons(rows)

    def only_numbers(self, value_if_allowed):
        if value_if_allowed.isdigit() or value_if_allowed == "":
            return True
        return False

    def _on_mousewheel(self, event):
        """Desplazar con la rueda del mouse."""
        self.scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def generate_dynamic_buttons(self, items):
        # Limpiar botones anteriores
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        for text in items:
            btn = Button(
                self.buttons_frame,
                text="Perfil: "+text[1],
                bg="#AADAFF",
                fg="black",
                font=("Arial", 14, "bold"),
                relief="flat",
                height=2,
                width=32
            )
            btn.configure(command=lambda t=text[0], b=btn: self.on_button_click(t, b))
            btn.pack(pady=5)
    
    def on_button_click(self, idPerfil, button):
        """Gestiona el botón activo."""
        # Si hay un botón activo previo, restablecerlo
        if self.active_button:
            self.active_button.configure(bg="#AADAFF")  # Color normal
        
        self.perfil_seleccionado = idPerfil
        # Activar este botón
        button.configure(bg="#6FC3FF")  # Color de selección
        self.active_button = button

        #print(f"Botón '{self.perfil_seleccionado}' seleccionado")

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
        new_root = inicio_sesion.LoginWindow()
        new_root.mainloop()

    def validate_entrys(self):
        entradas = [self.entry_1.get(),self.entry_3.get(),self.entry_4.get()]
        for entrada in entradas:
            if len(entrada)==0:
                messagebox.showwarning("Information","Los campos Nombre, Apellido y Edad deben estar rellenados.")
                return False
        edad = int(self.entry_3.get())
        if edad < 6 or edad > 14:
            messagebox.showwarning("Warning","La edad ingresada se encuentra fuera del rango para el uso adecuado de esta aplicación (De 8 a 12 años)")
            return False
        elif edad < 8 or edad > 12:
            respuesta = messagebox.askyesno("Confirmation","El uso optimo del contenido se encuentra entre el rango de edad de los 8 a 12 años ¿Desea continuar?")
            if respuesta:
                return True
            return False
        else:
            return True
    
    def on_create_perfil_button_clicked(self):
        if self.validate_entrys():
            nombre = self.entry_1.get()+" "+self.entry_4.get()
            edad = self.entry_3.get()
            alergias = self.entry_2.get("1.0","end-1c")
            cnxn = pyodbc.connect(connection_string)
            cursor = cnxn.cursor()
            cuenta = str(self.IDCuenta)
            if alergias == "":
                sql_query = "INSERT INTO Perfil Values ("+cuenta+",'"+nombre+"',"+edad+",'Ninguna');"
            else:
                sql_query = "INSERT INTO Perfil Values ("+cuenta+",'"+nombre+"',"+edad+",'"+alergias+"');"
            cursor.execute(sql_query)
            cnxn.commit()
            cursor.close()
            cnxn.close()
            messagebox.showinfo("Information","Perfil creado exitosamente.")
            self.setup_ui()

    def on_erase_perfil_button_clicked(self):
        if self.perfil_seleccionado == 0:
            messagebox.showinfo("Information","Seleccione un perfil")
        else:
            cnxn = pyodbc.connect(connection_string)
            cursor = cnxn.cursor()
            perfil = str(self.perfil_seleccionado)
            sql_query = "Select Nombre, Edad, Alergias FROM Perfil Where IDPerfil ="+perfil+";"
            cursor.execute(sql_query)
            rows = cursor.fetchall().pop()
            pregunta = messagebox.askyesno("Warning","Desea eliminar el siguiente perfil.\nNombre: "+rows[0]+"\nEdad: "+str(rows[1])+"\nAlergias: "+rows[2]+"\n¿Desea continuar?")
            if pregunta:
                sql_query ="DELETE FROM Historial Where IDPerfil ="+perfil
                cursor.execute(sql_query)
                cnxn.commit()
                sql_query="DELETE FROM Perfil Where IDPerfil ="+perfil
                cursor.execute(sql_query)
                cnxn.commit()
                messagebox.showinfo("Information","Perfil Eliminado.")
                self.setup_ui()
            else:
                messagebox.showinfo("Information","Operación Cancelada")
            cursor.close()
            cnxn.close()

    def on_next_button_clicked(self):
        if self.perfil_seleccionado == 0:
            messagebox.showinfo("Information","Seleccione un perfil")
        else:
            self.save_geometry()
            self.destroy()
            new_root = historial.HistorialWindow(self.perfil_seleccionado)
            new_root.mainloop()

if __name__ == "__main__":
    app = PerfilWindow(1)
    app.mainloop()
