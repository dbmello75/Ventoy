#include <assert.h>
#include <stdio.h>
#include <string.h>

int vtoy_json_escape_string(char *, int, const char *, int);

int main(void)
{
    unsigned char guarded[260];
    const char *samples[] = {"", "normal", "quote\"slash\\", "\b\f\n\r\t\001\037", "Português 한국어", NULL};
    int i, cap, newline;
    char output[128];
    assert(vtoy_json_escape_string(NULL, 0, "x", 0) == 0);
    assert(vtoy_json_escape_string(NULL, 10, "x", 0) == 0);
    memset(output, 'x', sizeof(output));
    assert(vtoy_json_escape_string(output, -1, "x", 0) == 0 && output[0] == 'x');
    vtoy_json_escape_string(output, sizeof(output), "\"\\\001\n", 0);
    assert(strcmp(output, "\"\\\"\\\\\\u0001\\n\",") == 0);
    for (i = 0; i < (int)(sizeof(samples) / sizeof(samples[0])); ++i)
    {
        for (cap = 0; cap <= 256; ++cap)
        {
            for (newline = 0; newline <= 1; ++newline)
            {
                int count, j;
                memset(guarded, 0xa5, sizeof(guarded));
                count = vtoy_json_escape_string((char *)guarded + 2, cap, samples[i], newline);
                assert(guarded[0] == 0xa5 && guarded[1] == 0xa5);
                for (j = cap + 2; j < (int)sizeof(guarded); ++j)
                    assert(guarded[j] == 0xa5);
                assert(count >= 0 && (cap == 0 ? count == 0 : count < cap));
                if (cap > 0)
                    assert(guarded[count + 2] == 0);
                if (count)
                {
                    assert(guarded[2] == '"');
                    assert(guarded[count + 1 - newline] == ',');
                    assert(guarded[count - newline] == '"');
                    /* Let the Python harness validate escapes and UTF-8 as JSON. */
                    printf("%s", guarded + 2);
                    if (!newline) putchar('\n');
                }
            }
        }
    }
    return 0;
}
