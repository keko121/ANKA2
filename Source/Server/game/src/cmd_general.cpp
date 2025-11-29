#include "stdafx.h"
#ifdef __FreeBSD__
#include <md5.h>
#else
#include "../../library/libthecore/include/xmd5.h"
#endif
#include <errno.h>
#include "utils.h"
#include "config.h"
#include "desc_client.h"
#include "desc_manager.h"
#include "char.h"
#include "char_manager.h"
#include "motion.h"
#include "packet.h"
#include "affect.h"
#include "pvp.h"
#include "start_position.h"
#include "party.h"
#include "guild_manager.h"
#include "p2p.h"
#include "dungeon.h"
#include "messenger_manager.h"
#include "war_map.h"
#include "questmanager.h"
#include "item_manager.h"
#include "mob_manager.h"
#include "item.h"
#include "arena.h"
#include "buffer_manager.h"
#include "unique_item.h"
#include "../../common/service.h"
#include "../../common/VnumHelper.h"
#include "log.h"
#include "locale.hpp"

#ifdef ENABLE_MOUNT_SYSTEM
	#include "MountSystem.h"
#endif

#ifdef ENABLE_PET_SYSTEM
	#include "PetSystem.h"
#endif

#ifdef ENABLE_MAINTENANCE_SYSTEM
	#include "maintenance.h"
#endif

extern int g_server_id;

extern int g_nPortalLimitTime;

#ifdef __AUTO_HUNT__
ACMD(do_auto_hunt)
{
	ch->GetAutoHuntCommand(argument);
}
#endif


#ifdef ENABLE_HORSE_SPAWN_EXPLOIT_FIX
ACMD(do_user_horse_ride)
{
	if (ch->IsObserverMode())
		return;

	if (ch->IsDead() || ch->IsStun())
		return;

	if (ch->IsHorseRiding() == false)
	{
		if (ch->GetMountVnum())
		{
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 282, "");
			return;
		}

		// Performans optimizasyonu: GetQuestFlag yerine direkt member variable
		if (ch->GetHorseCheckerFlag() > 0 && get_global_time() < ch->GetHorseCheckerFlag())
		{
			ch->ChatPacket(CHAT_TYPE_INFO, "<Sistem> Lütfen %d saniye bekleyin.", (ch->GetHorseCheckerFlag() - get_global_time()) % 180);
			return;
		}

		if (ch->GetHorse() == NULL)
		{
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 283, "");
			return;
		}

		ch->SetHorseCheckerFlag(get_global_time() + 3);
		ch->StartRiding();
	}
	else
	{
		ch->StopRiding();
	}
}

ACMD(do_user_horse_back)
{
	if (ch->GetHorse() != NULL)
	{
		// Performans optimizasyonu: GetQuestFlag yerine direkt member variable
		if (ch->GetHorseCheckerFlag() > 0 && get_global_time() < ch->GetHorseCheckerFlag())
		{
			ch->ChatPacket(CHAT_TYPE_INFO, "<Sistem> Lütfen %d saniye bekleyin.", (ch->GetHorseCheckerFlag() - get_global_time()) % 180);
			return;
		}
		ch->SetHorseCheckerFlag(get_global_time() + 3);
		ch->HorseSummon(false);
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 284, "");
	}
	else if (ch->IsHorseRiding() == true)
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 285, "");
	}
	else
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 283, "");
	}
}
#else
ACMD(do_user_horse_ride)
{
	if (ch->IsObserverMode())
		return;

	if (ch->IsDead() || ch->IsStun())
		return;

	if (ch->IsHorseRiding() == false)
	{
		if (ch->GetMountVnum())
		{
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 282, "");
			return;
		}

		if (ch->GetHorse() == NULL)
		{
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 283, "");
			return;
		}

		ch->StartRiding();
	}
	else
	{
		ch->StopRiding();
	}
}

ACMD(do_user_horse_back)
{
	if (ch->GetHorse() != NULL)
	{
		ch->HorseSummon(false);
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 284, "");
	}
	else if (ch->IsHorseRiding() == true)
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 285, "");
	}
	else
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 283, "");
	}
}
#endif

ACMD(do_user_horse_feed)
{
	if (ch->GetMyShop())
		return;

	if (ch->GetHorse() == NULL)
	{
		if (ch->IsHorseRiding() == false)
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 283, "");
		else
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 286, "");
		return;
	}

	DWORD dwFood = ch->GetHorseGrade() + 50054 - 1;

#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
	BYTE locale = ch->GetLanguage();
#endif

	if (ch->CountSpecifyItem(dwFood) > 0)
	{
		ch->RemoveSpecifyItem(dwFood, 1);
		ch->FeedHorse();
		const char* itemName = 
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
			LC_LOCALE_ITEM(dwFood, locale);
#else
			ITEM_MANAGER::instance().GetTable(dwFood)->szLocaleName;
#endif
		if (itemName)
		{
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 287, "%s", itemName);
		}
	}
	else
	{
		const char* itemName = 
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
			LC_LOCALE_ITEM(dwFood, locale);
#else
			ITEM_MANAGER::instance().GetTable(dwFood)->szLocaleName;
#endif
		if (itemName)
		{
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 171, "%s", itemName);
		}
	}
}

#define MAX_REASON_LEN 128

EVENTINFO(TimedEventInfo)
{
	DynamicCharacterPtr ch;
	int subcmd;
	int left_second;
	char szReason[MAX_REASON_LEN];

	TimedEventInfo() : ch() , subcmd( 0 ) , left_second( 0 ) {::memset( szReason, 0, MAX_REASON_LEN );}
};

#ifdef ENABLE_CHANGE_CHANNEL
EVENTINFO(ChangeChannelEventInfo)
{
	DynamicCharacterPtr ch;
	int channel_number;
	int left_second;

	ChangeChannelEventInfo() : ch() , channel_number( 0 ) , left_second( 0 ) {}
};
#endif

struct SendDisconnectFunc
{
	void operator () (LPDESC d)
	{
		if (d->GetCharacter())
		{
			if (d->GetCharacter()->GetGMLevel() == GM_PLAYER)
				d->GetCharacter()->ChatPacket(CHAT_TYPE_COMMAND, "quit Shutdown(SendDisconnectFunc)");
		}
	}
};

struct DisconnectFunc
{
	void operator () (LPDESC d)
	{
		if (d->GetType() == DESC_TYPE_CONNECTOR)
			return;

		if (d->IsPhase(PHASE_P2P))
			return;

		if (d->GetCharacter())
			d->GetCharacter()->Disconnect("Shutdown(DisconnectFunc)");

		d->SetPhase(PHASE_CLOSE);
	}
};

EVENTINFO(shutdown_event_data)
{
	int seconds;

	shutdown_event_data()
	: seconds( 0 )
	{
	}
};

EVENTFUNC(shutdown_event)
{
	shutdown_event_data* info = dynamic_cast<shutdown_event_data*>( event->info );

	if ( info == NULL )
	{
		sys_err( "shutdown_event> <Factor> Null pointer" );
		return 0;
	}

	int * pSec = & (info->seconds);

	if (*pSec < 0)
	{
		sys_log(0, "shutdown_event sec %d", *pSec);

		if (--*pSec == -10)
		{
			const DESC_MANAGER::DESC_SET & c_set_desc = DESC_MANAGER::instance().GetClientSet();
			std::for_each(c_set_desc.begin(), c_set_desc.end(), DisconnectFunc());
			return passes_per_sec;
		}
		else if (*pSec < -10)
			return 0;

		return passes_per_sec;
	}
	else if (*pSec == 0)
	{
		const DESC_MANAGER::DESC_SET & c_set_desc = DESC_MANAGER::instance().GetClientSet();
		std::for_each(c_set_desc.begin(), c_set_desc.end(), SendDisconnectFunc());
		g_bNoMoreClient = true;
		--*pSec;
		return passes_per_sec;
	}
	else
	{
		SendLocaleNotice(CHAT_TYPE_NOTICE, 0, 0, 288, "%d", *pSec);
		--*pSec;
		return passes_per_sec;
	}
}

void Shutdown(int iSec)
{
	if (g_bNoMoreClient)
	{
		thecore_shutdown();
		return;
	}

	CWarMapManager::instance().OnShutdown();

	SendLocaleNotice(CHAT_TYPE_NOTICE, 0, 0, 342, "%d", iSec);

	shutdown_event_data* info = AllocEventInfo<shutdown_event_data>();
	info->seconds = iSec;

	event_create(shutdown_event, info, 1);
}

ACMD(do_shutdown)
{
 	if (!ch)
		return;

	if (!ch->IsGM())
		return;

	TPacketGGShutdown p;
	p.bHeader = HEADER_GG_SHUTDOWN;
	P2P_MANAGER::instance().Send(&p, sizeof(TPacketGGShutdown));
	sys_err("Accept shutdown command from %s.", ch->GetName());
	Shutdown(10);
}

EVENTFUNC(timed_event)
{
	TimedEventInfo * info = dynamic_cast<TimedEventInfo *>( event->info );

	if ( info == NULL )
	{
		sys_err( "timed_event> <Factor> Null pointer" );
		return 0;
	}

	LPCHARACTER	ch = info->ch;
	if (ch == NULL)
	{
		return 0;
	}

	LPDESC d = ch->GetDesc();

	if (info->left_second <= 0)
	{
		ch->m_pkTimedEvent = NULL;

		switch (info->subcmd)
		{
			case SCMD_LOGOUT:
			case SCMD_QUIT:
			case SCMD_PHASE_SELECT:
				{
					TPacketNeedLoginLogInfo acc_info;
					acc_info.dwPlayerID = ch->GetDesc()->GetAccountTable().id;
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
					acc_info.bLanguage = ch->GetDesc()->GetAccountTable().bLanguage;
#endif

					db_clientdesc->DBPacket( HEADER_GD_VALID_LOGOUT, 0, &acc_info, sizeof(acc_info) );

					LogManager::instance().DetailLoginLog( false, ch );
				}
				break;
		}

		switch (info->subcmd)
		{
			case SCMD_LOGOUT:
				if (d)
					d->SetPhase(PHASE_CLOSE);
				break;

			case SCMD_QUIT:
				ch->ChatPacket(CHAT_TYPE_COMMAND, "quit");
				if (d)
					d->DelayedDisconnect(3);
				break;

			case SCMD_PHASE_SELECT:
				{
					ch->Disconnect("timed_event - SCMD_PHASE_SELECT");

					if (d)
					{
						d->SetPhase(PHASE_SELECT);
					}
				}
				break;
		}

		return 0;
	}
	else
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 288, "%d", info->left_second);
		--info->left_second;
	}

	return PASSES_PER_SEC(1);
}

#ifdef ENABLE_CHANGE_CHANNEL
EVENTFUNC(change_channel_event)
{
	ChangeChannelEventInfo * info = dynamic_cast<ChangeChannelEventInfo *>(event->info);

	if (info == NULL)
	{
		sys_err( "change_channel_event> <Factor> Null pointer" );
		return 0;
	}

	LPCHARACTER	ch = info->ch;
	if (ch == NULL)
	{
		return 0;
	}

	if (info->left_second <= 0)
	{
		ch->m_pkChangeChannelEvent = NULL;

		ch->ChangeChannel(info->channel_number);
	
		return 0;
	}
	else
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 289, "%d", info->left_second);
		--info->left_second;
	}

	return PASSES_PER_SEC(1);
}
#endif

ACMD(do_cmd)
{
	if (ch->m_pkTimedEvent)
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 290, "");
		event_cancel(&ch->m_pkTimedEvent);
		return;
	}

	switch (subcmd)
	{
		case SCMD_LOGOUT:
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 291, "");
			break;

		case SCMD_QUIT:
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 292, "");
			break;

		case SCMD_PHASE_SELECT:
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 293, "");
			break;
	}

	int nExitLimitTime = 10;

	if (ch->IsHack(false, true, nExitLimitTime) && (!ch->GetWarMap() || ch->GetWarMap()->GetType() == GUILD_WAR_TYPE_FLAG))
		return;

	switch (subcmd)
	{
		case SCMD_LOGOUT:
		case SCMD_QUIT:
		case SCMD_PHASE_SELECT:
			{
				TimedEventInfo* info = AllocEventInfo<TimedEventInfo>();

				{
					if (ch->IsPosition(POS_FIGHTING))
						info->left_second = 10;
					else
						info->left_second = 3;
				}

				info->ch = ch;
				info->subcmd = subcmd;
				strlcpy(info->szReason, argument, sizeof(info->szReason));

				ch->m_pkTimedEvent	= event_create(timed_event, info, 1);
			}
			break;
	}
}

ACMD(do_mount)
{
}

ACMD(do_fishing)
{
	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (!*arg1)
		return;

	char* endptr;
	double rotation = strtod(arg1, &endptr);
	if (*endptr != '\0' || errno == ERANGE)
		return;

	ch->SetRotation(rotation);
	ch->fishing();
}

ACMD(do_console)
{
	ch->ChatPacket(CHAT_TYPE_COMMAND, "ConsoleEnable");
}

