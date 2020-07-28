import unittest
from cpu import CPU


# I want to be able to give my CPUs RAM 
# a List of Instructions

class CPU_TEST(unittest.TestCase):
    def setUp(self):
        # initalize CPU 
        self.cpu = CPU()

    # CPU should have 256 bits of ram...
    def test_length_of_ram(self):
        self.assertEqual(len(self.cpu.ram), 256)

    # CPU should have a process count of 0
    def test_process_counter(self):
        self.assertEqual(self.cpu.pc, 0)


    
if __name__ == "__main__":
    unittest.main()