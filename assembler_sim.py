# assembler_sim.py
# IAS + Logical + 6-register 8-bit Instruction Set Simulator

OPCODES = {
    "MOV": 1,
    "LOAD": 2,
    "STORE": 3,
    "ADD": 4,
    "SUB": 5,
    "MUL": 6,
    "DIV": 7,
    "JUMP": 8,
    "JUMPZ": 9,
    "AND": 10,
    "OR": 11,
    "NOT": 12,
    "XOR": 13,
    "HLT": 15
}

REGISTERS_MAP = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5
}


def assemble_line(line):
    parts = line.strip().split()
    if not parts:
        return None
    instr = parts[0].upper()

    if instr == "MOV":
        reg = REGISTERS_MAP[parts[1]]
        val = int(parts[2])
        return f"{OPCODES[instr]} {reg} {val}\n"

    elif instr in ["ADD", "SUB", "MUL", "DIV", "AND", "OR", "XOR"]:
        r1 = REGISTERS_MAP[parts[1]]
        r2 = REGISTERS_MAP[parts[2]]
        return f"{OPCODES[instr]} {r1} {r2}\n"

    elif instr == "NOT":
        r1 = REGISTERS_MAP[parts[1]]
        return f"{OPCODES[instr]} {r1}\n"

    elif instr == "LOAD":
        reg = REGISTERS_MAP[parts[1]]
        addr = int(parts[2])
        return f"{OPCODES[instr]} {reg} {addr}\n"

    elif instr == "STORE":
        reg = REGISTERS_MAP[parts[1]]
        addr = int(parts[2])
        return f"{OPCODES[instr]} {reg} {addr}\n"

    elif instr in ["JUMP", "JUMPZ"]:
        addr = int(parts[1])
        return f"{OPCODES[instr]} {addr}\n"

    elif instr == "HLT":
        return f"{OPCODES[instr]}\n"

    else:
        return None


def assemble(code: str):
    assembled = []
    for line in code.splitlines():
        line_code = assemble_line(line)
        if line_code:
            assembled.append(line_code)
    return assembled


def execute(program):
    REGISTERS = [0] * 6
    MEMORY = [0] * 64
    pc = 0
    zero_flag = 0
    output_log = []

    while pc < len(program):
        parts = program[pc].strip().split()
        opcode = int(parts[0])

        if opcode == 1:  # MOV
            reg, val = int(parts[1]), int(parts[2])
            REGISTERS[reg] = val & 0xFF

        elif opcode == 2:  # LOAD
            reg, addr = int(parts[1]), int(parts[2])
            REGISTERS[reg] = MEMORY[addr]

        elif opcode == 3:  # STORE
            reg, addr = int(parts[1]), int(parts[2])
            MEMORY[addr] = REGISTERS[reg]

        elif opcode == 4:  # ADD
            r1, r2 = int(parts[1]), int(parts[2])
            REGISTERS[r1] = (REGISTERS[r1] + REGISTERS[r2]) & 0xFF

        elif opcode == 5:  # SUB
            r1, r2 = int(parts[1]), int(parts[2])
            REGISTERS[r1] = (REGISTERS[r1] - REGISTERS[r2]) & 0xFF

        elif opcode == 6:  # MUL
            r1, r2 = int(parts[1]), int(parts[2])
            REGISTERS[r1] = (REGISTERS[r1] * REGISTERS[r2]) & 0xFF

        elif opcode == 7:  # DIV
            r1, r2 = int(parts[1]), int(parts[2])
            if REGISTERS[r2] != 0:
                REGISTERS[r1] //= REGISTERS[r2]
            else:
                output_log.append("Error: Division by zero.")

        elif opcode == 8:  # JUMP
            addr = int(parts[1])
            pc = addr
            continue

        elif opcode == 9:  # JUMPZ
            addr = int(parts[1])
            if zero_flag == 1:
                pc = addr
                continue

        elif opcode == 10:  # AND
            r1, r2 = int(parts[1]), int(parts[2])
            REGISTERS[r1] = REGISTERS[r1] & REGISTERS[r2]

        elif opcode == 11:  # OR
            r1, r2 = int(parts[1]), int(parts[2])
            REGISTERS[r1] = REGISTERS[r1] | REGISTERS[r2]

        elif opcode == 12:  # NOT
            r1 = int(parts[1])
            REGISTERS[r1] = (~REGISTERS[r1]) & 0xFF  # ensure 8-bit

        elif opcode == 13:  # XOR
            r1, r2 = int(parts[1]), int(parts[2])
            REGISTERS[r1] = REGISTERS[r1] ^ REGISTERS[r2]

        elif opcode == 15:  # HLT
            break

        # Update zero flag (set if any register == 0)
        zero_flag = 1 if any(r == 0 for r in REGISTERS) else 0

        output_log.append(f"Executed: {program[pc].strip()} → {REGISTERS}")
        pc += 1

    return output_log, REGISTERS, MEMORY