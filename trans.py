
import sys

instr_type = {"add": "R", "nand":"R"
           "lw":"I", "sw": "I",
           "beq":"J","jalr": "J",
           "halt":"O", "noop":"O"}
opcodes = {"add": "R", "nand":"R"
           "lw":"I", "sw": "I",
           "beq":"J","jalr": "J",
           "halt":"O", "noop":"O"}

if len(sys.argv) < 3:
    print("huston we got prblm")
    exit

assembler = open(sys.argv[1], 'r')
machine = open(sys.argv[2], 'w')

label = ""
opcode = ""
arg0 = ""
arg1 = ""
arg2 = ""

for line in assembler:
    assemble = line.strip('\n').split('\t')