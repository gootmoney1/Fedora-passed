import os
import struct
os.chdir(os.path.dirname(os.path.abspath(__file__)))

OPCODES = {
    "OP_LOAD_CONST_INT": 1,
    "OP_LOAD_CONST_FLOAT": 2,

    "OP_STORE": 3,
    "OP_LOAD": 4,
    "OP_CLEAR": 5,

    "OP_ADD": 6,
    "OP_SUB": 7,
    "OP_MUL": 8,
    "OP_DIV": 9,

    "OP_PRINT": 10,
    "OP_HALT": 11,
}

facs = [
    "?",
    "print",
    "clear",
    "add",
    "sub",
    "mul",
    "div"
]

memeory_limit = open("cofing.txt").read().splitlines()[0].split("=")[1].strip()
base = int(memeory_limit)

source = open("source.txt").read()
source = source.replace(" ", "")
next_slot = 0
var_table = {}
amout_of_vars = 0
code = []

def emit_expr(expr):
    expr = expr.strip()

    if expr.startswith("add(") and expr.endswith(")"):
        inside = expr[4:-1]
        var1, var2 = inside.split(",", 1)
        emit_expr(var1)
        emit_expr(var2)
        code.append((OPCODES["OP_ADD"], 0))
        return

    if expr.startswith("sub(") and expr.endswith(")"):
        inside = expr[4:-1]
        var1, var2 = inside.split(",", 1)
        emit_expr(var1)
        emit_expr(var2)
        code.append((OPCODES["OP_SUB"], 0))
        return

    if expr.startswith("mul(") and expr.endswith(")"):
        inside = expr[4:-1]
        var1, var2 = inside.split(",", 1)
        emit_expr(var1)
        emit_expr(var2)
        code.append((OPCODES["OP_MUL"], 0))
        return

    if expr.startswith("div(") and expr.endswith(")"):
        inside = expr[4:-1]
        var1, var2 = inside.split(",", 1)
        emit_expr(var1)
        emit_expr(var2)
        code.append((OPCODES["OP_DIV"], 0))
        return

    if expr in var_table:
        var_id = var_table[expr]
        code.append((OPCODES["OP_LOAD"], base + var_id))
        return

    if "." in expr:
        code.append((OPCODES["OP_LOAD_CONST_FLOAT"], float(expr)))
        return

    if expr.isdigit() or (expr.startswith("-") and expr[1:].isdigit()):
        code.append((OPCODES["OP_LOAD_CONST_INT"], int(expr)))
        return

    print("error: unknown expression ->", expr)

for line in source.splitlines():
    if "?" in line:
        text = line[:-1]
        name = ""
        number = ""

        for ch in text:
            if ch.isalpha():
                name += ch
            elif ch.isdigit() or ch == "." or ch == "-":
                number += ch

        if name not in var_table:
            var_table[name] = next_slot
            next_slot += 1

        var_id = var_table[name]

        if "." in number:
            code.append((OPCODES["OP_LOAD_CONST_FLOAT"], float(number)))
        else:
            code.append((OPCODES["OP_LOAD_CONST_INT"], int(number)))

        code.append((OPCODES["OP_STORE"], base + var_id))

    if line.startswith("print"):
        expr = line.replace("print", "", 1)
        emit_expr(expr)
        code.append((OPCODES["OP_PRINT"], 0))

    if line.startswith("clear"):
        var = line.replace("clear", "", 1)
        if var in var_table:
            var_id = var_table[var]
            code.append((OPCODES["OP_CLEAR"], base + var_id))

code.append((OPCODES["OP_HALT"], 0))

print("Generated code:")
for opcode in code:
    print(opcode)

with open("code.bin", "wb") as f:
    for opcode in code:
        f.write(opcode[0].to_bytes(1, byteorder="little"))
        if isinstance(opcode[1], int):
            f.write(opcode[1].to_bytes(4, byteorder="little", signed=True))
        elif isinstance(opcode[1], float):
            f.write(bytearray(struct.pack("f", opcode[1])))