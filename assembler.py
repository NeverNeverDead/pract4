import struct
import sys

def assemble_instruction(opcode, a, b, c, d=0):
    if opcode in {3, 5, 0, 6}:  # Проверка кода операции
        return struct.pack('>BBBB', opcode, a, b, c) + (struct.pack('>B', d) if opcode == 6 else b'\x00')
    raise ValueError("Неверный код операции")

def assemble(source_file, binary_file, log_file):
    with open(source_file, 'r') as src, open(binary_file, 'wb') as bin_out, open(log_file, 'w') as log_out:
        for line in src:
            # Удаляем комментарии и пробелы
            line = line.split('#')[0].strip()
            if not line:  # Игнорируем пустые строки
                continue

            parts = list(map(int, line.split()))
            opcode = parts[0]
            instruction_bytes = assemble_instruction(*parts)
            bin_out.write(instruction_bytes)
            log_out.write(f"opcode={opcode}, a={parts[1]}, b={parts[2]}, c={parts[3]}, d={parts[4] if len(parts) > 4 else 0}\n")

if __name__ == "__main__":
    src_file = sys.argv[1]
    bin_file = sys.argv[2]
    log_file = sys.argv[3]
    assemble(src_file, bin_file, log_file)
