from tkinter import *
import tkinter as tk
#python controller.py
def create_first_window(length_var, width_var):
    global window
    window = tk.Tk()
    window.title('Project AI')
    window.geometry(f"{length_var}x{width_var}")
    window.attributes('-topmost', True)  # Cố định window

    # Menu setup
    name = tk.Label(window, font=('Arial', 25), text='Menu', fg='Black')
    name.pack()

    button_level1 = tk.Button(window, font=('Arial', 15), text='Level 1', width=20, height=1,
                              bg='Brown', command=handle_Button_Level1)
    button_level1.place(x=137, y=100)

    button_level2 = tk.Button(window, font=('Arial', 15), text='Level 2', width=20, height=1,
                              bg='Brown', command=handle_Button_Level2)
    button_level2.place(x=137, y=170)

    button_level3 = tk.Button(window, font=('Arial', 15), text='Level 3', width=20, height=1,
                              bg='Brown', command=handle_Button_Level3)
    button_level3.place(x=137, y=240)

    button_level4 = tk.Button(window, font=('Arial', 15), text='Level 4', width=20, height=1,
                              bg='Brown', command=handle_Button_Level4)
    button_level4.place(x=137, y=310)

    window.mainloop()

def handle_Button_Level1():
    window.destroy()
    newWindow_Level1 = tk.Tk()
    newWindow_Level1.title('Project AI')
    newWindow_Level1.geometry('500x500')
    newWindow_Level1.attributes('-topmost', True)  # Cố định window

    nameLevel1 = tk.Label(newWindow_Level1, font=('Arial', 25), text='Level 1', fg='Black')
    nameLevel1.pack()

    button_level1_astar = tk.Button(newWindow_Level1, font=('Arial', 15), text='A star', width=20, height=1,
                              bg='Brown')
    button_level1_astar.place(x=137, y=130)

    button_level1_bfs = tk.Button(newWindow_Level1, font=('Arial', 15), text='BFS', width=20, height=1,
                              bg='Brown')
    button_level1_bfs.place(x=137, y=230)

    button_level1_dfs = tk.Button(newWindow_Level1, font=('Arial', 15), text='DFS', width=20, height=1,
                              bg='Brown')
    button_level1_dfs.place(x=137, y=330)

    # CODE TEST

    # def handle():
    #     newWindow_Level1.destroy()
    #     create_first_window()
    # button = tk.Button(newWindow_Level1, font=('Arial', 15), text='Level 3', width=20, height=1,
    #                           bg='Brown', command=handle)
    # button.place(x=137, y=240)

    ################################

    newWindow_Level1.mainloop()

def handle_Button_Level2():
    print(2)

def handle_Button_Level3():
    print(3)

def handle_Button_Level4():
    print(4)

create_first_window(500,500)
