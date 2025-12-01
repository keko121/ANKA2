# ==============================================================================
# >  Metin2 DB Sunucusu Derleme Sistemi
# > Updated: Kasim 2025
# > Purpose: DB sunucusunu derleyin (FreeBSD + Linux desteği)
# ==============================================================================

# >> PLATFORM ALGILAMA <<
UNAME_S := $(shell uname -s)

# >> DERLEYICI VE VERSIYON <<
ifeq ($(UNAME_S),Linux)
    CC = ccache clang++-14
    # Fallback
    ifeq ($(shell which clang++-14 2>/dev/null),)
        CC = ccache clang++
    endif
else
    # FreeBSD
    CC = ccache clang++-devel
endif

DB_VERSION = 40142

# >> DOSYA SISTEMI YAPILANDIRMASI <<
INCDIR =
LIBDIR =
BINDIR = ..
OBJDIR = .obj

# Platform-specific output directory
ifeq ($(UNAME_S),Linux)
    DBDIR ?= $(BINDIR)
else
    DBDIR = /usr/home/share/bin
endif

$(shell if [ ! -d $(OBJDIR) ]; then mkdir $(OBJDIR); fi)

# >> YAPILANDIRMA SABITLERI <<
ENABLE_GCC_AUTODEPEND = 1

# >> BAGIMLILIK DOSYASI AYARI <<
ifneq ($(ENABLE_GCC_AUTODEPEND), 1)
DEPFILE = Depend
endif

# >> DERLEYICI BAYRAKLARI <<
CFLAGS = -m32 -g -w -Ofast -pipe -fno-rtti -fno-exceptions -std=c++2a -static-libstdc++ -Wno-long-long -pthread -D_THREAD_SAFE

# >> PLATFORM OZELLIKLERI <<
ifeq ($(UNAME_S),Linux)
    CFLAGS += -D__linux__
endif

# >> VERSIYON VE SISTEM BILGISI <<
CFLAGS += -D__USER__=\"$(USER)\" -D__HOSTNAME__=\"$(HOSTNAME)\" -D__PWD__=\"$(PWD)\" -D__DB_VERSION__=\"$(DB_VERSION)\"

# >> HARICI KUTUPHANE AYARLARI <<

# OpenSSL Sifreleme
INCDIR += -I/usr/include
LIBS += -lssl -lcrypto

# MySQL Veritabani
ifeq ($(UNAME_S),Linux)
    INCDIR += -I/usr/include/mysql -I/usr/include/mariadb
    LIBDIR += -L/usr/lib/i386-linux-gnu -L/usr/lib32
    LIBS += -lmysqlclient -lz
else
    INCDIR += -I/usr/local/include/mysql
    LIBS += /usr/local/lib/mysql/libmysqlclient.a /usr/lib/libz.a
endif

# >> PROJE KUTUPHANELERI <<
ifeq ($(UNAME_S),Linux)
    INCDIR += -I/usr/include
else
    INCDIR += -I/usr/local/include
endif

LIBDIR += -L../../library/libthecore/lib -L../../library/libsql -L../../library/libpoly -L../../library/libgame/lib
LIBS += -lthecore -lsql -lpoly -lgame -lm

# >> HEDEF DOSYA <<
TARGET = $(BINDIR)/db

# >> KAYNAK DOSYA LISTESI <<
CPPFILE =	BufferManager.cpp Config.cpp NetBase.cpp Peer.cpp PeerBase.cpp Main.cpp Lock.cpp DBManager.cpp \
			Cache.cpp LoginData.cpp ClientManager.cpp ClientManagerPlayer.cpp ClientManagerLogin.cpp \
			ClientManagerBoot.cpp ClientManagerParty.cpp ClientManagerGuild.cpp GuildManager.cpp \
			PrivManager.cpp MoneyLog.cpp ItemAwardManager.cpp ClientManagerEventFlag.cpp Marriage.cpp \
			ItemIDRangeManager.cpp ClientManagerHorseName.cpp version.cpp ProtoReader.cpp CsvReader.cpp \
			ClientManagerOfflineshop.cpp

# >> HEDEF DOSYA DONUSUMLERI <<
OBJS = $(CPPFILE:%.cpp=$(OBJDIR)/%.o)
ifeq ($(ENABLE_GCC_AUTODEPEND), 1)
CPPDEPS = $(OBJS:%.o=%.d)
endif

