import unittest
import os
import struct
import subprocess
import xml.etree.ElementTree as ET


class TestInterpreter(unittest.TestCase):
  def setUp(self):
    self.input_file = 'output.bin'
    self.result_file = 'result.xml'
    self.memory_range = (0, 255)
    with open(self.input_file, 'wb') as f:
      f.write(
        struct.pack('>B I', 0xFA, 122) + # LOAD_CONST 122
        struct.pack('>B I', 0xFA, 150) + # LOAD_CONST 150
        struct.pack('>B I', 0x13, 19) + # WRITE_MEM по адресу 19
        struct.pack('>B I', 0x13, 29) + # WRITE_MEM по адресу 29
        struct.pack('>B', 0x1D) +    # READ_MEM (чтение из памяти)
        struct.pack('>B I', 0x39, 946)  # ABS
      )

  def tearDown(self):
    os.remove(self.input_file)
    os.remove(self.result_file)

  def test_interpret(self):
    try:
      result = subprocess.run(['python', 'interpreter.py', self.input_file, self.result_file, str(self.memory_range[0]), str(self.memory_range[1])],
                  capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
      self.fail(f"Interpreter failed with return code {e.returncode}: {e.stderr}")

    try:
      tree = ET.parse(self.result_file)
      root = tree.getroot()
      results = {int(entry.get('address')): int(entry.text) for entry in root.findall('entry')} # предположим тег "entry"
    except (FileNotFoundError, ET.ParseError) as e:
      self.fail(f"Error parsing XML: {e}")

    expected_results = {
      19: 122,
      29: 150
    }
    self.assertEqual(results, expected_results)


if __name__ == '__main__':
  unittest.main()