# import unittest
# import subprocess
# import os
# import xml.etree.ElementTree as ET
#
#
# def check_xml(self, filepath, expected_data):
#   try:
#     tree = ET.parse(filepath)
#     root = tree.getroot()
#     actual_data = []
#     for elem in root:
#       entry = dict((subelem.tag, subelem.text) for subelem in elem)
#       actual_data.append(entry)
#
#     self.assertEqual(len(actual_data), len(expected_data))
#     for i in range(len(actual_data)):
#       self.assertDictEqual(actual_data[i], expected_data[i])
#
#   except FileNotFoundError:
#     self.fail(f"File not found: {filepath}")
#   except ET.ParseError as e:
#     self.fail(f"XML parse error in {filepath}: {e}")
#   except AssertionError as e:
#    self.fail(f"Assertion error while comparing XML data: {e}")
#
#
# class TestUVMMachine(unittest.TestCase):
#   def setUp(self):
#     os.makedirs("tests", exist_ok=True)
#
#   def run_assembler(self, input_file, output_file, log_file=None):
#       cmd = ["python", "assembler.py", input_file, output_file]
#       if log_file:
#           cmd.extend(["--log", log_file])
#       result = subprocess.run(cmd, check=False, capture_output=True, text=True)  # check=False чтобы не прерывать на ошибке
#       if result.returncode != 0:
#           print(f"Assembler error: {result.stderr}")  # Вывод ошибок ассемблера в консоль
#           self.fail(f"Assembler failed with exit code {result.returncode}: {result.stderr}")
#
#   def run_interpreter(self, input_file, output_file, mem_start, mem_end):
#       cmd = ["python", "interpreter.py", input_file, output_file, str(mem_start), str(mem_end)]
#       result = subprocess.run(cmd, check=False, capture_output=True,
#                               text=True)  # check=False чтобы не прерывать на ошибке
#       if result.returncode != 0:
#           print(f"Interpreter error: {result.stderr}")  # Вывод ошибок интерпретатора в консоль
#           self.fail(f"Interpreter failed with exit code {result.returncode}: {result.stderr}")
#
#   def test_load_constant(self):
#       self.run_assembler("tests/load_constant.asm", "tests/load_constant.bin", "tests/load_constant.xml")
#       self.run_interpreter("tests/load_constant.bin", "tests/load_constant_result.xml", 0, 1024)
#       check_xml(self, "tests/load_constant.xml", [{'line': '1', 'opcode': '122', 'operand': '1013'}])
#       check_xml(self, "tests/load_constant_result.xml", [{'address': '0', 'value': '1013'}])
#
#   def test_read_memory(self):
#     self.run_assembler("tests/read_memory.asm", "tests/read_memory.bin", "tests/read_memory.xml")
#     self.run_interpreter("tests/read_memory.bin", "tests/read_memory_result.xml", 0, 1024)
#     check_xml(self, "tests/read_memory.xml", [{'line': '1', 'opcode': '122', 'operand': '10'}, {'line': '2', 'opcode': '19', 'operand': '0'}, {'line': '3', 'opcode': '29', 'operand': '0'}])
#     check_xml(self, "tests/read_memory_result.xml", [{'address': '0', 'value': '10'}])
#
#
#   def test_write_memory(self):
#     self.run_assembler("tests/write_memory.asm", "tests/write_memory.bin", "tests/write_memory.xml")
#     self.run_interpreter("tests/write_memory.bin", "tests/write_memory_result.xml", 0, 1024)
#     check_xml(self, "tests/write_memory.xml", [{'line': '1', 'opcode': '122', 'operand': '176'}, {'line': '2', 'opcode': '19', 'operand': '10'}])
#     check_xml(self, "tests/write_memory_result.xml", [{'address': '10', 'value': '176'}])
#
#   def test_unary_operation(self):
#     self.run_assembler("tests/unary_operation.asm", "tests/unary_operation.bin", "tests/unary_operation.xml")
#     self.run_interpreter("tests/unary_operation.bin", "tests/unary_operation_result.xml", 0, 1024)
#     check_xml(self, "tests/unary_operation.xml", [{'line': '1', 'opcode': '122', 'operand': '10'}, {'line': '2', 'opcode': '19', 'operand': '10'}, {'line': '3', 'opcode': '57', 'operand': '10'}])
#     check_xml(self, "tests/unary_operation_result.xml", [{'address': '10', 'value': '10'}])
#
#   def test_error_handling(self):
#       with self.assertRaises(subprocess.CalledProcessError) as context:
#           self.run_assembler("tests/invalid_program.asm", "tests/invalid_program.bin")
#       self.assertIn("Invalid instruction operands", context.exception.stderr)  # Проверяем сообщение об ошибке ассемблера
#
#
# if __name__ == '__main__':
#   unittest.main()