#include "StdAfx.h"

#ifdef ENABLE_INGAME_WIKI_SYSTEM
#include <map>

#include "../GameLib/ItemManager.h"
#include "../eterPack/EterPackManager.h"

#include "PythonWiki.h"
#include "PythonNetworkStream.h"
#include "PythonPlayer.h"

bool printLocalDatainSysser = false;

CPythonWiki::~CPythonWiki(){Destroy();}
CPythonWiki::CPythonWiki(){Destroy();}

void CPythonWiki::Destroy()
{
	auto it = m_vecRefineTable.begin();
	while (it != m_vecRefineTable.end())
	{
		delete it->second;
		it = m_vecRefineTable.erase(it);
	}
	m_vecRefineTable.clear();
}

constexpr DWORD bossChests[][2] =
{
	{50070,691},
	{50071,791},
	{50073,2091},
	{50076,2191},
	{50078,1304},
	{50077,1901},
	{50079,2206},
};

constexpr DWORD dungeonChests[][2] =
{
	{50082,1093},
	{50186,2598},
};

constexpr DWORD otherChests[][2] =
{
	{27999,0},
};

constexpr DWORD eventChests[][2] =
{
	{50011,0},
	{50037,0},
	{71196,0},
	{71195,0},
	{71194,0},
};

constexpr DWORD eventBoss[] =
{
	1093,
	2493
};

const std::vector<DWORD> vnumRange(const std::vector<std::pair<DWORD, DWORD>>& ranges, const std::vector<DWORD>& individualVnums)
{
	std::vector<DWORD> result;
	auto individualVnumIt = individualVnums.begin();

	for (const auto& range : ranges)
	{
		std::vector<DWORD> rangeVnums;

		for (DWORD vnum = range.first; vnum <= range.second; ++vnum)
		{
			rangeVnums.push_back(vnum);
		}

		std::sort(rangeVnums.begin(), rangeVnums.end());

		for (DWORD vnum : rangeVnums)
		{
			while (individualVnumIt != individualVnums.end() && *individualVnumIt < vnum)
			{
				result.push_back(*individualVnumIt);
				++individualVnumIt;
			}
			result.push_back(vnum);
		}
	}

	result.insert(result.end(), individualVnumIt, individualVnums.end());

	return result;
}

const std::map<BYTE, std::vector<DWORD>> m_CostumeData =
{
	{0, //Weapon
		{
			vnumRange(
				{{40008, 40027}, {40101, 40106}, {40115, 40120}, {40129, 40134}, {40143, 40148}, {40178, 40183}},
				{/*out of range vnums*/}
			)
		}
	},

	{1, //Armor
		{
			vnumRange(
				{{41001, 41182}},
				{/*out of range vnums*/}
			)
		}
	},

	{2, //Hair
		{
			vnumRange(
				{{45001, 45209}},
				{/*out of range vnums*/}
			)
		}
	},

	{3, //Acce
		{
			vnumRange(
				{{85001, 85008}, {85011, 85018}, {85021, 85024}, {86001, 86008}, {86011, 86018}, {86021, 86028}, {86031, 86038}, {86041, 86048}, {86051, 86058}, {86061, 86064}},
				{/*out of range vnums*/}
			)
		}
	},

	{4, //Mount
		{
			vnumRange(
				{{71114, 71121}, {71125, 71128}, {71137, 71142}, {71164, 71166}, {71182, 71187}, {71222, 71236}, {71242, 71264}},
				{71161, 71171, 71172, 71176, 71177, 71192, 71193, 71197, 71198, 71220}
			)
		}
	},

	{5, //Pet
		{
			vnumRange(
				{{53001, 53003}, {53005, 53026}, {53218, 53309}, {53311, 53322}, {53329, 53331}},
				{/*out of range vnums*/}
				)
		}
	},

	{6, //Companion
		{
			vnumRange(
				{{55701, 55712}},
				{/*out of range vnums*/}
			)
		}
	},
};

void CPythonWiki::ReadData(const char *localeFile)
{
	if (!LoadRefineTable("locale/common/refine_table.txt"))
		TraceError("CPythonApplication - CPythonWiki::LoadRefineTable(locale/common/refine_table.txt)");

	char szItemProto[256];
	snprintf(szItemProto, sizeof(szItemProto), "%s/item_proto", localeFile);

	if (!LoadItemTable(szItemProto))
		TraceError("CPythonWiki - LoadItemTable(%s) Error", szItemProto);

	ReadSpecialDropItemFile("locale/common/special_item_group.txt");
	ReadMobDropItemFile("locale/common/mob_drop_item.txt");
}

bool CPythonWiki::ReadSpecialDropItemFile(const char *c_pszFileName)
{
	CTextFileLoader loader;
	if (!loader.Load(c_pszFileName))
		return false;

	int iVnum;
	std::vector<special_data> vecSpecialData;
	std::string stName;
	TTokenVector* pTok;

	for (DWORD i = 0; i < loader.GetChildNodeCount(); ++i)
	{
		loader.SetChildNode(i);
		loader.GetCurrentNodeName(&stName);
		if (!loader.GetTokenInteger("vnum", &iVnum))
		{
			TraceError("ReadSpecialDropItemFile:Syntax error %s : no vnum, node %s", c_pszFileName, stName.c_str());
			loader.SetParentNode();
			continue;
		}

		vecSpecialData.clear();
		for (int k = 1; k < 256; ++k)
		{
			char buf[4];
			snprintf(buf, sizeof(buf), "%d", k);
			if (loader.GetTokenVector(buf, &pTok))
			{
				vecSpecialData.push_back(special_data(std::stoi(pTok->at(0)), std::stoi(pTok->at(1))));
				continue;
			}
			break;
		}

		if (vecSpecialData.size())
		{
			if (printLocalDatainSysser)
			{
				TraceError("                ");
				TraceError("ChestIndex: %d", iVnum);
				for (DWORD j = 0; j < vecSpecialData.size(); ++j)
					TraceError("Chest Data - Index: %d  ItemVnum: %d ItemCount: %d", j, vecSpecialData[j].itemVnum, vecSpecialData[j].count);
			}
			m_vecSpecialDrop.emplace(iVnum, vecSpecialData);
		}
		loader.SetParentNode();
	}
	return true;
}

