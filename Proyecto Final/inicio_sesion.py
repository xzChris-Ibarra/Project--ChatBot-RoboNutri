from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
import registro, perfiles
import json
import os
import pyodbc
from db_connection import connection_string

CONFIG_FILE = "window_position.json" # Use the same config file

class LoginWindow(Tk):  # Hereda directamente de Tk
    def __init__(self):
        super().__init__()  # Inicializa la clase base (Tk)
        self.geometry("505x786")
        self.configure(bg="#FFFFFF")
        self.load_geometry()
        self.resizable(False, False)

        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(r"assets_Login\frame0")

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

        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(252.0, 393.0, image=self.image_image_1)

        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(252.3, 393.58, image=self.image_image_2)

        self.image_image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.canvas.create_image(252.0, 726.0, image=self.image_image_3)

        self.image_image_4 = PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.canvas.create_image(252.3, 193.63, image=self.image_image_4)

        self.canvas.create_rectangle(
            11.15, 376.0, 494.15, 677.0,
            fill="#FFFEEF", outline="")

        # Botón 1
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_register_clicked,
            relief="flat"
        )
        self.button_1.place(x=281.0, y=646.0, width=100.0, height=20.0)

        self.canvas.create_text(
            125.0, 646.0,
            anchor="nw",
            text="¿No tienes una cuenta?",
            fill="#000000",
            font=("Quicksand Regular", 14 * -1)
        )

        # Botón 2
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_login_clicked,
            relief="flat"
        )
        self.button_2.place(x=188.0, y=603.0, width=129.0, height=33.0)

        # Entrada 1 - Contraseña
        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.canvas.create_image(252.89, 565.0, image=self.entry_image_1)

        self.entry_1 = Entry(
            bd=0,
            bg="#58B5FD",
            fg="#000716",
            highlightthickness=0,
            show="*"
        )
        self.entry_1.place(x=131.89, y=544.0, width=242.0, height=40.0)

        self.canvas.create_rectangle(150.0, 486.0, 356.0, 536.0, fill="#C9EFFA", outline="")
        self.canvas.create_text(
            168.0, 491.0,
            anchor="nw",
            text="Contraseña",
            fill="#000000",
            font=("Fredoka Medium", 32 * -1)
        )

        # Entrada 2 - Correo
        self.entry_image_2 = PhotoImage(file=self.relative_to_assets("entry_2.png"))
        self.canvas.create_image(252.89, 447.0, image=self.entry_image_2)

        self.entry_2 = Entry(
            bd=0,
            bg="#58B5FD",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_2.place(x=131.89, y=426.0, width=242.0, height=40.0)

        self.canvas.create_rectangle(181.0, 380.0, 325.0, 418.0, fill="#C9EFFA", outline="")
        self.canvas.create_text(
            203.0, 380.0,
            anchor="nw",
            text="Correo",
            fill="#000000",
            font=("Fredoka Medium", 32 * -1)
        )

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
    
    def on_login_clicked(self):
        contraseña = self.entry_1.get()
        correo = self.entry_2.get()
        cnxn = pyodbc.connect(connection_string)
        cursor = cnxn.cursor()
        sql_query = "SELECT * FROM Cuenta Where Correo = '"+correo+"';"
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        if rows:
            fila = rows.pop()
            if (fila[3]) == contraseña:
                messagebox.showinfo("Information","Inicio de Sesion Exitoso")
                cursor.close()
                cnxn.close()
                self.on_login_successful(fila[0])
            else:
                messagebox.showerror("Error","Contraseña Incorrecta")
        else:
            messagebox.showinfo("Warning","Correo No Encontrado")
        cursor.close()
        cnxn.close()

    def on_login_successful(self,cuenta):
        self.save_geometry()
        self.destroy()
        new_root = perfiles.PerfilWindow(cuenta)
        new_root.mainloop()

    def on_register_clicked(self):
        self.save_geometry()
        self.destroy()

        new_root = registro.RegistroWindow()
        new_root.mainloop()


if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()