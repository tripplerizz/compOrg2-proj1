# Hector Rizo
# this program is written in python, using python version 3 or higher.
import sys

instr_type = {0: "R", 1:"R",
           2:"I", 3: "I",
           4:"I",5: "J",
           6:"O", 7:"O"}
op_type = {0:"add", 1:"nand",
           2:"lw", 3:"sw",
           4:"beq",5:"jalr",
           6:"halt", 7:"noop"}

class pc_state():
    pc = 0
    memNum = 0
    memory = [0] * 65536
    register = [0,0,0,0,0,0,0,0]
    done = 0

def twoConv(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits) 
    return val 

def numToBin(number):
    return '{0:032b}'.format(number)
def binToNum(number, neg):
    num = int(number, 2)
    if neg:
        if number[0] ==  '1':
            num = twoConv(num,len(number))
    return num
def r_type_instr(opcode,instr,state):
    arg0 = binToNum(instr[10:13],0)
    arg1 = binToNum(instr[13:16],0)
    arg2 = binToNum(instr[29:32],0)
    if op_type[opcode] == 'add':
        state.register[arg2] = state.register[arg0] + state.register[arg1]
    if op_type[opcode] == 'nand':
        state.register[arg2] = state.register[arg0] & state.register[arg1]
def i_type_instr(opcode, instr, state):
    arg0 = binToNum(instr[10:13],0)
    arg1 = binToNum(instr[13:16],0)
    arg2 = binToNum(instr[16:32],1)
    if op_type[opcode] == 'lw':  
        state.register[arg1] = state.memory[state.register[arg0] + arg2 ]  
    if op_type[opcode] == 'sw':
        state.memory[state.register[arg0] +arg2 + 1] = state.register[arg1]  
    if op_type[opcode] == 'beq':
        if (state.register[arg0] - state.register[arg1]) == 0:
            state.pc += arg2
def o_type_instr(opcode, instr, state):
    if op_type[opcode] == 'halt':
        state.done = 1
        return
    if op_type[opcode] == 'noop':
        return
def j_type_instr(opcode, instr, state):
    arg0 = binToNum(instr[10:13],0)
    arg1 = binToNum(instr[13:16],0)
    state.register[arg1] = state.pc +1
    state.pc = state.register[arg0]


def readInstr(instr, state):
    opcode = binToNum(instr[0:10],0)
    if instr_type[opcode] == 'R':
        r_type_instr(opcode, instr,state)
        return
    if instr_type[opcode] == 'O':
        o_type_instr(opcode, instr, state)
        return
    if instr_type[opcode] == 'I':
        i_type_instr(opcode, instr, state)
        return
    if instr_type[opcode] == 'J':
        j_type_instr(opcode, instr, state)
        return

    return 0
def printState(state):
    print("@@@")
    print("state:")
    print("\tpc {num}".format(num = state.pc))
    print("\tmemory:")
    for count, val in enumerate(state.memory[:state.memNum]):
        print("\t\tmem[ {index} ] {num}".format(index = count, num = val))
    print("\tregisters:")
    for count, val in enumerate(state.register):
        print("\t\treg[ {index} ] {num}".format(index = count, num = val))
    print("end state")
#------------------------------------------------------------------------
# start of the program
if len(sys.argv) < 3:
    print("huston we got prblm")
    exit

state = pc_state()
with open(sys.argv[1], 'r') as assembly:
    for line in assembly:
        state.memory[state.memNum] = (int(line))
        state.memNum +=1

with open(sys.argv[1], 'r') as assembly:
    while(True):
        printState(state)
        if state.done :
            break
        instr = numToBin(state.memory[state.pc])
        readInstr(instr, state)
        state.pc +=1