bool CPythonWiki::ReadMobDropItemFile(const char *c_pszFileName)
{
	CTextFileLoader loader;
	if (!loader.Load(c_pszFileName))
		return false;

	int iVnum;
	std::vector<special_data> vecSpecialData;
	std::string stName;
	TTokenVector* pTok;

	for (DWORD i = 0; i < loader.GetChildNodeCount(); ++i)
	{
		loader.SetChildNode(i);
		loader.GetCurrentNodeName(&stName);
		if (!loader.GetTokenInteger("mob", &iVnum))
		{
			TraceError("ReadMobDropItemFile:Syntax error %s : no vnum, node %s", c_pszFileName, stName.c_str());
			loader.SetParentNode();
			continue;
		}

		vecSpecialData.clear();
		for (int k = 1; k < 256; ++k)
		{
			char buf[4];
			snprintf(buf, sizeof(buf), "%d", k);
			if (loader.GetTokenVector(buf, &pTok))
			{
				vecSpecialData.push_back(special_data(std::stoi(pTok->at(0)), std::stoi(pTok->at(1))));
				continue;
			}
			break;
		}

		if (vecSpecialData.size())
		{
			if (printLocalDatainSysser)
			{
				TraceError("                ");
				TraceError("MobIndex: %d", iVnum);
				for (DWORD j = 0; j < vecSpecialData.size(); ++j)
					TraceError("Mob Data - Index: %d  ItemVnum: %d ItemCount: %d", j, vecSpecialData[j].itemVnum, vecSpecialData[j].count);
			}
			m_vecMobDrop.emplace(iVnum, vecSpecialData);
		}
		loader.SetParentNode();
	}
	return true;
}

bool CompareLevel(character_data i, character_data j)
{
	return (i.level > j.level);
}

bool CompareLevelLow(character_data i, character_data j)
{
	return (i.level < j.level);
}

bool CPythonWiki::LoadItemTable(const char *c_szFileName)
{
	CMappedFile file;
	LPCVOID pvData;

	if (!CEterPackManager::Instance().Get(file, c_szFileName, &pvData))
		return false;

	DWORD dwFourCC, dwElements, dwDataSize, dwVersion = 0, dwStride = 0;
	DWORD s_adwItemProtoKey[4] =
	{
		173217,
		72619434,
		408587239,
		27973291
	};

	file.Read(&dwFourCC, sizeof(DWORD));
	if (dwFourCC == MAKEFOURCC('M', 'I', 'P', 'X'))
	{
		file.Read(&dwVersion, sizeof(DWORD));
		file.Read(&dwStride, sizeof(DWORD));
		if (dwVersion != 1)
		{
			TraceError("CPythonItem::LoadItemTable: invalid item_proto[%s] VERSION[%d]", c_szFileName, dwVersion);
			return false;
		}
		if (dwStride != sizeof(CItemData::TItemTable))
		{
			TraceError("CPythonItem::LoadItemTable: invalid item_proto[%s] STRIDE[%d] != sizeof(SItemTable)",c_szFileName, dwStride, sizeof(CItemData::TItemTable));
			return false;
		}
	}
	else if (dwFourCC != MAKEFOURCC('M', 'I', 'P', 'T'))
	{
		TraceError("CPythonItem::LoadItemTable: invalid item proto type %s", c_szFileName);
		return false;
	}

	file.Read(&dwElements, sizeof(DWORD));
	file.Read(&dwDataSize, sizeof(DWORD));
	BYTE* pbData = new BYTE[dwDataSize];
	file.Read(pbData, dwDataSize);

	CLZObject zObj;
	if (!CLZO::Instance().Decompress(zObj, pbData, s_adwItemProtoKey))
	{
		delete[] pbData;
		return false;
	}

	CItemData::TItemTable* table = (CItemData::TItemTable*)zObj.GetBuffer();
	for (DWORD i = 0; i < dwElements; ++i, ++table)
		CPythonWiki::Instance().LoadItem(table);
	delete[] pbData;

	for (DWORD j = 0; j < 4; j++)
	{
		std::stable_sort(m_vecWeapon[j].begin(), m_vecWeapon[j].end(), CompareLevel);
		std::stable_sort(m_vecArmor[j].begin(), m_vecArmor[j].end(), CompareLevel);
		std::stable_sort(m_vecHelmets[j].begin(), m_vecHelmets[j].end(), CompareLevel);
		std::stable_sort(m_vecShields[j].begin(), m_vecShields[j].end(), CompareLevel);
		std::stable_sort(m_vecEarrings[j].begin(), m_vecEarrings[j].end(), CompareLevel);
		std::stable_sort(m_vecBracelet[j].begin(), m_vecBracelet[j].end(), CompareLevel);
		std::stable_sort(m_vecNecklace[j].begin(), m_vecNecklace[j].end(), CompareLevel);
		std::stable_sort(m_vecShoes[j].begin(), m_vecShoes[j].end(), CompareLevel);
		std::stable_sort(m_vecBelt[j].begin(), m_vecBelt[j].end(), CompareLevel);
		std::stable_sort(m_vecTalisman[j].begin(), m_vecTalisman[j].end(), CompareLevel);
	}

	return true;
}

