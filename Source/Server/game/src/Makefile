# ==============================================================================
# >  Metin2 Game Sunucusu Derleme Sistemi
# > Updated: Kasim 2025
# > Purpose: Game sunucusunu derleyin (FreeBSD + Linux desteği)
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

GAME_VERSION = 40250

# >> DOSYA SISTEMI YAPILANDIRMASI <<
INCDIR =
LIBDIR =
BINDIR = ..
OBJDIR = .obj

# Platform-specific output directory
ifeq ($(UNAME_S),Linux)
    GAMEDIR ?= $(BINDIR)
else
    GAMEDIR = /usr/home/share/bin
endif

$(shell if [ ! -d $(OBJDIR) ]; then mkdir $(OBJDIR); fi)

# >> YAPILANDIRMA SABITLERI <<
ENABLE_GCC_AUTODEPEND = 1

# >> BAGIMLILIK DOSYASI AYARI <<
ifneq ($(ENABLE_GCC_AUTODEPEND), 1)
DEPFILE = Depend
endif

# >> STANDART KUTUPHANELER <<
ifeq ($(UNAME_S),Linux)
    LIBS = -lm -lcrypt
else
    LIBS = -lm -lmd
endif

# >> DERLEYICI BAYRAKLARI <<
# Linux: 64-bit derleme (Ubuntu 22.04 uyumu)
# FreeBSD: 32-bit derleme (mevcut uyumluluk)
ifeq ($(UNAME_S),Linux)
    CFLAGS = -g -w -Ofast -pipe -fexceptions -Wno-enum-constexpr-conversion -std=c++2a -static-libstdc++ -pthread -D_THREAD_SAFE -DNDEBUG
else
    CFLAGS = -m32 -g -w -Ofast -pipe -fexceptions -Wno-enum-constexpr-conversion -std=c++2a -static-libstdc++ -pthread -D_THREAD_SAFE -DNDEBUG
endif

# >> PLATFORM OZELLIKLERI <<
ifeq ($(UNAME_S),Linux)
    CFLAGS += -D__linux__
endif

# >> GUVENLIK OZELLIKLERI <<
CFLAGS += -fstack-protector-all

# >> VERSIYON VE SISTEM BILGISI <<
CFLAGS += -D__USER__=\"$(USER)\" -D__HOSTNAME__=\"$(HOSTNAME)\" -D__PWD__=\"$(PWD)\" -D__GAME_VERSION__=\"$(GAME_VERSION)\"

# >> HARICI KUTUPHANE AYARLARI <<

# OpenSSL Sifreleme
ifeq ($(UNAME_S),Linux)
    INCDIR += -I/usr/include
    LIBS += -lssl -lcrypto -lcrypto++
else
    INCDIR += -I/usr/include
    LIBS += -lssl -lcrypto -lcryptopp
endif

# DevIL Grafik Kutuphanesi
INCDIR += -I../../library/libdevil
LIBDIR += -L../../library/libdevil
LIBS += -lIL -lpng -ltiff -lmng -llcms -ljpeg

# MySQL Veritabani
ifeq ($(UNAME_S),Linux)
    INCDIR += -I/usr/include/mysql -I/usr/include/mariadb
    LIBDIR += -L/usr/lib/x86_64-linux-gnu
    LIBS += -lmysqlclient -lz
else
    INCDIR += -I/usr/local/include/mysql
    LIBS += /usr/local/lib/mysql/libmysqlclient.a /usr/lib/libz.a
endif

# >> PROJE KUTUPHANELERI <<
ifeq ($(UNAME_S),Linux)
    INCDIR += -I/usr/include
    LIBDIR += -L/usr/lib/x86_64-linux-gnu
else
    INCDIR += -I/usr/include
    LIBDIR += -L/usr/local/lib
endif

INCDIR += -I../../library/liblua/include
INCDIR += -I../../library/msl
INCDIR += -I../../library
INCDIR += -I../../library/nlohmann
LIBDIR += -L../../library/libthecore/lib -L../../library/libpoly -L../../library/libsql -L../../library/libgame/lib -L../../library/liblua/lib
LIBS += -lthecore -lpoly -llua -llualib -lsql -lgame

# >> HEDEF DOSYA <<
TARGET = $(BINDIR)/game

# >> KAYNAK DOSYA LISTESI <<
MAINCPP = main.cpp
CFILE = minilzo.c

