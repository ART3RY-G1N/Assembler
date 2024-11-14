import struct
import sys
import xml.etree.ElementTree as ET

def interpret(input_file, output_file, memory_range):
    memory = {}
    stack = []

    with open(input_file, 'rb') as f:
        while True:
            byte = f.read(1)
            if not byte:
                break
            opcode = struct.unpack('>B', byte)[0]

            if opcode == 0xFA:  # LOAD_CONST
                A = struct.unpack('>I', f.read(4))[0]
                stack.append(A)
            elif opcode == 0x1D:  # READ_MEM
                address = stack.pop()
                value = memory.get(address, 0)
                stack.append(value)
            elif opcode == 0x13:  # WRITE_MEM
                B = struct.unpack('>I', f.read(4))[0]
                value = stack.pop()
                memory[B] = value
            elif opcode == 0x39:  # ABS
                B = struct.unpack('>I', f.read(4))[0]
                address = stack.pop()
                value = memory.get(address + B, 0)
                stack.append(abs(value))

    # Сохранение результатов в XML
    root = ET.Element("Results")
    for address in range(memory_range[0], memory_range[1] + 1):
        value = memory.get(address, 0)
        entry = ET.SubElement(root, "MemoryEntry", address=str(address))
        entry.text = str(value)

    tree = ET.ElementTree(root)
    tree.write(output_file)


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    memory_range = (int(sys.argv[3]), int(sys.argv[4]))
    interpret(input_file, output_file, memory_range)
    for line in open(output_file).readlines():
        print(line)