bool CPythonWiki::BlackList(DWORD vnum, DWORD type, DWORD subtype)
{
	switch (vnum)
	{
		// warrior & weapon blacklist. begin
		case 229:
		case 239:
		case 269:
		case 3189:
		case 3209:
		case 3179:
		// Ninja & weapon blacklist. begin
		case 1149:
		case 1159:
		case 4039:
		// Shaman & weapon blacklist. begin
		case 5139:
		case 5149:
		case 5159:
		case 7189:
		case 7179:
		// Sura & weapon blacklist. begin
		case 219:
		// Shields blacklist. begin
		case 13169:
		case 13189:
		// Shoes blacklist. begin
		case 15249:
			return false;
	}

	return true;
}

BYTE CPythonWiki::GetRefineLevel(DWORD vnum, DWORD type, DWORD subtype)
{
	if (type == CItemData::ITEM_TYPE_ARMOR && subtype == CItemData::ARMOR_PENDANT)
		return 20;

	constexpr DWORD darkVnums[] = {
		320,
		340,
		360,
		380,
		1190,
		1210,
		2210,
		2230,
		3230,
		3250,
		5170,
		5200,
		7310,
		7330,
		12780,
		12800,
		12820,
		12840,
		21210,
		21230,
		21250,
		21270,
		21310,
		21330,
		21350,
		21370
	};

	for (UINT i = 0; i < _countof(darkVnums); i++)
	{
		if (vnum >= darkVnums[i] && vnum <= darkVnums[i] + 15)
			return 15;
	}

	return 9;
}

refineTable* CPythonWiki::GetRefineItem(DWORD index)
{
	const auto it = m_vecRefineTable.find(index);
	if (it != m_vecRefineTable.end())
	{
		return it->second;
	}
	return NULL;
}

bool CPythonWiki::LoadRefineTable(const char *c_szFileName)
{
	CMappedFile File;
	LPCVOID pData;
	if (!CEterPackManager::Instance().Get(File, c_szFileName, &pData))
		return false;

	CMemoryTextFileLoader textFileLoader;
	textFileLoader.Bind(File.Size(), pData);

	CTokenVector TokenVector;
	for (DWORD i = 0; i < textFileLoader.GetLineCount(); ++i)
	{
		if (textFileLoader.GetLineString(i)[0] == '#')
			continue;

		if (!textFileLoader.SplitLine(i, &TokenVector, "\t"))
			continue;

		if (TokenVector.size() != 15)
		{
			TraceError("CPythonWiki::LoadRefineTable(%s) - StrangeLine in %d\n", c_szFileName, i);
			continue;
		}

		refineTable* p = new refineTable;
		memset(p, 0, sizeof(refineTable));

		p->id = (DWORD)atoi(TokenVector[0].c_str());
		p->refine_count = 0;

		int row = 1;
		for (DWORD j = 0; j < MAX_REFINE_ITEM;++j)
		{
			p->item_vnums[j] = (DWORD)atoi(TokenVector[row].c_str());
		
			if (p->item_vnums[j] != 0){
				p->refine_count = j + 1;
			}
			

			row += 1;
			p->item_count[j] = (DWORD)atoi(TokenVector[row].c_str());
			row += 1;
		}

		p->cost = (DWORD)atoi(TokenVector[11].c_str());
		p->prob = (DWORD)atoi(TokenVector[14].c_str());
		m_vecRefineTable.insert(std::make_pair(p->id, p));
	}
	return true;
}

bool isFirstItem(DWORD itemVnum, const char *szname)
{
	std::string str = szname;

	if (str.find("+0") != std::string::npos)
		return true;
	return false;
}

bool isLastItem(DWORD itemVnum, const char *szname, BYTE itemType, BYTE itemSubtype)
{
	std::string str = szname;

	DWORD maxRefine = CPythonWiki::Instance().GetRefineLevel(itemVnum, itemType, itemSubtype);
	std::string strrefine = "+";
	strrefine += std::to_string(maxRefine);

	if (str.find(strrefine.c_str()) != std::string::npos)
		return true;

	return false;
}

void CPythonWiki::ListReverse()
{
	for (DWORD j = 0; j < 3; j++)
	{
		std::stable_sort(m_vecStoneCategory[j].begin(), m_vecStoneCategory[j].end(), CompareLevelLow);
		std::stable_sort(m_vecBossCategory[j].begin(), m_vecBossCategory[j].end(), CompareLevelLow);
		std::stable_sort(m_vecMonsterCategory[j].begin(), m_vecMonsterCategory[j].end(), CompareLevelLow);
	}
}

