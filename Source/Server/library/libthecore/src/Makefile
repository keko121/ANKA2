# =============================================================================
# libthecore Makefile - Cross-Platform (FreeBSD + Linux)
# =============================================================================

# Platform detection
UNAME_S := $(shell uname -s)

# Compiler selection based on platform
# Use C++ compiler for .c files (they use C++ features like references)
ifeq ($(UNAME_S),Linux)
    CC = clang++-14
    # Fallback to clang++ if clang++-14 not found
    ifeq ($(shell which clang++-14 2>/dev/null),)
        CC = clang++
    endif
else
    # FreeBSD
    CC = clang++-devel
endif

BIN_DIR = ../lib
BIN     = $(BIN_DIR)/libthecore.a
INCLUDE = ../include

# Linux: 64-bit, FreeBSD: 32-bit
ifeq ($(UNAME_S),Linux)
    CFLAGS  = -Wall -w -O2 -pipe -g -I$(INCLUDE)
    # _GNU_SOURCE enables POSIX signal constants in C++ mode
    CFLAGS += -D_GNU_SOURCE
else
    CFLAGS  = -m32 -Wall -w -O2 -pipe -g -I$(INCLUDE)
endif
CFLAGS += -std=c++11

# Platform-specific flags
ifeq ($(UNAME_S),Linux)
    CFLAGS += -D__linux__
endif

LIBS    = 

OBJFILES = socket.o fdwatch.o buffer.o signal.o log.o utils.o \
	kstbl.o hangul.o heart.o main.o tea.o des.o gost.o memcpy.o xmd5.o

default:
	$(MAKE) $(BIN)

$(BIN): $(OBJFILES)
	if [ ! -d $(BIN_DIR) ]; then mkdir $(BIN_DIR); fi
	ar cru $(BIN) $(OBJFILES) $(LIBS)
	ranlib $(BIN)
	chmod 700 $(BIN)

clean:
	rm -f *.o
	rm -f $(BIN)

dep:
	$(CC) $(CFLAGS) -MM *.c > Depend

$(OBJFILES):
	$(CC) $(CFLAGS) -c $<

memcpy: memcpy.o utils.o log.o
	$(CC) $(CFLAGS) -c -D__MAIN__ memcpy.c
	$(CC) $(CFLAGS) -o memcpy memcpy.o utils.o log.o

include Depend
