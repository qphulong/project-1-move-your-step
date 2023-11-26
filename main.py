from level1 import Level1
from level4 import Level4

# #Duoi nay la test code
# m = Level1()
# m.getInputFile("input//input1-level1.txt")

m = Level4()
m.getInputFile("input//input1-level4.txt")

while True:
    if m.solve() == False:
        break
