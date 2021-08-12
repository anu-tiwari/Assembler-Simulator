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

AnswerList = []       # to store final binary encoding of instructions
Memory = {}         # to store instruction addresses and variable addresses (could be 0:'mov 1 $10')
VariableList = []   # to store the variables in a queue while parsing the start of the assembly code
LabelsDict = {}     # to store the labels and their instruction addresses while parsing the first time (could be label_name: instruction number)
# functions could return an error message if there is an error and return nothing and add in the answer list if there is none

# Type A
def TypeA(array):
    encoding = ""

    if len(array)!=4:
        return "Error: Incorrect syntax used for instructions"  #error in syntax

    if (array[1] not in Registers) or (array[2] not in Registers) or (array[3] not in Registers):
        return "Error: Invalid register name"    #invalid register name

    if (array[1] == 'FLAGS') or (array[2] == 'FLAGS') or (array[3] == 'FLAGS'):
        return "Error: Illegal use of flags register"    #illegal use of flags register
       
    encoding += Instruction[array[0]]['opcode']  
    encoding += '00'    #for unused bits
    encoding += Registers[array[1]]                  
    encoding += Registers[array[2]]
    encoding += Registers[array[3]]
    AnswerList.append(encoding)
    return "encoded"


#Type B
def TypeB(array):
    encoding = ""

    if len(array) != 3 or array[2][0] != "$" or array[2] in Registers:
        return "Error: Incorrect syntax used for instructions"    #error in syntax
    
    if array[1] not in Registers:
        return "Error: Invalid register name"    #invalid register name

    if array[1] == "FLAGS":
        return "Error: Illegal use of flags register"    #illegal use of flags register

    if array[0] != "mov":
        encoding += Instruction[array[0]]['opcode']  
        encoding += Registers[array[1]]  
        encoding += ToBinary(array[2])
        AnswerList.append(encoding)
        return "encoded"

    else:
        encoding += Instruction["movimm"]['opcode']  
        encoding += Registers[array[1]]  
        encoding += ToBinary(array[2])
        AnswerList.append(encoding)
        return "encoded"


# Type C
def TypeC(array):
    encoding = ""

    if len(array) != 3:
        return "Error: Incorrect syntax used for instructions"    #error in syntax
    
    if (array[1] not in Registers) or (array[2] not in Registers):
        return "Error: Invalid register name"    #invalid register name

    if (array[1] == "FLAGS") or (array[2] == "FLAGS"):
        return 'Error: Illegal use of flags register'    #illegal use of flags register

    if array[0] != "mov":
        encoding += Instruction[array[0]]['opcode']
        encoding += "00000"    #for unused bits
        encoding += Registers[array[1]]  
        encoding += Registers[array[2]] 
        AnswerList.append(encoding)
        return "encoded"
    else:
        encoding += Instruction["movreg"]['opcode']
        encoding += "00000"    #for unused bits
        encoding += Registers[array[1]]  
        encoding += Registers[array[2]] 
        AnswerList.append(encoding)
        return "encoded"


# Type D
def TypeD(array):
    encoding = ""

    if len(array) != 3:
        return "Error: Incorrect syntax used for instructions"    #error in syntax
        
    if array[1] not in Registers:
        return "Error: Invalid register name"    #invalid register name

    if array[1] == "FLAGS":
        return "Error: Illegal use of flags register"    #illegal use of flags register

    if array[2] not in VariableList:    #error in variable name
        if array[2] in Registers:
            return "Error: Register used as Variable"
        elif array[2] in LabelsDict:
            return "Error: Label used as Variable"
        elif array[2].isnumeric():
            return "Error: Immediate Value used as Variable"
        else:
            return "Error: Use of Undefined Variable"

    encoding += Instruction[array[0]]["opcode"]
    encoding += Registers[array[1]]
    encoding += ToBinary(Memory[array[2]])
    AnswerList.append(encoding)
    return "encoded"