bool BlackListMonster(DWORD vnum)
{
	if (vnum >= 8001 && vnum <= 8014)
		return false;

	if (vnum >= 8024 && vnum <= 8027)
		return false;

	if (vnum >= 8051 && vnum <= 8058 || vnum == 8062)
		return false;

	if (vnum >= 8494 && vnum <= 8497)
		return false;

	switch (vnum)
	{
		case 191:
		case 192:
		case 193:
		case 194:
		case 491:
		case 492:
		case 493:
		case 494:
		case 533:
		case 591:
		case 691:
		case 791:
		case 1091:
		case 1092:
		case 1093:
		case 2191:
		case 1304:
		case 2206:
		case 1901:
		case 1191:
		case 2091:
		case 2092:
		case 2307:
		case 2493:
		case 2598:
		case 3190:
		case 3191:
		case 3290:
		case 3291:
		case 3390:
		case 3391:
		case 3490:
		case 3491:
		case 3590:
		case 3591:
		case 3690:
		case 3691:
		case 3790:
		case 3791:
		case 3890:
		case 3891:
		case 4380:
		case 4381:
		case 4382:
		case 4383:
		case 4384:
		case 4385:
		case 4386:
		case 4387:
		case 4388:
		case 6091:
		case 6191:

		return false;
	}
	return true;
}

void CPythonWiki::LoadMonster(CPythonNonPlayer::TMobTable* monster)
{
	if (BlackListMonster(monster->dwVnum))
		return;

	if (monster->bType == 0 || monster->bType == 2)
	{
		if (monster->bLevel >= 1 && monster->bLevel <= 99)
		{
			if (monster->bType == 2)
				m_vecStoneCategory[0].emplace_back(character_data(monster->dwVnum, monster->bLevel));
			else if (monster->bRank >= CPythonNonPlayer::MOB_RANK_S_KNIGHT)
				m_vecBossCategory[0].emplace_back(character_data(monster->dwVnum, monster->bLevel));
			else
				m_vecMonsterCategory[0].emplace_back(character_data(monster->dwVnum, monster->bLevel));
		}
		else if (monster->bLevel >= 100 && monster->bLevel <= 120)
		{
			if (monster->bType == 2)
				m_vecStoneCategory[1].emplace_back(character_data(monster->dwVnum, monster->bLevel));
			else if (monster->bRank >= CPythonNonPlayer::MOB_RANK_S_KNIGHT)
				m_vecBossCategory[1].emplace_back(character_data(monster->dwVnum, monster->bLevel));
			else
				m_vecMonsterCategory[1].emplace_back(character_data(monster->dwVnum, monster->bLevel));
		}
		else if (monster->bLevel >= 121)
		{
			if (monster->bType == 2)
				m_vecStoneCategory[2].emplace_back(character_data(monster->dwVnum, monster->bLevel));
			else if (monster->bRank >= CPythonNonPlayer::MOB_RANK_S_KNIGHT)
				m_vecBossCategory[2].emplace_back(character_data(monster->dwVnum, monster->bLevel));
			else
				m_vecMonsterCategory[2].emplace_back(character_data(monster->dwVnum, monster->bLevel));
		}
	}
}

void CPythonWiki::ClearData()
{
	std::vector<std::vector<character_data>*> vecArray = {
		&m_vecBossCategory[0],
		&m_vecBossCategory[1],
		&m_vecBossCategory[2],
		&m_vecMonsterCategory[0],
		&m_vecMonsterCategory[1],
		&m_vecMonsterCategory[2],
		&m_vecStoneCategory[0],
		&m_vecStoneCategory[1],
		&m_vecStoneCategory[2],
		&m_vecWeapon[0],
		&m_vecArmor[0],
		&m_vecHelmets[0],
		&m_vecShields[0],
		&m_vecEarrings[0],
		&m_vecBracelet[0],
		&m_vecNecklace[0],
		&m_vecShoes[0],
		&m_vecBelt[0],
		&m_vecTalisman[0]
	};

	for (auto& i : vecArray)
	{
		i->clear();
	}
}

