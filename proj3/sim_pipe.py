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
noop = 0x1c00000
class IFIDType():
    instr = noop
    pcPlus1 = 0

class IDEXType():
    instr = noop
    pcPlus1 = 0
    readRegA = 0
    readRegB = 0
    offset = 0 
class EXMEMType():
    instr = noop
    branchTarget = 0
    aluResult = 0
    readRegB = 0
class MEMWBType(): 
    instr = noop
    writeData = 0
class WBENDType(): 
    instr = noop
    writeData = 0

class stateStruct():
    pc = 0
    numMemory = 0
    instrMem = [0] * 65536
    dataMem = [0] * 65536
    reg = [0,0,0,0,0,0,0,0]
    IFID = IFIDType()
    IDEX = IDEXType()
    EXMEM = EXMEMType()
    MEMWB = MEMWBType()
    WBEND = WBENDType()
    cycles = 0

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

def alu_calc(opcode, num1, num2):
    if op_type[opcode] == 'add':
        result = num1 + num2
    if op_type[opcode] == 'nand':
        result = nand(num1,num2)
    return result
def load_ifid(newState):
    newState.IFID.instr = newState.instrMem[newState.pc]
    newState.IFID.pcPlus1 = newState.pc + 1

def ifid_instr_ex(newState):
    instr = newState.IFID.instr 
    newState.IDEX.instr = instr
    newState.IDEX.pcPlus1 = newState.pc + 1
    newState.IDEX.instr = instr
    instr = numToBin(instr)
    newState.IDEX.readRegA = binToNum(instr[10:13],0)
    newState.IDEX.readRegB = binToNum(instr[13:16],0)
    newState.IDEX.offset = binToNum(instr[16:32],1)
    return

def idex_instr_ex(newState):
    instr = newState.IDEX.instr 
    newState.EXMEM.instr = instr
    newState.EXMEM.pcPlus1 = newState.pc + 1
    newState.EXMEM.branchTarget = alu_calc("add", newState.EXMEM.pcPlus1,newState.IDEX.offset)  
    opcode = op_type[binToNum( numToBin(newState.IDEX.instr)[0:10])]
    if opcode == 'lw' or opcode == 'sw':  
        newState.EXMEM.aluResult = alu_calc("add",newState.EXMEM.readRegA,newState.EXMEM.offset) 
    else:
        newState.EXMEM.aluResult = alu_calc(opcode, newState.IDEX.readRegA,newState.IDEX.readRegB)
    newState.EXMEM.readRegB = newState.IDEX.readRegB
    return
def exmem_instr_ex(newState):
    instr = newState.EXMEM.instr 
    newState.MEMWB.instr = instr
    newState.MEMWB.pcPlus1 = newState.pc + 1
    opcode = op_type[binToNum( numToBin(newState.MEMWB.instr)[0:10])]
    if opcode == "lw":
        newState.MEMWB.writeData = newState.dataMem[newState.EXMEM.aluResult] 
    if opcode == "sw":
        newState.dataMem[newState.EXMEM.aluResult] = newState.EXMEM.readRegB
    else:
        newState.MEMWB.writeData = newState.EXMEM.aluResult   
    return
def memwb_instr_ex(newState):
    instr = newState.MEMWB.instr 
    newState.WBEND.instr = instr
    newState.WBEND.pcPlus1 = newState.pc + 1
    newState.WBEND.writeData =newState.MEMWB.writeData 
    instr = numToBin(instr)
    opcode = op_type[binToNum(instr[0:10])]
    if opcode == "add"  or opcode == "nand":  
        offset = binToNum(instr[16:32],1)
        newState.reg[offset] = newState.WBEND.writeData
    if opcode == "lw":
        writeRegB = binToNum(instr[13:16],0)
        newState.reg[writeRegB] = newState.WBEND.writeData
    return
def wbend_instr_ex(newState):
    return
def pump_instr(state):
    load_ifid(state)
    ifid_instr_ex(state)
    idex_instr_ex(state)
    exmem_instr_ex(state)
    memwb_instr_ex(state)
    wbend_instr_ex(state)
    return
    
def o_type_instr(opcode, instr, state):
    if op_type[opcode] == 'halt':
        global done
        done = 1
        return
    if op_type[opcode] == 'noop':
        return

