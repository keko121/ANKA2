#pragma once

#ifdef ENABLE_RENEWAL_BATTLE_PASS
#ifndef __INC_METIN_II_BATTLE_PASS_H__
#define __INC_METIN_II_BATTLE_PASS_H__

#include "../../common/stl.h"
#include "../../common/length.h"
#include "../../common/tables.h"
#include "group_text_parse_tree.h"

#include "packet.h"

class CBattlePassManager : public singleton<CBattlePassManager>
{
	public:
		CBattlePassManager();
		virtual ~CBattlePassManager();

		bool InitializeBattlePass();

		bool ReadNormalBattlePassGroup();
		bool ReadNormalBattlePassMissions();
		bool ReadPremiumBattlePassGroup();
		bool ReadPremiumBattlePassMissions();

		void CheckBattlePassTimes();
		BYTE GetMissionIndex(BYTE bBattlePassType, BYTE bMissionType, DWORD dwCondition);
		BYTE GetMissionTypeByName(std::string stMissionName);
		BYTE GetMissionTypeByIndex(BYTE bBattlePassType, DWORD dwIndex);
		std::string GetMissionNameByType(BYTE bType);

		std::string GetNormalBattlePassNameByID(BYTE bID);
		std::string GetPremiumBattlePassNameByID(BYTE bID);

		void GetMissionSearchName(BYTE bMissionType, std::string*, std::string*);

		void BattlePassRequestOpen(LPCHARACTER pkChar, bool bAfterOpen = true);
		void BattlePassRewardMission(LPCHARACTER pkChar, BYTE bBattlePassType, DWORD bMissionType, DWORD bBattlePassId);
		bool BattlePassMissionGetInfo(BYTE bBattlePassType, BYTE bMissionIndex, BYTE bBattlePassId, BYTE bMissionType, DWORD* dwFirstInfo, DWORD* dwSecondInfo);

		void BattlePassRequestReward(LPCHARACTER pkChar, BYTE bBattlePassType);
		void BattlePassReward(LPCHARACTER pkChar, BYTE bBattlePassType, BYTE bBattlePassID);

		DWORD GetNormalBattlePassID() const { return m_dwActiveNormalBattlePassID; }
		DWORD GetPremiumBattlePassID() const { return m_dwActivePremiumBattlePassID; }

		DWORD GetNormalBattlePassStartTime() const { return m_dwNormalBattlePassStartTime; }
		DWORD GetNormalBattlePassEndTime() const { return m_dwNormalBattlePassEndTime; }
		DWORD GetPremiumBattlePassStartTime() const { return m_dwPremiumBattlePassStartTime; }
		DWORD GetPremiumBattlePassEndTime() const { return m_dwPremiumBattlePassEndTime; }

	protected:
		DWORD m_dwNormalBattlePassStartTime;
		DWORD m_dwNormalBattlePassEndTime;
		DWORD m_dwPremiumBattlePassStartTime;
		DWORD m_dwPremiumBattlePassEndTime;

		DWORD m_dwActiveNormalBattlePassID;
		DWORD m_dwActivePremiumBattlePassID;

	private:
		CGroupTextParseTreeLoader* m_pNormalLoader;
		CGroupTextParseTreeLoader* m_pPremiumLoader;

		typedef std::map <BYTE, std::string> TMapNormalBattlePassName;
		typedef std::map <std::string, std::vector<TExtBattlePassRewardItem>> TNormalMapBattlePassReward;
		typedef std::map <std::string, std::vector<TExtBattlePassMissionInfo>> TNormalMapBattleMissionInfo;

		TMapNormalBattlePassName m_map_normal_battle_pass_name;
		TNormalMapBattlePassReward m_map_normal_battle_pass_reward;
		TNormalMapBattleMissionInfo m_map_normal_battle_pass_mission_info;

		typedef std::map <BYTE, std::string> TMapPremiumBattlePassName;
		typedef std::map <std::string, std::vector<TExtBattlePassRewardItem>> TPremiumMapBattlePassReward;
		typedef std::map <std::string, std::vector<TExtBattlePassMissionInfo>> TPremiumMapBattleMissionInfo;

		TMapPremiumBattlePassName m_map_premium_battle_pass_name;
		TPremiumMapBattlePassReward	m_map_premium_battle_pass_reward;
		TPremiumMapBattleMissionInfo m_map_premium_battle_pass_mission_info;

		typedef std::map <BYTE, std::vector<TExtBattlePassTimeTable>> TMapNormalBattlePassTimeTable;
		typedef std::map <BYTE, std::vector<TExtBattlePassTimeTable>> TMapPremiumBattlePassTimeTable;

		TMapNormalBattlePassTimeTable m_map_normal_battle_pass_times;
		TMapPremiumBattlePassTimeTable	m_map_premium_battle_pass_times;
};
#endif
#endif
