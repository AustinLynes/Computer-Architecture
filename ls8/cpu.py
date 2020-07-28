"""CPU functionality."""

import sys
import ctypes

class Node: 
    def __init__(self, value):
        self.next
        self.value = value

class Stack:
    def __init__(self):
        self.head
    def push(self, value):
        # adds a new head node
        # no head
        new_node = Node(value)

        if self.head == None:
            self.head = new_node
        else:
            new_node.next = self.head
            self.head = new_node

    def pop(self):
        # removes the head node
        # and rearanges the pointers
        if self.head == None:
            return 
        else:
            self.head = self.head.next

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
        


        self.command = command
    # MAR 
    # Memory Address Register
    #   The MAR contains the address that is being read or written to.

    # MDR
    # Memory Data Register 
    #   The MDR contains the data that was read or the data to write. 
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

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1
    
        print(f"\033[32mPROGRAM_LOADED\033[0m aprox {address}bytes of RAM ")
    

    """ALU operations."""
    def alu(self, op, reg_a, reg_b):
    
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
                if command == 0b10000010:
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
                if command == 0b1000111:
                    MAR = self.ram[self.pc + 1]
                    print(self.reg[MAR])
                    self.pc += 1
                
                #   HLT 
                ## End the Program
                if command == 0b1:
                    running = False

                # at the end of the process increment the 
                # process counter
                self.pc += 1


