from Tkinter import *
from tkFileDialog import askopenfilename, askopenfilenames, askdirectory, asksaveasfilename
from PIL import ImageTk, Image

from gribreader import Grb, Grib

# Global Variables
FILE_NAME = None
GRIB = None
PARAMETERS = []
CURRENT_PAR = None
SELECTED_PAR = None
PLOT = None

# Define layout
root = Tk()
root.title("Grib Reader")
root.resizable(0, 0)
root.geometry("300x690")


# Global Methods
def raise_frame(frame):
    """Raise frame"""
    frame.grid(row=0, column=0, padx=15, pady=20, sticky=N + S + E + W)
    frame.tkraise()


def _quit():
    root.destroy()


def select_file():
    global PARAMETERS
    global GRIB
    FILE_NAME = askopenfilename(
        filetypes=(("Grib Files", "*.grib2"), ("All files", "*.*")), title="Select Grib File"
    )
    GRIB = Grib(path=FILE_NAME)
    PARAMETERS = GRIB.parameters
    f1_parameters.insert(END, *PARAMETERS)
    f2_parameters.insert(END, *PARAMETERS)


def poll_listbox():
    global CURRENT_PAR
    global SELECTED_PAR
    for box in [f1_parameters, f2_parameters]:
        now = box.curselection()
        if now != CURRENT_PAR:
            CURRENT_PAR = now
            if CURRENT_PAR:
                SELECTED_PAR = PARAMETERS[CURRENT_PAR[0]]
    f1_parameters.after(250, poll_listbox)


def plot_data():
    global PLOT
    if GRIB:
        grad = GRIB.select(SELECTED_PAR)
        plt = grad.plot_obj()
        plt.show()


# Frame Management
f0 = Frame(root)
f1 = Frame(root)
f2 = Frame(root)
f3 = Frame(root)
f4 = Frame(root)
f5 = Frame(root)

raise_frame(f0)


# Menu Management
menu = Menu(root)
root.config(menu=menu)

menu.add_command(label="Home", command=lambda: raise_frame(f0))
submenu = Menu(menu)
menu.add_cascade(label="Menu", menu=submenu)
submenu.add_command(label="PLOTING DATA", command=lambda: raise_frame(f1))
submenu.add_command(label="POINT VALUE", command=lambda: raise_frame(f2))
submenu.add_command(label="EXPORT DATA", command=lambda: raise_frame(f3))
submenu.add_command(label="EXPORT COMP", command=lambda: raise_frame(f4))
submenu.add_command(label="PLOT TEXT DATA", command=lambda: raise_frame(f5))

menu.add_command(label="Help", command="")


# Common data for frames
img_h = ImageTk.PhotoImage(Image.open("images/image3775.png"))
# img_h = PhotoImage(file="Images/logo_grib.png")

for frame, name in zip((f0, f1, f2, f3, f4, f5), ("f0", "f1", "f2", "f3", "f4", "f5")):
    panel_h = Label(frame, image=img_h)
    panel_h.pack(fill=X)

    if frame in [f1, f2, f3]:
        source_file = Button(
            frame, text="Select grib2 file", padx=26, pady=5, fg="blue", command=select_file
        )
        source_file.pack(fill=X, pady=2)

# FRAME-0
frame_1 = Button(
    f0, text="PLOTING DATA", font=("Helvetica", 10), fg="gray", command=lambda: raise_frame(f1)
)
frame_1.pack(pady=2, fill=X)

frame_2 = Button(
    f0, text="POINT VALUE", font=("Helvetica", 10), fg="gray", command=lambda: raise_frame(f2)
)
frame_2.pack(pady=2, fill=X)

frame_3 = Button(
    f0, text="EXPORT DATA", font=("Helvetica", 10), fg="gray", command=lambda: raise_frame(f3)
)
frame_3.pack(pady=2, fill=X)

frame_4 = Button(
    f0, text="EXPORT COMP", font=("Helvetica", 10), fg="gray", command=lambda: raise_frame(f4)
)
frame_4.pack(pady=2, fill=X)

frame_5 = Button(
    f0, text="PLOT TEXT DATA", font=("Helvetica", 10), fg="gray", command=lambda: raise_frame(f5)
)
frame_5.pack(pady=2, fill=X)


# FRAME-1 (Ploting Data)
f1_title = Label(f1, text="Parameters Plotting")
f1_title.pack(pady=2)

f1_parameters = Listbox(f1, selectmode=EXTENDED)
f1_parameters.pack(fill=X, expand=0)


plot_button = Button(f1, text="PLOT", padx=58, pady=10, fg="green", command=plot_data)
plot_button.pack(pady=2, fill=X)

stop_plot_button = Button(f1, text="STOP", padx=58, pady=10, fg="red", command=_quit)
stop_plot_button.pack(pady=2, fill=X)


lat_indi = Label(f1, text=" ")
lat_indi.pack(pady=2)

lon_indi = Label(f1, text=" ")
lon_indi.pack(pady=2)


# FRAME-2 (Point data value)
f2_title = Label(f2, text="Parameters Data Value")
f2_title.pack(pady=2)

f2_parameters = Listbox(f2, selectmode=EXTENDED)
f2_parameters.pack(fill=X, expand=0)


# UP gui
poll_listbox()
root.mainloop()
