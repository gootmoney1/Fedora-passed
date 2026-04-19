#include <stdio.h>
#include <stdlib.h>
#include "memorylib.h"

unsigned char* get_raw(Memory *array, int index) {
    if (index > 999) {
        exit(1);
    }

    if (array->memory[index] == NULL) {
        array->memory[index] = (unsigned char*)malloc(array->set_types[index]);
        if (array->memory[index] == NULL) {
            exit(1);
        }
    }

    return array->memory[index];
}

void add_superlong(Memory *array, long long x) {
    if (array->used > 999) {
        exit(1);
    }

    array->set_types[array->used] = sizeof(long long);
    array->memory[array->used] = get_raw(array, array->used);
    *(long long*)array->memory[array->used] = x;
    array->used++;
}

void add_double(Memory *array, double x) {
    if (array->used > 999) {
        exit(1);
    }

    array->set_types[array->used] = sizeof(double);
    array->memory[array->used] = get_raw(array, array->used);
    *(double*)array->memory[array->used] = x;
    array->used++;
}

void free_memory(Memory *array) {
    for (int i = 0; i < array->used; i++) {
        free(array->memory[i]);
        array->memory[i] = NULL;
    }
    array->used = 0;
}