#include <assert.h>
#include "ventoy_locale_list.h"

int main(void)
{
    char locales[4][8];
    assert(ventoy_parse_locale_list("en_US\nsat_IN\nhi_IN\n", 19, locales, 4) == 3);
    assert(strcmp(locales[1], "sat_IN") == 0 && !locales[3][0]);
    assert(ventoy_parse_locale_list("ar_ARen_US", 10, locales, 4) == 2);
    assert(strcmp(locales[1], "en_US") == 0);
    assert(ventoy_parse_locale_list("sat_IN", 6, locales, 4) == 1);
    assert(ventoy_parse_locale_list("toolong_locale\nen_US\n", 21, locales, 4) == 1);
    assert(ventoy_parse_locale_list("en_US\n", 6, locales, 1) == 0 && !locales[0][0]);
    assert(ventoy_parse_locale_list(NULL, 0, locales, 4) == 0);
    return 0;
}