ACMD(do_restart)
{
	if (false == ch->IsDead())
	{
		ch->ChatPacket(CHAT_TYPE_COMMAND, "CloseRestartWindow");
		ch->StartRecoveryEvent();
		return;
	}

	if (NULL == ch->m_pkDeadEvent)
		return;

	int iTimeToDead = (event_time(ch->m_pkDeadEvent) / passes_per_sec);

	if (subcmd != SCMD_RESTART_TOWN && (!ch->GetWarMap() || ch->GetWarMap()->GetType() == GUILD_WAR_TYPE_FLAG))
	{
		if (!test_server)
		{
			if (ch->IsHack())
			{
				ch->LocaleChatPacket(CHAT_TYPE_INFO, 294, "%d", iTimeToDead - (180 - g_nPortalLimitTime));
				return;
			}

			if (iTimeToDead > 170)
			{
				ch->LocaleChatPacket(CHAT_TYPE_INFO, 294, "%d", iTimeToDead - 170);
				return;
			}
		}
	}

	if (subcmd == SCMD_RESTART_TOWN)
	{
		if (ch->IsHack())
		{
			if ((!ch->GetWarMap() || ch->GetWarMap()->GetType() == GUILD_WAR_TYPE_FLAG))
			{
				ch->LocaleChatPacket(CHAT_TYPE_INFO, 294, "%d", iTimeToDead - (180 - g_nPortalLimitTime));
				return;
			}
		}

		if (iTimeToDead > 173)
		{
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 294, "%d", iTimeToDead - 170);
			return;
		}
	}

	ch->ChatPacket(CHAT_TYPE_COMMAND, "CloseRestartWindow");

	ch->GetDesc()->SetPhase(PHASE_GAME);
	ch->SetPosition(POS_STANDING);
	ch->StartRecoveryEvent();

	if (ch->GetDungeon())
		ch->GetDungeon()->UseRevive(ch);

	if (ch->GetWarMap() && !ch->IsObserverMode())
	{
		CWarMap * pMap = ch->GetWarMap();
		DWORD dwGuildOpponent = pMap ? pMap->GetGuildOpponent(ch) : 0;

		if (dwGuildOpponent)
		{
			switch (subcmd)
			{
				case SCMD_RESTART_TOWN:
					sys_log(0, "do_restart: restart town");
					PIXEL_POSITION pos;

					if (CWarMapManager::instance().GetStartPosition(ch->GetMapIndex(), ch->GetGuild()->GetID() < dwGuildOpponent ? 0 : 1, pos))
						ch->Show(ch->GetMapIndex(), pos.x, pos.y);
					else
						ch->ExitToSavedLocation();

					ch->PointChange(POINT_HP, ch->GetMaxHP() - ch->GetHP());
					ch->PointChange(POINT_SP, ch->GetMaxSP() - ch->GetSP());
					ch->ReviveInvisible(5);
#ifdef ENABLE_MOUNT_SYSTEM
					ch->CheckMount();
#endif
#ifdef ENABLE_PET_SYSTEM
					ch->CheckPet();
#endif
					break;

				case SCMD_RESTART_HERE:
					sys_log(0, "do_restart: restart here");
					ch->RestartAtSamePos();
					//ch->Show(ch->GetMapIndex(), ch->GetX(), ch->GetY());
					ch->PointChange(POINT_HP, ch->GetMaxHP() - ch->GetHP());
					ch->PointChange(POINT_SP, ch->GetMaxSP() - ch->GetSP());
					ch->ReviveInvisible(5);
#ifdef ENABLE_MOUNT_SYSTEM
					ch->CheckMount();
#endif
#ifdef ENABLE_PET_SYSTEM
					ch->CheckPet();
#endif
					break;
			}

			return;
		}
	}

	switch (subcmd)
	{
		case SCMD_RESTART_TOWN:
			sys_log(0, "do_restart: restart town");
			PIXEL_POSITION pos;

			if (SECTREE_MANAGER::instance().GetRecallPositionByEmpire(ch->GetMapIndex(), ch->GetEmpire(), pos))
				ch->WarpSet(pos.x, pos.y);
			else
				ch->WarpSet(EMPIRE_START_X(ch->GetEmpire()), EMPIRE_START_Y(ch->GetEmpire()));
			ch->PointChange(POINT_HP, 50 - ch->GetHP());
			ch->DeathPenalty(1);
			break;

		case SCMD_RESTART_HERE:
			sys_log(0, "do_restart: restart here");
			ch->RestartAtSamePos();
			//ch->Show(ch->GetMapIndex(), ch->GetX(), ch->GetY());
			ch->PointChange(POINT_HP, 50 - ch->GetHP());
			ch->DeathPenalty(0);
			ch->ReviveInvisible(5);
#ifdef ENABLE_MOUNT_SYSTEM
			ch->CheckMount();
#endif
#ifdef ENABLE_PET_SYSTEM
			ch->CheckPet();
#endif
			break;
	}
}

#define MAX_STAT 90

ACMD(do_stat_reset)
{
	ch->PointChange(POINT_STAT_RESET_COUNT, 12 - ch->GetPoint(POINT_STAT_RESET_COUNT));
}

ACMD(do_stat_minus) // Fix
{
	char arg1[256], arg2[256];
	two_arguments(argument, arg1, sizeof(arg1), arg2, sizeof(arg2));

	int vlaxc = 1;
	str_to_number(vlaxc, arg2);

	if (!*arg1 || vlaxc <= 0)
		return;

	if (ch->IsPolymorphed())
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 245, "");
		return;
	}

	if (ch->GetPoint(POINT_STAT_RESET_COUNT) <= 0)
		return;

	BYTE idx = 0;

	if (!strcmp(arg1, "st"))
	{
		if (ch->GetRealPoint(POINT_ST) <= JobInitialPoints[ch->GetJob()].st)
		{
			return;
		}
		idx = POINT_ST;
	}
	else if (!strcmp(arg1, "dx"))
	{
		if (ch->GetRealPoint(POINT_DX) <= JobInitialPoints[ch->GetJob()].dx)
		{
			return;
		}
		idx = POINT_DX;
	}
	else if (!strcmp(arg1, "ht"))
	{
		if (ch->GetRealPoint(POINT_HT) <= JobInitialPoints[ch->GetJob()].ht)
		{
			return;
		}
		idx = POINT_HT;
	}
	else if (!strcmp(arg1, "iq"))
	{
		if (ch->GetRealPoint(POINT_IQ) <= JobInitialPoints[ch->GetJob()].iq)
		{
			return;
		}
		idx = POINT_IQ;
	}
	else
		return;

	if (idx == 0)
		return;

	if (vlaxc > ch->GetPoint(POINT_STAT_RESET_COUNT))
		vlaxc = ch->GetPoint(POINT_STAT_RESET_COUNT);

	if (ch->GetRealPoint(idx) - vlaxc > MAX_STAT)
		vlaxc = MAX_STAT + ch->GetRealPoint(idx);

	ch->SetRealPoint(idx, ch->GetRealPoint(idx) - vlaxc);
	ch->SetPoint(idx, ch->GetPoint(idx) - vlaxc);
	ch->ComputePoints();
	ch->PointChange(idx, 0);

	if (idx == POINT_IQ)
		ch->PointChange(POINT_MAX_HP, 0);
	else if (idx == POINT_HT)
		ch->PointChange(POINT_MAX_SP, 0);

	ch->PointChange(POINT_STAT, + vlaxc);
	ch->PointChange(POINT_STAT_RESET_COUNT, - vlaxc);
	ch->ComputePoints();
}

ACMD(do_stat)
{
	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (!*arg1)
		return;

	if (ch->IsPolymorphed())
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 245, "");
		return;
	}

	if (ch->GetPoint(POINT_STAT) <= 0)
		return;

	BYTE idx = 0;

	if (!strcmp(arg1, "st"))
		idx = POINT_ST;
	else if (!strcmp(arg1, "dx"))
		idx = POINT_DX;
	else if (!strcmp(arg1, "ht"))
		idx = POINT_HT;
	else if (!strcmp(arg1, "iq"))
		idx = POINT_IQ;
	else
		return;

	if (ch->GetRealPoint(idx) >= MAX_STAT)
		return;

	ch->SetRealPoint(idx, ch->GetRealPoint(idx) + 1);
	ch->SetPoint(idx, ch->GetPoint(idx) + 1);
	ch->ComputePoints();
	ch->PointChange(idx, 0);

	if (idx == POINT_IQ)
	{
		ch->PointChange(POINT_MAX_HP, 0);
	}
	else if (idx == POINT_HT)
	{
		ch->PointChange(POINT_MAX_SP, 0);
	}

	ch->PointChange(POINT_STAT, -1);
	ch->ComputePoints();
}

ACMD(do_stat_val)
{
	char arg1[256], arg2[256];
	two_arguments(argument, arg1, sizeof(arg1), arg2, sizeof(arg2));

	int val = 0;
	str_to_number(val, arg2);

	if (!*arg1 || val <= 0)
		return;

	if (ch->IsPolymorphed())
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 245, "");
		return;
	}

	if (ch->GetPoint(POINT_STAT) <= 0)
		return;

	BYTE idx = 0;

	if (!strcmp(arg1, "st"))
		idx = POINT_ST;
	else if (!strcmp(arg1, "dx"))
		idx = POINT_DX;
	else if (!strcmp(arg1, "ht"))
		idx = POINT_HT;
	else if (!strcmp(arg1, "iq"))
		idx = POINT_IQ;
	else
		return;

	if (ch->GetRealPoint(idx) >= MAX_STAT)
		return;

	if (val > ch->GetPoint(POINT_STAT))
		val = ch->GetPoint(POINT_STAT);

	if (ch->GetRealPoint(idx) + val > MAX_STAT)
		val = MAX_STAT - ch->GetRealPoint(idx);

	ch->SetRealPoint(idx, ch->GetRealPoint(idx) + val);
	ch->SetPoint(idx, ch->GetPoint(idx) + val);
	ch->ComputePoints();
	ch->PointChange(idx, 0);

	if (idx == POINT_IQ)
		ch->PointChange(POINT_MAX_HP, 0);
	else if (idx == POINT_HT)
		ch->PointChange(POINT_MAX_SP, 0);

	ch->PointChange(POINT_STAT, -val);
	ch->ComputePoints();
}

ACMD(do_pvp)
{
	if (ch->GetArena() != NULL || CArenaManager::instance().IsArenaMap(ch->GetMapIndex()) == true)
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 192, "");
		return;
	}

	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	DWORD vid = 0;
	str_to_number(vid, arg1);
	LPCHARACTER pkVictim = CHARACTER_MANAGER::instance().Find(vid);

	if (!pkVictim)
		return;

	if (pkVictim->IsNPC())
		return;

#ifdef ENABLE_MESSENGER_BLOCK
	if (MessengerManager::Instance().IsBlocked(ch->GetName(), pkVictim->GetName()))
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 177, "%s", pkVictim->GetName());
		return;
	}
	else if (MessengerManager::Instance().IsBlocked(pkVictim->GetName(), ch->GetName()))
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 170, "%s", pkVictim->GetName());
		return;
	}
#endif

	if (pkVictim->GetArena() != NULL)
	{
		pkVictim->LocaleChatPacket(CHAT_TYPE_INFO, 296, "");
		return;
	}

	CPVPManager::instance().Insert(ch, pkVictim);
}

ACMD(do_guildskillup)
{
	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (!*arg1)
		return;

	if (!ch->GetGuild())
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 205, "");
		return;
	}

	CGuild* g = ch->GetGuild();
	TGuildMember* gm = g->GetMember(ch->GetPlayerID());
	if (gm->grade == GUILD_LEADER_GRADE)
	{
		DWORD vnum = 0;
		str_to_number(vnum, arg1);
		g->SkillLevelUp(vnum);
	}
	else
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 193, "");
	}
}

ACMD(do_skillup)
{
	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (!*arg1)
		return;

	DWORD vnum = 0;
	str_to_number(vnum, arg1);

	if (true == ch->CanUseSkill(vnum))
	{
		ch->SkillLevelUp(vnum);
	}
	else
	{
		switch(vnum)
		{
			case SKILL_HORSE_WILDATTACK:
			case SKILL_HORSE_CHARGE:
			case SKILL_HORSE_ESCAPE:
			case SKILL_HORSE_WILDATTACK_RANGE:

			case SKILL_7_A_ANTI_TANHWAN:
			case SKILL_7_B_ANTI_AMSEOP:
			case SKILL_7_C_ANTI_SWAERYUNG:
			case SKILL_7_D_ANTI_YONGBI:

			case SKILL_8_A_ANTI_GIGONGCHAM:
			case SKILL_8_B_ANTI_YEONSA:
			case SKILL_8_C_ANTI_MAHWAN:
			case SKILL_8_D_ANTI_BYEURAK:

			case SKILL_ADD_HP:
			case SKILL_RESIST_PENETRATE:
				ch->SkillLevelUp(vnum);
				break;
		}
	}
}

ACMD(do_safebox_close)
{
	ch->CloseSafebox();
}

ACMD(do_safebox_password)
{
	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));
	ch->ReqSafeboxLoad(arg1);
}

ACMD(do_safebox_change_password)
{
	char arg1[256];
	char arg2[256];

	two_arguments(argument, arg1, sizeof(arg1), arg2, sizeof(arg2));

	if (!*arg1 || strlen(arg1)>6)
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 48, "");
		return;
	}

	if (!*arg2 || strlen(arg2)>6)
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 48, "");
		return;
	}

	TSafeboxChangePasswordPacket p;

	p.dwID = ch->GetDesc()->GetAccountTable().id;
	strlcpy(p.szOldPassword, arg1, sizeof(p.szOldPassword));
	strlcpy(p.szNewPassword, arg2, sizeof(p.szNewPassword));

	db_clientdesc->DBPacket(HEADER_GD_SAFEBOX_CHANGE_PASSWORD, ch->GetDesc()->GetHandle(), &p, sizeof(p));
}

ACMD(do_mall_password)
{
	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (!*arg1 || strlen(arg1) > 6)
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 48, "");
		return;
	}

	int iPulse = thecore_pulse();

	if (ch->GetMall())
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 49, "");
		return;
	}

	if (iPulse - ch->GetMallLoadTime() < passes_per_sec * 10)
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 50, "");
		return;
	}

	ch->SetMallLoadTime(iPulse);

	TSafeboxLoadPacket p;
	p.dwID = ch->GetDesc()->GetAccountTable().id;
	strlcpy(p.szLogin, ch->GetDesc()->GetAccountTable().login, sizeof(p.szLogin));
	strlcpy(p.szPassword, arg1, sizeof(p.szPassword));

	db_clientdesc->DBPacket(HEADER_GD_MALL_LOAD, ch->GetDesc()->GetHandle(), &p, sizeof(p));
}

ACMD(do_mall_close)
{
	if (ch->GetMall())
	{
		ch->SetMallLoadTime(thecore_pulse());
		ch->CloseMall();
		ch->Save();
	}
}

#ifdef ENABLE_SPECIAL_INVENTORY
ACMD(do_new_safebox_open)
{
	if (!ch) return;
	if (ch->m_pkOpenSafeboxEvent) return;
	ch->SafeboxLoad();
}

ACMD(do_new_mall_open)
{
	if (!ch) return;
	if (ch->m_pkOpenMallEvent) return;
	ch->MallOpen();
}
#endif

ACMD(do_ungroup)
{
	if (!ch->GetParty())
		return;

	if (!CPartyManager::instance().IsEnablePCParty())
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 30, "");
		return;
	}

	if (ch->GetDungeon())
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 196, "");
		return;
	}

	LPPARTY pParty = ch->GetParty();

	if (pParty->GetMemberCount() == 2)
	{
		CPartyManager::instance().DeleteParty(pParty);
	}
	else
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 197, "");
		pParty->Quit(ch->GetPlayerID());
	}
}

ACMD(do_close_shop)
{
	if (ch->GetMyShop())
	{
		ch->CloseMyShop();
		return;
	}
}

ACMD(do_set_walk_mode)
{
	ch->SetNowWalking(true);
	ch->SetWalking(true);
}

