import unittest
import os
import struct

class TestAssembler(unittest.TestCase):
    def setUp(self):
        self.input_file = 'test.asm'
        self.output_file = 'output.bin'
        self.log_file = 'log.txt'
        with open(self.input_file, 'w') as f:
            f.write("LOAD_CONST 122 1013\n")
            f.write("LOAD_CONST 150 1014\n")
            f.write("WRITE_MEM 19 176\n")
            f.write("READ_MEM 29\n")
            f.write("ABS 57 946\n")

    def tearDown(self):
        os.remove(self.input_file)
        os.remove(self.output_file)
        os.remove(self.log_file)

    def test_assemble(self):
        os.system(f'python assembler.py {self.input_file} {self.output_file} {self.log_file}')

        # Проверка содержимого бинарного файла
        with open(self.output_file, 'rb') as f:
            data = f.read()

        expected_data = (
            struct.pack('>B I', 0xFA, 122) +
            struct.pack('>B I', 0xFA, 150) +
            struct.pack('>B I', 0x13, 176) +
            struct.pack('>B', 0x1D) +
            struct.pack('>B I', 0x39, 946)
        )

        self.assertEqual(data, expected_data)

    def test_log_file(self):
        os.system(f'python assembler.py {self.input_file} {self.output_file} {self.log_file}')

        # Проверка содержимого лог-файла
        with open(self.log_file, 'r') as f:
            log_entries = f.readlines()

        expected_log_entries = [
            "LOAD_CONST=A=122, B=1013\n",
            "LOAD_CONST=A=150, B=1014\n",
            "WRITE_MEM=A=19, B=176\n",
            "READ_MEM=A=29\n",
            "ABS=A=57, B=946\n"
        ]

        self.assertEqual(log_entries, expected_log_entries)

if __name__ == '__main__':
    unittest.main()
