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
done = 0
class stateStruct():
    pc = 0
    numMemory = 0
    mem = [0] * 65536
    reg = [0,0,0,0,0,0,0,0]

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
def nand(one,two):
    result = one & two
    result = ~result 
    return result
def r_type_instr(opcode,instr,state):
    arg0 = binToNum(instr[10:13],0)
    arg1 = binToNum(instr[13:16],0)
    arg2 = binToNum(instr[29:32],0)
    if op_type[opcode] == 'add':
        state.reg[arg2] = state.reg[arg0] + state.reg[arg1]
    if op_type[opcode] == 'nand':
        state.reg[arg2] = nand(state.reg[arg0],state.reg[arg1])
def i_type_instr(opcode, instr, state):
    arg0 = binToNum(instr[10:13],0)
    arg1 = binToNum(instr[13:16],0)
    arg2 = binToNum(instr[16:32],1)
    if op_type[opcode] == 'lw':  
        state.reg[arg1] = state.mem[state.reg[arg0] + arg2 ]  
        return
    if op_type[opcode] == 'beq':
        if (state.reg[arg0] - state.reg[arg1]) == 0:
            state.pc += arg2
            return
    if op_type[opcode] == 'sw':
        state.mem[state.reg[arg0] + arg2] = state.reg[arg1]  
def o_type_instr(opcode, instr, state):
    if op_type[opcode] == 'halt':
        global done
        done = 1
        return
    if op_type[opcode] == 'noop':
        return
def j_type_instr(opcode, instr, state):
    arg0 = binToNum(instr[10:13],0)
    arg1 = binToNum(instr[13:16],0)
    state.reg[arg1] = state.pc +1
    state.pc = state.reg[arg0] -1


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
    print("\tmem:")
    for count, val in enumerate(state.mem[:state.numMemory]):
        print("\t\tmem[ {index} ] {num}".format(index = count, num = val))
    print("\tregs:")
    for count, val in enumerate(state.reg):
        print("\t\treg[ {index} ] {num}".format(index = count, num = val))
    print("end state\n")
#------------------------------------------------------------------------
# start of the program
if len(sys.argv) < 2:
    print("huston we got prblm")
    exit

state = stateStruct()
with open(sys.argv[1], 'r') as assembly:
    for line in assembly:
        state.mem[state.numMemory] = (int(line))
        print("mem[{num}]={num2}".format(num = state.numMemory, num2 = state.mem[state.numMemory]))
        state.numMemory +=1
print("\n")

count = 0
while(True):
    if done:
        print("machine halted")
        print("total of {num} instructions executed".format(num = count))
        print("final state of machine:\n")
        
    printState(state)
    if done:
        break
    instr = numToBin(state.mem[state.pc])
    readInstr(instr, state)
    state.pc +=1
    count += 1
