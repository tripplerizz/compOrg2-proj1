# Hector Rizo
# this program is written in python, using python version 3 or higher.
import sys

instr_type = {"add": "R", "nand":"R",
           "lw":"I", "sw": "I",
           "beq":"I","jalr": "J",
           "halt":"O", "noop":"O",
           ".fill": "F"}
opcodes = {"add": 0, "nand":1,
           "lw":2, "sw":3,
           "beq":4,"jalr": 5,
           ".fill":0,"halt":6, 
           "noop":7}
def twoConv(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits) 
    return val  
def checkArgs(items):
    result = []
    for item in items:
        if item not in opcodes.keys() and not item.isnumeric() and item != '':
            if '-'not in item:
                result.append(item)

    return result

def getFills(items):
    result = {} 
    count = 0
    for line in items:
        assemble = line.strip('\n').split('\t')
        if assemble[0]: 
           result[assemble[0]] = count 
        count += 1

    return result

def getArgs(first, second, third):
    num1 = "{args0:b}".format(args0 = int(first)).zfill(3)
    num2 ="{args1:b}".format(args1 = int(second)).zfill(3)
    num3 = "{args2:b}".format(args2 = int(third)).zfill(16)
    return num1, num2, num3

if len(sys.argv) < 3:
    print("huston we got prblm")
    exit

assembler = open(sys.argv[1], 'r')
machine = open(sys.argv[2], 'w')
fill_dict = getFills(assembler)

assembler = open(sys.argv[1], 'r')
label = ""
opcode = ""
arg0 = ""
arg1 = ""
arg2 = ""

lineCount = 0
for line in assembler:
    assemble = line.strip('\n').split('\t')
    opcode = opcodes[assemble[1]]
    strTillOpp = "{opcode:b}".format(opcode = opcode).zfill(10)
    checkItems = checkArgs(assemble[1:5])
    for item in checkItems:
        if instr_type[assemble[1]] != 'F':
            if assemble[1] == 'beq':
                assemble[assemble.index(item)] = (fill_dict[item] - lineCount) - 1    
            else:
                assemble[assemble.index(item)] = fill_dict[item]
        else:
            assemble[assemble.index(item)] = fill_dict[item]

    if  instr_type[assemble[1]] == 'R':
        arg0, arg1, arg2 = getArgs(assemble[2], assemble[3], assemble[4])
    if  instr_type[assemble[1]] == 'J':
        arg0, arg1, arg2 = getArgs(assemble[2], assemble[3], '0')
    if  instr_type[assemble[1]] == 'I':
        arg0, arg1, arg2 = getArgs(assemble[2], assemble[3], '0')
        if not type(assemble[4]) == int: 
            num = (int(assemble[4])) 
        else:
            num = (assemble[4])
        if num < 0:
            num = (int(assemble[4]) ^ 0xFFFF) + 1
            num = twoConv(num, 16) * -1
        arg2 = "{args2:b}".format(args2 =num).zfill(16)
    if instr_type[assemble[1]] == 'O':
        arg0, arg1, arg2 = getArgs('0','0','0')
    if instr_type[assemble[1]] == 'F':
        num = (int(assemble[2]))
        if num < 0:
            num = (int(assemble[2]) ^ 0xFFFF) + 1
            num = twoConv(num, 16) * -1
            arg2 = "{args0:b}".format(args0 =num).zfill(16)
        else:
            arg2 = "{args0:b}".format(args0 =int(assemble[2])).zfill(16)
    if instr_type[assemble[1]] != 'F':
        temp = strTillOpp + arg0 + arg1 + arg2
        machine.writelines(str(int(temp,2)) + '\n')
        print(int(temp,2))
    else:
        machine.writelines(str(assemble[2]) + '\n')
        print(assemble[2])
    lineCount+=1
machine.close()