# >> RENK KODLARI <<
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[0;33m
BLUE = \033[0;34m
MAGENTA = \033[0;35m
CYAN = \033[0;36m
WHITE = \033[0;37m
BOLD = \033[1m
RESET = \033[0m

# >> ANA HEDEFLER <<
.PHONY: default all clean dep help

default: $(TARGET)

$(TARGET): $(OBJS)
	@echo -e "${MAGENTA}[BIRLESTIRME]${RESET} ${WHITE}$(TARGET)${RESET} olusturuluyor..."
	@$(CC) $(CFLAGS) $(LIBDIR) $(OBJS) $(LIBS) -o $(TARGET)
	@echo -e "${CYAN}[DOSYA TASI]${RESET} ${WHITE}$(DBDIR)${RESET} dizinine tasiniyor..."
	@mv $(TARGET) $(DBDIR)
	@echo -e "${GREEN}[TAMAMLANDI]${RESET} DB dosyasi ${WHITE}$(DBDIR)${RESET} dizininde hazir!"
	@echo -e "${BOLD}${CYAN}=== DB SUNUCUSU BASARIYLA DERLENDI ===${RESET}"

$(OBJDIR)/%.o: %.cpp
	@echo -e "[CPP]  ${YELLOW}$<${RESET} -> ${RED}$@${RESET}"
	@$(CC) $(CFLAGS) $(INCDIR) -c $< -o $@
ifeq ($(ENABLE_GCC_AUTODEPEND), 1)
	@$(CC) -MM $(CFLAGS) $(INCDIR) $< > $(OBJDIR)/$*.d.tmp
	@sed 's|$*.o:|$(OBJDIR)/$*.o:|g' $(OBJDIR)/$*.d.tmp > $(OBJDIR)/$*.d
	@rm -f $(OBJDIR)/$*.d.tmp
endif

$(OBJDIR):
	@echo -e "${BLUE}[DIZIN HAZIRLIGI]${RESET} ${WHITE}$(OBJDIR)${RESET} dizini olusturuluyor..."
	@mkdir $(OBJDIR)

clean:
	@echo -e "${RED}[TEMIZLIK]${RESET} Tum obje dosyalari temizleniyor..."
	@rm -f $(OBJS) $(DBDIR)/db
ifeq ($(ENABLE_GCC_AUTODEPEND), 1)
	@rm -f $(CPPDEPS)
endif
	@rm -rf $(OBJDIR)
	@echo -e "${GREEN}[OK]${RESET} Tum temizlik islemleri tamamlandi"

dep:
ifeq ($(ENABLE_GCC_AUTODEPEND), 1)
	@echo -e "${YELLOW}[BILGI]${RESET} GCC otomatik bagimlilik takibi aktif"
else
	@echo -e "${BLUE}[BAGIMLILIK]${RESET} Manuel bagimlilik dosyasi guncelleniyor..."
	@makedepend -f $(DEPFILE) $(INCDIR) -I/usr/include/c++/3.3 -I/usr/include/c++/4.2 -p$(OBJDIR)/ $(CPPFILE) 2> /dev/null > $(DEPFILE)
	@echo -e "${GREEN}[OK]${RESET} Bagimlilik dosyasi guncellendi"
endif

# >> YARDIM MESAJI <<
help:
	@echo -e "${BOLD}${CYAN}"
	@echo -e "================================================"
	@echo -e "         DB SUNUCUSU DERLEME SISTEMI"
	@echo -e "================================================"
	@echo -e "${RESET}"
	@echo -e "${BOLD}${WHITE}KULLANIM:${RESET}"
	@echo -e "  ${GREEN}make${RESET}        -> ${YELLOW}DB sunucusunu derle${RESET}"
	@echo -e "  ${GREEN}make clean${RESET}  -> ${RED}Tum obje dosyalarini temizle${RESET}"
	@echo -e "  ${GREEN}make dep${RESET}    -> ${MAGENTA}Bagimliliklari guncelle${RESET}"
	@echo -e "  ${GREEN}make help${RESET}   -> ${CYAN}Bu yardim mesajini goster${RESET}"
	@echo -e ""
	@echo -e "${BOLD}${WHITE}AYARLAR:${RESET}"
	@echo -e "  ${YELLOW}Derleyici:${RESET} $(CC)"
	@echo -e "  ${YELLOW}DB Versiyon:${RESET} $(DB_VERSION)"
	@echo -e "  ${YELLOW}C++ Standard:${RESET} C++2a"
	@echo -e "  ${YELLOW}Mimari:${RESET} 32-bit"
	@echo -e "  ${YELLOW}Cikti Dizini:${RESET} $(DBDIR)"
	@echo -e "  ${YELLOW}Kaynak Dosya:${RESET} $(words $(CPPFILE)) adet"
	@echo -e ""
	@echo -e "${BOLD}${WHITE}OZELLIKLER:${RESET}"
	@echo -e "  ${GREEN}✓${RESET} MySQL veritabani destegi"
	@echo -e "  ${GREEN}✓${RESET} OpenSSL sifreleme"
	@echo -e "  ${GREEN}✓${RESET} Cache ve buffer yonetimi"
	@echo -e "  ${GREEN}✓${RESET} Client yonetimi"
	@echo -e "  ${GREEN}✓${RESET} Guild sistemleri"

# >> OTOMATIK BAGIMLILIK KONTROLU <<
ifeq ($(ENABLE_GCC_AUTODEPEND), 1)
sinclude $(CPPDEPS)
else
sinclude $(DEPFILE)
endif
