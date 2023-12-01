from tkinter import *
import tkinter as tk
#python controller.py

window = tk.Tk()
window.title('Project AI')
window.geometry('500x500')
window.attributes('-topmost',True) #Cố định window

#Menu setup
name = tk.Label(window,font = ('Arial',25),text = 'Menu', fg = 'Black')
name.pack()

button_level1 = tk.Button(window, font = ('Arial',15), text = 'Level 1', width = 20, height = 1, bg = 'Brown')
button_level1.place(x = 137, y = 100)

button_level2 = tk.Button(window, font = ('Arial',15), text = 'Level 2', width = 20, height = 1, bg = 'Brown')
button_level2.place(x = 137, y = 170)

button_level3 = tk.Button(window, font = ('Arial',15), text = 'Level 3', width = 20, height = 1, bg = 'Brown')
button_level3.place(x = 137, y = 240)

button_level4 = tk.Button(window, font = ('Arial',15), text = 'Level 4', width = 20, height = 1, bg = 'Brown')
button_level4.place(x = 137, y = 310)


window.mainloop()