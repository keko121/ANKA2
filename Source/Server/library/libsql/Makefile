# =============================================================================
# libsql Makefile - Cross-Platform (FreeBSD + Linux)
# =============================================================================

# Platform detection
UNAME_S := $(shell uname -s)

# Compiler selection
ifeq ($(UNAME_S),Linux)
    CXX = clang++-14
    ifeq ($(shell which clang++-14 2>/dev/null),)
        CXX = clang++
    endif
else
    CXX = clang++-devel
endif

BIN = ./libsql.a

# Platform-specific include paths
ifeq ($(UNAME_S),Linux)
    IFLAGS = -I/usr/include/ -I/usr/include/mysql
else
    IFLAGS = -I/usr/local/include/ -I/usr/local/include/mysql
endif

CFLAGS = $(IFLAGS) -m32 -Wall -w -O2 -pipe -D_THREAD_SAFE -fno-exceptions
CFLAGS += -std=c++2a

# Platform flag
ifeq ($(UNAME_S),Linux)
    CFLAGS += -D__linux__
endif

LIBS =

OBJFILES = AsyncSQL.o Semaphore.o Tellwait.o Statement.o

default:
	$(MAKE) $(BIN)

$(BIN): $(OBJFILES)
	ar cru $(BIN) $(OBJFILES) $(LIBS)
	ranlib $(BIN)
	chmod 700 $(BIN)

clean:
	rm -f *.o
	rm -f $(BIN)

dep:
	touch Depend
	$(CXX) $(CFLAGS) -MM *.cpp > Depend

$(OBJFILES):
	$(CXX) $(CFLAGS) -c $<

sinclude Depend
