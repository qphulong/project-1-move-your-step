from level1 import Level1

#Duoi nay la test code
m = Level1()
m.getInputFile("input//input1-level1.txt")

while True:
    m.printSelf()  # Print the table each loop
    user_input = input("Enter 1 to move SW, 2 to move S, 3 to move SE, 4 to move W, 6 to move E, 7 to move NW, 8 to move N, 9 to move NE, or 'q' to quit: ")

    if user_input == 'q':
        break  # Exit the loop if the user enters 'q'
    elif user_input in {'1', '2', '3', '4', '6', '7', '8', '9'}:
        # Move the agent based on user input
        if user_input == '1':
            m.moveSW()
        elif user_input == '2':
            m.moveS()
        elif user_input == '3':
            m.moveSE()
        elif user_input == '4':
            m.moveW()
        elif user_input == '6':
            m.moveE()
        elif user_input == '7':
            m.moveNW()
        elif user_input == '8':
            m.moveN()
        elif user_input == '9':
            m.moveNE()
    else:
        print("Invalid input. Please enter 1, 2, 3, 4, 6, 7, 8, 9, or 'q'.")
