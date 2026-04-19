#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "memorylib.h"
#include <time.h>
typedef struct {
    unsigned char *data;
    int size;
    int ip; // instruction pointer
} Bytecode;

Bytecode load_bytecode(const char *filename) {
    Bytecode bc;
    FILE *f = fopen(filename, "rb");
    if (!f) {
        printf("failed to open file\n");
        exit(1);
    }
    fseek(f, 0, SEEK_END);
    bc.size = ftell(f);
    rewind(f);
    bc.data = malloc(bc.size);
    bc.ip = 0;
    fread(bc.data, 1, bc.size, f);
    fclose(f);
    return bc;
}
void next(Bytecode *bc, unsigned char *opcode, int *arg,Memory *mem) {
    if (bc->ip >= bc->size) {
        *opcode = 0;
        *arg = 0;
        return;
    }
    *opcode = bc->data[bc->ip];
    memcpy(arg, bc->data + bc->ip + 1, 4);
    bc->ip += 5;
}
const char *op_name(unsigned char op) {switch (op) {case 1: return "OP_LOAD_CONST_INT";case 2: return "OP_LOAD_CONST_FLOAT";case 3: return "OP_STORE";case 4: return "OP_LOAD";case 5: return "OP_CLEAR";case 6: return "OP_ADD";case 7: return "OP_SUB";case 8: return "OP_MUL";case 9: return "OP_DIV";case 10: return "OP_PRINT";case 11: return "OP_HALT";default: return "UNKNOWN";}}

int main() {
    Memory mem;
    mem.used = 0;
    mem.set_types[0] = 0; // Initialize set_types
    mem.memory[0] = NULL; // Initialize memorasy pointer
    Bytecode bc = load_bytecode("code.bin");
    unsigned char op;
    int arg;
    while(bc.ip < bc.size){
        next(&bc,&op,&arg,&mem);
        printf("Executing %s with argument %d\n", op_name(op), arg);
    }
    return 0;
}