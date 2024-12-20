import struct
import xml.etree.ElementTree as ET
import sys

def execute_program(binary_file, result_file):
    memory = [0] * 1024  # Инициализация памяти
    registers = [0] * 32  # Инициализация регистров
    results = ET.Element("results")
    
    with open(binary_file, 'rb') as bin_in:
        while True:
            instruction = bin_in.read(4)
            if not instruction:
                break
            opcode, a, b, c = struct.unpack('>BBBB', instruction)
            
            if opcode == 3:  # Загрузка константы
                registers[b] = c
            elif opcode == 5:  # Чтение из памяти
                registers[b] = memory[c]
            elif opcode == 0:  # Запись в память
                memory[c] = registers[b]
            elif opcode == 6:  # Бинарная операция "<"
                d = memory[registers[c] + c]
                registers[b] = 1 if registers[b] < d else 0
            
            # Добавить результаты в XML
            ET.SubElement(results, "result", addr=str(b), value=str(registers[b]))

    # Записать в XML файл
    tree = ET.ElementTree(results)
    tree.write(result_file)

if __name__ == "__main__":
    bin_file = sys.argv[1]
    result_file = sys.argv[2]
    execute_program(bin_file, result_file)