ACMD(do_set_run_mode)
{
	ch->SetNowWalking(false);
	ch->SetWalking(false);
}

ACMD(do_war)
{
	CGuild * g = ch->GetGuild();

	if (!g)
		return;

	if (g->UnderAnyWar())
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 297, "");
		return;
	}

	char arg1[256], arg2[256];
	int type = GUILD_WAR_TYPE_FIELD;
	two_arguments(argument, arg1, sizeof(arg1), arg2, sizeof(arg2));

	if (!*arg1)
		return;


#ifdef ENABLE_WAR_CRASHER_PROTECTION_FIX
	if (*arg2)
	{
		str_to_number(type, arg2);

		if(type < 0)
		{
			ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("<error> can't declare war with type less than zero."));
			return;
		}

		if (type >= GUILD_WAR_TYPE_MAX_NUM || type == 0)
			type = GUILD_WAR_TYPE_FIELD;
	}
#else
	if (*arg2)
	{
		str_to_number(type, arg2);

		if (type >= GUILD_WAR_TYPE_MAX_NUM || type < 0)
			type = GUILD_WAR_TYPE_FIELD;
	}
#endif

	DWORD gm_pid = g->GetMasterPID();

	if (gm_pid != ch->GetPlayerID())
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 298, "");
		return;
	}

	CGuild * opp_g = CGuildManager::instance().FindGuildByName(arg1);

	if (!opp_g)
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 299, "");
		return;
	}

	switch (g->GetGuildWarState(opp_g->GetID()))
	{
		case GUILD_WAR_NONE:
			{
				if (opp_g->UnderAnyWar())
				{
					ch->LocaleChatPacket(CHAT_TYPE_INFO, 300, "");
					return;
				}

				int iWarPrice = KOR_aGuildWarInfo[type].iWarPrice;

				if (g->GetGuildMoney() < iWarPrice)
				{
					ch->LocaleChatPacket(CHAT_TYPE_INFO, 218, "");
					return;
				}

				if (opp_g->GetGuildMoney() < iWarPrice)
				{
					ch->LocaleChatPacket(CHAT_TYPE_INFO, 218, "");
					return;
				}
			}
			break;

		case GUILD_WAR_SEND_DECLARE:
			{
				ch->LocaleChatPacket(CHAT_TYPE_INFO, 300, "");
				return;
			}
			break;

		case GUILD_WAR_RECV_DECLARE:
			{
				if (opp_g->UnderAnyWar())
				{
					ch->LocaleChatPacket(CHAT_TYPE_INFO, 300, "");
					g->RequestRefuseWar(opp_g->GetID());
					return;
				}
			}
			break;

		case GUILD_WAR_RESERVE:
			{
				ch->LocaleChatPacket(CHAT_TYPE_INFO, 301, "");
				return;
			}
			break;

		case GUILD_WAR_END:
			return;

		default:
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 300, "");
			g->RequestRefuseWar(opp_g->GetID());
			return;
	}

	if (!g->CanStartWar(type))
	{
		if (g->GetLadderPoint() == 0)
		{
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 302, "");
			sys_log(0, "GuildWar.StartError.NEED_LADDER_POINT");
		}
		else if (g->GetMemberCount() < GUILD_WAR_MIN_MEMBER_COUNT)
		{
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 303, "%d", GUILD_WAR_MIN_MEMBER_COUNT);
			sys_log(0, "GuildWar.StartError.NEED_MINIMUM_MEMBER[%d]", GUILD_WAR_MIN_MEMBER_COUNT);
		}
		else
		{
			sys_log(0, "GuildWar.StartError.UNKNOWN_ERROR");
		}
		return;
	}

	if (!opp_g->CanStartWar(GUILD_WAR_TYPE_FIELD))
	{
		if (opp_g->GetLadderPoint() == 0)
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 304, "");
		else if (opp_g->GetMemberCount() < GUILD_WAR_MIN_MEMBER_COUNT)
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 305, "");
		return;
	}

	do
	{
		if (g->GetMasterCharacter() != NULL)
			break;

		CCI *pCCI = P2P_MANAGER::instance().FindByPID(g->GetMasterPID());

		if (pCCI != NULL)
			break;

		ch->LocaleChatPacket(CHAT_TYPE_INFO, 306, "");
		g->RequestRefuseWar(opp_g->GetID());
		return;

	} while (false);

	do
	{
		if (opp_g->GetMasterCharacter() != NULL)
			break;

		CCI *pCCI = P2P_MANAGER::instance().FindByPID(opp_g->GetMasterPID());

		if (pCCI != NULL)
			break;

		ch->LocaleChatPacket(CHAT_TYPE_INFO, 306, "");
		g->RequestRefuseWar(opp_g->GetID());
		return;

	} while (false);

	g->RequestDeclareWar(opp_g->GetID(), type);
}

ACMD(do_nowar)
{
	CGuild* g = ch->GetGuild();
	if (!g)
		return;

	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (!*arg1)
		return;

	DWORD gm_pid = g->GetMasterPID();

	if (gm_pid != ch->GetPlayerID())
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 298, "");
		return;
	}

	CGuild* opp_g = CGuildManager::instance().FindGuildByName(arg1);

	if (!opp_g)
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 299, "");
		return;
	}

	g->RequestRefuseWar(opp_g->GetID());
}

ACMD(do_detaillog)
{
	ch->DetailLog();
}

ACMD(do_monsterlog)
{
	ch->ToggleMonsterLog();
}

ACMD(do_pkmode)
{
	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (!*arg1)
		return;

	BYTE mode = 0;
	str_to_number(mode, arg1);

	if (mode == PK_MODE_PROTECT)
		return;

	if (ch->GetLevel() < PK_PROTECT_LEVEL && mode != 0)
		return;

	ch->SetPKMode(mode);
}

ACMD(do_messenger_auth)
{
	if (ch->GetArena())
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 192, "");
		return;
	}

	char arg1[256], arg2[256];
	two_arguments(argument, arg1, sizeof(arg1), arg2, sizeof(arg2));

	if (!*arg1 || !*arg2)
		return;

	char answer = LOWER(*arg1);
	
	if (!MessengerManager::instance().AuthToAdd(ch->GetName(), arg2, answer == 'y' ? false : true))
		return;

	if (answer != 'y')
	{
		LPCHARACTER tch = CHARACTER_MANAGER::instance().FindPC(arg2);

		if (tch)
			tch->LocaleChatPacket(CHAT_TYPE_INFO, 307, "%s", ch->GetName());
#ifdef ENABLE_CROSS_CHANNEL_REQUESTS
		else
		{
			CCI* pkCCI = P2P_MANAGER::Instance().Find(arg2);
			if (pkCCI)
			{
				LPDESC pkDesc = pkCCI->pkDesc;
				pkDesc->SetRelay(arg2);
				pkDesc->LocaleChatPacket(CHAT_TYPE_INFO, 307, "%s", ch->GetName());
				pkDesc->SetRelay("");
			}
		}
#endif
	}
}

ACMD(do_setblockmode)
{
	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (*arg1)
	{
		BYTE flag = 0;
		str_to_number(flag, arg1);
		ch->SetBlockMode(flag);
	}
}

ACMD(do_unmount)
{
#ifdef ENABLE_MOUNT_SYSTEM
	if(ch->GetWear(WEAR_MOUNT))
	{
		CMountSystem* mountSystem = ch->GetMountSystem();
		LPITEM mount = ch->GetWear(WEAR_MOUNT);
#ifdef ENABLE_MOUNT_PET_SKIN
		LPITEM mountSkinItem = ch->GetWear(WEAR_COSTUME_MOUNT);
#endif

		if (!mountSystem && !mount)
			return;

#ifdef ENABLE_MOUNT_PET_SKIN
		DWORD mobVnum = mountSkinItem ? mountSkinItem->GetValue(1) : mount->GetValue(1);
#else
		DWORD mobVnum = mount->GetValue(1);
#endif

		if (ch->GetMountVnum())
		{
			if(mountSystem->CountSummoned() == 0)
			{
				mountSystem->Unmount(mobVnum);
			}
		}
		return;
	}

	LPITEM item = ch->GetWear(WEAR_UNIQUE1);
	LPITEM item2 = ch->GetWear(WEAR_UNIQUE2);
	LPITEM item3 = ch->GetWear(WEAR_MOUNT);

	if (item && item->IsRideItem())
		ch->UnequipItem(item);

	if (item2 && item2->IsRideItem())
		ch->UnequipItem(item2);

	if (item3 && item3->IsRideItem())
		ch->UnequipItem(item3);
#endif

	if (true == ch->UnEquipSpecialRideUniqueItem())
	{
		ch->RemoveAffect(AFFECT_MOUNT);
		ch->RemoveAffect(AFFECT_MOUNT_BONUS);

		if (ch->IsHorseRiding())
		{
			ch->StopRiding();
		}
	}
	else
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 191, "");
	}
}

ACMD(do_observer_exit)
{
	if (ch->IsObserverMode())
	{
		if (ch->GetWarMap())
			ch->SetWarMap(NULL);

		if (ch->GetArena() != NULL || ch->GetArenaObserverMode() == true)
		{
			ch->SetArenaObserverMode(false);

			if (ch->GetArena() != NULL)
				ch->GetArena()->RemoveObserver(ch->GetPlayerID());

			ch->SetArena(NULL);
			ch->WarpSet(ARENA_RETURN_POINT_X(ch->GetEmpire()), ARENA_RETURN_POINT_Y(ch->GetEmpire()));
		}
		else
		{
			ch->ExitToSavedLocation();
		}
		ch->SetObserverMode(false);
	}
}

ACMD(do_view_equip)
{
	if (ch->GetGMLevel() <= GM_PLAYER)
		return;

	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (*arg1)
	{
		DWORD vid = 0;
		str_to_number(vid, arg1);
		LPCHARACTER tch = CHARACTER_MANAGER::instance().Find(vid);

		if (!tch)
			return;

		if (!tch->IsPC())
			return;

#ifdef ENABLE_MESSENGER_BLOCK
		if (MessengerManager::Instance().IsBlocked(ch->GetName(), tch->GetName()))
		{
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 177, "%s", tch->GetName());
			return;
		}
		else if (MessengerManager::Instance().IsBlocked(tch->GetName(), ch->GetName()))
		{
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 170, "%s", tch->GetName());
			return;
		}
#endif

		tch->SendEquipment(ch);
	}
}

ACMD(do_party_request)
{
	if (ch->GetArena())
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 192, "");
		return;
	}

	if (ch->GetParty())
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 308, "");
		return;
	}

	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (!*arg1)
		return;

	DWORD vid = 0;
	str_to_number(vid, arg1);
	LPCHARACTER tch = CHARACTER_MANAGER::instance().Find(vid);

	if (tch)
		if (!ch->RequestToParty(tch))
			ch->ChatPacket(CHAT_TYPE_COMMAND, "PartyRequestDenied");
}

ACMD(do_party_request_accept)
{
	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (!*arg1)
		return;

	DWORD vid = 0;
	str_to_number(vid, arg1);
	LPCHARACTER tch = CHARACTER_MANAGER::instance().Find(vid);

	if (tch)
		ch->AcceptToParty(tch);
}

ACMD(do_party_request_deny)
{
	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (!*arg1)
		return;

	DWORD vid = 0;
	str_to_number(vid, arg1);
	LPCHARACTER tch = CHARACTER_MANAGER::instance().Find(vid);

	if (tch)
		ch->DenyToParty(tch);
}

struct GotoInfo
{
	std::string st_name;

	BYTE empire;
	int mapIndex;
	DWORD x, y;

	GotoInfo()
	{
		st_name = "";
		empire = 0;
		mapIndex = 0;

		x = 0;
		y = 0;
	}

	GotoInfo(const GotoInfo& c_src)
	{
		__copy__(c_src);
	}

	void operator = (const GotoInfo& c_src)
	{
		__copy__(c_src);
	}

	void __copy__(const GotoInfo& c_src)
	{
		st_name = c_src.st_name;
		empire = c_src.empire;
		mapIndex = c_src.mapIndex;

		x = c_src.x;
		y = c_src.y;
	}
};

extern void BroadcastNotice(const char * c_pszBuf);