void CPythonWiki::LoadItem(CItemData::TItemTable* item)
{
	constexpr BYTE flagList[CRaceData::JOB_MAX_NUM] = { CItemData::ITEM_ANTIFLAG_WARRIOR, CItemData::ITEM_ANTIFLAG_ASSASSIN, CItemData::ITEM_ANTIFLAG_SHAMAN, CItemData::ITEM_ANTIFLAG_SURA };

	if (isLastItem(item->dwVnum, item->szLocaleName, item->bType, item->bSubType))
	{
		if (!BlackList(item->dwVnum, item->bType, item->bSubType))
			return;

		DWORD itemLevel = 0;
		for (DWORD j = 0; j < CItemData::ITEM_LIMIT_MAX_NUM; j++)
		{
			if (item->aLimits[j].bType == CItemData::LIMIT_LEVEL)
			{
				itemLevel = item->aLimits[j].lValue;
				break;
			}
		}

		if (item->bType == CItemData::ITEM_TYPE_WEAPON)
		{
			for (BYTE j = 0; j < CRaceData::JOB_MAX_NUM; ++j)
			{
				if (!(item->dwAntiFlags & flagList[j]))
					m_vecWeapon[j].emplace_back(character_data(item->dwVnum, itemLevel));
			}
		}
		else if (item->bType == CItemData::ITEM_TYPE_ARMOR)
		{
			if (item->bSubType == CItemData::ARMOR_BODY)
			{
				for (BYTE j = 0; j < CRaceData::JOB_MAX_NUM; ++j)
				{
					if (!(item->dwAntiFlags & flagList[j]))
						m_vecArmor[j].emplace_back(character_data(item->dwVnum, itemLevel));
				}
			}
			else if (item->bSubType == CItemData::ARMOR_HEAD)
			{
				for (BYTE j = 0; j < CRaceData::JOB_MAX_NUM; ++j)
				{
					if (!(item->dwAntiFlags & flagList[j]))
						m_vecHelmets[j].emplace_back(character_data(item->dwVnum, itemLevel));
				}
			}
			else if (item->bSubType == CItemData::ARMOR_SHIELD)
			{
				for (BYTE j = 0; j < CRaceData::JOB_MAX_NUM; ++j)
				{
					if (!(item->dwAntiFlags & flagList[j]))
						m_vecShields[j].emplace_back(character_data(item->dwVnum, itemLevel));
				}
			}
			else if (item->bSubType == CItemData::ARMOR_WRIST)
			{
				for (BYTE j = 0; j < CRaceData::JOB_MAX_NUM; ++j)
				{
					if (!(item->dwAntiFlags & flagList[j]))
						m_vecBracelet[j].emplace_back(character_data(item->dwVnum, itemLevel));
				}
			}
			else if (item->bSubType == CItemData::ARMOR_FOOTS)
			{
				for (BYTE j = 0; j < CRaceData::JOB_MAX_NUM; ++j)
				{
					if (!(item->dwAntiFlags & flagList[j]))
						m_vecShoes[j].emplace_back(character_data(item->dwVnum, itemLevel));
				}
			}
			else if (item->bSubType == CItemData::ARMOR_NECK)
			{
				for (BYTE j = 0; j < CRaceData::JOB_MAX_NUM; ++j)
				{
					if (!(item->dwAntiFlags & flagList[j]))
						m_vecNecklace[j].emplace_back(character_data(item->dwVnum, itemLevel));
				}
			}
			else if (item->bSubType == CItemData::ARMOR_EAR)
			{
				for (BYTE j = 0; j < CRaceData::JOB_MAX_NUM; ++j)
				{
					if (!(item->dwAntiFlags & flagList[j]))
						m_vecEarrings[j].emplace_back(character_data(item->dwVnum, itemLevel));
				}
			}
			else if (item->bSubType == CItemData::ARMOR_BELT)
			{
				for (BYTE j = 0; j < CRaceData::JOB_MAX_NUM; ++j)
				{
					if (!(item->dwAntiFlags & flagList[j]))
						m_vecBelt[j].emplace_back(character_data(item->dwVnum, itemLevel));
				}
			}
#ifdef ENABLE_PENDANT_SYSTEM
			else if (item->bSubType == CItemData::ARMOR_PENDANT)
			{
				for (BYTE j = 0; j < CRaceData::JOB_MAX_NUM; ++j)
				{
					if (!(item->dwAntiFlags & flagList[j]))
						m_vecTalisman[j].emplace_back(character_data(item->dwVnum, itemLevel));
				}
			}
#endif
		}
	}
}

PyObject *wikiGetRefineItems(PyObject *poSelf, PyObject *poArgs)
{
	int iRefineIndex;
	if (!PyTuple_GetInteger(poArgs, 0, &iRefineIndex))
		return Py_BadArgument();

	const auto item = CPythonWiki::Instance().GetRefineItem(iRefineIndex);
	if (!item)
		return Py_BuildValue("i", 0);

	return Py_BuildValue("iiiiiiiiiiiiii", item->id,item->item_vnums[0], item->item_count[0],item->item_vnums[1], item->item_count[1],item->item_vnums[2], item->item_count[2],item->item_vnums[3], item->item_count[3],item->item_vnums[4], item->item_count[4],item->cost, item->prob, item->refine_count);
}

PyObject *wikiIsBlackList(PyObject *poSelf, PyObject *poArgs)
{
	int iItemVnum;
	if (!PyTuple_GetInteger(poArgs, 0, &iItemVnum))
		return Py_BadArgument();

	int iType = 0; // Fix
	if (!PyTuple_GetInteger(poArgs, 1, &iItemVnum))
		return Py_BadArgument();

	int iSubtype = 0; // Fix
	if (!PyTuple_GetInteger(poArgs, 2, &iItemVnum))
		return Py_BadArgument();

	return Py_BuildValue("i", CPythonWiki::Instance().BlackList(iItemVnum, iType, iSubtype));
}

PyObject *wikiGetCategorySize(PyObject *poSelf, PyObject *poArgs)
{
	int iType;
	if (!PyTuple_GetInteger(poArgs, 0, &iType))
		return Py_BadArgument();

	int iCategoryType;
	if (!PyTuple_GetInteger(poArgs, 1, &iCategoryType))
		return Py_BadArgument();

	if (iType >= 0 && iType <= 3)
	{
		if (iCategoryType == 0)
			return Py_BuildValue("i", CPythonWiki::Instance().m_vecWeapon[iType].size());
		else if (iCategoryType == 1)
			return Py_BuildValue("i", CPythonWiki::Instance().m_vecArmor[iType].size());
		else if (iCategoryType == 2)
			return Py_BuildValue("i", CPythonWiki::Instance().m_vecHelmets[iType].size());
		else if (iCategoryType == 3)
			return Py_BuildValue("i", CPythonWiki::Instance().m_vecShields[iType].size());
		else if (iCategoryType == 4)
			return Py_BuildValue("i", CPythonWiki::Instance().m_vecEarrings[iType].size());
		else if (iCategoryType == 5)
			return Py_BuildValue("i", CPythonWiki::Instance().m_vecBracelet[iType].size());
		else if (iCategoryType == 6)
			return Py_BuildValue("i", CPythonWiki::Instance().m_vecNecklace[iType].size());
		else if (iCategoryType == 7)
			return Py_BuildValue("i", CPythonWiki::Instance().m_vecShoes[iType].size());
		else if (iCategoryType == 8)
			return Py_BuildValue("i", CPythonWiki::Instance().m_vecBelt[iType].size());
		else if (iCategoryType == 9)
			return Py_BuildValue("i", CPythonWiki::Instance().m_vecTalisman[iType].size());
	}

	return Py_BuildValue("i", 0);
}

