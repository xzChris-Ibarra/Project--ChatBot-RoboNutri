from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
import inicio_sesion, perfiles
import json, os, re, pyodbc
from db_connection import connection_string

CONFIG_FILE = "window_position.json" # Use the same config file

class RegistroWindow(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("505x786")
        self.configure(bg="#FFFFFF")
        self.load_geometry()
        self.resizable(False, False)

        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(r"assets_Registro\frame0")

        self.setup_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def setup_ui(self):
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

        # Images
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(252.0, 393.0, image=self.image_image_1)

        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(252.3, 393.58, image=self.image_image_2)

        self.image_image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.canvas.create_image(252.0, 736.0, image=self.image_image_3)

        self.image_image_4 = PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.canvas.create_image(252.06, 136.0, image=self.image_image_4)

        # Botones
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_login_button_clicked(),
            relief="flat"
        )
        self.button_1.place(x=147.0, y=635.0, width=211.0, height=44.0)

        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_back_button_clicked(),
            relief="flat"
        )
        self.button_2.place(x=30.0, y=45.25, width=30.38, height=30.37)

        # Entradas
        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.canvas.create_image(252.88, 594.17, image=self.entry_image_1)
        self.entry_1 = Entry(bd=0, bg="#E6E3F9", fg="#000716", highlightthickness=0)
        self.entry_1.place(x=132.0, y=572.0, width=241.77, height=42.34)

        self.entry_image_2 = PhotoImage(file=self.relative_to_assets("entry_2.png"))
        self.canvas.create_image(252.76, 480.77, image=self.entry_image_2)
        self.entry_2 = Entry(bd=0, bg="#E6E3F9", fg="#000716", highlightthickness=0)
        self.entry_2.place(x=131.87, y=458.60, width=241.77, height=42.34)

        self.entry_image_3 = PhotoImage(file=self.relative_to_assets("entry_3.png"))
        self.canvas.create_image(330.66, 355.5, image=self.entry_image_3)
        self.entry_3 = Entry(bd=0, bg="#E6E3F9", fg="#000716", highlightthickness=0)
        self.entry_3.place(x=191.66, y=333.0, width=278.0, height=43.0)

        self.entry_image_4 = PhotoImage(file=self.relative_to_assets("entry_4.png"))
        self.canvas.create_image(330.66, 288.0, image=self.entry_image_4)
        self.entry_4 = Entry(bd=0, bg="#E6E3F9", fg="#000716", highlightthickness=0)
        self.entry_4.place(x=191.66, y=266.0, width=278.0, height=42.0)

        # Rectángulos y etiquetas
        self.canvas.create_rectangle(164.0, 518.0, 342.0, 562.0, fill="#9289CA", outline="")
        self.canvas.create_text(169.0, 520.0, anchor="nw", text="Contraseña", fill="#000000", font=("Fredoka Medium", -32))

        self.canvas.create_rectangle(192.0, 406.0, 305.0, 450.0, fill="#8F87C8", outline="")
        self.canvas.create_text(198.0, 408.0, anchor="nw", text="Correo", fill="#000000", font=("Fredoka Medium", -32))

        self.canvas.create_rectangle(41.0, 334.0, 169.0, 378.0, fill="#9289CA", outline="")
        self.canvas.create_text(52.0, 338.0, anchor="nw", text="Apellido", fill="#000000", font=("Fredoka Medium", -32))

        self.canvas.create_rectangle(41.0, 266.0, 169.0, 310.0, fill="#8F87C8", outline="")
        self.canvas.create_text(47.0, 269.0, anchor="nw", text="Nombre", fill="#000000", font=("Fredoka Medium", -32))


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
        self.save_geometry()
        self.destroy()

    def on_back_button_clicked(self):
        self.save_geometry()
        self.destroy()
        new_root = inicio_sesion.LoginWindow()
        new_root.mainloop()

    def on_login_button_clicked(self):
        if self.validate_entrys():
            nombre = self.entry_4.get()+" "+self.entry_3.get()
            email = self.entry_2.get()
            contraseña = self.entry_1.get()
            cnxn = pyodbc.connect(connection_string)
            cursor = cnxn.cursor()
            sql_query = "INSERT INTO Cuenta Values ('"+nombre+"','"+email+"','"+contraseña+"');"
            try:
                cursor.execute(sql_query)
                cnxn.commit()
                sql_query = "Select IDCuenta from Cuenta Where Correo='"+email+"';"
                cursor.execute(sql_query)
                cuenta = cursor.fetchall().pop()[0]
                cursor.close()
                cnxn.close()
                messagebox.showinfo("Information","Registro completo. Iniciando Sesion.")
                self.on_register_successeful(cuenta)
            except pyodbc.IntegrityError:
                messagebox.showwarning("Warning","El correo electronico ya esta en uso.")
            cursor.close()
            cnxn.close()

    def on_register_successeful(self,cuenta):
        self.save_geometry()
        self.destroy()
        new_root = perfiles.PerfilWindow(cuenta)
        new_root.mainloop()

    def validate_entrys(self):
        entradas = [self.entry_1.get(),self.entry_2.get(),self.entry_3.get(),self.entry_4.get()]
        for entrada in entradas:
            if len(entrada)==0:
                messagebox.showwarning("Information","Todos los campos deben estar rellenados.")
                return False
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        email = self.entry_2.get()
        if re.match(email_pattern, email):
            return True
        messagebox.showerror("Error","Formato de Correo Electronico Invalido")
        return False

if __name__ == "__main__":
    app = RegistroWindow()
    app.mainloop()