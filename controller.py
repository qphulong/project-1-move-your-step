from tkinter import *
import tkinter as tk

import level3
import level2
import level4
import level1
# from level2 import SearchTree
# from level3 import SearchTree
# import level3
# import level1
# import level2
#python controller.py

def create_first_window(length_var, width_var,win):
    win.destroy()
    window = tk.Tk()
    window.title('Project AI')
    window.geometry(f"{length_var}x{width_var}")
    window.attributes('-topmost', True)  # Cố định window

    # Menu setup
    name = tk.Label(window, font=('Arial', 25), text='Menu', fg='Black')
    name.pack()

    button_level1 = tk.Button(window, font=('Arial', 15), text='Level 1', width=20, height=1,
                              bg='Brown', command=lambda: handle_Button_Level1(window))
    button_level1.place(x=137, y=100)

    button_level2 = tk.Button(window, font=('Arial', 15), text='Level 2', width=20, height=1,
                              bg='Brown', command=lambda: handle_Button_Level2(window))
    button_level2.place(x=137, y=170)

    button_level3 = tk.Button(window, font=('Arial', 15), text='Level 3', width=20, height=1,
                              bg='Brown', command=lambda: handle_Button_Level3(window))
    button_level3.place(x=137, y=240)

    button_level4 = tk.Button(window, font=('Arial', 15), text='Level 4', width=20, height=1,
                              bg='Brown', command=lambda: handle_Button_Level4(window))
    button_level4.place(x=137, y=310)

    window.mainloop()

# UI LEVEL 1

def testcase_level1(win,str):
    win.destroy()
    newWindow_TestCaseScreen1 = tk.Tk()
    newWindow_TestCaseScreen1.title('Project AI')
    newWindow_TestCaseScreen1.geometry('500x500')
    newWindow_TestCaseScreen1.attributes('-topmost', True)  # Cố định window

    testCase = tk.Label(newWindow_TestCaseScreen1, font=('Arial', 25), text='Case Menu', fg='Black')
    testCase.pack()

    button_testcase1 = tk.Button(newWindow_TestCaseScreen1, font=('Arial', 15), text='Test case 1', width=20, height=1,
                              bg='Brown',command = lambda: solve_level1(str,1))
    button_testcase1.place(x=137, y=100)

    button_testcase2 = tk.Button(newWindow_TestCaseScreen1, font=('Arial', 15), text='Test case 2', width=20, height=1,
                              bg='Brown',command = lambda: solve_level1(str,2))
    button_testcase2.place(x=137, y=170)

    button_testcase3 = tk.Button(newWindow_TestCaseScreen1, font=('Arial', 15), text='Test case 3', width=20, height=1,
                              bg='Brown',command = lambda: solve_level1(str,3))
    button_testcase3.place(x=137, y=240)

    button_testcase4 = tk.Button(newWindow_TestCaseScreen1, font=('Arial', 15), text='Test case 4', width=20, height=1,
                              bg='Brown',command = lambda: solve_level1(str,4))
    button_testcase4.place(x=137, y=310)

    button_testcase5 = tk.Button(newWindow_TestCaseScreen1, font=('Arial', 15), text='Test case 5', width=20, height=1,
                                 bg='Brown',command = lambda: solve_level1(str,5))
    button_testcase5.place(x=137, y=380)

    back_to_menu = tk.Button(newWindow_TestCaseScreen1, font=('Arial', 15), text='Back to menu', width=20, height=1,
                                 bg='Brown', command=lambda: handle_Button_Level1(newWindow_TestCaseScreen1))
    back_to_menu.place(x=137, y=450)

    newWindow_TestCaseScreen1.mainloop()