CPPFILE =	BattleArena.cpp FSM.cpp MarkConvert.cpp MarkImage.cpp MarkManager.cpp OXEvent.cpp TrafficProfiler.cpp ani.cpp\
			arena.cpp banword.cpp battle.cpp blend_item.cpp cube_renewal.cpp buffer_manager.cpp building.cpp\
			char.cpp char_affect.cpp char_aura.cpp char_battle.cpp char_change_empire.cpp char_horse.cpp char_item.cpp char_manager.cpp\
			char_quickslot.cpp char_resist.cpp char_skill.cpp char_state.cpp PetSystem.cpp cmd.cpp cmd_emotion.cpp cmd_general.cpp\
			cmd_gm.cpp cmd_oxevent.cpp config.cpp constants.cpp crc32.cpp db.cpp desc.cpp\
			desc_client.cpp desc_manager.cpp desc_p2p.cpp dungeon.cpp empire_text_convert.cpp entity.cpp\
			entity_view.cpp event.cpp event_queue.cpp exchange.cpp file_loader.cpp fishing.cpp gm.cpp guild.cpp\
			guild_manager.cpp guild_war.cpp horse_rider.cpp horsename_manager.cpp input.cpp input_auth.cpp input_db.cpp\
			input_login.cpp input_main.cpp input_p2p.cpp input_udp.cpp ip_ban.cpp\
			item.cpp item_addon.cpp item_attribute.cpp item_manager.cpp item_manager_idrange.cpp locale.cpp\
			locale_service.cpp log.cpp login_data.cpp lzo_manager.cpp marriage.cpp\
			messenger_manager.cpp mining.cpp mob_manager.cpp motion.cpp p2p.cpp packet_info.cpp\
			party.cpp polymorph.cpp priv_manager.cpp pvp.cpp\
			questevent.cpp questlua.cpp questlua_affect.cpp questlua_arena.cpp questlua_ba.cpp questlua_building.cpp\
			questlua_danceevent.cpp questlua_dungeon.cpp questlua_game.cpp questlua_global.cpp\
			questlua_guild.cpp questlua_horse.cpp questlua_pet.cpp questlua_item.cpp questlua_marriage.cpp\
			questlua_npc.cpp questlua_oxevent.cpp questlua_party.cpp questlua_pc.cpp\
			questlua_quest.cpp questlua_target.cpp questmanager.cpp questnpc.cpp questpc.cpp\
			refine.cpp regen.cpp safebox.cpp sectree.cpp sectree_manager.cpp shop.cpp\
			skill.cpp start_position.cpp target.cpp text_file_loader.cpp trigger.cpp utils.cpp vector.cpp war_map.cpp\
			wedding.cpp xmas_event.cpp version.cpp map_location.cpp\
			BlueDragon.cpp BlueDragon_Binder.cpp DragonLair.cpp questlua_dragonlair.cpp\
			skill_power.cpp affect.cpp MountSystem.cpp switchbot_manager.cpp CsvReader.cpp\
			buff_on_attributes.cpp dragon_soul_table.cpp DragonSoul.cpp\
			group_text_parse_tree.cpp char_dragonsoul.cpp questlua_dragonsoul.cpp\
			shop_manager.cpp shopEx.cpp item_manager_read_tables.cpp biolog_manager.cpp event_function_handler.cpp\
			event_manager.cpp char_cards.cpp battlepass_manager.cpp char_premium.cpp mob_timer_manager.cpp\
			offline_shop.cpp offlineshop_manager.cpp offlineshop_search_manager.cpp maintenance.cpp growth_pet.cpp changelook.cpp char_hunting.cpp\
			BotPlayer.cpp mount_up_grade.cpp


# >> HEDEF DOSYA DONUSUMLERI <<
COBJS = $(CFILE:%.c=$(OBJDIR)/%.o)
CPPOBJS = $(CPPFILE:%.cpp=$(OBJDIR)/%.o)
ifeq ($(ENABLE_GCC_AUTODEPEND), 1)
CDEPS = $(COBJS:%.o=%.d)
CPPDEPS = $(CPPOBJS:%.o=%.d)
endif

MAINOBJ = $(MAINCPP:%.cpp=$(OBJDIR)/%.o)
ifeq ($(ENABLE_GCC_AUTODEPEND), 1)
MAINDEPS = $(MAINOBJ:%.o=%.d)
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
.PHONY: default all clean tag dep help

default: $(TARGET)

$(OBJDIR)/%.o: %.c
	@echo -e "[C]    ${YELLOW}$<${RESET} -> ${RED}$@${RESET}"
	@$(CC) $(CFLAGS) $(INCDIR) -c $< -o $@
ifeq ($(ENABLE_GCC_AUTODEPEND), 1)
	@$(CC) -MM $(CFLAGS) $(INCDIR) $< > $(OBJDIR)/$*.d.tmp
	@sed 's|$*.o:|$(OBJDIR)/$*.o:|g' $(OBJDIR)/$*.d.tmp > $(OBJDIR)/$*.d
	@rm -f $(OBJDIR)/$*.d.tmp
endif

$(OBJDIR)/%.o: %.cpp
	@echo -e "[CPP]  ${YELLOW}$<${RESET} -> ${RED}$@${RESET}"
	@$(CC) $(CFLAGS) $(INCDIR) -c $< -o $@