static const char* FN_point_string(int apply_number)
{
	switch (apply_number)
	{
		case POINT_MAX_HP:							return "Hit Points +%d";
		case POINT_MAX_SP:							return "Spell Points +%d";
		case POINT_HT:								return "Endurance +%d";
		case POINT_IQ:								return "Intelligence +%d";
		case POINT_ST:								return "Strength +%d";
		case POINT_DX:								return "Dexterity +%d";
		case POINT_ATT_SPEED:						return "Attack Speed +%d";
		case POINT_MOV_SPEED:						return "Movement Speed %d";
		case POINT_CASTING_SPEED:					return "Cooldown Time -%d";
		case POINT_HP_REGEN:						return "Energy Recovery +%d";
		case POINT_SP_REGEN:						return "Spell Point Recovery +%d";
		case POINT_POISON_PCT:						return "Poison Attack %d";
		case POINT_STUN_PCT:						return "Star +%d";
		case POINT_SLOW_PCT:						return "Speed Reduction +%d";
		case POINT_CRITICAL_PCT:					return "Critical Attack with a chance of %d%%";
		case POINT_RESIST_CRITICAL:					return "Critical Resistance %d%%";
		case POINT_PENETRATE_PCT:					return "Chance of a Speared Attack of %d%%";
		case POINT_RESIST_PENETRATE:				return "Penetrate Resistance %d%%";
		case POINT_ATTBONUS_HUMAN:					return "Player's Attack Power against Monsters +%d%%";
		case POINT_ATTBONUS_ANIMAL:					return "Horse's Attack Power against Monsters +%d%%";
		case POINT_ATTBONUS_ORC:					return "Attack Boost against Wonggui + %d%%";
		case POINT_ATTBONUS_MILGYO:					return "Attack Boost against Milgyo + %d%%";
		case POINT_ATTBONUS_UNDEAD:					return "Attack boost against zombies + %d%%";
		case POINT_ATTBONUS_DEVIL:					return "Attack boost against devils + %d%%";
		case POINT_STEAL_HP:						return "Absorbing of Energy %d%% while attacking.";
		case POINT_STEAL_SP:						return "Absorption of Spell Points (SP) %d%% while attacking.";
		case POINT_MANA_BURN_PCT:					return "With a chance of %d%% Spell Points (SP) will be taken from the enemy.";
		case POINT_DAMAGE_SP_RECOVER:				return "Absorbing of Spell Points (SP) with a chance of %d%%";
		case POINT_BLOCK:							return "%d%% Chance of blocking a close-combat attack";
		case POINT_DODGE:							return "%d%% Chance of blocking a long range attack";
		case POINT_RESIST_SWORD:					return "One-Handed Sword defence %d%%";
		case POINT_RESIST_TWOHAND:					return "Two-Handed Sword Defence %d%%";
		case POINT_RESIST_DAGGER:					return "Two-Handed Sword Defence %d%%";
		case POINT_RESIST_BELL:						return "Bell Defence %d%%";
		case POINT_RESIST_FAN:						return "Fan Defence %d%%";
		case POINT_RESIST_BOW:						return "Distant Attack Resistance %d%%";
		case POINT_RESIST_FIRE:						return "Fire Resistance %d%%";
		case POINT_RESIST_ELEC:						return "Lightning Resistance %d%%";
		case POINT_RESIST_MAGIC:					return "Magic Resistance %d%%";
		case POINT_RESIST_WIND:						return "Wind Resistance %d%%";
		case POINT_RESIST_ICE:						return "Ice Resistance %d%%";
		case POINT_RESIST_EARTH:					return "Earth Resistance %d%%";
		case POINT_RESIST_DARK:						return "Dark Resistance %d%%";
		case POINT_REFLECT_MELEE:					return "Reflect Direct Hit: %d%%";
		case POINT_REFLECT_CURSE:					return "Reflect Curse: %d%%";
		case POINT_POISON_REDUCE:					return "Poison Resistance %d%%";
		case POINT_KILL_SP_RECOVER:					return "Spell Points (SP) will be increased by %d%% if you win.";
		case POINT_EXP_DOUBLE_BONUS:				return "Experience increases by %d%% if you win against an opponent.";
		case POINT_GOLD_DOUBLE_BONUS:				return "Increase of Yang up to %d%% if you win.";
		case POINT_ITEM_DROP_BONUS:					return "Increase of captured Items up to %d%% if you win.";
		case POINT_POTION_BONUS:					return "Power increase of up to %d%% after taking the potion.";
		case POINT_KILL_HP_RECOVERY:				return "%d%% Chance of filling up Hit Points after a victory.";
		case POINT_ATT_GRADE_BONUS:					return "Attack Power + %d";
		case POINT_DEF_GRADE_BONUS:					return "Armour + %d";
		case POINT_MAGIC_ATT_GRADE:					return "Magical Attack + %d";
		case POINT_MAGIC_DEF_GRADE:					return "Magical Defence + %d";
		case POINT_MAX_STAMINA:						return "Maximum Endurance + %d";
		case POINT_ATTBONUS_WARRIOR:				return "Strong against Warriors + %d%%";
		case POINT_ATTBONUS_ASSASSIN:				return "Strong against Ninjas + %d%%";
		case POINT_ATTBONUS_SURA:					return "Strong against Sura + %d%%";
		case POINT_ATTBONUS_SHAMAN:					return "Strong against Shamans + %d%%";
		case POINT_ATTBONUS_MONSTER:				return "Strength against monsters + %d%%";
		case POINT_MALL_ATTBONUS:					return "Attack + %d%%";
		case POINT_MALL_DEFBONUS:					return "Defence + %d%%";
		case POINT_MALL_EXPBONUS:					return "Experience %d%%";
		case POINT_MALL_ITEMBONUS:					return "Chance to find an Item %. 1f";
		case POINT_MALL_GOLDBONUS:					return "Chance to find Yang %. 1f";
		case POINT_MAX_HP_PCT:						return "Maximum Energy +%d%%";
		case POINT_MAX_SP_PCT:						return "Maximum Energy +%d%%";
		case POINT_SKILL_DAMAGE_BONUS:				return "Skill Damage %d%%";
		case POINT_NORMAL_HIT_DAMAGE_BONUS:			return "Hit Damage %d%%";
		case POINT_SKILL_DEFEND_BONUS:				return "Resistance against Skill Damage %d%%";
		case POINT_NORMAL_HIT_DEFEND_BONUS:			return "Resistance against Hits %d%%";
		case POINT_RESIST_WARRIOR:					return "%d%% Resistance against Warrior Attacks";
		case POINT_RESIST_ASSASSIN:					return "%d%% Resistance against Ninja Attacks";
		case POINT_RESIST_SURA:						return "%d%% Resistance against Sura Attacks";
		case POINT_RESIST_SHAMAN:					return "%d%% Resistance against Shaman Attacks";
#ifdef ENABLE_PENDANT_SYSTEM
		case POINT_ATTBONUS_ELEC:					return "Strong against Elec + %d%%";
		case POINT_ATTBONUS_FIRE:					return "Strong against Fire + %d%%";
		case POINT_ATTBONUS_ICE:					return "Strong against Ice + %d%%";
		case POINT_ATTBONUS_WIND:					return "Strong against Wind + %d%%";
		case POINT_ATTBONUS_EARTH:					return "Strong against Earth + %d%%";
		case POINT_ATTBONUS_DARK:					return "Strong against Dark + %d%%";
#endif
#ifdef ENABLE_ATTBONUS_METIN
		case POINT_ATTBONUS_METIN:					return "Strong against Metin Stones + %d%%";
#endif
#ifdef ENABLE_ATTBONUS_BOSS
		case POINT_ATTBONUS_BOSS:					return "Strong against Boss + %d%%";
#endif
		default:									return NULL;
	}
}

static bool FN_hair_affect_string(LPCHARACTER ch, char *buf, size_t bufsiz)
{
	if (NULL == ch || NULL == buf)
		return false;

	CAffect* aff = NULL;
	time_t expire = 0;
	struct tm ltm;
	int	year, mon, day;
	int	offset = 0;

	aff = ch->FindAffect(AFFECT_HAIR);

	if (NULL == aff)
		return false;

	expire = ch->GetQuestFlag("hair.limit_time");

	if (expire < get_global_time())
		return false;

	offset = snprintf(buf, bufsiz, FN_point_string(aff->bApplyOn), aff->lApplyValue);

	if (offset < 0 || offset >= (int) bufsiz)
		offset = bufsiz - 1;

	localtime_r(&expire, &ltm);

	year = ltm.tm_year + 1900;
	mon = ltm.tm_mon + 1;
	day = ltm.tm_mday;

	snprintf(buf + offset, bufsiz - offset, "(Procedure: %d y- %d m - %d d)", year, mon, day);

	return true;
}

ACMD(do_hair)
{
	char buf[256];

	if (false == FN_hair_affect_string(ch, buf, sizeof(buf)))
		return;

	ch->ChatPacket(CHAT_TYPE_INFO, buf);
}

ACMD(do_inventory)
{
	int	index = 0;
	int	count = 1;

	char arg1[256];
	char arg2[256];

	LPITEM	item;

	two_arguments(argument, arg1, sizeof(arg1), arg2, sizeof(arg2));

	if (!*arg1)
	{
		ch->ChatPacket(CHAT_TYPE_INFO, "Usage: inventory <start_index> <count>");
		return;
	}

	if (!*arg2)
	{
		index = 0;
		str_to_number(count, arg1);
	}
	else
	{
		str_to_number(index, arg1); index = MIN(index, INVENTORY_MAX_NUM);
		str_to_number(count, arg2); count = MIN(count, INVENTORY_MAX_NUM);
	}

	for (int i = 0; i < count; ++i)
	{
		if (index >= INVENTORY_MAX_NUM)
			break;

		item = ch->GetInventoryItem(index);

		ch->ChatPacket(CHAT_TYPE_INFO, "inventory [%d] = %s", index, item ? item->GetLocaleName() : "<NONE>");
		++index;
	}
}

ACMD(do_gift)
{
	ch->ChatPacket(CHAT_TYPE_COMMAND, "gift");
}

ACMD(do_cube)
{
#ifndef ENABLE_RENEWAL_CUBE
	if (!ch->CanDoCube())
		return;

	int cube_index = 0, inven_index = 0;
#endif

	const char *line;
	char arg1[256], arg2[256], arg3[256];
	line = two_arguments(argument, arg1, sizeof(arg1), arg2, sizeof(arg2));
	one_argument(line, arg3, sizeof(arg3));

	if (0 == arg1[0])
	{
#ifndef ENABLE_RENEWAL_CUBE
		ch->ChatPacket(CHAT_TYPE_INFO, "Usage: cube open");
		ch->ChatPacket(CHAT_TYPE_INFO, "       cube close");
		ch->ChatPacket(CHAT_TYPE_INFO, "       cube add <inveltory_index>");
		ch->ChatPacket(CHAT_TYPE_INFO, "       cube delete <cube_index>");
		ch->ChatPacket(CHAT_TYPE_INFO, "       cube list");
		ch->ChatPacket(CHAT_TYPE_INFO, "       cube cancel");
		ch->ChatPacket(CHAT_TYPE_INFO, "       cube make [all]");
#endif
		return;
	}

#ifndef ENABLE_RENEWAL_CUBE
	const std::string& strArg1 = std::string(arg1);

	if (strArg1 == "r_info")
	{
		if (0 == arg2[0])
			Cube_request_result_list(ch);
		else
		{
			if (isdigit(*arg2))
			{
				int listIndex = 0, requestCount = 1;
				str_to_number(listIndex, arg2);

				if (0 != arg3[0] && isdigit(*arg3))
					str_to_number(requestCount, arg3);

				Cube_request_material_info(ch, listIndex, requestCount);
			}
		}

		return;
	}
#endif

	switch (LOWER(arg1[0]))
	{
		case 'o':
			Cube_open(ch);
			break;

#ifndef ENABLE_RENEWAL_CUBE
		case 'c':
			Cube_close(ch);
			break;

		case 'l':
			Cube_show_list(ch);
			break;

		case 'a':
			{
				if (0 == arg2[0] || !isdigit(*arg2) || 0 == arg3[0] || !isdigit(*arg3))
					return;

				str_to_number(cube_index, arg2);
				str_to_number(inven_index, arg3);
				Cube_add_item (ch, cube_index, inven_index);
			}
			break;

		case 'd':
			{
				if (0 == arg2[0] || !isdigit(*arg2))
					return;

				str_to_number(cube_index, arg2);
				Cube_delete_item (ch, cube_index);
			}
			break;

		case 'm':
			Cube_make(ch);
			break;
#endif

		default:
			return;
	}
}

ACMD(do_in_game_mall)
{
	char buf[512+1];
	char sas[33];
	MD5_CTX ctx;
	const char sas_key[] = "GF9001";

	char language[3];

#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
	if (ch->GetDesc() != NULL)
		strlcpy(language, get_locale(ch->GetLanguage()), sizeof(language));
	else
		strlcpy(language, "en", sizeof(language));
#else
	strlcpy(language, "en", sizeof(language));
#endif

	snprintf(buf, sizeof(buf), "%u%u%s", ch->GetPlayerID(), ch->GetAID(), sas_key);

	MD5Init(&ctx);
	MD5Update(&ctx, (const unsigned char *) buf, strlen(buf));
#ifdef __FreeBSD__
	MD5End(&ctx, sas);
#else
	static const char hex[] = "0123456789abcdef";
	unsigned char digest[16];
	MD5Final(digest, &ctx);
	int i;
	for (i = 0; i < 16; ++i) {
		sas[i+i] = hex[digest[i] >> 4];
		sas[i+i+1] = hex[digest[i] & 0x0f];
	}
	sas[i+i] = '\0';
#endif

	snprintf(buf, sizeof(buf), "mall https://www.%s/shop?pid=%u&lang=%s&sid=%d&sas=%s", g_strWebMallURL.c_str(), ch->GetPlayerID(), language, g_server_id, sas);

	ch->ChatPacket(CHAT_TYPE_COMMAND, buf);
}

ACMD(do_dice)
{
	char arg1[256], arg2[256];
	int start = 1, end = 100;

	two_arguments(argument, arg1, sizeof(arg1), arg2, sizeof(arg2));

	if (*arg1 && *arg2)
	{
		char* endptr1, *endptr2;
		errno = 0;
		long val1 = strtol(arg1, &endptr1, 10);
		long val2 = strtol(arg2, &endptr2, 10);
		
		if (*endptr1 != '\0' || *endptr2 != '\0' || errno == ERANGE)
			return;
		
		if (val1 < INT_MIN || val1 > INT_MAX || val2 < INT_MIN || val2 > INT_MAX)
			return;
		
		start = (int)val1;
		end = (int)val2;
	}
	else if (*arg1 && !*arg2)
	{
		char* endptr;
		errno = 0;
		long val = strtol(arg1, &endptr, 10);
		
		if (*endptr != '\0' || errno == ERANGE)
			return;
		
		if (val < INT_MIN || val > INT_MAX)
			return;
		
		start = 1;
		end = (int)val;
	}

	end = MAX(start, end);
	start = MIN(start, end);

	int n = number(start, end);

#ifdef ENABLE_DICE_SYSTEM
	if (ch->GetParty())
		ch->GetParty()->ChatPacketToAllMember(CHAT_TYPE_DICE_INFO, 309, "%s#%d#%d#%d", ch->GetName(), n, start, end);
	else
		ch->LocaleChatPacket(CHAT_TYPE_DICE_INFO, 310, "%d#%d#%d", n, start, end);
#else
	if (ch->GetParty())
		ch->GetParty()->ChatPacketToAllMember(CHAT_TYPE_INFO, 309, "%s#%d#%d#%d", ch->GetName(), n, start, end);
	else
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 310, "%d#%d#%d", n, start, end);
#endif
}

ACMD(do_click_safebox)
{
	if ((ch->GetGMLevel() <= GM_PLAYER) && (ch->GetDungeon() || ch->GetWarMap()))
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 311, "");
		return;
	}

	ch->SetSafeboxOpenPosition();
	ch->ChatPacket(CHAT_TYPE_COMMAND, "ShowMeSafeboxPassword");
}

ACMD(do_click_mall)
{
	ch->ChatPacket(CHAT_TYPE_COMMAND, "ShowMeMallPassword");
}

ACMD(do_ride)
{
    if (ch->IsDead() || ch->IsStun() || ch->IsPolymorphed())
	return;

    int CalcLastAttackSec = (get_dword_time() - ch->GetLastAttackedTime()) / 1000 + 0.5;

    if (CalcLastAttackSec < 10)
    {
        ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("You have to wait a few seconds after being attacked!"));
        return;
    }

	if (ch->GetMapIndex() == 113)
		return;