def handle_Button_Level1(win):
    win.destroy()
    newWindow_Level1 = tk.Tk()
    newWindow_Level1.title('Project AI')
    newWindow_Level1.geometry('500x500')
    newWindow_Level1.attributes('-topmost', True)  # Cố định window

    nameLevel1 = tk.Label(newWindow_Level1, font=('Arial', 25), text='Level 1', fg='Black')
    nameLevel1.pack()

    button_level1_astar = tk.Button(newWindow_Level1, font=('Arial', 15), text='A star', width=20, height=1,
                              bg='Brown', command = lambda: testcase_level1(newWindow_Level1,"astar"))
    button_level1_astar.place(x=137, y=100)

    button_level1_bfs = tk.Button(newWindow_Level1, font=('Arial', 15), text='BFS', width=20, height=1,
                              bg='Brown', command = lambda: testcase_level1(newWindow_Level1,"bfs"))
    button_level1_bfs.place(x=137, y=170)

    button_level1_dfs = tk.Button(newWindow_Level1, font=('Arial', 15), text='UCS', width=20, height=1,
                              bg='Brown', command = lambda: testcase_level1(newWindow_Level1,"ucs"))
    button_level1_dfs.place(x=137, y=240)

    back = tk.Button(newWindow_Level1, font=('Arial', 15), text='Back', width=20, height=1,
                                  bg='Brown', command=lambda: create_first_window(500,500,newWindow_Level1))
    back.place(x=137, y=310)

    # CODE TEST

    # def handle():
    #     newWindow_Level1.destroy()
    #     create_first_window()
    # button = tk.Button(newWindow_Level1, font=('Arial', 15), text='Level 3', width=20, height=1,
    #                           bg='Brown', command=handle)
    # button.place(x=137, y=240)

    ################################

    newWindow_Level1.mainloop()

#UI MENU LEVEL 2,3,4

def testcase_level234(win,level):
    if(win.winfo_exists()):
        print("Tkinter root window exists.")
        win.destroy()
    else:
        print("Tkinter root window not exists.")
    newWindow_TestCaseScreen1 = tk.Tk()
    newWindow_TestCaseScreen1.title('Project AI')
    newWindow_TestCaseScreen1.geometry('500x500')
    newWindow_TestCaseScreen1.attributes('-topmost', True)  # Cố định window

    testCase = tk.Label(newWindow_TestCaseScreen1, font=('Arial', 25), text='Case Menu', fg='Black')
    testCase.pack()

    button_testcase1 = tk.Button(newWindow_TestCaseScreen1, font=('Arial', 15), text='Test case 1', width=20, height=1,
                              bg='Brown',command = lambda: solve_level(level,newWindow_TestCaseScreen1,1))
    button_testcase1.place(x=137, y=100)

    button_testcase2 = tk.Button(newWindow_TestCaseScreen1, font=('Arial', 15), text='Test case 2', width=20, height=1,
                              bg='Brown',command = lambda: solve_level(level,newWindow_TestCaseScreen1,2))
    button_testcase2.place(x=137, y=170)

    button_testcase3 = tk.Button(newWindow_TestCaseScreen1, font=('Arial', 15), text='Test case 3', width=20, height=1,
                              bg='Brown',command = lambda: solve_level(level,newWindow_TestCaseScreen1,3))
    button_testcase3.place(x=137, y=240)

    button_testcase4 = tk.Button(newWindow_TestCaseScreen1, font=('Arial', 15), text='Test case 4', width=20, height=1,
                              bg='Brown',command = lambda: solve_level(level,newWindow_TestCaseScreen1,4))
    button_testcase4.place(x=137, y=310)

    button_testcase5 = tk.Button(newWindow_TestCaseScreen1, font=('Arial', 15), text='Test case 5', width=20, height=1,
                                 bg='Brown',command = lambda: solve_level(level,newWindow_TestCaseScreen1,5))
    button_testcase5.place(x=137, y=380)

    back_to_menu = tk.Button(newWindow_TestCaseScreen1, font=('Arial', 15), text='Back to menu', width=20, height=1,
                                 bg='Brown', command=lambda: create_first_window(500,500,newWindow_TestCaseScreen1))
    back_to_menu.place(x=137, y=450)

    newWindow_TestCaseScreen1.mainloop()

