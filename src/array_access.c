#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static volatile uint64_t global_sink = 0;

static uint32_t lcg_next(uint32_t *state) {
    *state = (*state * 1664525u) + 1013904223u;
    return *state;
}

static void make_permutation(uint32_t *idx, size_t n) {
    for (size_t i = 0; i < n; i++) {
        idx[i] = (uint32_t)i;
    }

    uint32_t state = 123456789u;

    for (size_t i = n - 1; i > 0; i--) {
        size_t j = lcg_next(&state) % (i + 1);
        uint32_t temp = idx[i];
        idx[i] = idx[j];
        idx[j] = temp;
    }
}

static void init_data(int *data, size_t n) {
    for (size_t i = 0; i < n; i++) {
        data[i] = (int)((i * 17u + 13u) & 0xFFFF);
    }
}

static uint64_t run_sequential(const int *data, size_t n, int repeats) {
    uint64_t sum = 0;

    for (int r = 0; r < repeats; r++) {
        for (size_t i = 0; i < n; i++) {
            sum += (uint64_t)data[i];
        }
    }

    return sum;
}

static uint64_t run_stride(const int *data, size_t n, int repeats, int stride) {
    uint64_t sum = 0;

    for (int r = 0; r < repeats; r++) {
        for (int offset = 0; offset < stride && (size_t)offset < n; offset++) {
            for (size_t i = (size_t)offset; i < n; i += (size_t)stride) {
                sum += (uint64_t)data[i];
            }
        }
    }

    return sum;
}

static uint64_t run_random(const int *data, const uint32_t *idx, size_t n, int repeats) {
    uint64_t sum = 0;

    for (int r = 0; r < repeats; r++) {
        for (size_t i = 0; i < n; i++) {
            sum += (uint64_t)data[idx[i]];
        }
    }

    return sum;
}

int main(int argc, char **argv) {
    if (argc < 5) {
        fprintf(stderr, "Usage: %s <seq|stride|random> <size> <repeats> <stride>\n", argv[0]);
        return 1;
    }

    const char *mode = argv[1];
    size_t n = (size_t)strtoull(argv[2], NULL, 10);
    int repeats = atoi(argv[3]);
    int stride = atoi(argv[4]);

    if (n == 0 || repeats <= 0 || stride <= 0) {
        fprintf(stderr, "Invalid argument value.\n");
        return 1;
    }

    int *data = NULL;
    uint32_t *idx = NULL;

    if (posix_memalign((void **)&data, 64, n * sizeof(int)) != 0) {
        fprintf(stderr, "Failed to allocate data array.\n");
        return 1;
    }

    if (posix_memalign((void **)&idx, 64, n * sizeof(uint32_t)) != 0) {
        fprintf(stderr, "Failed to allocate index array.\n");
        free(data);
        return 1;
    }

    init_data(data, n);
    make_permutation(idx, n);

    uint64_t result = 0;

    if (strcmp(mode, "seq") == 0) {
        result = run_sequential(data, n, repeats);
    } else if (strcmp(mode, "stride") == 0) {
        result = run_stride(data, n, repeats, stride);
    } else if (strcmp(mode, "random") == 0) {
        result = run_random(data, idx, n, repeats);
    } else {
        fprintf(stderr, "Unknown mode: %s\n", mode);
        free(data);
        free(idx);
        return 1;
    }

    global_sink = result;

    printf("mode=%s size=%zu repeats=%d stride=%d checksum=%llu\n",
           mode, n, repeats, stride, (unsigned long long)global_sink);

    free(data);
    free(idx);

    return 0;
}
