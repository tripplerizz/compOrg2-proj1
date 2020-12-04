# Hector Rizo
# this program is written in python, using python version 3 or higher.
#developed on windows using python3 ... it can run on linprog
# pipelining works. and data hazards with addition works. other hazards are missing
import sys
import copy

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
hist = {}
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
    if opcode == 'add':
        result = num1 + num2
    elif opcode == 'nand':
        result = nand(num1,num2)
    else:
        result = 0
    return result
def load_ifid(state,newState):
    newState.IFID.instr = state.instrMem[state.pc]
    newState.IFID.pcPlus1 = state.pc + 1
    return

def ifid_instr_ex(state,newState):
    global hist
    instr = state.IFID.instr 
    newState.IDEX.instr = instr
    newState.IDEX.pcPlus1 = state.IFID.pcPlus1 
    instr = numToBin(instr)
    opcode = op_type[binToNum(instr[0:10], 0)]
    num1 =  binToNum(instr[10:13],0)
    num2 =  binToNum(instr[13:16],0)
    num3 = binToNum(instr[16:32],1)
    # hazard control
    if num1 not in hist:
        newState.IDEX.readRegA = state.reg[num1]
    else:
        newState.IDEX.readRegA = None
    if num2 not in hist:
        newState.IDEX.readRegB = state.reg[num2]
    else:
        newState.IDEX.readRegB = None
    newState.IDEX.offset = num3
    if opcode == "add" or opcode == "nand":
        hist[num3] = state.cycles
    if opcode == "lw" :
        hist[num2] = state.cycles
    return

def which_hazard(state,hist, num):
    result = 0
    dif = state.cycles - hist[num] - 1
    if dif == 1:
        result = state.EXMEM.aluResult 
    if dif == 2:
        result = state.MEMWB.writeData 
    if dif == 0:
        result = state.reg[num]
    return result

def idex_instr_ex(state,newState):
    global hist
    global noop
    instr = state.IDEX.instr 
    newState.EXMEM.instr = instr
    opcode = op_type[binToNum( numToBin(state.IDEX.instr)[0:10],0)]
    #dealing w hazard
    tempInstr = numToBin(instr)
    reg_str_1 =  binToNum(tempInstr[10:13],0)
    reg_str_2 =  binToNum(tempInstr[13:16],0)
    reg_str_3 = binToNum(tempInstr[16:32],1)
    num1 =state.IDEX.readRegA  
    num2 = state.IDEX.readRegB 
    num3 = state.IDEX.offset
    
    if state.IDEX.readRegA == None:
       num1 = which_hazard(state, hist, reg_str_1)
    if state.IDEX.readRegB == None:
       opcode = op_type[binToNum( numToBin(state.EXMEM.instr)[0:10],0)]
       if opcode == 'lw':
           newState.IDEX.instr = noop
       num2 = which_hazard(state, hist, reg_str_2)
    if state.IDEX.offset == None:
       num3 = which_hazard(state, hist, reg_str_3)
    # regular execution
    newState.EXMEM.branchTarget = alu_calc("add", state.IDEX.pcPlus1,num3)  
    if opcode == 'lw' or opcode == 'sw':  
        newState.EXMEM.aluResult = alu_calc("add",num1,num3) 
    else:
        newState.EXMEM.aluResult = alu_calc(opcode, num1,num2)
    newState.EXMEM.readRegB = num2
    #taking branch sometimes
    if opcode == 'beq':
        if num1 - num2 == 0:
            newState.pc = newState.EXMEM.branchTarget
    return
def exmem_instr_ex(state,newState):
    instr = state.EXMEM.instr 
    newState.MEMWB.instr = instr
    opcode = op_type[binToNum( numToBin(state.EXMEM.instr)[0:10], 0)]
    if opcode == "lw":
        newState.MEMWB.writeData = state.dataMem[state.EXMEM.aluResult] 
    elif opcode == "sw":
        newState.dataMem[state.EXMEM.aluResult] = state.EXMEM.readRegB
    elif opcode == "halt":
        return
    else:
        newState.MEMWB.writeData = state.EXMEM.aluResult   
    return
def memwb_instr_ex(state,newState):
    global hist
    instr = state.MEMWB.instr 
    newState.WBEND.instr = instr
    newState.WBEND.writeData =state.MEMWB.writeData 
    instr = numToBin(instr)
    opcode = op_type[binToNum(instr[0:10],0)]
    if opcode == "add"  or opcode == "nand":  
        offset = binToNum(instr[16:32],1)
        hist.pop(offset)
        newState.reg[offset] = state.MEMWB.writeData
    if opcode == "lw":
        writeRegB = binToNum(instr[13:16],0)
        hist.pop(writeRegB)
        newState.reg[writeRegB] = state.MEMWB.writeData
    return
def wbend_instr_ex(state,newState):
    return
def pump_instr(state, newState):
    load_ifid(state,newState)
    ifid_instr_ex(state,newState)
    idex_instr_ex(state,newState)
    exmem_instr_ex(state,newState)
    memwb_instr_ex(state,newState)
    wbend_instr_ex(state,newState)
    return

