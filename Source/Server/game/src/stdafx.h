#ifndef __GAME_SRC_STDAFX_H__
#define __GAME_SRC_STDAFX_H__

#include "../../library/libthecore/include/stdafx.h"

#include "../../common/singleton.h"
#include "../../common/utils.h"
#include "../../common/service.h"

#include <algorithm>
#include <math.h>
#include <list>
#include <map>
#include <set>
#include <queue>
#include <string>
#include <vector>
#include <inttypes.h>

#ifdef __GNUC__
	#include <float.h>
	#include <unordered_map>
	#include <unordered_set>
#else
	#include <iterator>
	#include <unordered_map>
	#include <unordered_set>
	#define isdigit iswdigit
	#define isspace iswspace
#endif

#include "typedef.h"
#include "locale.hpp"
#include "event.h"

#define PASSES_PER_SEC(sec) ((sec) * passes_per_sec)

#ifndef M_PI
	#define M_PI 3.14159265358979323846 /* pi */
#endif
#ifndef M_PI_2
	#define M_PI_2 1.57079632679489661923 /* pi/2 */
#endif

#define IN
#define OUT

// Linux compatibility: strlcpy and strlcat are BSD-specific
#if defined(__linux__)
#include <cstring>
#ifndef strlcpy
inline size_t strlcpy(char *dst, const char *src, size_t size) {
    size_t srclen = strlen(src);
    if (size > 0) {
        size_t copylen = (srclen >= size) ? size - 1 : srclen;
        memcpy(dst, src, copylen);
        dst[copylen] = '\0';
    }
    return srclen;
}
#endif
#ifndef strlcat
inline size_t strlcat(char *dst, const char *src, size_t size) {
    size_t srclen = strlen(src);
    size_t dstlen = strlen(dst);
    if (dstlen >= size) return size + srclen;
    if (srclen < size - dstlen) {
        memcpy(dst + dstlen, src, srclen + 1);
    } else {
        memcpy(dst + dstlen, src, size - dstlen - 1);
        dst[size - 1] = '\0';
    }
    return dstlen + srclen;
}
#endif
#endif

#ifdef ENABLE_TELEPORT_TO_A_FRIEND
	#include <chrono>
	#define CHRONO_steady_clock_point std::chrono::steady_clock::time_point
	#define CHRONO_steady_clock_now std::chrono::steady_clock::now()
#endif

#endif