PyObject *wikiGetCategoryData(PyObject *poSelf, PyObject *poArgs)
{
	int iType;
	if (!PyTuple_GetInteger(poArgs, 0, &iType))
		return Py_BadArgument();

	int iCategoryType;
	if (!PyTuple_GetInteger(poArgs, 1, &iCategoryType))
		return Py_BadArgument();

	int iIndex;
	if (!PyTuple_GetInteger(poArgs, 2, &iIndex))
		return Py_BadArgument();

	if (iType >= 0 && iType <= 3)
	{
		if (iCategoryType == 0)
			return Py_BuildValue("i", CPythonWiki::Instance().m_vecWeapon[iType][iIndex].itemVnum);
		else if (iCategoryType == 1)
			return Py_BuildValue("i", CPythonWiki::Instance().m_vecArmor[iType][iIndex].itemVnum);
		else if (iCategoryType == 2)
			return Py_BuildValue("i", CPythonWiki::Instance().m_vecHelmets[iType][iIndex].itemVnum);
		else if (iCategoryType == 3)
			return Py_BuildValue("i", CPythonWiki::Instance().m_vecShields[iType][iIndex].itemVnum);
		else if (iCategoryType == 4)
			return Py_BuildValue("i", CPythonWiki::Instance().m_vecEarrings[iType][iIndex].itemVnum);
		else if (iCategoryType == 5)
			return Py_BuildValue("i", CPythonWiki::Instance().m_vecBracelet[iType][iIndex].itemVnum);
		else if (iCategoryType == 6)
			return Py_BuildValue("i", CPythonWiki::Instance().m_vecNecklace[iType][iIndex].itemVnum);
		else if (iCategoryType == 7)
			return Py_BuildValue("i", CPythonWiki::Instance().m_vecShoes[iType][iIndex].itemVnum);
		else if (iCategoryType == 8)
			return Py_BuildValue("i", CPythonWiki::Instance().m_vecBelt[iType][iIndex].itemVnum);
		else if (iCategoryType == 9)
			return Py_BuildValue("i", CPythonWiki::Instance().m_vecTalisman[iType][iIndex].itemVnum);
	}

	return Py_BuildValue("i", 0);
}

PyObject *wikiReadData(PyObject *poSelf, PyObject *poArgs)
{
	char *locale;
	if (!PyTuple_GetString(poArgs, 0, &locale))
		return Py_BuildException();

	CPythonWiki::Instance().ReadData(locale);

	return Py_BuildNone();
}

PyObject *wikiGetRefineMaxLevel(PyObject *poSelf, PyObject *poArgs)
{
	int iItemVnum;
	if (!PyTuple_GetInteger(poArgs, 0, &iItemVnum))
		return Py_BuildException();

	CItemManager::Instance().SelectItemData(iItemVnum);
	CItemData* pItemData = CItemManager::Instance().GetSelectedItemDataPointer();

	if (!pItemData)
		return Py_BuildValue("i", CPythonWiki::Instance().GetRefineLevel(iItemVnum, 0, 0));

	return Py_BuildValue("i", CPythonWiki::Instance().GetRefineLevel(iItemVnum, pItemData->GetType(), pItemData->GetSubType()));
}

PyObject *wikiGetChestSize(PyObject *poSelf, PyObject *poArgs)
{
	int iType;
	if (!PyTuple_GetInteger(poArgs, 0, &iType))
		return Py_BuildException();

	if (iType == 0)
		return Py_BuildValue("i", _countof(bossChests));
	else if (iType == 1)
		return Py_BuildValue("i", _countof(dungeonChests));
	else if (iType == 2)
		return Py_BuildValue("i", _countof(otherChests));
	else if (iType == 3)
		return Py_BuildValue("i", _countof(eventChests));

	return Py_BuildValue("i", 0);
}

PyObject *wikiGetChestData(PyObject *poSelf, PyObject *poArgs)
{
	int iType;
	if (!PyTuple_GetInteger(poArgs, 0, &iType))
		return Py_BuildException();

	int iIndex;
	if (!PyTuple_GetInteger(poArgs, 1, &iIndex))
		return Py_BuildException();

	if (iType == 0)
		return Py_BuildValue("ii", bossChests[iIndex][0], bossChests[iIndex][1]);
	else if (iType == 1)
		return Py_BuildValue("ii", dungeonChests[iIndex][0], dungeonChests[iIndex][1]);
	else if (iType == 2)
		return Py_BuildValue("ii", otherChests[iIndex][0], otherChests[iIndex][1]);
	else if (iType == 3)
		return Py_BuildValue("ii", eventChests[iIndex][0], eventChests[iIndex][1]);

	return Py_BuildValue("ii", 0,0);
}

