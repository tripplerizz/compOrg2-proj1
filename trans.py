
import sys

instr_type = {"add": "R", "nand":"R",
           "lw":"I", "sw": "I",
           "beq":"J","jalr": "J",
           "halt":"O", "noop":"O"}
opcodes = {"add": 0, "nand":1,
           "lw":2, "sw":3,
           "beq":4,"jalr": 5,
           "halt":6, "noop":7}
def checkArgs(items):
    result = []
    for item in items:
        if item not in opcodes.keys() and not item.isnumeric():
            result.append(item)

    return result

def getFills(items):
    result = {} 
    count = 0
    for line in items:
        assemble = line.strip('\n').split('\t')
        if assemble[1] == '.fill':
           result[assemble[0]] = count 
        count += 1

    return result

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

for line in assembler:
    assemble = line.strip('\n').split('\t')
    opcode = opcodes[assemble[1]]
    strTillOpp = "{opcode:b}".format(opcode = opcode).zfill(10)
    checkItems = checkArgs(assemble[1:5])
    for item in checkItems:
        assemble[assemble.index(item)] = fill_dict[item]
    if instr_type[assemble[1]] == 'I':
        arg0 = "{args0:b}".format(args0 = int(assemble[2])).zfill(3)
        arg1 ="{args1:b}".format(args1 = int(assemble[3])).zfill(3)
        arg2 = "{args2:b}".format(args2 = int(assemble[4])).zfill(16)
    if instr_type[assemble[1]] == 'J':
        arg0 = "{args0:b}".format(args0 = int(assemble[2])).zfill(3)
        arg1 ="{args1:b}".format(args1 = int(assemble[3])).zfill(3)
        arg2 = "{args2:b}".format(args2 = int(assemble[4])).zfill(16)

    temp = strTillOpp + arg0 + arg1 + arg2
    print(temp)