# Type E
def TypeE(array):
    encoding = ""

    if len(array) !=2:
        return "Error: Incorrect Syntax used for Instruction"    #error in syntax

    if array[1] not in LabelsDict:
        if array[1] in VariableList:
            return "Error: Variable used as Label"
        elif array[1].isnumeric():
            return "Error: Immediate Value Used as Label"
        elif array[1] in Registers:
            return "Error: Register Used as Label"
        else:
            return "Error: Use of Undefined Label"

    encoding += Instruction[array[0]]["opcode"]
    encoding += "000"
    encoding += ToBinary(LabelsDict(array[1]))
    AnswerList.append(encoding)
    return "encoded"


# Type F
def TypeF(array):
    encoding = ""

    if array[0] == 'hlt':
        encoding += Instruction[array[0]]['opcode']
        encoding += "0" * 11
        AnswerList.append(encoding)
        return "encoded"


#consider this the main function

# variablesstart = 0      # could be used for determining from which point variables start in the memory (altho can also use address of halt instruction for this)
error = ""              # for storing error message
PC = 0                  # program counter to see which instruction number we're at
VC = 0
# this loop could be used for just parsing variables and another for other instructions

halt = 0
# while True:

# while True:
#     if (array)
#             if (len(array)!=2):
#                 print('Error: Invalid Variable Declaration')
#                 break
#             else:
#                 VariableList[array[1]]

# create a list with all lines, and append the front set of variables to the end
# create a list with all lines, and append the front set of variables at their respective positions in the memory array at the beginning
#  ist ist ist ist ist var var var var 
while True:
    try:
        SingleLine = input()
        array = SingleLine.split()

        if SingleLine == "":
            continue
        
        if (array[0]=='var'):
            PC+=1
            VC+=1
            if (PC==VC):
                VariableList.append(array[1])
            else:
                print('Error: Variable not declared at the beginning')
                break
            
        badLabel = 0

        if array[0][-1] ==":":
            for ele in array[0][:-1]:
                if ele.isalnum()==False and ele!='_':
                    print('Error: Invalid label name')
                    badLabel = 1
                    break
            if badLabel!=1:
                LabelsDict[array[0]] = PC
                array.remove(array[0])

        # if array[0]=='var':
        #     print('Error: Variable declared not at ')
        if halt == 1:
            print("Error: Halt appeared more than once / in the middle")
            break

        #Type A
        if array[0] == 'add' or array[0] == 'sub' or array[0] == 'mul' or array[0] == 'xor' or array[0] == 'or' or array[0] == 'and':
            RetString = TypeA(array)
            if RetString != "encoded":
                print(RetString)
                break
            else:
                PC+=1
        
        
        #Type B
        elif array[0] == "mov" or array[0] == "rs" or array[0] == "ls":
            RetString = TypeB(array)
            if RetString != "encoded":
                print(RetString)
                break
            else:
                PC+=1
            
        #Type C    
        elif array[0] == "mov" or array[0] == "div" or array[0] == "not" or array[0] == "cmp":
            RetString = TypeC(array)
            if RetString != "encoded":
                print(RetString)
                break
            else:
                PC+=1

        #Type D
        elif array[0] == "ld" or array[0] == "st":
            RetString = TypeD(array)
            if RetString != "encoded":
                print(RetString)
                break
            else:
                PC+=1

        #Type E
        elif array[0] == "jmp" or array[0] == "jlt" or array[0] == "jgt" or array[0] == "je":
            RetString = TypeE(array)
            if RetString != "encoded":
                print(RetString)
                break
            else:
                PC+=1
                
        #Type F
        elif array[0] == 'hlt':
            halt = 1
            RetString = TypeF(array)
            if RetString != "encoded":
                print(RetString)
                break
            else:
                PC+=1

        else:
            print('Error: Invalid Instruction Type')

    except EOFError:
        break