PyObject *wikiGetSpecialInfoSize(PyObject *poSelf, PyObject *poArgs)
{
	int iItemVnum;
	if (!PyTuple_GetInteger(poArgs, 0, &iItemVnum))
		return Py_BuildException();

	const auto it = CPythonWiki::Instance().m_vecSpecialDrop.find(iItemVnum);
	if (it != CPythonWiki::Instance().m_vecSpecialDrop.end())
		return Py_BuildValue("i", it->second.size());

	return Py_BuildValue("i", 0);
}

PyObject *wikiGetSpecialInfoData(PyObject *poSelf, PyObject *poArgs)
{
	int iItemVnum;
	if (!PyTuple_GetInteger(poArgs, 0, &iItemVnum))
		return Py_BuildException();

	int iIndex;
	if (!PyTuple_GetInteger(poArgs, 1, &iIndex))
		return Py_BuildException();

	const auto it = CPythonWiki::Instance().m_vecSpecialDrop.find(iItemVnum);
	if (it != CPythonWiki::Instance().m_vecSpecialDrop.end())
		return Py_BuildValue("ii", it->second[iIndex].itemVnum, it->second[iIndex].count);

	return Py_BuildValue("ii", 0, 0);
}

PyObject *wikiGetMobInfoSize(PyObject *poSelf, PyObject *poArgs)
{
	int iItemVnum;
	if (!PyTuple_GetInteger(poArgs, 0, &iItemVnum))
		return Py_BuildException();

	const auto it = CPythonWiki::Instance().m_vecMobDrop.find(iItemVnum);
	if (it != CPythonWiki::Instance().m_vecMobDrop.end())
		return Py_BuildValue("i", it->second.size());

	return Py_BuildValue("i", 0);
}

PyObject *wikiGetMobInfoData(PyObject *poSelf, PyObject *poArgs)
{
	int iItemVnum;
	if (!PyTuple_GetInteger(poArgs, 0, &iItemVnum))
		return Py_BuildException();

	int iIndex;
	if (!PyTuple_GetInteger(poArgs, 1, &iIndex))
		return Py_BuildException();

	const auto it = CPythonWiki::Instance().m_vecMobDrop.find(iItemVnum);
	if (it == CPythonWiki::Instance().m_vecMobDrop.end())
		return Py_BuildValue("ii",0,0);

	return Py_BuildValue("ii", it->second[iIndex].itemVnum, it->second[iIndex].count);
}

PyObject *wikiGetBossSize(PyObject *poSelf, PyObject *poArgs)
{
	int iType;
	if (!PyTuple_GetInteger(poArgs, 0, &iType))
		return Py_BadArgument();

	if (iType == 3) // event boss
		return Py_BuildValue("i", (sizeof(eventBoss) / sizeof(eventBoss[0])));

	return Py_BuildValue("i", CPythonWiki::Instance().m_vecBossCategory[iType].size());
}

PyObject *wikiGetBossData(PyObject *poSelf, PyObject *poArgs)
{
	int iType;
	if (!PyTuple_GetInteger(poArgs, 0, &iType))
		return Py_BadArgument();

	int iIndex;
	if (!PyTuple_GetInteger(poArgs, 1, &iIndex))
		return Py_BadArgument();

	if (iType == 3) // event boss
		return Py_BuildValue("i", eventBoss[iIndex]);

	return Py_BuildValue("i", CPythonWiki::Instance().m_vecBossCategory[iType][iIndex]);
}

PyObject *wikiCostumeSize(PyObject *poSelf, PyObject *poArgs)
{
	int iType;
	if (!PyTuple_GetInteger(poArgs, 0, &iType))
		return Py_BadArgument();

	const auto it = m_CostumeData.find(iType);
	if (it != m_CostumeData.end())
		return Py_BuildValue("i", it->second.size());

	return Py_BuildValue("i", 0);
}
PyObject *wikiCostumeData(PyObject *poSelf, PyObject *poArgs)
{
	int iType;
	if (!PyTuple_GetInteger(poArgs, 0, &iType))
		return Py_BadArgument();

	int iIndex;
	if (!PyTuple_GetInteger(poArgs, 1, &iIndex))
		return Py_BadArgument();

	const auto it = m_CostumeData.find(iType);
	if (it != m_CostumeData.end())
		return Py_BuildValue("i", it->second[iIndex]);

	return Py_BuildValue("i", 0);
}

PyObject *wikiGetMonsterSize(PyObject *poSelf, PyObject *poArgs)
{
	int iType;
	if (!PyTuple_GetInteger(poArgs, 0, &iType))
		return Py_BadArgument();

	return Py_BuildValue("i", CPythonWiki::Instance().m_vecMonsterCategory[iType].size());
}

PyObject *wikiGetMonsterData(PyObject *poSelf, PyObject *poArgs)
{
	int iType;
	if (!PyTuple_GetInteger(poArgs, 0, &iType))
		return Py_BadArgument();

	int iIndex;
	if (!PyTuple_GetInteger(poArgs, 1, &iIndex))
		return Py_BadArgument();

	return Py_BuildValue("i", CPythonWiki::Instance().m_vecMonsterCategory[iType][iIndex]);
}

PyObject *wikiGetStoneSize(PyObject *poSelf, PyObject *poArgs)
{
	int iType;
	if (!PyTuple_GetInteger(poArgs, 0, &iType))
		return Py_BadArgument();

	return Py_BuildValue("i", CPythonWiki::Instance().m_vecStoneCategory[iType].size());
}