def solve_level(level,win,testcase):
    win.destroy()
    print(f"Solving level {level}")
    if level == 2:
        searchTree2 = level2.SearchTree()
        if testcase == 1: searchTree2.getInputFile("input//input1-level2.txt")
        if testcase == 2: searchTree2.getInputFile("input//input2-level2.txt")
        if testcase == 3: searchTree2.getInputFile("input//input3-level2.txt")
        if testcase == 4: searchTree2.getInputFile("input//input4-level2.txt")
        if testcase == 5: searchTree2.getInputFile("input//input5-level2.txt")
        searchTree2.AStar()

        if(searchTree2.getCheckRoot() == False):
            print('false')
            testcase_level234(tk.Tk(),level)

    if level == 3:
        searchTree2 = level3.SearchTree()
        if testcase == 1: searchTree2.getInputFile("input//input1-level3.txt")
        if testcase == 2: searchTree2.getInputFile("input//input2-level3.txt")
        if testcase == 3: searchTree2.getInputFile("input//input3-level3.txt")
        if testcase == 4: searchTree2.getInputFile("input//input4-level3.txt")
        if testcase == 5: searchTree2.getInputFile("input//input5-level3.txt")
        searchTree2.Greedy_BFS()

        if (searchTree2.getCheckRoot() == False):
            print('false')
            testcase_level234(tk.Tk(), level)

    if level == 4:
        searchTree2 = level4.SearchTree()
        if testcase == 1: searchTree2.getInputFile("input//input1-level4.txt")
        # if testcase == 2: searchTree2.getInputFile("input//input2-level4.txt")
        if testcase == 3: searchTree2.getInputFile("input//input3-level4.txt")
        if testcase == 4: searchTree2.getInputFile("input//input4-level4.txt")
        # if testcase == 5: searchTree2.getInputFile("input//input5-level4.txt")
        searchTree2.solve()


        testcase_level234(tk.Tk(), level)

    if level == 1:
        myLevel1 = level1.Level1()
        myLevel1.getInputFile("input//input5-level1.txt")
        myLevel1.solve()

def solve_level1(str,testcase):
    if str == 'astar':
        myLevel1 = level1.Level1()
        if testcase == 1: myLevel1.getInputFile("input//input1-level1.txt")
        if testcase == 2: myLevel1.getInputFile("input//input2-level1.txt")
        if testcase == 3: myLevel1.getInputFile("input//input3-level1.txt")
        if testcase == 4: myLevel1.getInputFile("input//input4-level1.txt")
        if testcase == 5: myLevel1.getInputFile("input//input5-level1.txt")
        myLevel1.solve(1)
    if str == 'ucs':
        myLevel1 = level1.Level1()
        if testcase == 1: myLevel1.getInputFile("input//input1-level1.txt")
        if testcase == 2: myLevel1.getInputFile("input//input2-level1.txt")
        if testcase == 3: myLevel1.getInputFile("input//input3-level1.txt")
        if testcase == 4: myLevel1.getInputFile("input//input4-level1.txt")
        if testcase == 5: myLevel1.getInputFile("input//input5-level1.txt")
        myLevel1.solve(3)
    if str == 'bfs':
        myLevel1 = level1.Level1()
        if testcase == 1: myLevel1.getInputFile("input//input1-level1.txt")
        if testcase == 2: myLevel1.getInputFile("input//input2-level1.txt")
        if testcase == 3: myLevel1.getInputFile("input//input3-level1.txt")
        if testcase == 4: myLevel1.getInputFile("input//input4-level1.txt")
        if testcase == 5: myLevel1.getInputFile("input//input5-level1.txt")
        myLevel1.solve(3)


def handle_Button_Level2(win):
    testcase_level234(win,2)


def handle_Button_Level3(win):
    testcase_level234(win,3)

def handle_Button_Level4(win):
    testcase_level234(win,4)

w = tk.Tk() # a little bit error voi cai nay nhma chua can thiet
create_first_window(500,500,w)

