from numpy import pi, e
from animation import *
from customtkinter import *


def str_to_num(s):
    lst = s.split(',')
    arr = np.array([eval(lst[j]) for j in range(len(lst))])
    return arr


def my_float(s):
    constants = {"pi": pi, "e": e}
    if s in constants:
        return constants[s]
    else:
        return float(s)


def checked():
    if cb.get() == 1:
        name.pack(pady=12, padx=10)
    else:
        name.pack_forget()


def clicked():
    global name_string
    mass1 = float(m1.get())
    mass2 = float(m2.get())
    length1 = float(L1.get())
    length2 = float(L2.get())
    gravity = float(g.get())
    damping = float(b.get())
    time = float(t.get())
    saving = cb.get()
    string_ic = ic.get()
    initial_conditions = str_to_num(string_ic)
    lbl.configure(text="Loading...")
    if selected.get() == "2D":
        if saving == 1:
            lbl.configure(text="Close animation to save!")
            name_string = name.get()
        ani_2d = animate2d(initial_conditions, mass1, mass2, length1, length2, gravity, damping, time)
        if saving == 1:
            saving_window = CTkToplevel(window)
            saving_window.title("Saving...")
            saving_window.geometry('250x150')
            progressbar = CTkProgressBar(master=saving_window)
            save_lbl = CTkLabel(saving_window, text="Saving...")
            save_lbl.pack(pady=12, padx=10)
            progressbar.pack(pady=12, padx=10)
            ani_2d.save(f'{name_string}.mp4', fps=100, progress_callback=lambda j, n: progressbar.set(j / n))
            save_lbl.configure(text="Saved!")
    elif selected.get() == "3D":
        if saving == 1:
            lbl.configure(text="Close animation to save!")
            name_string = name.get()
        ani_3d = animate3d(initial_conditions, mass1, mass2, length1, length2, gravity, damping, time)
        if saving == 1:
            saving_window = CTkToplevel(window)
            saving_window.title("Saving...")
            saving_window.geometry('250x150')
            progressbar = CTkProgressBar(master=saving_window)
            save_lbl = CTkLabel(saving_window, text="Saving...")
            save_lbl.pack(pady=12, padx=10)
            progressbar.pack(pady=12, padx=10)
            ani_3d.save(f'{name_string}.mp4', fps=100, progress_callback=lambda j, n: progressbar.set(j / n))
            save_lbl.configure(text="Saved!")
    else:
        lbl.configure(text="Enter number of dimensions!")


set_appearance_mode('light')
set_default_color_theme('blue')

window = CTk()
window.title("Double pendulum!")
window.geometry('600x800')

frame = CTkFrame(master=window)
frame.pack(pady=20, padx=60, fill='both', expand=True)

selected = StringVar()
option_menu = CTkOptionMenu(frame, values=["2D", "3D"], variable=selected)
option_menu.pack(pady=12, padx=10)
option_menu.set("Dimensions")


m1 = CTkEntry(frame, width=300, placeholder_text="Enter mass of first ball:")
m1.pack(pady=12, padx=10)
m2 = CTkEntry(frame, width=300, placeholder_text="Enter mass of second ball:")
m2.pack(pady=12, padx=10)
L1 = CTkEntry(frame, width=300, placeholder_text="Enter length of first ball:")
L1.pack(pady=12, padx=10)
L2 = CTkEntry(frame, width=300, placeholder_text="Enter length of second ball:")
L2.pack(pady=12, padx=10)
g = CTkEntry(frame, width=300, placeholder_text="Enter gravity:")
g.pack(pady=12, padx=10)
b = CTkEntry(frame, width=300, placeholder_text="Enter damping coefficient:")
b.pack(pady=12, padx=10)
t = CTkEntry(frame, width=300, placeholder_text="Enter time of animation:")
t.pack(pady=12, padx=10)
ic = CTkEntry(frame, width=300,
              placeholder_text="Enter initial conditions separated by commas: θ1(0), θ2(0), θ1'(0), θ2'(0)")
ic.pack(pady=12, padx=10)


btn = CTkButton(frame, text="Animation!", command=clicked)
btn.pack(pady=12, padx=10)
lbl = CTkLabel(frame, text="Waiting...")
lbl.pack(pady=12, padx=10)
cb = CTkCheckBox(master=frame, text="Save animation", command=checked, hover=True)
cb.pack(pady=12, padx=10)
name = CTkEntry(frame, width=300, placeholder_text="Enter saving name:")
name_string = name.get()

window.mainloop()
