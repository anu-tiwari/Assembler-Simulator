import sys

Registers = {'000': 0, '001':0, '010': 0, '011': 0, '100':0, '101': 0, '110': 0, '111': 0}
Instructions = {'00000': 'A', '00001': 'A', '00010': 'B', '00011': 'C', '00100': 'D', '00101': 'D', '00110':'A', '00111': 'C', '01000': 'B', '01001':'B', '01010': 'A', '01011':'A', '01100':'A', '01101':'C', '01110': 'C', '01111': 'E', '10000': 'E', '10001': 'E', '10010': 'E', '10011': 'F'}
PC = 0
Cycle = 0
Memory = ['0'*16]*256

allLines = sys.stdin.read()
separateLines = allLines.split('\n')
for i in range(len(separateLines)):
    Memory[i] = separateLines[i]