PyObject *wikiGetStoneData(PyObject *poSelf, PyObject *poArgs)
{
	int iType;
	if (!PyTuple_GetInteger(poArgs, 0, &iType))
		return Py_BadArgument();

	int iIndex;
	if (!PyTuple_GetInteger(poArgs, 1, &iIndex))
		return Py_BadArgument();

	return Py_BuildValue("i", CPythonWiki::Instance().m_vecStoneCategory[iType][iIndex]);
}

PyObject *wikiGetItemDropFromChest(PyObject *poSelf, PyObject *poArgs)
{
	int szItemVnum = 0;
	if (!PyTuple_GetInteger(poArgs, 0, &szItemVnum))
		return Py_BadArgument();

	bool szIsRefineItem = false;
	if (!PyTuple_GetBoolean(poArgs, 1, &szIsRefineItem))
		return Py_BadArgument();

	PyObject *poList = PyList_New(0);

	const BYTE refineLevel = szIsRefineItem ? CPythonWiki::Instance().GetRefineLevel(szItemVnum, 0, 0) : 0;
	const auto m_vec_ItemRange = CPythonWiki::Instance().GetSpecialDrop();

	for (const auto& [chestVnum, chestData] : m_vec_ItemRange)
	{
		if (chestData.size() > 0)
		{
			if (szIsRefineItem)
			{
				for (const auto& dataItem : chestData)
				{
					if (szItemVnum >= dataItem.itemVnum && szItemVnum <= dataItem.itemVnum + refineLevel)
					{
						const auto obj = Py_BuildValue("i", chestVnum);
						PyList_Append(poList, obj);
						break;
					}
				}
			}
			else
			{
				for (const auto& dataItem : chestData)
				{
					if (szItemVnum == dataItem.itemVnum)
					{
						const auto obj = Py_BuildValue("i", chestVnum);
						PyList_Append(poList, obj);
						break;
					}

				}
			}

		}
	}
	return Py_BuildValue("O", poList);
}

PyObject *wikiGetItemDropFromMonster(PyObject *poSelf, PyObject *poArgs)
{
	int szItemVnum = 0;
	if (!PyTuple_GetInteger(poArgs, 0, &szItemVnum))
		return Py_BadArgument();

	bool szIsRefineItem = false;
	if (!PyTuple_GetBoolean(poArgs, 1, &szIsRefineItem))
		return Py_BadArgument();

	PyObject *poList = PyList_New(0);
	const BYTE refineLevel = szIsRefineItem ? CPythonWiki::Instance().GetRefineLevel(szItemVnum, 0, 0) : 0;
	const auto m_vec_ItemRange = CPythonWiki::Instance().GetMobDrop();
	for (const auto& [mobVnum, mobData] : m_vec_ItemRange)
	{
		if (mobData.size() > 0)
		{
			if (szIsRefineItem)
			{
				for (const auto& dataItem : mobData)
				{
					if (szItemVnum >= dataItem.itemVnum && szItemVnum <= dataItem.itemVnum + refineLevel)
					{
						const auto obj = Py_BuildValue("i", mobVnum);
						PyList_Append(poList, obj);
						break;
					}
				}
			}
			else
			{
				for (const auto& dataItem : mobData)
				{
					if (szItemVnum == dataItem.itemVnum)
					{
						const auto obj = Py_BuildValue("i", mobVnum);
						PyList_Append(poList, obj);
						break;
					}

				}
			}
		}
	}

	return Py_BuildValue("O", poList);
}

void initWiki()
{
	static PyMethodDef s_methods[] =
	{
		{ "GetRefineItems",			wikiGetRefineItems,			METH_VARARGS },
		{ "IsBlackList",			wikiIsBlackList,			METH_VARARGS },

		{ "GetCategorySize",		wikiGetCategorySize,		METH_VARARGS },
		{ "GetCategoryData",		wikiGetCategoryData,		METH_VARARGS },

		{ "GetBossSize",			wikiGetBossSize,			METH_VARARGS },
		{ "GetBossData",			wikiGetBossData,			METH_VARARGS },

		{ "GetMonsterSize",			wikiGetMonsterSize,			METH_VARARGS },
		{ "GetMonsterData",			wikiGetMonsterData,			METH_VARARGS },

		{ "GetCostumeSize",			wikiCostumeSize,			METH_VARARGS },
		{ "GetCostumeData",			wikiCostumeData,			METH_VARARGS },

		{ "GetStoneSize",			wikiGetStoneSize,			METH_VARARGS },
		{ "GetStoneData",			wikiGetStoneData,			METH_VARARGS },

		{ "GetChestSize",			wikiGetChestSize,			METH_VARARGS },
		{ "GetChestData",			wikiGetChestData,			METH_VARARGS },

		{ "GetSpecialInfoSize",		wikiGetSpecialInfoSize,		METH_VARARGS },
		{ "GetSpecialInfoData",		wikiGetSpecialInfoData,		METH_VARARGS },

		{ "GetMobInfoSize",			wikiGetMobInfoSize,			METH_VARARGS },
		{ "GetMobInfoData",			wikiGetMobInfoData,			METH_VARARGS },

		{ "ReadData",				wikiReadData,				METH_VARARGS },

		{ "GetRefineMaxLevel",		wikiGetRefineMaxLevel,		METH_VARARGS },

		{ "GetItemDropFromChest",	wikiGetItemDropFromChest,	METH_VARARGS },
		{ "GetItemDropFromMonster",	wikiGetItemDropFromMonster,	METH_VARARGS },

		{ nullptr, nullptr },
	};

	PyObject *poModule = Py_InitModule("wiki", s_methods);
}
#endif
