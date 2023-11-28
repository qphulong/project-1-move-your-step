from level1 import Level1
from level4 import Level4

# #Duoi nay la test code
# m = Level1()
# m.getInputFile("input//input1-level1.txt")

m = Level1()
m.getInputFile("input//input4_level1.txt")

while True:
    if m.solve() == False:
        break
