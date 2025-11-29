# =============================================================================
# libgame Makefile - Cross-Platform (FreeBSD + Linux)
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

BIN_DIR = ../lib
BIN = $(BIN_DIR)/libgame.a

CFLAGS = -m32 -Wall -w -O2 -pipe -fno-exceptions -I../include
CFLAGS += -std=c++2a

# Platform flag
ifeq ($(UNAME_S),Linux)
    CFLAGS += -D__linux__
endif

LIBS =

OBJFILES = grid.o attribute.o targa.o

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
	touch Depend
	$(CXX) $(CFLAGS) -MM *.cc > Depend

$(OBJFILES):
	$(CXX) $(CFLAGS) -c $<

include Depend

