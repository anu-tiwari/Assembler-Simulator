# CO M21 Assignment
Repository for Computer Organization, Monsoon 2021 semester, assignment at IIITD, created by Team 15:
* Apoorva Arya 2020032 
* Anusha Tiwari 2020362 
* Saumik Shashwat 2020404 

## Adding code
* Add the assembler code in the `Simple-Assembler` directory. Add the commands to execute the assembler in `Simple-Assembler/run`.
* Add the simulator code in the `SimpleSimulator` directory. Add the commands to execute the assembler in `SimpleSimulator/run`.
* Make sure that both the assembler and the simulator read from `stdin`.
* Make sure that both the assembler and the simulator write to `stdout`.

## How to evaluate
* Go to the `automatedTesting` directory and execute the `run` file with appropiate options passed as arguments.
* Options available for automated testing:
	1. `--verbose`: Prints verbose output
	2. `--no-asm`: Does not evaluate the assembler
	3. `--no-sim`: Does not evaluate the simulator

## Simple-Assembler
* The main Python file for the Simple-Assembler is called `Main.py`.
* Other than Main.py, we have also created three Python modules called `InstructionDict.py`, which stores a dictionary for all the instructions supported by the ISA; `Registers.py`, which stores the binary encoding of all the registers; `BinaryConvert.py`, which has a function which converts decimal to 8-bit binary, or returns an overflow error.
* The Shell file `run` inside the `Simple-Assembler` directory contains the relevant instruction to run `Main.py`.

## SimpleSimulator
* The main Python file for the SimpleSimulator is called `Main.py`.
* Other than Main.py, we have also created one Python module called `BinDec.py`, which has three functions which convert 
⋅⋅⋅1)decimal to 8-bit binary or gives an overflow error⋅⋅
⋅⋅⋅2)decimal to 16-bit binary or gives an overflow error⋅⋅
⋅⋅⋅3)binary to decimal⋅⋅
* The Shell file `run` inside the `SimpleSimulator` directory contains the relevant instruction to run `Main.py`.
