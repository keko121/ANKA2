#pragma once
#include "stdafx.h"

#ifdef ENABLE_BIOLOG_SYSTEM
#include "../../common/tables.h"
#include "affect.h"

class CBiologSystem {
	const DWORD BIOLOG_CHANCE_ITEM = 71035;
	const DWORD BIOLOG_TIME_ITEM = 31031;
	const int BIOLOG_AFF_TIME = 60*60*60*365;

	public:
		enum ECGPackets
		{
			CG_BIOLOG_OPEN,
			CG_BIOLOG_SEND,
			CG_BIOLOG_TIMER,
		};

		enum EGCPackets
		{
			GC_BIOLOG_OPEN,
			GC_BIOLOG_ALERT,
			GC_BIOLOG_CLOSE,
		};

	public:
		CBiologSystem(LPCHARACTER m_pkChar);
		~CBiologSystem();

		void ResetMission();
		void SendBiologInformation(bool bUpdate = false);
		void SendBiologItem(bool bAdditionalChance, bool bAdditionalTime);
		void GiveRewardByMission(BYTE bMission);
		bool GetBiologItemByMobVnum(LPCHARACTER pkKiller, WORD MonsterVnum, DWORD& ItemVnum, BYTE& bChance);
		void ActiveAlert(bool bReminder);
		void BroadcastAlert();
		int RecvClientPacket(BYTE bSubHeader, const char* c_pData, size_t uiBytes);
		void SendClientPacket(LPDESC pkDesc, BYTE bSubHeader, const void* c_pvData, size_t iSize);
		void SendClientPacket(DWORD dwPID, BYTE bSubHeader, const void* c_pvData, size_t iSize);

	private:
		LPCHARACTER m_pkChar;
		std::string s_current_biolog_reminder;
};

class CBiologSystemManager : public singleton<CBiologSystemManager>
{
	public:
		typedef std::map<BYTE, TBiologMissionsProto> TMissionProtoMap;
		typedef std::map<BYTE, TBiologRewardsProto> TRewardProtoMap;
		typedef std::map<BYTE, std::vector<TBiologMonstersProto*>> TMonstersProtoMap;

	public:
		CBiologSystemManager();
		~CBiologSystemManager();

		void InitializeMissions(TBiologMissionsProto* pData, size_t size);
		TBiologMissionsProto* GetMission(BYTE bMission);
		void InitializeRewards(TBiologRewardsProto* pData, size_t size);
		TBiologRewardsProto* GetReward(BYTE bMission);
		void InitializeMonsters(TBiologMonstersProto* pData, size_t size);
		bool GetMonsters(BYTE bMission, std::vector<TBiologMonstersProto*>& monsters);
		friend void CBiologSystem::SendBiologItem(bool bAdditionalChance, bool bAdditionalTime);

	private:
		TMissionProtoMap m_mapMission_Proto;
		TRewardProtoMap m_mapReward_Proto;
		TMonstersProtoMap m_mapMonsters_Proto;
};
#endif