#ifdef ENABLE_MOUNT_SYSTEM
	if (ch->IsPolymorphed() == true)
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 62, "");
		return;
	}

	if(ch->GetWear(WEAR_MOUNT))
	{
		CMountSystem* mountSystem = ch->GetMountSystem();
		LPITEM mount = ch->GetWear(WEAR_MOUNT);
#ifdef ENABLE_MOUNT_PET_SKIN
		LPITEM mountSkinItem = ch->GetWear(WEAR_COSTUME_MOUNT);
#endif

		if (!mountSystem && !mount)
			return;

#ifdef ENABLE_MOUNT_PET_SKIN
		DWORD mobVnum = mountSkinItem ? mountSkinItem->GetValue(1) : mount->GetValue(1);
#else
		DWORD mobVnum = mount->GetValue(1);
#endif

		if (ch->GetMountVnum())
		{
			if(mountSystem->CountSummoned() == 0)
			{
				mountSystem->Unmount(mobVnum);
			}
		}
		else
		{
			if(mountSystem->CountSummoned() == 1)
			{
				mountSystem->Mount(mobVnum, mount);
			}
		}
		
		return;
	}
#endif

	if (ch->IsHorseRiding())
	{
		ch->StopRiding();
		return;
	}

	if (ch->GetHorse() != NULL)
	{
		ch->StartRiding();
		return;
	}

	for (BYTE i=0; i<INVENTORY_MAX_NUM; ++i)
	{
		LPITEM item = ch->GetInventoryItem(i);
		if (NULL == item)
			continue;

		if (item->GetType() == ITEM_MOUNT)
		{
			ch->UseItem(TItemPos (INVENTORY, i));
			return;
		}
	}

	ch->LocaleChatPacket(CHAT_TYPE_INFO, 283, "");
}

#ifdef ENABLE_CHANGE_CHANNEL
ACMD(do_change_channel)
{
	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	DWORD channel_number = 0;
	str_to_number(channel_number, arg1);

	if (!ch)
	{
		return;
	}

	if (channel_number == 99 || g_bChannel == 99)
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 61, "");
		return;
	}

	if (channel_number == g_bChannel)
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 312, "");
		return;
	}

	if (ch->IsDead() || !ch->CanWarp())
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 313, "");
		return;
	}

	if (channel_number <= 0 || channel_number > 6)
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 314, "");
		return;
	}

	if (channel_number != 0)
	{
		if (ch->m_pkChangeChannelEvent)
		{
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 315, "");
			event_cancel(&ch->m_pkChangeChannelEvent);
			return;
		}

		ChangeChannelEventInfo* info = AllocEventInfo<ChangeChannelEventInfo>();

		{
			if (ch->IsPosition(POS_FIGHTING))
				info->left_second = 10;
			else
				info->left_second = 3;
		}

		info->ch = ch;
		info->channel_number = channel_number;

		ch->m_pkChangeChannelEvent = event_create(change_channel_event, info, 1);
	}
}
#endif

#ifdef ENABLE_SORT_INVENTORY
bool sortByType(CItem* a, CItem* b)
{
	return (a->GetType() < b->GetType());
}

bool sortBySubType(CItem* a, CItem* b)
{
	return (a->GetSubType() < b->GetSubType());
}

bool sortByVnum(CItem* a, CItem* b)
{
	return (a->GetVnum() < b->GetVnum());
}

bool sortBySocket(CItem* a, CItem* b)
{
	return (a->GetSocket(0) < b->GetSocket(0));
}

ACMD(do_sort_items)
{
	if (ch->IsDead())
		return;

	if (ch->GetExchange() || ch->GetShopOwner() || ch->GetMyShop() || ch->IsOpenSafebox() || ch->IsCubeOpen())
		return;

	int lastSortInventoryPulse = ch->GetSortInventoryPulse();
	int currentPulse = thecore_pulse();

	if (lastSortInventoryPulse > currentPulse)
	{
		int deltaInSeconds = ((lastSortInventoryPulse / PASSES_PER_SEC(1)) - (currentPulse / PASSES_PER_SEC(1)));
		int minutes = deltaInSeconds / 60;
		int seconds = (deltaInSeconds - (minutes * 60));
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 316, "%d", seconds);
		return;
	}

#ifdef ENABLE_INVENTORY_EXPANSION_SYSTEM
	int UNLOCK_SLOTS = 90+(5*ch->GetUnlockSlotsW());
	for (int i = 0; i < UNLOCK_SLOTS; ++i)
#else
	for (int i = 0; i < INVENTORY_MAX_NUM; ++i)
#endif
	{
		LPITEM item = ch->GetInventoryItem(i);

		if(!item)
			continue;

		if(item->isLocked())
			continue;

		if(item->GetCount() == ITEM_MAX_COUNT)
			continue;

		if (item->IsStackable() && !IS_SET(item->GetAntiFlag(), ITEM_ANTIFLAG_STACK))
		{
#ifdef ENABLE_INVENTORY_EXPANSION_SYSTEM
			int UNLOCK_SLOTS = 90+(5*ch->GetUnlockSlotsW());
			for (int j = i; j < UNLOCK_SLOTS; ++j)
#else
			for (int j = i; j < INVENTORY_MAX_NUM; ++j)
#endif
			{
				LPITEM item2 = ch->GetInventoryItem(j);

				if(!item2)
					continue;

				if(item2->isLocked())
					continue;

				if (item2->GetVnum() == item->GetVnum())
				{
					bool bStopSockets = false;

					for (int k = 0; k < ITEM_SOCKET_MAX_NUM; ++k)
					{
						if (item2->GetSocket(k) != item->GetSocket(k))
						{
							bStopSockets = true;
							break;
						}
					}

					if(bStopSockets)
						continue;

#ifdef ENABLE_STACK_LIMIT
					WORD bAddCount = MIN(ITEM_MAX_COUNT - item->GetCount(), item2->GetCount());
#else
					BYTE bAddCount = MIN(ITEM_MAX_COUNT - item->GetCount(), item2->GetCount());
#endif

					item->SetCount(item->GetCount() + bAddCount);
					item2->SetCount(item2->GetCount() - bAddCount);
					continue;
				}
			}
		}
	}

	ch->SetNextSortInventoryPulse(thecore_pulse() + PASSES_PER_SEC(10));
}

ACMD (do_sort_special_storage)
{
	if (!ch)
		return;

	if (!ch->CanHandleItem())
		return;

	int lastSortSpecialStoragePulse = ch->GetSortSpecialStoragePulse();
	int currentPulse = thecore_pulse();

	if (lastSortSpecialStoragePulse > currentPulse)
	{
		int deltaInSeconds = ((lastSortSpecialStoragePulse / PASSES_PER_SEC(1)) - (currentPulse / PASSES_PER_SEC(1)));
		int minutes = deltaInSeconds / 60;
		int seconds = (deltaInSeconds - (minutes * 60));

		ch->LocaleChatPacket(CHAT_TYPE_INFO, 316, "%d", seconds);
		return;
	}

	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (!*arg1)
		return;

	std::vector<CItem*> collectItems;

	for (int i = SKILL_BOOK_INVENTORY_SLOT_START; i < SKILL_BOOK_INVENTORY_SLOT_END; ++i)
	{
		if (!ch)
			continue;

		LPITEM item = ch->GetSkillBookInventoryItem(i);

		if (item)
		{
			collectItems.push_back(item);
		}
	}

	for (int i = UPGRADE_ITEMS_INVENTORY_SLOT_START; i < UPGRADE_ITEMS_INVENTORY_SLOT_END; ++i)
	{
		if (!ch)
			continue;

		LPITEM item = ch->GetUpgradeItemsInventoryItem(i);

		if (item)
		{
			collectItems.push_back(item);
		}
	}

	for (int i = STONE_INVENTORY_SLOT_START; i < STONE_INVENTORY_SLOT_END; ++i)
	{
		if (!ch)
			continue;

		LPITEM item = ch->GetStoneInventoryItem(i);

		if (item)
		{
			collectItems.push_back(item);
		}
	}

	for (int i = GIFT_BOX_INVENTORY_SLOT_START; i < GIFT_BOX_INVENTORY_SLOT_END; ++i)
	{
		if (!ch)
			continue;

		LPITEM item = ch->GetGiftBoxInventoryItem(i);

		if (item)
		{
			collectItems.push_back(item);
		}
	}

	for (int i = CHANGERS_INVENTORY_SLOT_START; i < CHANGERS_INVENTORY_SLOT_END; ++i)
	{
		if (!ch)
			continue;

		LPITEM item = ch->GetChangersInventoryItem(i);

		if (item)
		{
			collectItems.push_back(item);
		}
	}

	for (std::vector<CItem*>::iterator it = collectItems.begin() ; it != collectItems.end(); ++it)
	{
		if (!ch)
			continue;

		LPITEM item = *it;
		item->RemoveFromCharacter();
	}

	std::sort(collectItems.begin(), collectItems.end(), sortByType);
	std::sort(collectItems.begin(), collectItems.end(), sortBySubType);
	std::sort(collectItems.begin(), collectItems.end(), sortByVnum);
	std::sort(collectItems.begin(), collectItems.end(), sortBySocket);

	for (std::vector<CItem*>::iterator iit = collectItems.begin(); iit < collectItems.end(); ++iit)
	{
		if (!ch)
			continue;

		LPITEM sortedItem = *iit;
		if (sortedItem)
		{
#ifdef ENABLE_STACK_LIMIT
			WORD dwCount = sortedItem->GetCount();
#else
			BYTE dwCount = sortedItem->GetCount();
#endif
			if (sortedItem->IsStackable() && !IS_SET(sortedItem->GetAntiFlag(), ITEM_ANTIFLAG_STACK))
			{
				for (int i = SKILL_BOOK_INVENTORY_SLOT_START; i < SKILL_BOOK_INVENTORY_SLOT_END; ++i)
				{
					LPITEM item2 = ch->GetSkillBookInventoryItem(i);

					if (!item2)
					{
						continue;
					}

					if (item2->GetVnum() == sortedItem->GetVnum())
					{
						int j;

						for (j = 0; j < ITEM_SOCKET_MAX_NUM; ++j)
						{
							if (item2->GetSocket(j) != sortedItem->GetSocket(j))
							{
								break;
							}
						}

						if (j != ITEM_SOCKET_MAX_NUM)
						{
							continue;
						}

#ifdef ENABLE_STACK_LIMIT
						WORD dwCount2 = MIN(ITEM_MAX_COUNT - item2->GetCount(), dwCount);
#else
						BYTE dwCount2 = MIN(ITEM_MAX_COUNT - item2->GetCount(), dwCount);
#endif
						dwCount -= dwCount2;

						item2->SetCount(item2->GetCount() + dwCount2);

						if (dwCount == 0)
						{
							M2_DESTROY_ITEM(sortedItem);
							break;
						}
						else
						{
							sortedItem->SetCount(dwCount);
						}
					}
				}

				for (int i = UPGRADE_ITEMS_INVENTORY_SLOT_START; i < UPGRADE_ITEMS_INVENTORY_SLOT_END; ++i)
				{
					LPITEM item2 = ch->GetUpgradeItemsInventoryItem(i);

					if (!item2)
					{
						continue;
					}

					if (item2->GetVnum() == sortedItem->GetVnum())
					{
						int j;

						for (j = 0; j < ITEM_SOCKET_MAX_NUM; ++j)
						{
							if (item2->GetSocket(j) != sortedItem->GetSocket(j))
							{
								break;
							}
						}

						if (j != ITEM_SOCKET_MAX_NUM)
						{
							continue;
						}

#ifdef ENABLE_STACK_LIMIT
						WORD dwCount2 = MIN(ITEM_MAX_COUNT - item2->GetCount(), dwCount);
#else
						BYTE dwCount2 = MIN(ITEM_MAX_COUNT - item2->GetCount(), dwCount);
#endif
						dwCount -= dwCount2;

						item2->SetCount(item2->GetCount() + dwCount2);

						if (dwCount == 0)
						{
							M2_DESTROY_ITEM(sortedItem);
							break;
						}
						else
						{
							sortedItem->SetCount(dwCount);
						}
					}
				}

				for (int i = STONE_INVENTORY_SLOT_START; i < STONE_INVENTORY_SLOT_END; ++i)
				{
					LPITEM item2 = ch->GetStoneInventoryItem(i);

					if (!item2)
					{
						continue;
					}

					if (item2->GetVnum() == sortedItem->GetVnum())
					{
						int j;

						for (j = 0; j < ITEM_SOCKET_MAX_NUM; ++j)
						{
							if (item2->GetSocket(j) != sortedItem->GetSocket(j))
							{
								break;
							}
						}

						if (j != ITEM_SOCKET_MAX_NUM)
						{
							continue;
						}

#ifdef ENABLE_STACK_LIMIT
						WORD dwCount2 = MIN(ITEM_MAX_COUNT - item2->GetCount(), dwCount);
#else
						BYTE dwCount2 = MIN(ITEM_MAX_COUNT - item2->GetCount(), dwCount);
#endif
						dwCount -= dwCount2;

						item2->SetCount(item2->GetCount() + dwCount2);

						if (dwCount == 0)
						{
							M2_DESTROY_ITEM(sortedItem);
							break;
						}
						else
						{
							sortedItem->SetCount(dwCount);
						}
					}
				}

				for (int i = GIFT_BOX_INVENTORY_SLOT_START; i < GIFT_BOX_INVENTORY_SLOT_END; ++i)
				{
					LPITEM item2 = ch->GetGiftBoxInventoryItem(i);

					if (!item2)
					{
						continue;
					}

					if (item2->GetVnum() == sortedItem->GetVnum())
					{
						int j;

						for (j = 0; j < ITEM_SOCKET_MAX_NUM; ++j)
						{
							if (item2->GetSocket(j) != sortedItem->GetSocket(j))
							{
								break;
							}
						}

						if (j != ITEM_SOCKET_MAX_NUM)
						{
							continue;
						}

#ifdef ENABLE_STACK_LIMIT
						WORD dwCount2 = MIN(ITEM_MAX_COUNT - item2->GetCount(), dwCount);
#else
						BYTE dwCount2 = MIN(ITEM_MAX_COUNT - item2->GetCount(), dwCount);
#endif
						dwCount -= dwCount2;

						item2->SetCount(item2->GetCount() + dwCount2);

						if (dwCount == 0)
						{
							M2_DESTROY_ITEM(sortedItem);
							break;
						}
						else
						{
							sortedItem->SetCount(dwCount);
						}
					}
				}

				for (int i = CHANGERS_INVENTORY_SLOT_START; i < CHANGERS_INVENTORY_SLOT_END; ++i)
				{
					LPITEM item2 = ch->GetChangersInventoryItem(i);

					if (!item2)
					{
						continue;
					}

					if (item2->GetVnum() == sortedItem->GetVnum())
					{
						int j;

						for (j = 0; j < ITEM_SOCKET_MAX_NUM; ++j)
						{
							if (item2->GetSocket(j) != sortedItem->GetSocket(j))
							{
								break;
							}
						}

						if (j != ITEM_SOCKET_MAX_NUM)
						{
							continue;
						}

#ifdef ENABLE_STACK_LIMIT
						WORD dwCount2 = MIN(ITEM_MAX_COUNT - item2->GetCount(), dwCount);
#else
						BYTE dwCount2 = MIN(ITEM_MAX_COUNT - item2->GetCount(), dwCount);
#endif
						dwCount -= dwCount2;

						item2->SetCount(item2->GetCount() + dwCount2);

						if (dwCount == 0)
						{
							M2_DESTROY_ITEM(sortedItem);
							break;
						}
						else
						{
							sortedItem->SetCount(dwCount);
						}
					}
				}
			}

			if (dwCount > 0)
			{
				int cell;

				if (sortedItem->IsSkillBook())
					cell = ch->GetEmptySkillBookInventory(sortedItem->GetSize());
				else if (sortedItem->IsUpgradeItem())
					cell = ch->GetEmptyUpgradeItemsInventory(sortedItem->GetSize());
				else if(sortedItem->IsStone())
					cell = ch->GetEmptyStoneInventory(sortedItem->GetSize());
				else if(sortedItem->IsGiftBox())
					cell = ch->GetEmptyGiftBoxInventory(sortedItem->GetSize());
				else if(sortedItem->IsChanger())
					cell = ch->GetEmptyChangersInventory(sortedItem->GetSize());

				sortedItem->AddToCharacter(ch, TItemPos(INVENTORY, cell));
			}
		}
	}

	ch->SetNextSortSpecialStoragePulse(thecore_pulse() + PASSES_PER_SEC(10));
}
#endif

