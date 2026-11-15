"""Hack assembler (Nand to Tetris). K = 48 -> K mod 3 = 0 -> writes symbols.txt
Usage: python assembler.py Prog.asm   (creates Prog.hack and symbols.txt)
"""
import sys

COMP = {
    '0': '0101010', '1': '0111111', '-1': '0111010', 'D': '0001100',
    'A': '0110000', '!D': '0001101', '!A': '0110001', '-D': '0001111',
    '-A': '0110011', 'D+1': '0011111', 'A+1': '0110111', 'D-1': '0001110',
    'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011', 'A-D': '0000111',
    'D&A': '0000000', 'D|A': '0010101',
    'M': '1110000', '!M': '1110001', '-M': '1110011', 'M+1': '1110111',
    'M-1': '1110010', 'D+M': '1000010', 'D-M': '1010011', 'M-D': '1000111',
    'D&M': '1000000', 'D|M': '1010101',
}
DEST = {'': '000', 'M': '001', 'D': '010', 'MD': '011',
        'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'}
JUMP = {'': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
        'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}


def predefined():
    t = {f'R{i}': i for i in range(16)}
    t.update({'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
              'SCREEN': 16384, 'KBD': 24576})
    return t


def clean(line):
    return line.split('//')[0].replace(' ', '').replace('\t', '').strip()


def assemble(lines):
    symbols = predefined()
    # First reading: remove comments/blank lines, record labels
    code, pc = [], 0
    for raw in lines:
        line = clean(raw)
        if not line:
            continue
        if line.startswith('('):
            symbols[line[1:-1]] = pc
        else:
            code.append(line)
            pc += 1
    # Second reading: translate
    out, next_var = [], 16
    for line in code:
        if line[0] == '@':
            s = line[1:]
            if s.isdigit():
                n = int(s)
            else:
                if s not in symbols:
                    symbols[s] = next_var
                    next_var += 1
                n = symbols[s]
            out.append(format(n, '016b'))
        else:
            dest, jump = '', ''
            if '=' in line:
                dest, line = line.split('=', 1)
            if ';' in line:
                line, jump = line.split(';', 1)
            out.append('111' + COMP[line] + DEST[dest] + JUMP[jump])
    return out, symbols


def write_symbols(symbols, path='symbols.txt'):
    """Extra feature (K mod 3 == 0): save labels and variables with addresses."""
    pre = predefined()
    with open(path, 'w') as f:
        for name, addr in symbols.items():
            if name not in pre:
                f.write(f'{name}={addr}\n')


if __name__ == '__main__':
    src = sys.argv[1]
    with open(src) as f:
        binary, syms = assemble(f.readlines())
    with open(src.rsplit('.', 1)[0] + '.hack', 'w') as f:
        f.write('\n'.join(binary) + '\n')
    write_symbols(syms)
    print(f'{src}: {len(binary)} instructions, symbols saved to symbols.txt')