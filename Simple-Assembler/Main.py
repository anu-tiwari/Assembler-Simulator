#import
from Registers import *
from InstructionDict import *
from helper import *
# Type A - arithmetic operations - add, sub, mul, xor, or, and
# Type B - mov, rs, ls
# Type C -  mov, div, not
# Type D - ld, str
# Type E - jmp, jlt, jgt, je
# Type F - hlt

Answerlist=[]       # to store final binary encoding of instructions
Memory = {}         # to store instruction addresses and variable addresses (could be 0:'mov 1 $10)
Variabledict = {}   # to store the variables in a queue while parsing the start of the assembly code
Labelsdict = {}     # to store the labels and their instruction addresses while parsing the first time
# functions could return an error message if there is an error and return nothing and add in the answer list if there is none

# Type A
def TypeA(line):
    array = line.split()
    encoding = ""

    if len(array) == 4:
        if (array[1] not in Registers) or (array[2] not in Registers) or (array[3] not in Registers):      
            return 'Error: Invalid Register Name'                       #error in reg name
        if (array[1]=='FLAGS') or (array[2]=='FLAGS') or (array[3]=='FLAGS'):
            return 'Error: Illegal use of flags register'               #to check for illegal use of FLAGS reg
    if len(array) == 3:
        if (array[1] not in Registers) or (array[2] not in Registers):
            return 'Error: Invalid Register Name'
        if (array[1]=='FLAGS') or (array[2]=='FLAGS'):
            return 'Error: Illegal use of flags register'    
    pass

# Type B
def TypeB(line):
    pass

# Type C
def TypeC(line):
    pass

# Type D
def TypeD(line):
    array = line.split()
    encoding = ""
    if array[1] not in Registers:                   # error in register name
        return 'Error: Invalid Register Name'
    # have to check if flags can be used this way or not
    if array[1]=='FLAGS':
        return 'Error: Illegal use of flags register'
    if array[2] not in Variabledict:                # error in variable name
        if array[2] in Registers:
            return 'Error: Register used as Variable'
        elif array[2] in Labelsdict:
            return 'Error: Label used as Variable'
        elif array[2].isnumeric():
            return 'Error: Immediate Value used as Variable'
        else:
            return 'Error: Undeclared Variable Used'
    if array[0] == 'ld' or array[0] == 'st':            # if no errors
        encoding += Instruction[array[0]]['opcode']
        encoding += Registers[array[1]]
        encoding += tobinary(Memory[array[2]])
        Answerlist.append(encoding)

# Type E
def TypeE(line):
    pass

# Type F
def TypeF(line):
    pass

#consider this the main function

variablesstart = 0      # could be used for determining from which point variables start in the memory (altho can also use address of halt instruction for this)
error = ""              # for storing error message
PC = 0                  # program counter to see which instruction number we're at
# this loop could be used for just parsing variables and another for other instructions

while True:
    try:
        SingleLine = input()
        #start here
# we'll prolly need to parse the entire code once and store it in a list and then process the list because we need the number of the last instruction to store the variables after it
    except EOFError:
        break