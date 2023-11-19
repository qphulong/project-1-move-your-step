from level1 import Level1

#Duoi nay la test code
m = Level1()
m.getInputFile("input//input1-level1.txt")

while True:
    if m.solve() == False:
        break
