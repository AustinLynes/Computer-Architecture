"""CPU functionality."""
import sys


class CPU:

    """Construct a new CPU."""
    def __init__(self, command=""):
        # initalize a CPU with
        # * RAM 
        # * a process counter
        # * a simple 8 slot register to handle processes
        print("\033[34mINITALIZING\033[0m")

        self.ram = [0] * 256 # RAM
        self.pc = 0 # process counter
        self.reg = [0] * 8 # 8 slot register
        
        self.COMMANDS = {
            "NOP":      0b00000000,     
            "HLT":      0b00000001,     
            "PRN":      0b01000111,     
            "LDI":      0b10000010,     
            "CALL":     0b01010000,     
            "ADD":      0b10100000,
            "SUB":      0b10100001,
            "DIV":      0b10100011,
            "MOD":      0b10100100,
            "MUL":      0b10100010,
            "PUSH":      0b01000101,
            "POP":       0b01000110
        }
        
        self.sp = 7
        self.command = command
 
    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    """Load a program into memory."""
    def load(self):
        print("\033[32mLOADING\033[0m ")
        address = 0

        # For now, we've just hardcoded a program:
        
        # 130 0 8 73 0 1
        program = []
        
        # Open up our .lse file..
        with open(f"examples/{self.command}") as f:
            # save each line
            _code = f.readlines()
            # create a list to hold the instructions we will find
            instructions  = []
            # for each line inside our .ls8 _code file
            for i in _code:
                if i[0] != "#" and len(i) > 1: 
                    # add the first complete string found on each line... 
                    # allows for the most basic use of comments
                    instruction = i.split()[0]
                    instructions.append(instruction)
            
            # for each instruction we found
            for i in instructions:
                # add it to the program.
                # it is a string right now...
                # so it needs to be converted to an integer... 
                # base 2

                # print(i)
                program.append(int(i, 2))
        
        # close the file 
        f.close()

        for instruction in program:
            self.ram[address] = instruction
            address += 1
    
        print(f"\033[32mPROGRAM_LOADED\033[0m aprox {address}bytes of RAM ")
    

    """ALU operations."""
    def alu(self, op, reg_a, reg_b):
    
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB": 
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "MOD":
            self.reg[reg_a] %= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    """
    Handy function to print out the CPU state. You might want to call this
    from run() if you need help debugging.
    """
    def trace(self):
    
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    """Run the CPU."""
    def run(self):

        
        IR = self.reg[self.pc]
        
        running = True

        # while the program is running
        while running:
            limit = len(self.ram)-1
            
            if self.pc <= limit:
                # read the current command from the RAM
                command = self.ram[self.pc]

                #   LDI 
                ## 3 Byte
                ## Needing to know the the information of 
                ## 2 different bytes this command needs 
                ## to increment the process counter by 2 when it resolves
                if command == self.COMMANDS["LDI"]:
                    # save to the register with the index
                    # corrispoding to this process + 1
                    MAR = self.ram[self.pc + 1]
                    MDR = self.ram[self.pc + 2]
                    self.reg[MAR] = MDR
                    self.pc += 2

                #   PRN 
                ## 2 Byte
                ## Needing to know the information of 1 other byte
                ## the prcess counter needs to be incremented by 1
                if command == self.COMMANDS["PRN"]:
                    MAR = self.ram[self.pc + 1]
                    print(self.reg[MAR])

                    self.pc += 1
                
                # CALL
                ## 2 Byte
                ## Needing to know the information of 1 other byte
                ## the prcess counter needs to be incremented by 1
                if command == self.COMMANDS["CALL"]:
                    MAR = self.ram[self.pc + 1]
                    self.reg[MAR]

                    self.pc += 1

                # MUL
                ## 3 Byte
                ## Needing to know the information of 2 other byte
                ## the prcess counter needs to be incremented by 2
                if command == self.COMMANDS["MUL"]:
                    _a = self.ram[self.pc + 1]
                    _b = self.ram[self.pc + 2]

                    self.alu("MUL",_a, _b)
                    self.pc += 2
                
                # ADD
                ## 3 Byte
                ## Needing to know the information of 2 other byte
                ## the prcess counter needs to be incremented by 2
                if command == self.COMMANDS["ADD"]:
                    _a = self.ram[self.pc + 1]
                    _b = self.ram[self.pc + 2]

                    self.alu("ADD",_a, _b)
                    self.pc += 2
                
                # SUB
                ## 3 Byte
                ## Needing to know the information of 2 other byte
                ## the prcess counter needs to be incremented by 2
                if command == self.COMMANDS["SUB"]:
                    _a = self.ram[self.pc + 1]
                    _b = self.ram[self.pc + 2]

                    self.alu("SUB",_a, _b)
                    self.pc += 2

                # DIV
                ## 3 Byte
                ## Needing to know the information of 2 other byte
                ## the prcess counter needs to be incremented by 2
                if command == self.COMMANDS["DIV"]:
                    _a = self.ram[self.pc + 1]
                    _b = self.ram[self.pc + 2]

                    self.alu("DIV",_a, _b)
                    self.pc += 2

                # MOD
                ## 3 Byte
                ## Needing to know the information of 2 other byte
                ## the prcess counter needs to be incremented by 2
                if command == self.COMMANDS["MOD"]:
                    _a = self.ram[self.pc + 1]
                    _b = self.ram[self.pc + 2]

                    self.alu("MOD",_a, _b)
                    self.pc += 2

                if command == self.COMMANDS["PUSH"]:
                    # self.reg[self.ram[self.pc + 1]].append(self.ram[self.pc + 1])
                    self.reg[self.sp] -= 1
                    old_num = self.ram[self.pc + 1]
                    val = self.reg[old_num]
                    address= self.reg[self.sp]

                    self.ram[address] = val

                    self.pc += 1

                if command == self.COMMANDS["POP"]:
                    # self.reg[self.ram[self.pc + 1]].pop()
                    val = self.ram_read(self.reg[self.sp])
                    self.reg[self.ram_read(self.pc + 1)]= val

                    self.reg[self.sp] += 1
                  
                    self.pc += 1
                    
                
                if command == self.COMMANDS["HLT"]:
                    running = False

                # at the end of the process increment the 
                # process counter
                self.pc += 1