#ifdef ENABLE_HIDE_COSTUME_SYSTEM
ACMD(do_hide_costume)
{
	char arg1[256], arg2[256];
	two_arguments(argument, arg1, sizeof(arg1), arg2, sizeof(arg2));

	if (!*arg1)
		return;

	bool hidden = true;
	BYTE bPartPos = 0;
	BYTE bHidden = 0;

	str_to_number(bPartPos, arg1);

	if (*arg2)
	{
		str_to_number(bHidden, arg2);

		if (bHidden == 0)
			hidden = false;
	}

	if (ch->IsDead())
		return;

	bool bAttacking = (get_dword_time() - ch->GetLastAttackTime()) < 1500;
	bool bMoving = (get_dword_time() - ch->GetLastMoveTime()) < 1500;
	bool bDelayedCMD = false;

	if (ch->IsStateMove() || bAttacking || bMoving)
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 317, "");
		return;
	}

	if (bDelayedCMD)
	{
		int iPulse = thecore_pulse();
		if (iPulse - ch->GetHideCostumePulse() < passes_per_sec * 3)
		{
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 318, "");
			return;
		}
		ch->SetHideCostumePulse(iPulse);
	}

	if (bPartPos == 1)
		ch->SetBodyCostumeHidden(hidden);
	else if (bPartPos == 2)
		ch->SetHairCostumeHidden(hidden);
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	else if (bPartPos == 3)
		ch->SetAcceCostumeHidden(hidden);
#endif
#ifdef ENABLE_WEAPON_COSTUME_SYSTEM
	else if (bPartPos == 4)
		ch->SetWeaponCostumeHidden(hidden);
#endif
#ifdef ENABLE_AURA_COSTUME_SYSTEM
	else if (bPartPos == 5)
		ch->SetAuraCostumeHidden(hidden);
#endif
	else
		return;

	ch->UpdatePacket();
}
#endif

#ifdef ENABLE_RESTART_INSTANT
ACMD(do_restart_now)
{
	if (false == ch->IsDead())
	{
		ch->ChatPacket(CHAT_TYPE_COMMAND, "CloseRestartWindow");
		ch->StartRecoveryEvent();
		return;
	}

	if (ch->GetGold() < 500000)
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 319, "");
		return;
	}

	if (NULL == ch->m_pkDeadEvent)
		return;

	int iTimeToDead = (event_time(ch->m_pkDeadEvent) / passes_per_sec);

	if (!ch->GetWarMap() || ch->GetWarMap()->GetType() == GUILD_WAR_TYPE_FLAG)
	{
		if (!test_server)
		{
			if (ch->IsHack())
			{
				if ((!ch->GetWarMap() || ch->GetWarMap()->GetType() == GUILD_WAR_TYPE_FLAG))
				{
					ch->LocaleChatPacket(CHAT_TYPE_INFO, 320, "");
					return;
				}
			}
		}

		ch->ChatPacket(CHAT_TYPE_COMMAND, "CloseRestartWindow");
		ch->GetDesc()->SetPhase(PHASE_GAME);
		ch->SetPosition(POS_STANDING);
		ch->StartRecoveryEvent();
		ch->RestartAtSamePos();
		ch->PointChange(POINT_HP, ch->GetMaxHP() - ch->GetHP());
		ch->DeathPenalty(0);
		ch->ReviveInvisible(5);
		ch->PointChange(POINT_GOLD, -500000, false);
	}
}
#endif

#ifdef ENABLE_MINIGAME_OKEY_CARDS_SYSTEM
ACMD(do_cards)
{
	const char *line;
	char arg1[256], arg2[256];

	line = two_arguments(argument, arg1, sizeof(arg1), arg2, sizeof(arg2));
	switch (LOWER(arg1[0]))
	{
		case 'o':
			if (isdigit(*arg2))
			{
				DWORD safemode;
				str_to_number(safemode, arg2);
				ch->Cards_open(safemode);
			}
			break;

		case 'p':
			ch->Cards_pullout();
			break;

		case 'e':
			ch->CardsEnd();
			break;

		case 'd':
			if (isdigit(*arg2))
			{
				DWORD destroy_index;
				str_to_number(destroy_index, arg2);
				ch->CardsDestroy(destroy_index);
			}
			break;

		case 'a':
			if (isdigit(*arg2))
			{
				DWORD accpet_index;
				str_to_number(accpet_index, arg2);
				ch->CardsAccept(accpet_index);
			}
			break;

		case 'r':
			if (isdigit(*arg2))
			{
				DWORD restore_index;
				str_to_number(restore_index, arg2);
				ch->CardsRestore(restore_index);
			}
			break;

		default:
			return;
	}
}
#endif

#ifdef ENABLE_ANTI_EXP
ACMD(do_anti_exp)
{
	time_t real_time = time(0);
	if (ch->GetProtectTime("anti.exp") > real_time)
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 77, "%d", ch->GetProtectTime("anti.exp") - real_time);
		return;
	}

	ch->SetProtectTime("anti.exp", real_time + 3);
	ch->SetAntiExp(!ch->GetAntiExp());
	ch->ChatPacket(CHAT_TYPE_COMMAND, "SetAntiExp %d", ch->GetAntiExp() ? 1:0);
}
#endif

#ifdef ENABLE_MULTI_FARM_BLOCK
ACMD(do_multi_farm)
{
	if (!ch->GetDesc())
		return;

	if (ch->GetProtectTime("multi-farm") > get_global_time())
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 77, "%d", ch->GetProtectTime("multi-farm") - get_global_time());
		return;
	}

	ch->SetProtectTime("multi-farm", get_global_time() + 10);

	CHARACTER_MANAGER::instance().CheckMultiFarmAccount(ch->GetDesc()->GetHostName(), ch->GetPlayerID(), ch->GetName(), !ch->GetRewardStatus());
}
#endif

#ifdef ENABLE_AUTOMATIC_PICK_UP_SYSTEM
ACMD(do_setpickupmode)
{
	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (*arg1)
	{
		DWORD flag = 0;
		str_to_number(flag, arg1);
		ch->ChangePickUPMode(flag);
	}
}
#endif

#ifdef ENABLE_MAINTENANCE_SYSTEM
ACMD(do_maintenance_text)
{
	char arg1[256];
	char arg2[256];
	two_arguments(argument, arg1, sizeof(arg1), arg2, sizeof(arg2));

	if (!*arg1)
	{
		ch->ChatPacket(CHAT_TYPE_NOTICE, "<Syntax> The arguments available for this command are:");
		ch->ChatPacket(CHAT_TYPE_NOTICE, "<Syntax> /m_text disable");
		ch->ChatPacket(CHAT_TYPE_NOTICE, "<Syntax> /m_text enable <text>");
		return;
	}

	if (*arg1 && !strcmp(arg1, "disable"))
	{
		MaintenanceManager::instance().Send_Text(ch, "rmf");
	}

	else if (*arg1 && !strcmp(arg1, "enable"))
	{
		const char* sReason = one_argument(argument, arg2, sizeof(arg2));
		MaintenanceManager::instance().Send_Text(ch, sReason);
	}
}

ACMD(do_maintenance)
{
	char arg1[256];
	char arg2[256];

	two_arguments(argument, arg1, sizeof(arg1), arg2, sizeof(arg2));

	if (*arg1 && !strcmp(arg1, "force_stop"))
	{
		MaintenanceManager::instance().Send_DisableSecurity(ch);
	}
	else
	{
		long time_maintenance = parse_time_str(arg1);
		long duration_maintenance = parse_time_str(arg2);

		MaintenanceManager::instance().Send_ActiveMaintenance(ch, time_maintenance, duration_maintenance);
	}
}
#endif

#ifdef ENABLE_RENEWAL_SKILL_SELECT
ACMD(do_renewal_skill_select)
{
	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (!*arg1)
		return;

	if (ch->GetSkillGroup() != 0 || ch->GetLevel() < 5)
	{
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 78, "");
		return;
	}

	int iValue = 0;
	str_to_number(iValue, arg1);
	ch->SetSkillGroup(iValue);
	ch->ClearSkill();
}
#endif

#ifdef ENABLE_RENEWAL_INGAME_ITEMSHOP
ACMD(do_ishop)
{
	std::vector<std::string> vecArgs;
	split_argument(argument, vecArgs);

	if (vecArgs.size() < 2) { return; }
	else if (vecArgs[1] == "data")
	{
		if (ch->GetProtectTime("itemshop.load") == 1)
			return;

		ch->SetProtectTime("itemshop.load", 1);

		if (vecArgs.size() < 3) { return; }
		int updateTime;
		str_to_number(updateTime, vecArgs[2].c_str());

		CHARACTER_MANAGER::Instance().LoadItemShopData(ch, CHARACTER_MANAGER::Instance().GetItemShopUpdateTime() != updateTime);
	}
	else if (vecArgs[1] == "log")
	{
		if (ch->GetProtectTime("itemshop.log") == 1)
			return;
		ch->SetProtectTime("itemshop.log", 1);

		CHARACTER_MANAGER::Instance().LoadItemShopLog(ch);
	}
	else if (vecArgs[1] == "buy")
	{
		if (vecArgs.size() < 4) { return; }
		int itemID;
		str_to_number(itemID, vecArgs[2].c_str());

		int itemCount;
		str_to_number(itemCount, vecArgs[3].c_str());
		if(itemCount < 1 || itemCount > 20)
			return;

		CHARACTER_MANAGER::Instance().LoadItemShopBuy(ch, itemID, itemCount);
	}
	else if (vecArgs[1] == "wheel")
	{
		if (vecArgs.size() < 3) { return; }
		else if (vecArgs[2] == "start")
		{
			if (vecArgs.size() < 4) { return; }
			BYTE ticketType;
			if (!str_to_number(ticketType, vecArgs[3].c_str()))
				return;

			if (ticketType > 1)
				return;
			else if (ch->GetProtectTime("WheelWorking") != 0)
			{
				ch->LocaleChatPacket(CHAT_TYPE_INFO, 683, "");
				return;
			}

			if (ticketType == 0)
			{
				if (ch->CountSpecifyItem(80013) <= 0)
				{
					ch->LocaleChatPacket(CHAT_TYPE_INFO, 684, "");
					return;
				}

				ch->RemoveSpecifyItem(80013, 1);
			}
			else if (ticketType == 1)
			{
				long long dragonCoin = ch->GetCoins();
				if(dragonCoin-10 < 0)
				{
					ch->LocaleChatPacket(CHAT_TYPE_INFO, 685, "");
					return;
				}

				ch->SetCoins(dragonCoin - 10);
				ch->ChatPacket(CHAT_TYPE_COMMAND, "SetDragonCoin %lld", dragonCoin - 10);

				BYTE subIndex = ITEMSHOP_LOG_ADD;
				DWORD accountID = ch->GetDesc()->GetAccountTable().id;

				char playerName[CHARACTER_NAME_MAX_LEN+1];
				char ipAdress[16];

				strlcpy(playerName,ch->GetName(),sizeof(playerName));
				strlcpy(ipAdress,ch->GetDesc()->GetHostName(),sizeof(ipAdress));

				db_clientdesc->DBPacketHeader(HEADER_GD_ITEMSHOP, ch->GetDesc()->GetHandle(), sizeof(BYTE)+sizeof(DWORD)+sizeof(playerName)+sizeof(ipAdress));
				db_clientdesc->Packet(&subIndex, sizeof(BYTE));
				db_clientdesc->Packet(&accountID, sizeof(DWORD));
				db_clientdesc->Packet(&playerName, sizeof(playerName));
				db_clientdesc->Packet(&ipAdress, sizeof(ipAdress));

				if (ch->GetProtectTime("itemshop.log") == 1)
				{
					char timeText[21];
					time_t now = time(0);
					struct tm tstruct = *localtime(&now);
					strftime(timeText, sizeof(timeText), "%Y-%m-%d %X", &tstruct);
					ch->ChatPacket(CHAT_TYPE_COMMAND, "ItemShopAppendLog %s %d %s %s 1 1 10", timeText, time(0), playerName, ipAdress);
				}
			}

			std::vector<std::pair<long, long>> m_important_item = {
				{72320, 1},
				{72320, 2},
				{72319, 1},
				{72319, 2},
				{70063, 1},
				{70064, 1},
				{84014, 1},
			};

			std::map<std::pair<long, long>, int> m_normal_item = {
				{{71084, 5}, 30},
				 {{71084, 10}, 30},
				 {{71084, 10}, 30},
				 {{71084, 20}, 30},
				 {{71084, 20}, 30},
				 {{71084, 100}, 30},
				 {{70005, 1}, 30},
				 {{25041, 1}, 30},
				 {{25041, 2}, 10},
				 {{71035, 1}, 30},
				 {{70043, 1}, 30},
				 {{71155, 1}, 30},
				 {{85001, 1}, 30},
				 {{80003, 1}, 30},
			};

			std::vector<std::pair<long, long>> m_send_items;
			if (m_important_item.size())
			{
				int random = number(0,m_important_item.size()-1);
				m_send_items.emplace_back(m_important_item[random].first, m_important_item[random].second);
			}

			while (true)
			{
				for (auto it = m_normal_item.begin(); it != m_normal_item.end(); ++it)
				{
					int randomEx = number(0, 4);
					if (randomEx == 4)
					{
						int random = number(0, 100);
						if (it->second >= random)
						{
							auto itFind = std::find(m_send_items.begin(), m_send_items.end(), it->first);
							if (itFind == m_send_items.end())
							{
								m_send_items.emplace_back(it->first.first, it->first.second);
								if (m_send_items.size() >= 10)
									break;
							}
						}
					}
				}
				if (m_send_items.size() >= 10)
					break;
			}

			std::string cmd_wheel = "";
			if (m_send_items.size())
			{
				for (auto it = m_send_items.begin(); it != m_send_items.end(); ++it)
				{
					cmd_wheel += std::to_string(it->first);
					cmd_wheel += "|";
					cmd_wheel += std::to_string(it->second);
					cmd_wheel += "#";
				}
			}

			int luckyWheel = number(0, 9);
			if (luckyWheel == 0)
				if (number(0, 1) == 0)
					luckyWheel = number(0, 9);

			ch->SetProtectTime("WheelLuckyIndex", luckyWheel);
			ch->SetProtectTime("WheelLuckyItemVnum", m_send_items[luckyWheel].first);
			ch->SetProtectTime("WheelLuckyItemCount", m_send_items[luckyWheel].second);

			ch->SetProtectTime("WheelWorking", 1);

			ch->ChatPacket(CHAT_TYPE_COMMAND, "SetWheelItemData %s", cmd_wheel.c_str());
			ch->ChatPacket(CHAT_TYPE_COMMAND, "OnSetWhell %d", luckyWheel);
		}
		else if (vecArgs[2] == "done")
		{
			if (ch->GetProtectTime("WheelWorking") == 0)
				return;

			ch->AutoGiveItem(ch->GetProtectTime("WheelLuckyItemVnum"), ch->GetProtectTime("WheelLuckyItemCount"));
			ch->ChatPacket(CHAT_TYPE_COMMAND, "GetWheelGiftData %d %d", ch->GetProtectTime("WheelLuckyItemVnum"), ch->GetProtectTime("WheelLuckyItemCount"));
			ch->SetProtectTime("WheelLuckyIndex", 0);
			ch->SetProtectTime("WheelLuckyItemVnum", 0);
			ch->SetProtectTime("WheelLuckyItemCount", 0);
			ch->SetProtectTime("WheelWorking", 0);
		}
	}
}
#endif

