#remove variable



#imports
import sys
from BinDec import * 
import matplotlib.pyplot as plt

#global variables

#dictionary stores the 16-bit values for each of the 8 registers (R0-R6, FLAGS)
Registers = {'000': '0'*16, '001': '0'*16, '010': '0'*16, '011': '0'*16, '100': '0'*16, '101': '0'*16, '110': '0'*16, '111': '0'*16}

PC = 0 #program counter
Cycle = 0 #cycle number
Halted = False
Memory = ['0'*16]*256 #Memory holds the instructions and variables, and returns the 16bit value stored at the address
#Memory address is given in decimal

CycleListInst = [] #x coordinates for the instructions' plot, holds the Cycle number
CycleListldst = [] #x coordinates for the load/store instructions, holds the Cycle number
CycleListLabel = [] #x coordinates for the jump instructions, holds the Cycle number
MemoryListInst = [] #y coordinates for the instructions' plot, holds the memory address in decimal
MemoryListldst = [] #y coordinates for the load/store, holds the memory address in decimal
MemoryListLabel = [] #y coordinates for the jump instructions, holds the memory address in decimal


#read from stdin
allLines = sys.stdin.read()
separateLines = allLines.split('\n')

#storing every line of the binary code into the memory
for i in range(len(separateLines)):
    Memory[i] = separateLines[i]

#Type A
def TypeA(inst):
    #inst[0:5] = opcode ; inst[5:7] = unused bits ; inst[7:10] = reg1 ; inst[10:13] = reg2 ; inst[13:] = reg3
    global PC
    if inst[:5] =='00000': #add
        SUM = ToDecimal(Registers[inst[10:13]]) + ToDecimal(Registers[inst[13:]])
        if ToBinary(SUM) == 'overflow error':
            Registers['111'] = ('0'*12) + '1' + ('0'*3) #setting overflow flag
        else:
            Registers[inst[7:10]] = ToBinary(SUM)
        PC += 1

    elif inst[:5]== '00001': #subtract
        DIFF = ToDecimal(Registers[inst[10:13]]) - ToDecimal(Registers[inst[13:]])
        if ToBinary(DIFF) == 'overflow error':
            Registers['111'] = ('0'*12) + '1' + ('0'*3) #setting overflow flag
        else:
            Registers[inst[7:10]] = ToBinary(DIFF)
        PC += 1

    elif inst[:5] == '00110': #multiply
        PROD = ToDecimal(Registers[inst[10:13]]) * ToDecimal(Registers[inst[13:]])
        if ToBinary(PROD) == 'overflow error':
            Registers['111'] = ('0'*12) + '1' + ('0'*3) #setting overflow flag
        else:
            Registers[inst[7:10]] = ToBinary(PROD)
        PC += 1

    elif inst[:5] == '01010': #xor
        XOR = ToDecimal(Registers[inst[10:13]]) ^ ToDecimal(Registers[inst[13:]])
        Registers[inst[7:10]] = ToBinary(XOR)
        PC += 1

    elif inst[:5] == '01011': #or
        OR = ToDecimal(Registers[inst[10:13]]) | ToDecimal(Registers[inst[13:]])
        Registers[inst[7:10]] = ToBinary(OR)
        PC += 1

    elif inst[:5] == '01100': #and
        AND = ToDecimal(Registers[inst[10:13]]) & ToDecimal(Registers[inst[13:]])
        Registers[inst[7:10]] = ToBinary(AND)
        PC += 1

#TypeB
def TypeB(inst):
    global PC
    if inst[:5] == '00010': #move immediate
        Registers[inst[5:8]] = inst[8:].zfill(16)

    elif inst[:5] == '01000': #right shift
        shift = ToDecimal(inst[8:])
        Registers[inst[5:8]] = '0'*shift + Registers[inst[5:8]][:-1 * shift]

    elif inst[:5] == '01001': #left shift
        shift = ToDecimal(inst[8:])
        Registers[inst[5:8]] = Registers[inst[5:8]][shift:] + '0'*shift
    
    PC += 1

