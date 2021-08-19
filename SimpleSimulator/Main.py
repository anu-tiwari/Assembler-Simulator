#imports
import sys
from BinDec import * 

#global variables
Registers = {'000': '0'*16, '001': '0'*16, '010': '0'*16, '011': '0'*16, '100': '0'*16, '101': '0'*16, '110': '0'*16, '111': '0'*16}
Instructions = {'00000': 'A', '00001': 'A', '00010': 'B', '00011': 'C', '00100': 'D', '00101': 'D', '00110':'A', '00111': 'C', '01000': 'B', '01001':'B', '01010': 'A', '01011':'A', '01100':'A', '01101':'C', '01110': 'C', '01111': 'E', '10000': 'E', '10001': 'E', '10010': 'E', '10011': 'F'}
PC = 0
Cycle = 0
Halted = False
Memory = ['0'*16]*256

#read from stdin
allLines = sys.stdin.read()
separateLines = allLines.split('\n')
for i in range(len(separateLines)):
    Memory[i] = separateLines[i]

#Type A
def TypeA(inst):
    #inst[:5] = opcode inst[5:7] = unused bits inst[7:10] = reg1 inst[10:13] = reg2 inst[13:] = reg3
    global PC
    if inst[:5] =='00000':
        SUM = ToDecimal(Registers[inst[10:13]]) + ToDecimal(Registers[inst[13:]])
        if ToBinary(SUM) == 'overflow error':
            Registers['111'] = ('0'*12) + '1' + ('0'*3)
        else:
            Registers[inst[7:10]] = ToBinary(SUM)
        PC += 1
    elif inst[:5]== '00001':
        DIFF = ToDecimal(Registers[inst[10:13]]) - ToDecimal(Registers[inst[13:]])
        if ToBinary(DIFF) == 'overflow error':
            Registers['111'] = ('0'*12) + '1' + ('0'*3)
        else:
            Registers[inst[7:10]] = ToBinary(DIFF)
        PC += 1
    elif inst[:5] == '00110':
        PROD = ToDecimal(Registers[inst[10:13]]) * ToDecimal(Registers[inst[13:]])
        if ToBinary(PROD) == 'overflow error':
            Registers['111'] = ('0'*12) + '1' + ('0'*3)
        else:
            Registers[inst[7:10]] = ToBinary(PROD)
        PC += 1
    elif inst[:5] == '01010':
        XOR = ToDecimal(Registers[inst[10:13]]) ^ ToDecimal(Registers[inst[13:]])
        Registers[inst[7:10]] = ToBinary(XOR)
        PC += 1
    elif inst[:5] == '01011':
        OR = ToDecimal(Registers[inst[10:13]]) | ToDecimal(Registers[inst[13:]])
        Registers[inst[7:10]] = ToBinary(OR)
        PC += 1
    elif inst[:5] == '01100':
        AND = ToDecimal(Registers[inst[10:13]]) & ToDecimal(Registers[inst[13:]])
        Registers[inst[7:10]] = ToBinary(AND)
        PC += 1

#TypeB
def TypeB(inst):
    global PC
    if inst[:5] == '00010':
        Registers[inst[5:8]] = inst[8:].zfill(16)

    elif inst[:5] == '01000':
        shift = ToDecimal(Registers[inst[8:]])
        Registers[inst[5:8]] = '0'*shift + Registers[inst[5:8]][:-1 * shift]

    elif inst[:5] == '01001':
        shift = ToDecimal(Registers[inst[8:]])
        Registers[inst[5:8]] = Registers[inst[5:8]][shift:] + '0'*shift
    
    PC += 1

#Type C
def TypeC(inst):
    global PC
    if inst[:5] == '00011':
        Registers[inst[10:13]] = Registers[inst[13:]]
        Registers['111'] = '0'*16

    elif inst[:5] == '00111':
        dividend = ToDecimal(Registers[inst[10:13]])
        divisor = ToDecimal(Registers[inst[13:]])
        quotient = ToBinary(dividend // divisor)
        remainder = ToBinary(dividend % divisor)

        Registers['000'] = quotient
        Registers['001'] = remainder

    elif inst[:5] == '01101':
        a = ToDecimal(Registers[inst[13:]])
        a = ~a
        a = ToBinary(a)
        Registers[inst[10:13]] = a

    elif inst[:5] == '01110':
        val1 = Registers[inst[10:13]]
        val2 = Registers[inst[13:]]

        if val1 > val2:
            Registers['111'] = '0'*14 + '1' + '0'

        elif val1 == val2:
            Registers['111'] = '0'*15 + '1'

        elif val1 < val2:
            Registers['111'] = '0'*13 + '1' + '0'*2

    PC += 1

#Type D
def TypeD(inst):
    # inst[0:5]=opcode, inst[5:8] = reg, str[8:] = mem_addr
    global PC
    if inst[0:5]=='00100':
        Registers[inst[5:8]] = Memory[ToDecimal(inst[8:])]
        PC+=1
    elif inst[0:5]=='00101':
        Memory[ToDecimal(inst[8:])] = Registers[inst[5:8]]
        PC+=1

#Type E
def TypeE(inst):
    # str[0:5] = opcode, str[8:] = mem_addr
    global PC
    if inst[0:5]=='01111':
        PC = ToDecimal(inst[8:])
    elif inst[0:5]=='10000':
        if Registers['111'][13]=='1':
            PC = ToDecimal(inst[8:])
        else:
            PC+=1
    elif inst[0:5]=='10001':
        if Registers['111'][14]=='1':
            PC = ToDecimal(inst[8:])
        else:
            PC+=1
    elif inst[0:5]=='10010':
        if Registers['111'][15]=='1':
            PC = ToDecimal(inst[8:])
        else:
            PC+=1
    Registers['111'] = '0'*16

#Type F
def TypeF(inst):
    global Halted
    Halted = True


#Main
while Halted == False:
    inst = Memory[PC]
    opcode = inst[:5]
    print(ToBinaryMem(PC), end = ' ')

    if opcode == '00000' or opcode == '00001' or opcode == '00110' or opcode == '01010' or opcode == '01011' or opcode == '01100':
        Registers['111'] = '0'*16
        TypeA(inst)

    elif opcode == '00010' or opcode == '01000' or opcode == '01001':
        Registers['111'] = '0'*16
        TypeB(inst)

    elif opcode == '00011' or opcode == '00111' or opcode == '01101' or opcode == '01110':
        if not(inst[13:] == '111' and opcode == '00011'):
            Registers['111'] = '0'*16
        TypeC(inst)
    
    elif opcode == '00100' or opcode == '00101':
        Registers['111'] = '0'*16
        TypeD(inst)

    elif opcode == '01111' or opcode == '10000' or opcode == '10001' or opcode == '10010':
        TypeE(inst)

    elif opcode == '10011':
        Registers['111'] = '0'*16
        TypeF(inst)

    #printing after each instruction
    for i in Registers:
        if i != '111':
            print(Registers[i], end = ' ')
        else: 
            print(Registers[i])

else:
    for i in Memory:
        print(i)