#ifdef ENABLE_FISH_GAME
#include "fishing.h"

ACMD(do_fish_game)
{
	if (!ch->m_pkFishingEvent)
		return;
	else if (quest::CQuestManager::instance().GetEventFlag("fishgame_event") != 1)
		return;

	LPITEM rod = ch->GetWear(WEAR_WEAPON);
	if (!rod)
		return;

	std::vector<std::string> vecArgs;
	split_argument(argument, vecArgs);
	if (vecArgs.size() < 3) { return; }

	int gameKey;
	if(!str_to_number(gameKey, vecArgs[1].c_str()))
		return;
	if (ch->GetProtectTime("fish_game_key") != gameKey)
	{
		ch->ChatPacket(CHAT_TYPE_COMMAND, "CloseFishGame");
		return;
	}
	else if (vecArgs[2] == "close")
	{
		fishing::FishingFail(ch);
	}
	else if (vecArgs[2] == "score")
	{
		if (vecArgs.size() < 4) { return; }
		int scoreType;
		if(!str_to_number(scoreType, vecArgs[3].c_str()))
			return;

		int totalClick = ch->GetProtectTime("fish_game_total_click");
		totalClick += 1;
		ch->SetProtectTime("fish_game_total_click", totalClick);

		int totalScore = ch->GetProtectTime("fish_game_total_score");
		if (scoreType == 1)
		{
			totalScore += 1;
			ch->SetProtectTime("fish_game_total_score", totalScore);
		}

		if (totalClick == 3)
		{
			if(totalScore == 3)
				ch->fishing_take();
			else
			{
				event_cancel(&ch->m_pkFishingEvent);
				fishing::FishingFail(ch);
			}
		}
		else
			ch->ChatPacket(CHAT_TYPE_COMMAND, "SetFishGameGoal %d", totalScore);
	}
}
#endif

#ifdef ENABLE_INVENTORY_EXPANSION_SYSTEM
ACMD(do_reload_inventory)
{
	if (!ch)
		return;

	for (int i = 0; i < UNLOCK_INVENTORY_MAX; ++i)
	{
		ch->ChatPacket(CHAT_TYPE_COMMAND, "ManagerInventoryUnlock Hide|%d|%d", ch->GetUnlockSlotsW(i),i);
	}
}

ACMD(do_unlock_inventory)
{
	if (!ch)
		return;

	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (!*arg1)
	{
		return;
	}

	DWORD type_inventory;
	str_to_number(type_inventory, arg1);

	DWORD inv = ch->GetUnlockSlotsW(type_inventory);
	int cant;

	if (inv > 0)
	{
		cant = (inv+1)*2;
		if (ch->CountSpecifyItem(72320) >= cant)
		{
			ch->RemoveSpecifyItem(72320, cant);
			ch->ChatPacket(CHAT_TYPE_COMMAND, "ManagerInventoryUnlock Hide|%d|%d", inv+1, type_inventory);
			ch->SetUnlockSlotsW(inv+1, type_inventory);
		}
		else
		{
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 112, "%d", cant);
		}
	}
	else
	{
		cant = 2;
		if (ch->CountSpecifyItem(72320) >= cant)
		{
			ch->RemoveSpecifyItem(72320, cant);
			ch->ChatPacket(CHAT_TYPE_COMMAND, "ManagerInventoryUnlock Hide|%d|%d", 1, type_inventory);
			ch->SetUnlockSlotsW(1, type_inventory);
		}
		else
		{
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 112, "%d", cant);
		}
	}
}
#endif

#ifdef ENABLE_RENEWAL_TELEPORT_SYSTEM
ACMD(do_open_warping_window)
{
	if (!ch)
		return;

	ch->ChatPacket(CHAT_TYPE_COMMAND, "BINARY_OpenWarpWindow");
}

ACMD(do_warp_on)
{
	if (!ch)
		return;

	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (!*arg1)
		return;

	int map_index;
	str_to_number(map_index, arg1);

	ch->StartWarpOn(map_index);
}
#endif

#ifdef ENABLE_DUNGEON_TRACKING_SYSTEM
#include "mob_timer_manager.h"

ACMD(do_track_window)
{
	std::vector<std::string> vecArgs;
	split_argument(argument, vecArgs);

	if (vecArgs.size() < 2) { return; }
	else if (vecArgs[1] == "load")
	{
		if (ch->GetProtectTime("track_dungeon")==1)
			return;

		ch->GetDungeonCooldown(WORD_MAX);

		for (BYTE i = 2; i < vecArgs.size(); ++i)
		{
			WORD globalBossID;
			if (!str_to_number(globalBossID, vecArgs[i].c_str()))
				continue;

			CMobTimerManager::Instance().GetTrackData(ch, globalBossID);
		}

		ch->SetProtectTime("track_dungeon", 1);
	}
	else if (vecArgs[1] == "reenter")
	{
		if (!ch->IsGM())
			return;

		if (vecArgs.size() < 4) { return; }

		WORD testVnum;
		if (!str_to_number(testVnum, vecArgs[2].c_str()))
			return;

		int testTime;
		if (!str_to_number(testTime, vecArgs[3].c_str()))
			return;

		ch->GetDungeonCooldownTest(testVnum, testTime, false);
	}
	else if (vecArgs[1] == "cooldown")
	{
		if (!ch->IsGM())
			return;

		if (vecArgs.size() < 4) { return; }

		WORD testVnum;
		if (!str_to_number(testVnum, vecArgs[2].c_str()))
			return;

		int testTime;
		if (!str_to_number(testTime, vecArgs[3].c_str()))
			return;

		ch->GetDungeonCooldownTest(testVnum, testTime, true);
	}
	else if (vecArgs[1] == "teleport")
	{
		if (vecArgs.size() < 3) { return; }

		WORD mobIndex;
		if (!str_to_number(mobIndex, vecArgs[2].c_str()))
			return;

		const std::map<WORD, std::pair<std::pair<long, long>,std::pair<WORD, std::pair<BYTE,BYTE>>>> m_TeleportData = {
			//{mobindex - {{X, Y}, {PORT, {MINLVL, MAXLVL},}}},
			{9836, { {3840, 14323}, {0, {40, 60}} }},
			{9844, { {17268, 23855}, {0, {65, 85}} }},
			{9838, { {3840, 14861}, {0, {80, 100}} }},
			{9840, { {4350, 14850}, {0, {95, 115}} }},
			{9842, { {3327, 15384}, {0, {105, 120}} }},
			{1093, { {5905, 1105}, {0, {40, 120}} }},
			{2092, { {689, 6111}, {0, {70, 120}} }},
			{2493, { {1800, 12199}, {0, {75, 120}} }},
			{2598, { {5918, 993}, {0, {80, 120}} }},
			{6091, { {5984, 7073}, {0, {90, 120}} }},
			{6191, { {4319, 1647}, {0, {90, 120}} }},
			{9018, { {11082, 17824}, {0, {105, 120}} }},
			{20442, { {7358, 6237}, {0, {110, 120}} }},
		};

		const auto it = m_TeleportData.find(mobIndex);
		if (it != m_TeleportData.end())
		{
			if (ch->GetLevel() < it->second.second.second.first || ch->GetLevel() > it->second.second.second.second)
			{
				ch->LocaleChatPacket(CHAT_TYPE_INFO, 735, "");
				return;
			}

			ch->WarpSet(it->second.first.first * 100, it->second.first.second * 100, it->second.second.first);
		}
	}
}
#endif

#ifdef ENABLE_SPIRIT_STONE_READING
LPEVENT ruhtimer = NULL;

EVENTINFO(TMainEventInfo)
{
	LPCHARACTER	kim;
	long skillindexx;
	
	TMainEventInfo() 
	: kim( NULL )
	, skillindexx( 0 )
	{
	}

} ;

EVENTFUNC(ruh_event)
{
	TMainEventInfo * info = dynamic_cast<TMainEventInfo *>(  event->info );

	if ( info == NULL )
	{
		sys_err( "ruh_event> <Factor> Null pointer" );
		return 0;
	}
	
	LPCHARACTER	ch = info->kim;
	long skillindex = info->skillindexx;
	
	if (NULL == ch || skillindex == 0)
		return 0;

	if (!ch)
		return 0;

	if (!ch->GetDesc())
		return 0;
 
	if (!ch->IsPC())
		return 0;
 
	if (ch->IsDead() || ch->IsStun())
		return 0;

	if (ch->IsHack())
		return 0;

	if(ch->CountSpecifyItem(50513) < 1 )
	{
		//ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("ruhtasiyok"));
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 784, "");
		return 0;
	}

	int skilllevel = ch->GetSkillLevel(skillindex);

	if (skilllevel >= 40)
	{
		//ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("ruhskillson"));
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 785, "");
		return 0;
	}

	int gerekenderece = (1000+500*(skilllevel-30));
	int derecem = (ch->GetRealAlignment()/10);
	int sonuc = (-19000+gerekenderece);
	if (derecem < 0)
	{
		gerekenderece = gerekenderece*2;
		sonuc = (-19000-gerekenderece);
	}

	if (derecem > sonuc)
	{
		int gerekliknk = gerekenderece;
		int kactane = gerekliknk/500;
		if (kactane < 0)
		{
			kactane = 0 - kactane;
		}

		if (derecem < 0)
		{
			if (ch->CountSpecifyItem(70102) < kactane)
			{
				//ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("ruhzenbitti %d"),kactane);
				ch->LocaleChatPacket(CHAT_TYPE_INFO, 780, "%d", kactane);
				return 0;
			}

			int delta = MIN(-(ch->GetAlignment()), 500);
			ch->UpdateAlignment(delta*kactane);
			ch->RemoveSpecifyItem(70102,kactane);
			//ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("ruhzenbastim"));
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 781, "");
		}
	}

	// Performans optimizasyonu: GetQuestFlag yerine direkt member variable
	if(ch->GetRuhSureFlag() > get_global_time())
	{
		if (ch->CountSpecifyItem(71001) < 1 )
		{
			//ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("ruhsuredolmadi"));
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 782, "");
			return 0;
		}
		else
		{
			ch->RemoveSpecifyItem(71001,1);
		}
			
	}

	if (ch->CountSpecifyItem(71094) >= 1)
	{
		ch->AddAffect(512, aApplyInfo[0].bPointType, 0, 0, 536870911, 0, false);
		ch->RemoveSpecifyItem(71094,1);
		//ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("ruhmunzevikullandim"));
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 783, "");
	}

	if (gerekenderece < 0)
	{
		ch->UpdateAlignment(gerekenderece*10);
	}
	else
	{
		ch->UpdateAlignment(-gerekenderece*10);
	}

		ch->LearnGrandMasterSkill(skillindex);
	ch->RemoveSpecifyItem(50513,1);
	DWORD new_ruh_sure = get_global_time()+60*60*24;
	ch->SetRuhSureFlag(new_ruh_sure);  // Performans optimizasyonu: GetQuestFlag yerine direkt member variable

	return 1;
}

