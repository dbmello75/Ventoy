#ifndef VENTOY_LOCALE_LIST_H
#define VENTOY_LOCALE_LIST_H

#include <stddef.h>
#include <string.h>

/* New lists are line delimited, allowing ISO 639-3 locales such as sat_IN.
 * Continue to accept the historical concatenated five-byte locale format. */
static size_t ventoy_parse_locale_list(const char *data, size_t length,
                                      char (*out)[8], size_t capacity)
{
    size_t pos = 0, count = 0;
    int legacy;
    if (!capacity)
        return 0;
    memset(out, 0, capacity * sizeof(*out));
    if (!data)
        return 0;
    legacy = !memchr(data, '\n', length) && length % 5 == 0;
    while (pos < length && count + 1 < capacity)
    {
        size_t start = pos, size, i;
        int valid = 1;
        if (legacy)
            pos += 5;
        else
        {
            while (pos < length && data[pos] != '\n' && data[pos] != '\r')
                ++pos;
        }
        size = pos - start;
        for (i = start; i < pos; ++i)
            if (!((data[i] >= 'a' && data[i] <= 'z') ||
                  (data[i] >= 'A' && data[i] <= 'Z') ||
                  (data[i] >= '0' && data[i] <= '9') || data[i] == '_'))
                valid = 0;
        if (valid && size >= 5 && size < sizeof(*out))
            memcpy(out[count++], data + start, size);
        if (!legacy)
            while (pos < length && (data[pos] == '\n' || data[pos] == '\r'))
                ++pos;
    }
    return count;
}

#endif
