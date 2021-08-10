#import
from Registers import *
from InstructionDict import *
import sys

#reading the lines
while True:
    try:
        SingleLine = input()
        
    except EOFError:
        break;