def getInstruction(instr):
    instr_str = numToBin(instr)
    opcode_str = op_type[binToNum(instr_str[:10], 0)]
    result = ""
    if instr_type[opcode_str] == 'R':
        arg0 = binToNum(instr_str[10:13],0)
        arg1 = binToNum(instr_str[13:16],0)
        arg2 = binToNum(instr_str[29:32],0)
        result = "{0} {0} {0} {0}".format(opcode_str, arg0, arg1, arg2)
    if instr_type[opcode_str] == 'O':
        result = "{0} {0} {0} {0}".format(opcode_str, 0, 0, 0)
    if instr_type[opcode_str] == 'I':
        arg0 = binToNum(instr_str[10:13],0)
        arg1 = binToNum(instr_str[13:16],0)
        arg2 = binToNum(instr_str[16:32],1)
        result = "{0} {0} {0} {0}".format(opcode_str, arg0, arg1, arg2)
    if instr_type[opcode_str] == 'J':
        arg0 = binToNum(instr_str[10:13],0)
        arg1 = binToNum(instr_str[13:16],0)
        result = "{0} {0} {0} {0}".format(opcode_str, arg0, arg1, 0)
    return result

def printState(state):
    print("\n@@@\nstate before cycle {num} starts\n".format(num =state.cycles))
    print("\tpc {num}\n".format(num = state.pc))

    print("\tdata memory:\n")
    for index,val in enumerate(state.dataMem):
	    print("\t\tdataMem[ {num1} ] {num2}\n".format(num1 = index, num2 = val))

    print("\tregisters:\n")
    for index,val in enumerate(state.reg):
	    print("\t\treg[ {num1} ] {num2}\n".format(num1 = index, num2 = val))
    print("\tIFID:\n")
    print("\t\tinstruction ")
    print(getInstruction(state.IFID.instr))
    print("\t\tpcPlus1 {num}\n".format(num = state.IFID.pcPlus1))
    print("\tIDEX:\n")
    print("\t\tinstruction ")
    print(getInstruction(state.IDEX.instr))
    print("\t\tpcPlus1 {num}\n".format(num = state.IDEX.pcPlus1))
    print("\t\treadRegA {num}\n".format(num = state.IDEX.readRegA))
    print("\t\treadRegB {num}\n".format(num = state.IDEX.readRegB))
    print("\t\toffset {num}\n".format(num = state.IDEX.offset))
    print("\tEXMEM:\n")
    print("\t\tinstruction ")
    print(getInstruction(state.EXMEM.instr))
    print("\t\tbranchTarget {num}\n".format(num = state.EXMEM.branchTarget))
    print("\t\taluResult {num}\n".format(num = state.EXMEM.aluResult))
    print("\t\treadRegB {num}\n".format(num = state.EXMEM.readRegB))
    print("\tMEMWB:\n")
    print("\t\tinstruction ")
    print(getInstruction( state.MEMWB.instr))
    print("\t\twriteData {num}\n".format(num = state.MEMWB.writeData))
    print("\tWBEND:\n")
    print("\t\tinstruction ")
    print(getInstruction(state.WBEND.instr))
    print("\t\twriteData {num}\n".format(num = state.WBEND.writeData))


#------------------------------------------------------------------------
# start of the program
if len(sys.argv) < 2:
    print("huston we got prblm")
    exit

state = stateStruct()
newState = stateStruct()
with open(sys.argv[1], 'r') as assembly:
    for line in assembly:
        state.instrMem[state.numMemory] = (int(line))
        state.dataMem[state.numMemory] = (int(line))
        print("mem[{num}]={num2}".format(num = state.numMemory, num2 = state.dataMem[state.numMemory]))
        state.numMemory +=1
print("\tinstruction memory:")
for index, val in enumerate(state.instrMem):
    print("\t\tinstrMem[ {num} ]= {num2}".format(num = index, num2 = getInstruction(val)))

count = 0
while(True):
    if done:
        print("machine halted")
        print("total of {num} instructions executed".format(num = count))
        print("final state of machine:\n")
    printState(state)
    if done:
        break
    newState = state
    newState.cycles+=1
    pump_instr(newState)
    newState.pc +=1
    count += 1
    state = newState