ifeq ($(ENABLE_GCC_AUTODEPEND), 1)
	@$(CC) -MM $(CFLAGS) $(INCDIR) $< > $(OBJDIR)/$*.d.tmp
	@sed 's|$*.o:|$(OBJDIR)/$*.o:|g' $(OBJDIR)/$*.d.tmp > $(OBJDIR)/$*.d
	@rm -f $(OBJDIR)/$*.d.tmp
endif

$(TARGET): $(CPPOBJS) $(COBJS) $(MAINOBJ)
	@echo -e "${MAGENTA}[BIRLESTIRME]${RESET} ${WHITE}$(TARGET)${RESET} olusturuluyor..."
	@$(CC) $(CFLAGS) $(LIBDIR) $(COBJS) $(CPPOBJS) $(MAINOBJ) $(LIBS) -o $(TARGET)
	@echo -e "${CYAN}[DOSYA TASI]${RESET} ${WHITE}$(GAMEDIR)${RESET} dizinine tasiniyor..."
	@mv $(TARGET) $(GAMEDIR)
	@echo -e "${GREEN}[TAMAMLANDI]${RESET} Game dosyasi ${WHITE}$(GAMEDIR)${RESET} dizininde hazir!"

dump:
	@$(CC) -dM -E - < /dev/null > .nope.nope

clean:
	@echo -e "${RED}[TEMIZLIK]${RESET} Tum obje dosyalari temizleniyor..."
	@rm -f $(COBJS) $(CPPOBJS) $(MAINOBJ)
ifeq ($(ENABLE_GCC_AUTODEPEND), 1)
	@rm -f $(CDEPS) $(CPPDEPS) $(MAINDEPS)
endif
	@rm -f $(GAMEDIR)/game_r* $(BINDIR)/conv
	@rm -f $(GAMEDIR)/game
	@rm -rf $(OBJDIR)
	@echo -e "${GREEN}[OK]${RESET} Tum temizlik islemleri tamamlandi"

tag:
	@echo -e "${BLUE}[TAG OLUSTURMA]${RESET} CTags dosyasi olusturuluyor..."
	@ctags *.cpp *.h *.c
	@echo -e "${GREEN}[OK]${RESET} Tag dosyasi olusturuldu"

dep:
ifeq ($(ENABLE_GCC_AUTODEPEND), 1)
	@echo -e "${YELLOW}[BILGI]${RESET} GCC otomatik bagimlilik takibi aktif"
else
	@echo -e "${BLUE}[BAGIMLILIK]${RESET} Manuel bagimlilik dosyasi guncelleniyor..."
	@makedepend -f $(DEPFILE) $(INCDIR) -I/usr/include/c++/3.3 -I/usr/include/c++/4.2 -p$(OBJDIR)/ $(CPPFILE) $(CFILE) $(MAINCPP) 2> /dev/null > $(DEPFILE)
	@echo -e "${GREEN}[OK]${RESET} Bagimlilik dosyasi guncellendi"
endif

# >> YARDIM MESAJI <<
help:
	@echo -e "${BOLD}${CYAN}"
	@echo -e "================================================"
	@echo -e "         GAME SUNUCUSU DERLEME SISTEMI"
	@echo -e "================================================"
	@echo -e "${RESET}"
	@echo -e "${BOLD}${WHITE}KULLANIM:${RESET}"
	@echo -e "  ${GREEN}make${RESET}        -> ${YELLOW}Game sunucusunu derle${RESET}"
	@echo -e "  ${GREEN}make clean${RESET}  -> ${RED}Tum obje dosyalarini temizle${RESET}"
	@echo -e "  ${GREEN}make tag${RESET}    -> ${BLUE}CTags dosyasi olustur${RESET}"
	@echo -e "  ${GREEN}make dep${RESET}    -> ${MAGENTA}Bagimliliklari guncelle${RESET}"
	@echo -e "  ${GREEN}make help${RESET}   -> ${CYAN}Bu yardim mesajini goster${RESET}"
	@echo -e ""
	@echo -e "${BOLD}${WHITE}AYARLAR:${RESET}"
	@echo -e "  ${YELLOW}Derleyici:${RESET} $(CC)"
	@echo -e "  ${YELLOW}Game Versiyon:${RESET} $(GAME_VERSION)"
	@echo -e "  ${YELLOW}C++ Standard:${RESET} C++2a"
	@echo -e "  ${YELLOW}Mimari:${RESET} 32-bit"
	@echo -e "  ${YELLOW}Cikti Dizini:${RESET} $(GAMEDIR)"
	@echo -e "  ${YELLOW}Toplam Kaynak:${RESET} $(words $(CPPFILE)) CPP, $(words $(CFILE)) C"

# >> OTOMATIK BAGIMLILIK KONTROLU <<
ifeq ($(ENABLE_GCC_AUTODEPEND), 1)
sinclude $(CDEPS)
sinclude $(CPPDEPS)
sinclude $(MAINDEPS)
else
sinclude $(DEPFILE)
endif
