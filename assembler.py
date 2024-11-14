import struct
import sys


def assemble(input_file, output_file, log_file):
    instructions = []
    log_entries = []

    with open(input_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue

            command = parts[0]
            if command == "LOAD_CONST":
                A = int(parts[1])
                B = int(parts[2])
                instructions.append(struct.pack('>B I', 0xFA, A))
                log_entries.append(f"LOAD_CONST=A={A}, B={B}")
            elif command == "READ_MEM":
                A = int(parts[1])
                instructions.append(struct.pack('>B', 0x1D))
                log_entries.append(f"READ_MEM=A={A}")
            elif command == "WRITE_MEM":
                A = int(parts[1])
                B = int(parts[2])
                instructions.append(struct.pack('>B I', 0x13, B))
                log_entries.append(f"WRITE_MEM=A={A}, B={B}")
            elif command == "ABS":
                A = int(parts[1])
                B = int(parts[2])
                instructions.append(struct.pack('>B I', 0x39, B))
                log_entries.append(f"ABS=A={A}, B={B}")

    with open(output_file, 'wb') as f:
        for instruction in instructions:
            f.write(instruction)

    with open(log_file, 'w') as f:
        for entry in log_entries:
            f.write(entry + '\n')


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]
    assemble(input_file, output_file, log_file)