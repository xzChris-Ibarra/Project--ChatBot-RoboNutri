from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\chris\Downloads\Code Python ChatBot RoboNutri gui\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("505x786")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 786,
    width = 505,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    505.0,
    786.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    11.24249267578125,
    11.54095458984375,
    494.2342224121094,
    774.4752197265625,
    fill="#FFFEEF",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=47.882781982421875,
    y=51.14384460449219,
    width=39.55538558959961,
    height=30.207761764526367
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=421.1307373046875,
    y=38.7843017578125,
    width=55.02061462402344,
    height=57.41300582885742
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    160.8828125,
    400.60430908203125,
    image=image_image_1
)

canvas.create_rectangle(
    28.8486328125,
    662.6927490234375,
    479.12542724609375,
    760.7224044799805,
    fill="#A2DDFF",
    outline="")

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    80.93463134765625,
    711.2867431640625,
    image=image_image_2
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    271.5341491699219,
    713.2344551086426,
    image=entry_image_1
)
entry_1 = Text(
    bd=0,
    bg="#FFFEEF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=133.23910522460938,
    y=679.79443359375,
    width=276.590087890625,
    height=64.88004302978516
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=418.1566162109375,
    y=679.7944946289062,
    width=53.23616027832031,
    height=66.88004302978516
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    259.85986328125,
    100.74111938476562,
    image=image_image_3
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=436.32977294921875,
    y=251.16766357421875,
    width=57.99469757080078,
    height=300.8075866699219
)
window.resizable(False, False)
window.mainloop()
