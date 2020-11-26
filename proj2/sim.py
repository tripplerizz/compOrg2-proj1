import sys

class pc_state():
    pc = 0
    memNum = 0
    memory = [0,0,0,0,0,0,0,0,0,0]
    register = [0,0,0,0,0,0,0,0,0,0]

def numToBin(number):
    return '{0:032b}'.format(number)
def binToNum(number, neg):
    if neg:
        if num < 0:
            num = (int(assemble[4]) ^ 0xFFFF) + 1
            num = twos_comp(num, 16) * -1
            arg2 = "{args0:b}".format(args0 =num).zfill(16)
        else:
            arg2 = "{args2:b}".format(args2 = int(assemble[4])).zfill(16)

    return int(number, 2)
def printState(state):
    print("@@@")
    print("state:")
    print("\tpc {num}".format(num = state.pc))
    print("\tmemory:")
    for count, val in enumerate(state.memory):
        print("\t\tmem[ {index} ] {num}".format(index = count, num = val))
    print("\tregisters:")
    for count, val in enumerate(state.register):
        print("\t\treg[ {index} ] {num}".format(index = count, num = val))
    print("end state")

if len(sys.argv) < 3:
    print("huston we got prblm")
    exit

assembly = open(sys.argv[1], 'r')
for line in assembly:
    print(numToBin(int(line)))
state = pc_state()
printState(state)