ACMD(do_ruhoku)
{
	int gelen;
	long skillindex;
	char arg1[256], arg2[256];

	two_arguments(argument, arg1, sizeof(arg1), arg2, sizeof(arg2));
	str_to_number(gelen, arg1);
	str_to_number(skillindex, arg2);

	if (!ch)
		return;

	if (!ch->IsPC())
		return;

	if (ch->IsDead() || ch->IsStun())
		return;
 
	if (ch->IsHack())
		return;

	if(ch->GetExchange() || ch->GetMyShop() || ch->GetShopOwner() || ch->IsOpenSafebox() || ch->IsCubeOpen()
#ifdef ENABLE_OFFLINE_PRIVATE_SHOP_SYSTEM
		|| ch->GetOfflineShopOwner()
#endif
		)
	{
		ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("´Ù¸¥ °Å·¡Áß(Ã¢°í,±³È¯,»óÁ¡)¿¡´Â °³ÀÎ»óÁ¡À» »ç¿ëÇÒ ¼ö ¾ø½À´Ï´Ù."));
		return;
	}

	if(ch->CountSpecifyItem(50513) < 1 )
	{
		//ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("ruhtasiyok"));
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 784, "");
		return;
	}

	LPITEM slot1 = ch->GetWear(WEAR_UNIQUE1);
	LPITEM slot2 = ch->GetWear(WEAR_UNIQUE2);

	if (NULL != slot1)
	{
		if (slot1->GetVnum() == 70048)
		{
			ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("pelerin_cikar"));
			return;
		}
	}
	if (NULL != slot2)
	{
		if (slot2->GetVnum() == 70048)
		{
			ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("pelerin_cikar"));
			return;
		}
	}

	int skillgrup = ch->GetSkillGroup();
	if (skillgrup == 0)
	{
		//ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("ruhokuyamazsin"));
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 787, "");
		return;
	}

	if (gelen == 1) ///tek
	{
		int skilllevel = ch->GetSkillLevel(skillindex);
		int gerekenderece = (1000+500*(skilllevel-30));
		int derecem = (ch->GetRealAlignment()/10);
		int sonuc = (-19000+gerekenderece);

		// Performans optimizasyonu: GetQuestFlag yerine direkt member variable
		if(ch->GetRuhYeniSureFlag() > get_global_time())
		{
			//ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("ruh1sn"));
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 786, "");
			return;
		}
		if (derecem < 0)
		{
			gerekenderece = gerekenderece*2;
			sonuc = (-19000-gerekenderece);
		}

		if (derecem > sonuc)
		{
			int gerekliknk = gerekenderece;
			int kactane = gerekliknk/500;
			if (kactane < 0)
			{
				kactane = 0 - kactane;
			}

			if (derecem < 0)
			{
				if (ch->CountSpecifyItem(70102) < kactane)
				{
					//ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("ruhzenbitti %d"),kactane);
					ch->LocaleChatPacket(CHAT_TYPE_INFO, 780, "%d", kactane);
					return;
				}

				int delta = MIN(-(ch->GetAlignment()), 500);
				ch->UpdateAlignment(delta*kactane);
				ch->RemoveSpecifyItem(70102,kactane);
				//ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("ruhzenbastim"));
				ch->LocaleChatPacket(CHAT_TYPE_INFO, 781, "");
			}
		}

		// Performans optimizasyonu: GetQuestFlag yerine direkt member variable
		if(ch->GetRuhSureFlag() > get_global_time())
		{
			if (ch->CountSpecifyItem(71001) < 1 )
			{
				//ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("ruhsuredolmadi"));
				ch->LocaleChatPacket(CHAT_TYPE_INFO, 782, "");
				return;
			}
			else
			{
				ch->RemoveSpecifyItem(71001,1);
			}
		}

		if (ch->CountSpecifyItem(71094) >= 1)
		{
			ch->AddAffect(512, aApplyInfo[0].bPointType, 0, 0, 536870911, 0, false);
			ch->RemoveSpecifyItem(71094,1);
			//ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("ruhmunzevikullandim"));
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 783, "");
		}

		if (gerekenderece < 0)
		{
			ch->UpdateAlignment(gerekenderece*10);
		}
		else
		{
			ch->UpdateAlignment(-gerekenderece*10);
		}

		ch->LearnGrandMasterSkill(skillindex);
		ch->RemoveSpecifyItem(50513,1);
		DWORD new_ruh_sure = get_global_time()+60*60*24;
		DWORD new_ruh_yenisure = get_global_time()+1;
		ch->SetRuhSureFlag(new_ruh_sure);  // Performans optimizasyonu: GetQuestFlag yerine direkt member variable
		ch->SetRuhYeniSureFlag(new_ruh_yenisure);  // Performans optimizasyonu: GetQuestFlag yerine direkt member variable
		

	}
	else if(gelen == 0) ///hepsi
	{
		if (ruhtimer)
		{
			event_cancel(&ruhtimer);
		}

		TMainEventInfo* info = AllocEventInfo<TMainEventInfo>();

		info->kim = ch;
		info->skillindexx = skillindex;
		ruhtimer = event_create(ruh_event, info, PASSES_PER_SEC(1));
	}

	return;
}
#endif

#ifdef ENABLE_SKILL_BOOK_READING
LPEVENT bktimer = NULL;

EVENTINFO(TMainEventInfo2)
{
	LPCHARACTER	kim;
	long skillindexx;
	
	TMainEventInfo2() 
	: kim( NULL )
	, skillindexx( 0 )
	{
	}

} ;

EVENTFUNC(bk_event)
{
	TMainEventInfo2 * info = dynamic_cast<TMainEventInfo2 *>(  event->info );

	if ( info == NULL )
	{
		sys_err( "ruh_event> <Factor> Null pointer" );
		return 0;
	}

	LPCHARACTER	ch = info->kim;
	long skillindex = info->skillindexx;

	if (NULL == ch || skillindex == 0)
		return 0;

	if (!ch)
		return 0;

	if (ch)
	{
		if(ch->CountSpecifyItem(50300) < 1 )
		{
			//ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("bkyok"));
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 778, "");
			return 0;
		}

		int skilllevel = ch->GetSkillLevel(skillindex);
		if (skilllevel >= 30)
		{
			//ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("bkskillson"));
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 774, "");
			return 0;
		}

		int dwVnum = ch->BKBul(skillindex);
		if (dwVnum == 999)
		{
			//ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("bkskillyok"));
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 776, "");
			return 0;
		}

		LPITEM item = ch->GetInventoryItem(dwVnum);

		if (item->GetVnum() != 50300 || item->GetSocket(0) != skillindex)
		{
			return 0;
		}

		if (ch->CountSpecifyItem(71001) > 0)
		{
			if (!ch->IsAffectFlag(513))
			{
				ch->AddAffect(513, aApplyInfo[0].bPointType, 0, 0, 536870911, 0, false);
				ch->RemoveSpecifyItem(71001,1);
			}
		}

		if (ch->CountSpecifyItem(71001) < 1)
		{
			//ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("bkkoturuhyok"));
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 779, "");
			return 0;
		}

		if (ch->CountSpecifyItem(71094) >= 1)
		{
			if (!ch->IsAffectFlag(512))
			{
				ch->AddAffect(512, aApplyInfo[0].bPointType, 0, 0, 536870911, 0, false);
				ch->RemoveSpecifyItem(71094,1);
			}
		}

		if (item->GetVnum() == 50300)
		{
			if (true == ch->LearnSkillByBook(skillindex))
			{
				if (item->GetVnum() == 50300 && item->GetSocket(0) == skillindex)
				{
					item->SetCount(item->GetCount() - 1);
					int iReadDelay;
					iReadDelay= number(SKILLBOOK_DELAY_MIN, SKILLBOOK_DELAY_MAX);
					ch->SetSkillNextReadTime(skillindex, get_global_time() + iReadDelay);
					DWORD new_bk_yenisure = get_global_time() + 1;
					ch->SetBkYeniSureFlag(new_bk_yenisure);  // Performans optimizasyonu: GetQuestFlag yerine direkt member variable
				}
			}
			else
			{
				if (item->GetVnum() == 50300 && item->GetSocket(0) == skillindex)
				{
					item->SetCount(item->GetCount() - 1);
					int iReadDelay;
					iReadDelay= number(SKILLBOOK_DELAY_MIN, SKILLBOOK_DELAY_MAX);
					ch->SetSkillNextReadTime(skillindex, get_global_time() + iReadDelay);
					DWORD new_bk_yenisure = get_global_time() + 1;
					ch->SetBkYeniSureFlag(new_bk_yenisure);  // Performans optimizasyonu: GetQuestFlag yerine direkt member variable
				}
			}
		}
		return 1;
	}
	return 0;
}

ACMD(do_bkoku)
{
	int gelen;
	long skillindex;
	char arg1[256], arg2[256];
	two_arguments(argument, arg1, sizeof(arg1), arg2, sizeof(arg2));
	str_to_number(gelen, arg1);
	str_to_number(skillindex, arg2);

	if (!ch)
		return;

	if (!ch->IsPC())
		return;

	if (ch->IsDead() || ch->IsStun())
		return;

	if (ch->IsHack())
		return;

	if(ch->GetExchange() || ch->GetMyShop() || ch->GetShopOwner() || ch->IsOpenSafebox() || ch->IsCubeOpen()
#ifdef ENABLE_OFFLINE_PRIVATE_SHOP_SYSTEM
		|| ch->GetOfflineShopOwner()
#endif
		)
	{
		ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("´Ù¸¥ °Å·¡Áß(Ã¢°í,±³È¯,»óÁ¡)¿¡´Â °³ÀÎ»óÁ¡À» »ç¿ëÇÒ ¼ö ¾ø½À´Ï´Ù."));
		return;
	}

	int skillgrup = ch->GetSkillGroup();
	if (skillgrup == 0)
	{
		//ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("bkokuyamazsin"));
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 775, "");
		return;
	}

	if(ch->CountSpecifyItem(50300) < 1)
	{
		//ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("bkyok"));
		ch->LocaleChatPacket(CHAT_TYPE_INFO, 778, "");
		return;
	}

	if (gelen == 1) ///tek
	{
		int skilllevel = ch->GetSkillLevel(skillindex);

		if (skilllevel >= 30)
		{
			ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("ruhskillson"));
			return;
		}

		// Performans optimizasyonu: GetQuestFlag yerine direkt member variable
		if (ch->GetBkYeniSureFlag() > get_global_time())
		{
			//ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("bk1sn"));
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 777, "");
			return;
		}

		int dwVnum = ch->BKBul(skillindex);
		if (dwVnum == 999)
		{
			//ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("bkskillyok"));
			ch->LocaleChatPacket(CHAT_TYPE_INFO, 776, "");
			return;
		}

		LPITEM item = ch->GetInventoryItem(dwVnum);

		if (item->GetVnum() != 50300 || item->GetSocket(0) != skillindex)
		{
			return;
		}

		if (ch->CountSpecifyItem(71001) > 0)
		{
			if (!ch->IsAffectFlag(513))
			{
				ch->AddAffect(513, aApplyInfo[0].bPointType, 0, 0, 536870911, 0, false);
				ch->RemoveSpecifyItem(71001,1);
			}
		}

		if (ch->CountSpecifyItem(71094) >= 1)
		{
			if (!ch->IsAffectFlag(512))
			{
				ch->AddAffect(512, aApplyInfo[0].bPointType, 0, 0, 536870911, 0, false);
				ch->RemoveSpecifyItem(71094,1);
			}
		}

		if (item->GetVnum() == 50300)
		{
			if (ch->FindAffect(AFFECT_SKILL_NO_BOOK_DELAY) == false && ch->CountSpecifyItem(71001) < 1)
			{
				ch->SkillLearnWaitMoreTimeMessage(ch->GetSkillNextReadTime(skillindex) - get_global_time());
				return;
			}

			if (true == ch->LearnSkillByBook(skillindex))
			{
				if (item->GetVnum() == 50300 && item->GetSocket(0) == skillindex)
				{
					item->SetCount(item->GetCount() - 1);
					int iReadDelay;
					iReadDelay= number(SKILLBOOK_DELAY_MIN, SKILLBOOK_DELAY_MAX);
					ch->SetSkillNextReadTime(skillindex, get_global_time() + iReadDelay);
				}
			}
			else
			{
				if (item->GetVnum() == 50300 && item->GetSocket(0) == skillindex)
				{
					item->SetCount(item->GetCount() - 1);
					int iReadDelay;
					iReadDelay= number(SKILLBOOK_DELAY_MIN, SKILLBOOK_DELAY_MAX);
					ch->SetSkillNextReadTime(skillindex, get_global_time() + iReadDelay);
				}
			}
			DWORD new_bk_yenisure = get_global_time() + 1;
			ch->SetBkYeniSureFlag(new_bk_yenisure);  // Performans optimizasyonu: GetQuestFlag yerine direkt member variable
			ch->SetBkYeniSureFlag(new_bk_yenisure);  // Performans optimizasyonu: GetQuestFlag yerine direkt member variable
		}
	}
	else if(gelen == 0) ///hepsi
	{
		if (bktimer)
		{
			event_cancel(&bktimer);
		}

		TMainEventInfo2* info = AllocEventInfo<TMainEventInfo2>();
		info->kim = ch;
		info->skillindexx = skillindex;
		bktimer = event_create(bk_event, info, PASSES_PER_SEC(1));
	}

	return;
}
#endif

#ifdef ENABLE_AUTO_SELL_SYSTEM
ACMD(do_autosell_info)
{
	ch->SendItemProcessInfo();
}

ACMD(do_autosell_status)
{
	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (!*arg1)
		return;

	int status = 0;
	str_to_number(status, arg1);
	
	ch->SetAutoSellStatus(status == 1);
	ch->SendItemProcessInfo();
}

ACMD(do_autosell_add)
{
	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (!*arg1)
		return;

	DWORD item_vnum = 0;
	str_to_number(item_vnum, arg1);
	
	ch->AddAutoSellItem(item_vnum);
	ch->SendItemProcessInfo();
}

ACMD(do_autosell_remove)
{
	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (!*arg1)
		return;

	DWORD item_vnum = 0;
	str_to_number(item_vnum, arg1);
	
	ch->RemoveAutoSellItem(item_vnum);
	ch->SendItemProcessInfo();
}

ACMD(do_autosell_remove_all)
{
	ch->RemoveAllAutoSellItem();
	ch->SendItemProcessInfo();
	// ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("oto_sat_tum_liste_temizlendi"));
}

ACMD(do_auto_sell)
{
	char arg1[256];
	one_argument(argument, arg1, sizeof(arg1));

	if (!*arg1)
	{
		ch->ChatPacket(CHAT_TYPE_INFO, "Kullan©¥m: /autosell <0|1>");
		return;
	}

	if (!strcmp(arg1, "0"))
		ch->SetAutoSellStatus(true);
	else if (!strcmp(arg1, "1"))
		ch->SetAutoSellStatus(false);
	else
		ch->ChatPacket(CHAT_TYPE_INFO, "Kullan©¥m: /autosell <0|1>");
}
#endif

#ifdef ENABLE_PLAYERS_ONLINE
ACMD(do_players_online){
	if (!ch)
		return;
	
	int iTotal;
	int * paiEmpireUserCount;
	int iLocal;

	DESC_MANAGER::instance().GetUserCount(iTotal, &paiEmpireUserCount, iLocal);
	
	ch->ChatPacket(CHAT_TYPE_COMMAND, "SetPlayersOnline %d", iTotal);
}
#endif

