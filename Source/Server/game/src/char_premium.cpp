#include "stdafx.h"

#ifdef ENABLE_RENEWAL_PREMIUM_SYSTEM
#include "constants.h"
#include "utils.h"
#include "config.h"
#include "char.h"
#include "char_manager.h"
#include "db.h"
#include "packet.h"
#include "desc_client.h"
#include "item.h"
#include "item_manager.h"
#include "locale_service.h"
#include "affect.h"

void CHARACTER::LoadPremium()
{
	if (!IsPC() || !GetDesc())
		return;

	DWORD mID = GetPlayerID();
	DWORD accountId = GetDesc()->GetAccountId();

	char szQuery[QUERY_MAX_LEN];
	snprintf(szQuery, sizeof(szQuery), "SELECT UNIX_TIMESTAMP(mRegister), UNIX_TIMESTAMP(mExpire) FROM common.premium WHERE mID=%i", mID);
	std::unique_ptr<SQLMsg> pSelectMsg(DBManager::instance().DirectQuery(szQuery));

	if (!pSelectMsg)
		return;

	SQLResult* pRes = pSelectMsg->Get();

	int mExpire = 0;
	int mRegister = 0;
	if (pRes->uiNumRows > 0)
	{
		MYSQL_ROW row = mysql_fetch_row(pRes->pSQLResult);
		str_to_number(mRegister, row[0]);
		str_to_number(mExpire, row[1]);
	}

	SetRegistrationTime(mRegister);
	SetPremiumTime(mExpire);
}

void CHARACTER::CheckPremium()
{
	if (!IsPC())
		return;

	auto mExpire = GetPremiumTime() - get_global_time();

	if (mExpire < 0)
	{
		if (m_afAffectFlag.IsSet(AFF_PREMIUM) || FindAffect(AFFECT_PREMIUM_ACCOUNT))
			LocaleChatPacket(CHAT_TYPE_INFO, 100, "");

		if (m_afAffectFlag.IsSet(AFF_PREMIUM))
			m_afAffectFlag.Reset(AFF_PREMIUM);

		if (FindAffect(AFFECT_PREMIUM_ACCOUNT))
			RemoveAffect(AFFECT_PREMIUM_ACCOUNT);
	}
	else
	{
		if (!m_afAffectFlag.IsSet(AFF_PREMIUM))
			m_afAffectFlag.Set(AFF_PREMIUM);

		if (!FindAffect(AFFECT_PREMIUM_ACCOUNT))
			AddAffect(AFFECT_PREMIUM_ACCOUNT, POINT_NONE, 0, AFF_PREMIUM, mExpire, 0, true, false);
	}
}

bool CHARACTER::IsPremium() const
{
	return (m_afAffectFlag.IsSet(AFF_PREMIUM) && FindAffect(AFFECT_PREMIUM_ACCOUNT));
}

bool CHARACTER::ActivatePremium(int seconds)
{
	if (IsPremium())
	{
		LocaleChatPacket(CHAT_TYPE_INFO, 101, "");
		return false;
	}

	DWORD mID = GetPlayerID();
	DWORD accountId = GetDesc()->GetAccountId();

	char szQuery[QUERY_MAX_LEN];
	snprintf(szQuery, sizeof(szQuery), "INSERT INTO common.premium%s (mID, mRegister, mExpire) VALUES (%i, NOW(), TIMESTAMPADD(SECOND,%d,NOW())) ON DUPLICATE KEY UPDATE mExpire = TIMESTAMPADD(SECOND,%d,NOW());", get_table_postfix(), mID, seconds, seconds);
	std::unique_ptr<SQLMsg> pSelectMsg(DBManager::instance().DirectQuery(szQuery));

	LoadPremium();
	CheckPremium();

	LocaleChatPacket(CHAT_TYPE_INFO, 102, "");
	return true;
}
#endif