def getInstruction(instr):
    instr_str = numToBin(instr)
    opcode_num = binToNum(instr_str[:10], 0)
    opcode_str = op_type[opcode_num]
    result = ""
    if instr_type[opcode_num] == 'R':
        arg0 = binToNum(instr_str[10:13],0)
        arg1 = binToNum(instr_str[13:16],0)
        arg2 = binToNum(instr_str[16:32],0)
        result = "{0} {1} {2} {3}".format(opcode_str, arg0, arg1, arg2)
    if instr_type[opcode_num] == 'O':
        result = "{0} {1} {2} {3}".format(opcode_str, 0, 0, 0)
    if instr_type[opcode_num] == 'I':
        arg0 = binToNum(instr_str[10:13],0)
        arg1 = binToNum(instr_str[13:16],0)
        arg2 = binToNum(instr_str[16:32],1)
        result = "{0} {1} {2} {3}".format(opcode_str, arg0, arg1, arg2)
    if instr_type[opcode_num] == 'J':
        arg0 = binToNum(instr_str[10:13],0)
        arg1 = binToNum(instr_str[13:16],0)
        result = "{0} {1} {2} {3}".format(opcode_str, arg0, arg1, 0)
    return result

def printState(state):
    print("\n@@@\nstate before cycle {num} starts".format(num =state.cycles))
    print("\tpc {num}".format(num = state.pc))

    print("\tdata memory:")
    for index,val in enumerate(state.dataMem):
        if index == state.numMemory:
            break
        print("\t\tdataMem[ {num1} ] {num2}".format(num1 = index, num2 = val))

    print("\tregisters:")
    for index,val in enumerate(state.reg):
        print("\t\treg[ {num1} ] {num2}".format(num1 = index, num2 = val))
    print("\tIFID:")
    print("\t\tinstruction",getInstruction(state.IFID.instr))
    print("\t\tpcPlus1 {num}".format(num = state.IFID.pcPlus1))
    print("\tIDEX:")
    print("\t\tinstruction",getInstruction(state.IDEX.instr))
    print("\t\tpcPlus1 {num}".format(num = state.IDEX.pcPlus1))
    print("\t\treadRegA {num}".format(num = state.IDEX.readRegA))
    print("\t\treadRegB {num}".format(num = state.IDEX.readRegB))
    print("\t\toffset {num}".format(num = state.IDEX.offset))
    print("\tEXMEM:")
    print("\t\tinstruction",getInstruction(state.EXMEM.instr))
    print("\t\tbranchTarget {num}".format(num = state.EXMEM.branchTarget))
    print("\t\taluResult {num}".format(num = state.EXMEM.aluResult))
    print("\t\treadRegB {num}".format(num = state.EXMEM.readRegB))
    print("\tMEMWB:")
    print("\t\tinstruction",getInstruction( state.MEMWB.instr))
    print("\t\twriteData {num}".format(num = state.MEMWB.writeData))
    print("\tWBEND:")
    print("\t\tinstruction",getInstruction(state.WBEND.instr))
    print("\t\twriteData {num}".format(num = state.WBEND.writeData))

def megaCOPY(new, old):
    new.pc = copy.deepcopy(old.pc)
    new.numMemory = copy.deepcopy(old.numMemory)
    new.instrMem = copy.deepcopy(old.instrMem)
    new.dataMem = copy.deepcopy(old.dataMem)
    new.reg = copy.deepcopy(old.reg)
    new.IFID = copy.deepcopy(old.IFID)
    new.IDEX = copy.deepcopy(old.IDEX)
    new.EXMEM = copy.deepcopy(old.EXMEM)
    new.MEMWB = copy.deepcopy(old.MEMWB)
    new.WBEND = copy.deepcopy(old.WBEND)
    new.cycles = copy.deepcopy(old.cycles)
#------------------------------------------------------------------------
# start of the program
if len(sys.argv) < 2:
    print("huston we got prblm")
    exit

state = stateStruct()
with open(sys.argv[1], 'r') as assembly:
    for line in assembly:
        state.instrMem[state.numMemory] = (int(line))
        state.dataMem[state.numMemory] = (int(line))
        print("memory[{num}]={num2}".format(num = state.numMemory, num2 = state.dataMem[state.numMemory]))
        state.numMemory +=1
print("{num} memory words".format(num = state.numMemory))
print("\tinstruction memory:")
for index, val in enumerate(state.instrMem):
    if index == state.numMemory:
        break
    print("\t\tinstrMem[ {num} ] {num2}".format(num = index, num2 = getInstruction(val)))

count = 0
while(True):
    printState(state)
    newState = copy.deepcopy(state)
    megaCOPY(newState, state)
    newState.cycles+=1
    opcode = numToBin(state.MEMWB.instr)
    opcode_str = op_type[binToNum(opcode[:10], 0)]
    if opcode_str == "halt":
	    print("machine halted")
	    print("total of {num} cycles executed\n".format(num = state.cycles))
	    exit(0)
    pump_instr(state,newState)
    newState.pc +=1
    count += 1
    state = copy.deepcopy(newState)

