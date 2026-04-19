#ifndef MEMORYLIB_H
#define MEMORYLIB_H

typedef struct
{
    unsigned char *memory[1000];
    int set_types[1000];
    int used;

    
} Memory;

unsigned char* get_raw(Memory *array, int index);
void add_superlong(Memory *array, long long x);
void add_double(Memory *array, double x);
void free_memory(Memory *array);

#endif