#Type C
def TypeC(inst):
    global PC
    if inst[:5] == '00011': #move register
        Registers[inst[10:13]] = Registers[inst[13:]]
        Registers['111'] = '0'*16

    elif inst[:5] == '00111': #divide
        dividend = ToDecimal(Registers[inst[10:13]])
        divisor = ToDecimal(Registers[inst[13:]])
        quotient = ToBinary(dividend // divisor)
        remainder = ToBinary(dividend % divisor)

        Registers['000'] = quotient
        Registers['001'] = remainder

    elif inst[:5] == '01101': #invert
        a = Registers[inst[13:]]
        inverted = ''
        for i in a:
            if i == '0':
                inverted += '1'
            else:
                inverted += '0'
        Registers[inst[10:13]] = inverted

    elif inst[:5] == '01110': #compare
        val1 = Registers[inst[10:13]]
        val2 = Registers[inst[13:]]

        if val1 > val2:
            Registers['111'] = '0'*14 + '1' + '0' #setting greater than flag

        elif val1 == val2:
            Registers['111'] = '0'*15 + '1' #setting equal to flag

        elif val1 < val2:
            Registers['111'] = '0'*13 + '1' + '0'*2 #setting less than flag

    PC += 1

#Type D
def TypeD(inst):
    # inst[0:5]=opcode, inst[5:8] = reg, str[8:] = mem_addr
    global Cycle
    global PC
    CycleListldst.append(Cycle)
    MemoryListldst.append(ToDecimal(inst[8:]))

    if inst[0:5]=='00100': #load
        Registers[inst[5:8]] = Memory[ToDecimal(inst[8:])]
        PC+=1

    elif inst[0:5]=='00101': #store
        Memory[ToDecimal(inst[8:])] = Registers[inst[5:8]]
        PC+=1

#Type E
def TypeE(inst):
    # str[0:5] = opcode, str[8:] = mem_addr
    global PC
    global Cycle

    if inst[0:5]=='01111': #unconditional jump
        PC = ToDecimal(inst[8:]) #updating program counter to the address of the label
        CycleListLabel.append(Cycle)
        MemoryListLabel.append(PC)

    elif inst[0:5]=='10000': #jump if less than
        if Registers['111'][13]=='1':
            PC = ToDecimal(inst[8:]) #updating program counter to the address of the label
            CycleListLabel.append(Cycle)
            MemoryListLabel.append(PC)
        else:
            PC+=1

    elif inst[0:5]=='10001': #jump if greater than
        if Registers['111'][14]=='1':
            PC = ToDecimal(inst[8:]) #updating program counter to the address of the label
            CycleListLabel.append(Cycle)
            MemoryListLabel.append(PC)
        else:
            PC+=1

    elif inst[0:5]=='10010': #jump if equal
        if Registers['111'][15]=='1':
            PC = ToDecimal(inst[8:]) #updating program counter to the address of the label
            CycleListLabel.append(Cycle)
            MemoryListLabel.append(PC)
        else:
            PC+=1
    Registers['111'] = '0'*16

#Type F
def TypeF(inst): #halt
    global Halted
    Halted = True


#Main
variable = 0
while Halted == False:
    CycleListInst.append(Cycle) #appending cycle number to the cycle list for instructions
    inst = Memory[PC] #fetching instructions from the memory
    MemoryListInst.append(PC) #appending memory address in memory list for instructions
    
    opcode = inst[:5]
    print(ToBinaryMem(PC), end = ' ') #printing the program counter

    if opcode == '00000' or opcode == '00001' or opcode == '00110' or opcode == '01010' or opcode == '01011' or opcode == '01100': #type A
        Registers['111'] = '0'*16
        TypeA(inst)

    elif opcode == '00010' or opcode == '01000' or opcode == '01001': #type B
        Registers['111'] = '0'*16
        TypeB(inst)

    elif opcode == '00011' or opcode == '00111' or opcode == '01101' or opcode == '01110': #type C
        if not(inst[13:] == '111' and opcode == '00011'):
            Registers['111'] = '0'*16
        TypeC(inst)
    
    elif opcode == '00100' or opcode == '00101': #type D
        Registers['111'] = '0'*16
        TypeD(inst)

    elif opcode == '01111' or opcode == '10000' or opcode == '10001' or opcode == '10010': #type E
        TypeE(inst)

    elif opcode == '10011': #type F
        Registers['111'] = '0'*16
        TypeF(inst)

    
    print(str(variable)+')')
    variable+=1
    #printing the registers after each instruction
    for i in Registers:
        
        if i != '111':
            print(Registers[i], end = ' ')
        else: 
            print(Registers[i])
        
    Cycle += 1

#printing the memory state
else:
    for i in Memory:
        print(str(variable)+')')
        print(i)
        variable+=1


#scatter plot (bonus question)
#we have categorised our memory access trace, as-
plt.scatter(CycleListInst, MemoryListInst, label = 'Instructions') #1) fetching instructions from memory
plt.scatter(CycleListldst, MemoryListldst, label = 'Load/Store instructions') #2) accessing memory addresses for load/store instructions
plt.scatter(CycleListLabel, MemoryListLabel, label = 'Label addresses') #3) accessing memory addresses for jump instructions
plt.title('Memory Access Trace') #adding title to the plot
plt.xlabel('Cycle Number') #adding label on the x-axis
plt.ylabel('Memory Address') #adding label on the y-axis
plt.legend() #showing the legend for our categories
plt.show() #showing the scatter plot