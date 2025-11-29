if __USE_DYNAMIC_MODULE__:
	import pyapi

app = __import__(pyapi.GetModuleName("app"))
chr = __import__(pyapi.GetModuleName("chr"))
player = __import__(pyapi.GetModuleName("player"))
net = __import__(pyapi.GetModuleName("net"))
pack = __import__(pyapi.GetModuleName("pack"))

import ui
import uiScriptLocale
import dbg
import snd
import mouseModule
import wndMgr
import skill
import playerSettingModule
import quest
import localeInfo
import uiToolTip
import constInfo
import emotion
import chat

if app.ENABLE_RENEWAL_QUEST:
	import math
	import uiQuest

if app.ENABLE_RENEWAL_BONUS_BOARD:
	import item
	from uiToolTip import ItemToolTip

if app.ENABLE_SKILL_COLOR_SYSTEM:
	import uiSkillColor

SHOW_ONLY_ACTIVE_SKILL = False

HIDE_SUPPORT_SKILL_POINT = True

SHOW_LIMIT_SUPPORT_SKILL_LIST = [121, 122, 123, 124, 126, 127, 128, 129, 130, 131, 137, 138, 139, 140]

FACE_IMAGE_DICT = {
	playerSettingModule.RACE_WARRIOR_M : "icon/face/warrior_m.tga",
	playerSettingModule.RACE_WARRIOR_W : "icon/face/warrior_w.tga",
	playerSettingModule.RACE_ASSASSIN_M : "icon/face/assassin_m.tga",
	playerSettingModule.RACE_ASSASSIN_W : "icon/face/assassin_w.tga",
	playerSettingModule.RACE_SURA_M : "icon/face/sura_m.tga",
	playerSettingModule.RACE_SURA_W : "icon/face/sura_w.tga",
	playerSettingModule.RACE_SHAMAN_M : "icon/face/shaman_m.tga",
	playerSettingModule.RACE_SHAMAN_W : "icon/face/shaman_w.tga",
}

def unsigned32(n):
	return n & 0xFFFFFFFFL

if app.ENABLE_RENEWAL_BONUS_BOARD:
	bonus_list = [
		[localeInfo.BONUS_BOARD_CATEGORY_1,
			[
				[item.APPLY_ATTBONUS_HUMAN, 43],
				[item.APPLY_ATTBONUS_MONSTER, 53],
				[item.APPLY_ATTBONUS_ANIMAL, 44],
				[item.APPLY_ATTBONUS_ORC, 45],
				[item.APPLY_ATTBONUS_MILGYO, 46],
				[item.APPLY_ATTBONUS_UNDEAD, 47],
				[item.APPLY_ATTBONUS_DEVIL, 48],
				[item.APPLY_ATTBONUS_METIN, 141],
				[item.APPLY_ATTBONUS_BOSS, 164],
				[item.APPLY_ATT_GRADE_BONUS, 95],
				[item.APPLY_DEF_GRADE_BONUS, 96],
				[item.APPLY_SKILL_DAMAGE_BONUS, 121],
				[item.APPLY_NORMAL_HIT_DAMAGE_BONUS, 122],
				[item.APPLY_SKILL_DEFEND_BONUS, 123],
				[item.APPLY_NORMAL_HIT_DEFEND_BONUS, 124],
				[item.APPLY_MELEE_MAGIC_ATTBONUS_PER, 130],
				[item.APPLY_MAGIC_ATTBONUS_PER, 97],
				[item.APPLY_CRITICAL_PCT, 40],
				[item.APPLY_PENETRATE_PCT, 41],
				[item.APPLY_ANTI_CRITICAL_PCT, 134],
				[item.APPLY_ANTI_PENETRATE_PCT, 135],
			]
		],
		[localeInfo.BONUS_BOARD_CATEGORY_2,
			[
				[item.APPLY_RESIST_MAGIC, 77],
				[item.APPLY_RESIST_ELEC, 76],
				[item.APPLY_ATTBONUS_ELEC, 136],
				[item.APPLY_RESIST_ICE, 131],
				[item.APPLY_ATTBONUS_ICE, 51],
				[item.APPLY_RESIST_DARK, 133],
				[item.APPLY_ATTBONUS_DARK, 139],
				[item.APPLY_RESIST_FIRE, 75],
				[item.APPLY_ATTBONUS_FIRE, 50],
				[item.APPLY_RESIST_WIND, 78],
				[item.APPLY_ATTBONUS_WIND, 137],
				[item.APPLY_RESIST_EARTH, 132],
				[item.APPLY_ATTBONUS_EARTH, 138],
			]
		],
		[localeInfo.BONUS_BOARD_CATEGORY_3,
			[
				[item.APPLY_ATTBONUS_WARRIOR, 54],
				[item.APPLY_RESIST_WARRIOR, 59],
				[item.APPLY_ATTBONUS_ASSASSIN, 55],
				[item.APPLY_RESIST_ASSASSIN, 60],
				[item.APPLY_ATTBONUS_SURA, 56],
				[item.APPLY_RESIST_SURA, 61],
				[item.APPLY_ATTBONUS_SHAMAN, 57],
				[item.APPLY_RESIST_SHAMAN, 62],
			]
		],
		[localeInfo.BONUS_BOARD_CATEGORY_4,
			[
				[item.APPLY_RESIST_SWORD, 69],
				[item.APPLY_RESIST_TWOHAND, 70],
				[item.APPLY_RESIST_DAGGER, 71],
				[item.APPLY_RESIST_BELL, 72],
				[item.APPLY_RESIST_FAN, 73],
				[item.APPLY_RESIST_BOW, 74],
			]
		],
		[localeInfo.BONUS_BOARD_CATEGORY_5,
			[
				[item.APPLY_CAST_SPEED, 21],
				[item.APPLY_STUN_PCT, 38],
				[item.APPLY_SLOW_PCT, 39],
				[item.APPLY_POISON_PCT, 37],
				[item.APPLY_POISON_REDUCE, 81],
				[item.APPLY_STEAL_HP, 63],
				[item.APPLY_STEAL_SP, 64],
				[item.APPLY_HP_REGEN, 32],
				[item.APPLY_SP_REGEN, 33],
				[item.APPLY_BLOCK, 67],
				[item.APPLY_DODGE, 68],
				[item.APPLY_REFLECT_MELEE, 79],
				[item.APPLY_KILL_HP_RECOVER, 87],
				[item.APPLY_KILL_SP_RECOVER, 82],
				[item.APPLY_EXP_DOUBLE_BONUS, 83],
				[item.APPLY_GOLD_DOUBLE_BONUS, 84],
				[item.APPLY_ITEM_DROP_BONUS, 85],
			]
		],
	]

	stat_list = [
		[localeInfo.STATS_BOARD_JINNO_PLAYERS, player.POINT_BLUE_PLAYER_KILLED],
		[localeInfo.STATS_BOARD_SHINSOO_PLAYERS, player.POINT_YELLOW_PLAYER_KILLED],
		[localeInfo.STATS_BOARD_CHUNJO_PLAYERS, player.POINT_RED_PLAYER_KILLED],
		[localeInfo.STATS_BOARD_PLAYERS_KILLED, player.POINT_ALL_PLAYER_KILLED],
		[localeInfo.STATS_BOARD_DUELS_WON, player.POINT_KILL_DUELWON],
		[localeInfo.STATS_BOARD_LOST_DUELS, player.POINT_KILL_DUELLOST],
		[localeInfo.STATS_BOARD_KILLED_MONSTER, player.POINT_MONSTER_KILLED],
		[localeInfo.STATS_BOARD_DEFEATED_BOSSES, player.POINT_BOSS_KILLED],
		[localeInfo.STATS_BOARD_DESTROYED_STONES, player.POINT_STONE_KILLED]
	]

if app.ENABLE_RENEWAL_QUEST:
	quest_slot_listbar = {
		"name" : "Quest_Slot", "type" : "listbar",
		"x" : 0, "y" : 0,
		"width" : 210, "height" : 20,

		"text" : "Quest title",
		"align" : "left",

		"horizontal_align" : "left",
		"vertical_align" : "left",
		"text_horizontal_align" : "left",
		"all_align" : "left",

		"text_height": 40
	}

	quest_lable_expend_img_path_dict = {
		0: "d:/ymir work/ui/quest_re/tabcolor_1_main.tga",
		1: "d:/ymir work/ui/quest_re/tabcolor_2_sub.tga",
		2: "d:/ymir work/ui/quest_re/tabcolor_3_levelup.tga",
		3: "d:/ymir work/ui/quest_re/tabcolor_4_event.tga",
		4: "d:/ymir work/ui/quest_re/tabcolor_5_collection.tga",
		5: "d:/ymir work/ui/quest_re/tabcolor_6_system.tga",
		6: "d:/ymir work/ui/quest_re/tabcolor_7_scroll.tga",
		7: "d:/ymir work/ui/quest_re/tabcolor_8_daily.tga"
	}

	quest_label_dict = {
		0 : localeInfo.QUEST_CATEGORY_00,
		1 : localeInfo.QUEST_CATEGORY_01,
		2 : localeInfo.QUEST_CATEGORY_02,
		3 : localeInfo.QUEST_CATEGORY_03,
		4 : localeInfo.QUEST_CATEGORY_04,
		5 : localeInfo.QUEST_CATEGORY_05,
		6 : localeInfo.QUEST_CATEGORY_06,
		7 : localeInfo.QUEST_CATEGORY_07,
	}

class CharacterWindow(ui.ScriptWindow):

	ACTIVE_PAGE_SLOT_COUNT = 8
	SUPPORT_PAGE_SLOT_COUNT = 12

	PAGE_SLOT_COUNT = 12
	PAGE_HORSE = 2

	SKILL_GROUP_NAME_DICT = {
		playerSettingModule.JOB_WARRIOR : { 1 : localeInfo.SKILL_GROUP_WARRIOR_1, 2 : localeInfo.SKILL_GROUP_WARRIOR_2, },
		playerSettingModule.JOB_ASSASSIN : { 1 : localeInfo.SKILL_GROUP_ASSASSIN_1, 2 : localeInfo.SKILL_GROUP_ASSASSIN_2, },
		playerSettingModule.JOB_SURA : { 1 : localeInfo.SKILL_GROUP_SURA_1, 2 : localeInfo.SKILL_GROUP_SURA_2, },
		playerSettingModule.JOB_SHAMAN : { 1 : localeInfo.SKILL_GROUP_SHAMAN_1, 2 : localeInfo.SKILL_GROUP_SHAMAN_2, },
	}

	STAT_DESCRIPTION = {
		"HTH" : localeInfo.STAT_TOOLTIP_CON,
		"INT" : localeInfo.STAT_TOOLTIP_INT,
		"STR" : localeInfo.STAT_TOOLTIP_STR,
		"DEX" : localeInfo.STAT_TOOLTIP_DEX,
	}

	STAT_MINUS_DESCRIPTION = localeInfo.STAT_MINUS_DESCRIPTION
	if app.ENABLE_RENEWAL_QUEST:
		MAX_QUEST_PAGE_HEIGHT = 336.5

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.state = "STATUS"
		self.isLoaded = 0

		if app.ENABLE_RENEWAL_BONUS_BOARD:
			self.BonusToolTip = uiToolTip.ItemToolTip()
			self.BonusToolTip.Hide()

		if app.ENABLE_RENEWAL_QUEST:
			self.isQuestCategoryLoad = FALSE

		if app.ENABLE_SKILL_COLOR_SYSTEM:
			self.skillColorWnd = None
			self.skillColorButton = []

		self.toolTipSkill = 0

		self.__Initialize()
		self.__LoadWindow()

		self.statusPlusCommandDict = {
			"HTH" : "/stat_val ht ",
			"INT" : "/stat_val iq ",
			"STR" : "/stat_val st ",
			"DEX" : "/stat_val dx ",
		}

		self.statusMinusCommandDict = {
			"HTH-" : "/stat- ht",
			"INT-" : "/stat- iq",
			"STR-" : "/stat- st",
			"DEX-" : "/stat- dx",
		}

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __Initialize(self):
		self.refreshToolTip = 0
		self.curSelectedSkillGroup = 0
		self.canUseHorseSkill = -1

		self.toolTip = None
		self.toolTipJob = None
		self.toolTipAlignment = None
		self.toolTipSkill = None
		self.toolTipCharacterBoard = None

		self.faceImage = None
		self.statusPlusLabel = None
		self.statusPlusValue = None
		self.activeSlot = None
		self.tabDict = None
		self.tabButtonDict = None
		self.tabCharacterPageDict = None
		self.pageDict = None
		self.titleBarDict = None
		self.statusPlusButtonDict = None
		self.statusPlusButtonDict2 = None
		self.statusMinusButtonDict = None

		self.skillPageDict = None

		if app.ENABLE_RENEWAL_QUEST:
			self.questScrollBar = None
			self.questLastScrollPosition = 0
			self.questPage = None
			self.questTitleBar = None
			self.questSlotList = []
			self.questCategory = {}
			self.questCategoryList = []

			self.questColorList = {
				"green" : 0xFF83C055,
				"blue": 0xFF45678D,
				"golden": 0xFFCAB62F,
				"default_title": 0xFFCEC6B5
			}

			self.questOpenedCategories = []
			self.questMaxOpenedCategories = 1

			self.questClicked = []
			self.questIndexMap = {}
			self.questCounterList = []
			self.questClockList = []
			self.questSeparatorList = []

			self.displayY = 0
			self.baseCutY = 0
			self.questCategoryRenderPos = []

			self.questSlideWnd = {}
			self.questSlideWndNewKey = 0
		else:
			self.questShowingStartIndex = 0
			self.questScrollBar = None
			self.questSlot = None
			self.questNameList = None
			self.questLastTimeList = None
			self.questLastCountList = None
		self.skillGroupButton = ()

		self.activeSlot = None
		self.activeSkillPointValue = None
		self.supportSkillPointValue = None
		self.skillGroupButton1 = None
		self.skillGroupButton2 = None
		self.activeSkillGroupName = None

		self.guildNameSlot = None
		self.guildNameValue = None
		self.characterNameSlot = None
		self.characterNameValue = None

		self.emotionToolTip = None
		self.soloEmotionSlot = None
		self.dualEmotionSlot = None
		self.specialEmotionSlot = None
		self.specialEmotionSlot2 = None
		self.prevButton = None
		self.nextButton = None
		self.currentPageBack = None
		self.currentPageText = None
		self.currentPage = 1

	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)

	def __LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)

	def __BindObject(self):
		self.toolTip = uiToolTip.ToolTip()
		self.toolTipJob = uiToolTip.ToolTip()
		self.toolTipAlignment = uiToolTip.ToolTip(130)
		self.toolTipCharacterBoard = uiToolTip.ToolTip()

		self.faceImage = self.GetChild("Face_Image")

		faceSlot = self.GetChild("Face_Slot")

		self.statusPlusLabel = self.GetChild("Status_Plus_Label")
		self.statusPlusValue = self.GetChild("Status_Plus_Value")

		self.characterNameSlot = self.GetChild("Character_Name_Slot")
		self.characterNameValue = self.GetChild("Character_Name")
		self.guildNameSlot = self.GetChild("Guild_Name_Slot")
		self.guildNameValue = self.GetChild("Guild_Name")
		self.characterNameSlot.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowAlignmentToolTip)
		self.characterNameSlot.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideAlignmentToolTip)

		self.activeSlot = self.GetChild("Skill_Active_Slot")
		self.activeSkillPointValue = self.GetChild("Active_Skill_Point_Value")
		self.supportSkillPointValue = self.GetChild("Support_Skill_Point_Value")
		self.skillGroupButton1 = self.GetChild("Skill_Group_Button_1")
		self.skillGroupButton2 = self.GetChild("Skill_Group_Button_2")
		self.activeSkillGroupName = self.GetChild("Active_Skill_Group_Name")

		if app.ENABLE_RENEWAL_QUEST:
			self.questScrollBar = self.GetChild("Quest_ScrollBar")
			self.questPage = self.GetChild("Quest_Page")
			self.questTitleBar = self.GetChild("Quest_TitleBar")
			self.quest_page_board_window = self.GetChild("quest_page_board_window")
			self.quest_object_board_window = self.GetChild("quest_object_board_window")

		self.tabDict = {
			"STATUS" : self.GetChild("Tab_01"),
			"SKILL" : self.GetChild("Tab_02"),
			"EMOTICON" : self.GetChild("Tab_03"),
			"QUEST" : self.GetChild("Tab_04"),
		}

		self.tabButtonDict = {
			"STATUS" : self.GetChild("Tab_Button_01"),
			"SKILL" : self.GetChild("Tab_Button_02"),
			"EMOTICON" : self.GetChild("Tab_Button_03"),
			"QUEST" : self.GetChild("Tab_Button_04"),
		}

		self.tabCharacterPageDict = {
			0 : self.GetChild("change_status_button"),
			1 : self.GetChild("bonus_board_button"),
			2 : self.GetChild("stats_board_button"),
		}

		self.pageDict = {
			"STATUS" : self.GetChild("Character_Page"),
			"SKILL" : self.GetChild("Skill_Page"),
			"EMOTICON" : self.GetChild("Emoticon_Page"),
			"QUEST" : self.GetChild("Quest_Page"),
		}

		self.titleBarDict = {
			"STATUS" : self.GetChild("Character_TitleBar"),
			"SKILL" : self.GetChild("Skill_TitleBar"),
			"EMOTICON" : self.GetChild("Emoticon_TitleBar"),
			"QUEST" : self.GetChild("Quest_TitleBar"),
		}

		self.statusPlusButtonDict = {
			"HTH" : self.GetChild("HTH_Plus"),
			"INT" : self.GetChild("INT_Plus"),
			"STR" : self.GetChild("STR_Plus"),
			"DEX" : self.GetChild("DEX_Plus"),
		}

		self.statusPlusButtonDict2 = {
			"HTH" : self.GetChild("HTH_Plus2"),
			"INT" : self.GetChild("INT_Plus2"),
			"STR" : self.GetChild("STR_Plus2"),
			"DEX" : self.GetChild("DEX_Plus2"),
		}

		self.statusMinusButtonDict = {
			"HTH-" : self.GetChild("HTH_Minus"),
			"INT-" : self.GetChild("INT_Minus"),
			"STR-" : self.GetChild("STR_Minus"),
			"DEX-" : self.GetChild("DEX_Minus"),
		}

		self.skillPageDict = {
			"ACTIVE" : self.GetChild("Skill_Active_Slot"),
			"SUPPORT" : self.GetChild("Skill_ETC_Slot"),
			"HORSE" : self.GetChild("Skill_Active_Slot"),
		}

		self.skillPageStatDict = {
			"SUPPORT" : player.SKILL_SUPPORT,
			"ACTIVE" : player.SKILL_ACTIVE,
			"HORSE" : player.SKILL_HORSE,
		}

		self.labelPageStatDict = {
			"SUPPORT" : self.GetChild("Support_Skill_Point_Label"),
			"ACTIVE" : self.GetChild("Active_Skill_Point_Label"),
			"HORSE" : self.GetChild("Horse_Skill_Point_Label"),
		}

		self.characterPageDict = {
			0 : self.GetChild("Status_Window"),
			1 : self.GetChild("Bonus_Window"),
			2 : self.GetChild("Stats_Window"),
		}

		self.skillGroupButton = (
			self.GetChild("Skill_Group_Button_1"),
			self.GetChild("Skill_Group_Button_2"),
		)

		self.HTH_IMG = self.GetChild("HTH_IMG")
		self.INT_IMG = self.GetChild("INT_IMG")
		self.STR_IMG = self.GetChild("STR_IMG")
		self.DEX_IMG = self.GetChild("DEX_IMG")

		self.HEL_IMG = self.GetChild("HEL_IMG")
		self.SP_IMG = self.GetChild("SP_IMG")
		self.ATT_IMG = self.GetChild("ATT_IMG")
		self.DEF_IMG = self.GetChild("DEF_IMG")

		self.HTH_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowHTHToolTip)
		self.HTH_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideHTHToolTip)

		self.INT_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowINTToolTip)
		self.INT_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideINTToolTip)

		self.STR_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowSTRToolTip)
		self.STR_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideSTRToolTip)

		self.DEX_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowDEXToolTip)
		self.DEX_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideDEXToolTip)

		self.HEL_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowHELToolTip)
		self.HEL_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideHELToolTip)

		self.SP_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowSPToolTip)
		self.SP_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideSPToolTip)

		self.ATT_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowATTToolTip)
		self.ATT_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideATTToolTip)

		self.DEF_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowDEFToolTip)
		self.DEF_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideDEFToolTip)

		self.MSPD_IMG = self.GetChild("MSPD_IMG")
		self.ASPD_IMG = self.GetChild("ASPD_IMG")
		self.CSPD_IMG = self.GetChild("CSPD_IMG")
		self.MATT_IMG = self.GetChild("MATT_IMG")
		self.MDEF_IMG = self.GetChild("MDEF_IMG")
		self.ER_IMG = self.GetChild("ER_IMG")

		self.MSPD_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowMSPDToolTip)
		self.MSPD_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideMSPDToolTip)

		self.ASPD_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowASPDToolTip)
		self.ASPD_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideASPDToolTip)

		self.CSPD_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowCSPDToolTip)
		self.CSPD_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideCSPDToolTip)

		self.MATT_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowMATTToolTip)
		self.MATT_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideMATTToolTip)

		self.MDEF_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowMDEFToolTip)
		self.MDEF_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideMDEFToolTip)

		self.ER_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowERToolTip)
		self.ER_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideERToolTip)

		for _, label in self.labelPageStatDict.items():
			label.Hide()

		self.GetChild("Support_Skill_Point_Label").Hide()

		self.soloEmotionSlot = self.GetChild("SoloEmotionSlot")
		self.dualEmotionSlot = self.GetChild("DualEmotionSlot")
		self.specialEmotionSlot = self.GetChild("SpecialEmotionSlot")
		self.specialEmotionSlot2 = self.GetChild("SpecialEmotionSlot2")
		self.prevButton = self.GetChild("prev_button")
		self.nextButton = self.GetChild("next_button")
		self.currentPageBack = self.GetChild("CurrentPageBack")
		self.currentPageText = self.GetChild("CurrentPage")
		self.__SetEmotionSlot()
		self.RefreshEmotionPage()

		if app.ENABLE_RENEWAL_QUEST:
			self.questScrollBar.SetParent(self.quest_page_board_window)
			for i in xrange(quest.QUEST_CATEGORY_MAX_NUM):
				self.questCategory = ui.SubTitleBar()
				self.questCategory.SetParent(self.questPage)
				self.questCategory.MakeSubTitleBar(210, "red")
				self.questCategory.SetText(quest_label_dict[i])
				self.questCategory.SetSize(210, 16)
				self.questCategory.SetPosition(13, 0)
				self.questCategoryList.append(self.questCategory)

				self.questCategoryRenderPos.append(0)

			self.questScrollBar.SetParent(self.questPage)
			self.RearrangeQuestCategories(xrange(quest.QUEST_CATEGORY_MAX_NUM))
		else:
			self.questShowingStartIndex = 0
			self.questScrollBar = self.GetChild("Quest_ScrollBar")
			self.questScrollBar.SetScrollEvent(ui.__mem_func__(self.OnQuestScroll))
			self.questSlot = self.GetChild("Quest_Slot")
			for i in xrange(quest.QUEST_MAX_NUM):
				self.questSlot.HideSlotBaseImage(i)
				self.questSlot.SetCoverButton(i,\
					"d:/ymir work/ui/game/quest/slot_button_01.sub",\
					"d:/ymir work/ui/game/quest/slot_button_02.sub",\
					"d:/ymir work/ui/game/quest/slot_button_03.sub",\
					"d:/ymir work/ui/game/quest/slot_button_03.sub", TRUE)

			self.questNameList = []
			self.questLastTimeList = []
			self.questLastCountList = []
			for i in xrange(quest.QUEST_MAX_NUM):
				self.questNameList.append(self.GetChild("Quest_Name_0" + str(i)))
				self.questLastTimeList.append(self.GetChild("Quest_LastTime_0" + str(i)))
				self.questLastCountList.append(self.GetChild("Quest_LastCount_0" + str(i)))

		if app.ENABLE_RENEWAL_BONUS_BOARD:
			self.statWindow = self.GetChild("Stats_Window")
			self.bonusWindow = self.GetChild("Bonus_Window")

			self.scrollBar = ui.ScrollBar4()
			self.scrollBar.SetParent(self.bonusWindow)
			self.scrollBar.SetPosition((self.bonusWindow.GetWidth() - self.scrollBar.GetWidth()) - 22, 3)
			self.scrollBar.SetScrollBarSize((self.bonusWindow.GetHeight() - 5) - 5)
			self.scrollBar.SetScrollEvent(ui.__mem_func__(self.Refresh))
			self.scrollBar.Show()
			self.ElementDictionary["scrollBar"] = self.scrollBar

			self.scrollBar2 = ui.ScrollBar4()
			self.scrollBar2.SetParent(self.statWindow)
			self.scrollBar2.SetPosition((self.statWindow.GetWidth() - self.scrollBar2.GetWidth()) - 18, 3)
			self.scrollBar2.SetScrollBarSize((self.statWindow.GetHeight() - 5) - 5)
			self.scrollBar2.SetScrollEvent(ui.__mem_func__(self.Refresh))
			self.scrollBar2.Show()
			self.ElementDictionary["scrollBar2"] = self.scrollBar2

			for i in xrange(len(stat_list)):
				background = ui.ImageBox()
				background.SetParent(self.statWindow)
				background.LoadImage("d:/ymir work/ui/game/windows/statistics.tga")
				background.Show()
				background.SetClippingMaskWindow(self.statWindow)
				self.ElementDictionary["background"] = background

				for j in xrange(len(stat_list)):
					statName = ui.TextLine()
					statName.SetParent(background)
					statName.AddFlag("not_pick")
					statName.SetPosition(70, 15+(j*40))
					statName.SetFontName("Tahoma:13")
					statName.SetHorizontalAlignCenter()
					statName.SetText(stat_list[j][0])
					statName.Show()
					statName.SetClippingMaskWindow(self.statWindow)
					self.ElementDictionary["%d_stat_name" % j] = statName

					statValue = ui.TextLine()
					statValue.AddFlag("not_pick")
					statValue.SetParent(background)
					statValue.SetPosition(180, 15+(j*40))
					statValue.SetFontName("Tahoma:13")
					statValue.SetHorizontalAlignCenter()
					statValue.Show()
					statValue.SetClippingMaskWindow(self.statWindow)
					self.ElementDictionary["%d_stat" % j] = statValue

			for i in xrange(len(bonus_list)):
				bonus_data = bonus_list[i][1]

				category = ui.ExpandedImageBox()
				category.SetParent(self.bonusWindow)
				category.LoadImage("d:/ymir work/ui/game/windows/category_bar.tga")
				category.buttonStatus = 0
				category.SetEvent(ui.__mem_func__(self.SetBonusCategory), "mouse_click", i)
				category.Show()
				self.ElementDictionary["%d_category" % i] = category

				categoryText = ui.TextLine()
				categoryText.SetParent(category)
				categoryText.SetHorizontalAlignLeft()
				categoryText.SetPosition(8, 3)
				categoryText.SetText("|Eemoji/key_plus|e " + bonus_list[i][0])
				categoryText.Show()
				self.ElementDictionary["%d_categoryText" % i] = categoryText

				for j in xrange(len(bonus_data)):
					bonusImage = ui.ExpandedImageBox()
					bonusImage.SetParent(self.bonusWindow)
					bonusImage.LoadImage("d:/ymir work/ui/game/windows/bonus_item.tga")
					bonusImage.Show()
					self.ElementDictionary["%d_%d_image" % (i, j)] = bonusImage

					bonusTextValue = ItemToolTip.AFFECT_DICT[bonus_data[j][0]]
					if callable(bonusTextValue):
						bonusText = bonusTextValue(0)
					else:
						bonusText = str(bonusTextValue)

					disabledStr = ["%","+"]
					newText = ""
					for x in bonusText:
						if x in disabledStr:
							continue
						if x.isdigit():
							continue
						newText += x
					bonusText = newText
					bonusImage.SAFE_SetStringEvent("MOUSE_OVER_IN", self.OverInBonus, bonusText)
					bonusImage.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.OverOutBonus)

					bonusName = ui.TextLine()
					bonusName.AddFlag("not_pick")
					bonusName.SetParent(bonusImage)
					bonusName.SetHorizontalAlignLeft()
					bonusName.SetPosition(5, 3)
					bonusName.SetFontName("Tahoma:13")
					bonusName.SetText(bonusText)

					newText = ""
					if bonusName.GetTextSize()[0] > 130:
						for o in xrange(100):
							if bonusName.GetTextSize()[0] > 130:
								newText = bonusName.GetText()[:len(bonusName.GetText()) - 2] + "..."
								bonusName.SetText(bonusName.GetText()[:len(bonusName.GetText()) - 2])
							else:
								break

					if newText != "":
						bonusName.SetText(newText)

					bonusName.Show()
					self.ElementDictionary["%d_%d_name" % (i, j)] = bonusName

					bonusValue = ui.TextLine()
					bonusValue.AddFlag("not_pick")
					bonusValue.SetParent(bonusImage)
					bonusValue.SetHorizontalAlignCenter()
					bonusValue.SetPosition(170, 3)
					bonusValue.SetFontName("Tahoma:13")
					bonusValue.SetText("0")
					bonusValue.Show()
					self.ElementDictionary["%d_%d_value" % (i, j)] = bonusValue

	def __SetSkillSlotEvent(self):
		for skillPageValue in self.skillPageDict.itervalues():
			skillPageValue.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			skillPageValue.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectSkill))
			skillPageValue.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
			skillPageValue.SetUnselectItemSlotEvent(ui.__mem_func__(self.ClickSkillSlot))
			skillPageValue.SetUseSlotEvent(ui.__mem_func__(self.ClickSkillSlot))
			skillPageValue.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			skillPageValue.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			skillPageValue.SetPressedSlotButtonEvent(ui.__mem_func__(self.OnPressedSlotButton))
			skillPageValue.AppendSlotButton("d:/ymir work/ui/game/windows/btn_plus_up.sub",\
				"d:/ymir work/ui/game/windows/btn_plus_over.sub",\
				"d:/ymir work/ui/game/windows/btn_plus_down.sub")

	def OnClickPrevPage(self):
		if self.currentPage == 2:
			self.currentPage = self.currentPage - 1
			self.currentPageText.SetText(str(self.currentPage))
		self.RefreshEmotionPage()

	def OnClickNextPage(self):
		if self.currentPage == 1:
			self.currentPage = self.currentPage + 1
		self.currentPageText.SetText(str(self.currentPage))
		self.RefreshEmotionPage()

	def RefreshEmotionPage(self):
		if self.currentPage == 1:
			self.specialEmotionSlot.Show()
			self.specialEmotionSlot2.Hide()
		else:
			self.specialEmotionSlot.Hide()
			self.specialEmotionSlot2.Show()

	def __SetEmotionSlot(self):
		self.prevButton.SetEvent(ui.__mem_func__(self.OnClickPrevPage))
		self.nextButton.SetEvent(ui.__mem_func__(self.OnClickNextPage))
		self.currentPageText.SetText(str(self.currentPage))

		self.emotionToolTip = uiToolTip.ToolTip()

		for slot in (self.soloEmotionSlot, self.dualEmotionSlot, self.specialEmotionSlot, self.specialEmotionSlot2):
			slot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			slot.SetSelectItemSlotEvent(ui.__mem_func__(self.__SelectEmotion))
			slot.SetUnselectItemSlotEvent(ui.__mem_func__(self.__ClickEmotionSlot))
			slot.SetUseSlotEvent(ui.__mem_func__(self.__ClickEmotionSlot))
			slot.SetOverInItemEvent(ui.__mem_func__(self.__OverInEmotion))
			slot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutEmotion))
			slot.AppendSlotButton("d:/ymir work/ui/game/windows/btn_plus_up.sub", "d:/ymir work/ui/game/windows/btn_plus_over.sub", "d:/ymir work/ui/game/windows/btn_plus_down.sub")

		for slotIdx, datadict in emotion.EMOTION_DICT.items():
			emotionIdx = slotIdx

			slot = self.soloEmotionSlot

			if slotIdx > 50 and slotIdx <= 60:
				slot = self.dualEmotionSlot
			if slotIdx > 60 and slotIdx <= 72:
				slot = self.specialEmotionSlot
			if slotIdx > 72:
				slot = self.specialEmotionSlot2

			slot.SetEmotionSlot(slotIdx, emotionIdx)
			slot.SetCoverButton(slotIdx)

		self.soloEmotionSlot.SetSlot(24, 2, 32, 32, skill.GetEmptySkill())
		for i in xrange(3):
			self.dualEmotionSlot.SetSlot(54+i, 2, 32, 32, skill.GetEmptySkill())
		for i in xrange(3):
			self.specialEmotionSlot2.SetSlot(82+i, 2, 32, 32, skill.GetEmptySkill())

	def __SelectEmotion(self, slotIndex):
		if not slotIndex in emotion.EMOTION_DICT:
			return

		if app.IsPressed(app.DIK_LCONTROL):
			player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_EMOTION, slotIndex)
			return

		mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_EMOTION, slotIndex, slotIndex)

	def __ClickEmotionSlot(self, slotIndex):
		if not slotIndex in emotion.EMOTION_DICT:
			return

		if player.IsActingEmotion():
			return

		command = emotion.EMOTION_DICT[slotIndex]["command"]

		if slotIndex > 50 and slotIndex <= 60:
			vid = player.GetTargetVID()

			if 0 == vid or vid == player.GetMainCharacterIndex() or chr.IsNPC(vid) or chr.IsEnemy(vid):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.EMOTION_CHOOSE_ONE)
				return

			command += " " + chr.GetNameByVID(vid)

		net.SendChatPacket(command)

	def ActEmotion(self, emotionIndex):
		self.__ClickEmotionSlot(emotionIndex)

	def __OverInEmotion(self, slotIndex):
		if self.emotionToolTip:

			if not slotIndex in emotion.EMOTION_DICT:
				return

			# Bonus tooltip'i kapat
			if app.ENABLE_RENEWAL_BONUS_BOARD:
				if self.BonusToolTip and hasattr(self.BonusToolTip, 'HideToolTip'):
					self.BonusToolTip.HideToolTip()

			self.emotionToolTip.ClearToolTip()
			self.emotionToolTip.SetTitle(emotion.EMOTION_DICT[slotIndex]["name"])
			self.emotionToolTip.AlignHorizonalCenter()
			self.emotionToolTip.ShowToolTip()

	def __OverOutEmotion(self):
		if self.emotionToolTip:
			if hasattr(self.emotionToolTip, 'IsShow') and self.emotionToolTip.IsShow():
				self.emotionToolTip.HideToolTip()
			elif hasattr(self.emotionToolTip, 'HideToolTip'):
				self.emotionToolTip.HideToolTip()

	def __BindEvent(self):
		for i in xrange(len(self.skillGroupButton)):
			self.skillGroupButton[i].SetEvent(ui.__mem_func__(self.__SelectSkillGroup),i)

		self.RefreshQuest()
		self.__HideJobToolTip()

		for (tabKey, tabButton) in self.tabButtonDict.items():
			tabButton.SetEvent(ui.__mem_func__(self.__OnClickTabButton), tabKey)

		for (tabCharacterKey, tabCharacterButton) in self.tabCharacterPageDict.items():
			tabCharacterButton.SetEvent(ui.__mem_func__(self.SetStatusPage), tabCharacterKey)
			tabCharacterButton.ShowToolTip = lambda arg = tabCharacterKey: self.__OverInCharacterButton(arg)
			tabCharacterButton.HideToolTip = lambda arg = tabCharacterKey: self.__OverOutCharacterButton()

			if tabCharacterKey == 3:
				tabCharacterButton.Hide()

		for (statusPlusKey, statusPlusButton) in self.statusPlusButtonDict.items():
			statusPlusButton.SAFE_SetEvent(self.__OnClickStatusPlusButton, statusPlusKey)
			statusPlusButton.ShowToolTip = lambda arg = statusPlusKey: self.__OverInStatButton(arg)
			statusPlusButton.HideToolTip = lambda arg = statusPlusKey: self.__OverOutStatButton()

		for (statusPlusKey2, statusPlusButton2) in self.statusPlusButtonDict2.items():
			statusPlusButton2.SAFE_SetEvent(self.__OnClickStatusPlusButton2, statusPlusKey2)
			statusPlusButton2.ShowToolTip = lambda arg = statusPlusKey2: self.__OverInStatButton2(arg)
			statusPlusButton2.HideToolTip = lambda arg = statusPlusKey2: self.__OverOutStatButton()

		for (statusMinusKey, statusMinusButton) in self.statusMinusButtonDict.items():
			statusMinusButton.SAFE_SetEvent(self.__OnClickStatusMinusButton, statusMinusKey)
			statusMinusButton.ShowToolTip = lambda arg = statusMinusKey: self.__OverInStatMinusButton(arg)
			statusMinusButton.HideToolTip = lambda arg = statusMinusKey: self.__OverOutStatMinusButton()

		for titleBarValue in self.titleBarDict.itervalues():
			titleBarValue.SetCloseEvent(ui.__mem_func__(self.Close))

		if app.ENABLE_RENEWAL_QUEST:
			self.questTitleBar.SetCloseEvent(ui.__mem_func__(self.Close))
			self.questScrollBar.SetScrollEvent(ui.__mem_func__(self.__OnScrollQuest))

			for i in xrange(quest.QUEST_CATEGORY_MAX_NUM):
				self.questCategoryList[i].SetEvent(ui.__mem_func__(self.__OnClickQuestCategoryButton), i)
		else:
			self.questSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.__SelectQuest))

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			self.__LoadScript("UIScript/CharacterWindow.py")

			self.__BindObject()
			self.__BindEvent()
		except:
			import exception
			exception.Abort("CharacterWindow.__LoadWindow")

		self.SetState("STATUS")

	def Destroy(self):
		self.ClearDictionary()

		self.__Initialize()

	def Close(self):
		# C tuþu ile kapatýldýðýnda tüm tooltip'leri kapat
		from uiToolTip import ToolTip
		for tooltip in ToolTip._allToolTips:
			if tooltip and hasattr(tooltip, 'IsShow') and tooltip.IsShow():
				if hasattr(tooltip, 'HideToolTip'):
					tooltip.HideToolTip()
				elif hasattr(tooltip, 'Hide'):
					tooltip.Hide()

		if self.toolTipSkill:
			self.toolTipSkill.Hide()

		if app.ENABLE_RENEWAL_QUEST:
			if self.questSlideWndNewKey > 0:
				if self.questSlideWnd[self.questSlideWndNewKey-1] is not None:
					self.questSlideWnd[self.questSlideWndNewKey-1].CloseSelf()

		if app.ENABLE_SKILL_COLOR_SYSTEM:
			if self.skillColorWnd and self.skillColorWnd.IsShow():
				self.skillColorWnd.Hide()

		self.Hide()

	if app.ENABLE_RENEWAL_BONUS_BOARD:
		def SetBonusCategory(self, emptyArg, categoryIndex):
			category = self.ElementDictionary["%d_category" % categoryIndex]
			category.buttonStatus = not category.buttonStatus

			if category.buttonStatus == 0:
				self.ElementDictionary["%d_categoryText" % categoryIndex].SetText("|Eemoji/key_plus|e " + bonus_list[categoryIndex][0])
			else:
				self.ElementDictionary["%d_categoryText" % categoryIndex].SetText("|Eemoji/key_minus|e " + bonus_list[categoryIndex][0])

			self.Refresh()

		def Refresh(self):
			(X_POS, Y_POS) = (3, 3)
			CATEGORY_Y_RANGE = 25
			CATEGORY_Y_FIRST_BONUS_RANGE = 29
			BONUS_X = 8
			STATS_X = 0
			STATS_Y = 2.3

			(basePos, windowHeight) = (0, self.bonusWindow.GetHeight() - 6)

			maxHeight = 0
			for i in xrange(len(bonus_list)):
				bonus_data = bonus_list[i][1]
				if self.ElementDictionary.has_key("%d_category" % i):
					categoryBtn = self.ElementDictionary["%d_category" % i]
					if categoryBtn.buttonStatus == 0:
						maxHeight += CATEGORY_Y_RANGE
					else:
						maxHeight += CATEGORY_Y_FIRST_BONUS_RANGE
						for j in xrange(len(bonus_data)):
							maxHeight += CATEGORY_Y_FIRST_BONUS_RANGE

			if maxHeight > windowHeight:
				scrollLen = maxHeight - windowHeight
				basePos = int(self.scrollBar.GetPos() * scrollLen)
				stepSize = 1.0 / (scrollLen / 100.0)
				self.scrollBar.SetScrollStep(stepSize)
				self.scrollBar.SetMiddleBarSize(float(windowHeight - 5) / float(maxHeight))
				self.scrollBar.Show()
			else:
				self.scrollBar.Hide()

			textLines = []
			images = []
			_wy = self.bonusWindow.GetGlobalPosition()[1] + 3

			for i in xrange(len(bonus_list)):
				bonus_data = bonus_list[i][1]
				if self.ElementDictionary.has_key("%d_category" % i):
					categoryBtn = self.ElementDictionary["%d_category" % i]
					categoryBtn.SetPosition(X_POS, Y_POS - basePos)
					categoryBtn.Show()

					images.append(categoryBtn)
					textLines.append(self.ElementDictionary["%d_categoryText" % i])

					if categoryBtn.buttonStatus == 0:
						Y_POS += CATEGORY_Y_RANGE
						for j in xrange(len(bonus_data)):
							self.ElementDictionary["%d_%d_image" % (i, j)].Hide()
					else:
						Y_POS += CATEGORY_Y_FIRST_BONUS_RANGE
						for j in xrange(len(bonus_data)):
							self.ElementDictionary["%d_%d_image" % (i, j)].Show()
							self.ElementDictionary["%d_%d_image" % (i, j)].SetPosition(BONUS_X, Y_POS - basePos)
							self.ElementDictionary["%d_%d_value" % (i, j)].SetText(str(player.GetStatus(bonus_data[j][1])))

							Y_POS += CATEGORY_Y_FIRST_BONUS_RANGE

							images.append(self.ElementDictionary["%d_%d_image" % (i, j)])
							textLines.append(self.ElementDictionary["%d_%d_name" % (i, j)])
							textLines.append(self.ElementDictionary["%d_%d_value" % (i, j)])

			for childItem in textLines:
				(_x, _y) = childItem.GetGlobalPosition()

				if _y < _wy:
					if childItem.IsShow():
						childItem.Hide()
				elif _y > (_wy + windowHeight - 20):
					if childItem.IsShow():
						childItem.Hide()
				else:
					if not childItem.IsShow():
						childItem.Show()

			for childItem in images:
				childHeight = childItem.GetHeight()
				(_x, _y) = childItem.GetGlobalPosition()

				if _y < _wy:
					childItem.SetRenderingRect(0, ui.calculateRect(childHeight - abs(_y - _wy), childHeight), 0, 0)
				elif _y + childHeight > (_wy+windowHeight - 4):
					calculate = (_wy + windowHeight - 4) - (_y + childHeight)

					if calculate == 0:
						return

					f = ui.calculateRect(childHeight - abs(calculate), childHeight)
					childItem.SetRenderingRect(0, 0, 0, f)
				else:
					childItem.SetRenderingRect(0, 0, 0, 0)

			(basePos2, windowHeight2) = (0, self.statWindow.GetHeight() - 6)

			maxHeight2 = 0
			for i in xrange(len(stat_list)):
				if self.ElementDictionary.has_key("%d_stat" % i):
					maxHeight2 += STATS_Y
					for j in xrange(len(stat_list[i][0])):
						maxHeight2 += STATS_Y

			if maxHeight2 > windowHeight2:
				scrollLen = maxHeight2 - windowHeight2
				basePos2 = int(self.scrollBar2.GetPos() * scrollLen)
				stepSize = 1.0 / (scrollLen / 100.0)
				self.scrollBar2.SetScrollStep(stepSize)
				self.scrollBar2.SetMiddleBarSize(float(windowHeight2 - 5) / float(maxHeight2))
				self.scrollBar2.Show()

			for i in xrange(len(stat_list)):
				if self.ElementDictionary.has_key("%d_stat" % i):
					self.ElementDictionary["background"].Show()
					self.ElementDictionary["background"].SetPosition(STATS_X, STATS_Y - basePos2)
					self.ElementDictionary["%d_stat" % i].SetText(localeInfo.NumberToDecimalString(player.GetStatus(stat_list[i][1])))

					images.append(self.ElementDictionary["background"])
					textLines.append(self.ElementDictionary["%d_stat_name" % i])
					textLines.append(self.ElementDictionary["%d_stat" % i])

		def OverOutBonus(self):
			if self.BonusToolTip:
				if hasattr(self.BonusToolTip, 'IsShow') and self.BonusToolTip.IsShow():
					self.BonusToolTip.HideToolTip()
				elif hasattr(self.BonusToolTip, 'HideToolTip'):
					self.BonusToolTip.HideToolTip()

		def OverInBonus(self, bonusName):
			if self.BonusToolTip:
				# Diðer tooltip'leri kapat
				self.__HideStatToolTip()
				if self.toolTipJob and hasattr(self.toolTipJob, 'HideToolTip'):
					self.toolTipJob.HideToolTip()
				if self.toolTipAlignment and hasattr(self.toolTipAlignment, 'HideToolTip'):
					self.toolTipAlignment.HideToolTip()
				if self.toolTipCharacterBoard and hasattr(self.toolTipCharacterBoard, 'HideToolTip'):
					self.toolTipCharacterBoard.HideToolTip()
				if self.emotionToolTip and hasattr(self.emotionToolTip, 'HideToolTip'):
					self.emotionToolTip.HideToolTip()
				
				self.BonusToolTip.ClearToolTip()
				self.BonusToolTip.AppendTextLine(bonusName)
				self.BonusToolTip.ShowToolTip()

	def SetSkillToolTip(self, toolTipSkill):
		self.toolTipSkill = toolTipSkill

	def __OnClickStatusPlusButton(self, statusKey):
		cmd = self.statusPlusCommandDict[statusKey]
		cmd = cmd + "1"
		net.SendChatPacket(cmd)

	def __OnClickStatusPlusButton2(self, statusKey):
		cmd = self.statusPlusCommandDict[statusKey]
		cmd = cmd + "10"
		net.SendChatPacket(cmd)

	def __OnClickStatusMinusButton(self, statusKey):
		try:
			statusMinusCommand = self.statusMinusCommandDict[statusKey]
			net.SendChatPacket(statusMinusCommand)
		except KeyError, msg:
			dbg.TraceError("CharacterWindow.__OnClickStatusMinusButton KeyError: %s", msg)

	def __OnClickTabButton(self, stateKey):
		self.SetState(stateKey)

	def SetStatusPage(self, statusPage):
		if self.state != "STATUS":
			return

		for key, label in self.characterPageDict.items():
			label.Show() if key == statusPage else label.Hide()

		for key_b, button in self.tabCharacterPageDict.items():
			button.SetUp() if key_b != statusPage else button.Down()

	def SetState(self, stateKey):
		self.state = stateKey

		if app.ENABLE_RENEWAL_QUEST:
			if stateKey != "QUEST":
				self.questPage.Hide()
				if self.questSlideWndNewKey > 0:
					if self.questSlideWnd[self.questSlideWndNewKey-1] is not None:
						self.questSlideWnd[self.questSlideWndNewKey-1].CloseSelf()
			else:
				self.__LoadQuestCategory()

		for (tabKey, tabButton) in self.tabButtonDict.items():
			if stateKey!=tabKey:
				tabButton.SetUp()

		for tabValue in self.tabDict.itervalues():
			tabValue.Hide()

		for pageValue in self.pageDict.itervalues():
			pageValue.Hide()

		for titleBarValue in self.titleBarDict.itervalues():
			titleBarValue.Hide()

		self.titleBarDict[stateKey].Show()
		self.tabDict[stateKey].Show()
		self.pageDict[stateKey].Show()

	def GetState(self):
		return self.state

	def __GetTotalAtkText(self):
		minAtk = player.GetStatus(player.ATT_MIN)
		maxAtk = player.GetStatus(player.ATT_MAX)
		atkBonus = player.GetStatus(player.ATT_BONUS)
		attackerBonus = player.GetStatus(player.ATTACKER_BONUS)

		if minAtk==maxAtk:
			return "%s" % (localeInfo.NumberToDecimalString(minAtk+atkBonus+attackerBonus))
		else:
			return "%s-%s" % (localeInfo.NumberToDecimalString(minAtk+atkBonus+attackerBonus), localeInfo.NumberToDecimalString(maxAtk+atkBonus+attackerBonus))

	def __GetTotalMagAtkText(self):
		minMagAtk = player.GetStatus(player.MAG_ATT)+player.GetStatus(player.MIN_MAGIC_WEP)
		maxMagAtk = player.GetStatus(player.MAG_ATT)+player.GetStatus(player.MAX_MAGIC_WEP)

		if minMagAtk==maxMagAtk:
			return "%s" % (localeInfo.NumberToDecimalString(minMagAtk))
		else:
			return "%s-%s" % (localeInfo.NumberToDecimalString(minMagAtk), localeInfo.NumberToDecimalString(maxMagAtk))

	def __GetTotalDefText(self):
		defValue=player.GetStatus(player.DEF_GRADE)
		if constInfo.ADD_DEF_BONUS_ENABLE:
			defValue+=player.GetStatus(player.DEF_BONUS)
		return "%s" % (localeInfo.NumberToDecimalString(defValue))

	def RefreshStatus(self):
		if self.isLoaded == 0:
			return

		try:
			self.GetChild("Level_Value").SetText(str(player.GetStatus(player.LEVEL)))
			self.GetChild("Exp_Value").SetText(localeInfo.NumberToDecimalString(unsigned32(player.GetEXP())))
			self.GetChild("RestExp_Value").SetText(localeInfo.NumberToDecimalString(unsigned32(player.GetStatus(player.NEXT_EXP)) - unsigned32(player.GetStatus(player.EXP))))
			self.GetChild("HP_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.HP)) + '/' + localeInfo.NumberToDecimalString(player.GetStatus(player.MAX_HP)))
			self.GetChild("SP_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.SP)) + '/' + localeInfo.NumberToDecimalString(player.GetStatus(player.MAX_SP)))

			self.GetChild("STR_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.ST)))
			self.GetChild("DEX_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.DX)))
			self.GetChild("HTH_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.HT)))
			self.GetChild("INT_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.IQ)))

			self.GetChild("ATT_Value").SetText(self.__GetTotalAtkText())
			self.GetChild("DEF_Value").SetText(self.__GetTotalDefText())

			self.GetChild("MATT_Value").SetText(self.__GetTotalMagAtkText())

			self.GetChild("MDEF_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.MAG_DEF)))
			self.GetChild("ASPD_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.ATT_SPEED)))
			self.GetChild("MSPD_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.MOVING_SPEED)))
			self.GetChild("CSPD_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.CASTING_SPEED)))
			self.GetChild("ER_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.EVADE_RATE)))

		except:
			pass

		self.__RefreshStatusPlusButtonList()
		self.__RefreshStatusMinusButtonList()
		self.RefreshAlignment()

		if self.refreshToolTip:
			self.refreshToolTip()

	def __RefreshStatusPlusButtonList(self):
		if self.isLoaded==0:
			return

		statusPlusPoint = player.GetStatus(player.STAT)

		if statusPlusPoint > 0:
			self.statusPlusValue.SetText(str(statusPlusPoint))
			self.statusPlusLabel.Show()
			self.ShowStatusPlusButtonList()
			self.ShowStatusPlusButtonList2()
		else:
			self.statusPlusValue.SetText(str(0))
			self.statusPlusLabel.Hide()
			self.HideStatusPlusButtonList()
			self.HideStatusPlusButtonList2()

	def __RefreshStatusMinusButtonList(self):
		if self.isLoaded==0:
			return

		statusMinusPoint=self.__GetStatMinusPoint()

		if statusMinusPoint>0:
			self.__ShowStatusMinusButtonList()
		else:
			self.__HideStatusMinusButtonList()

	def RefreshAlignment(self):
		point, grade = player.GetAlignmentData()

		import colorInfo
		COLOR_DICT = {
			0 : colorInfo.TITLE_RGB_GOOD_4,
			1 : colorInfo.TITLE_RGB_GOOD_3,
			2 : colorInfo.TITLE_RGB_GOOD_2,
			3 : colorInfo.TITLE_RGB_GOOD_1,
			4 : colorInfo.TITLE_RGB_NORMAL,
			5 : colorInfo.TITLE_RGB_EVIL_1,
			6 : colorInfo.TITLE_RGB_EVIL_2,
			7 : colorInfo.TITLE_RGB_EVIL_3,
			8 : colorInfo.TITLE_RGB_EVIL_4,
		}
		colorList = COLOR_DICT.get(grade, colorInfo.TITLE_RGB_NORMAL)
		gradeColor = ui.GenerateColor(colorList[0], colorList[1], colorList[2])

		self.toolTipAlignment.ClearToolTip()
		self.toolTipAlignment.AutoAppendTextLine(localeInfo.TITLE_NAME_LIST[grade], gradeColor)
		self.toolTipAlignment.AutoAppendTextLine(localeInfo.ALIGNMENT_NAME + localeInfo.NumberToDecimalString(point))
		self.toolTipAlignment.AlignHorizonalCenter()

	def __ShowStatusMinusButtonList(self):
		for (stateMinusKey, statusMinusButton) in self.statusMinusButtonDict.items():
			statusMinusButton.Show()

	def __HideStatusMinusButtonList(self):
		for (stateMinusKey, statusMinusButton) in self.statusMinusButtonDict.items():
			statusMinusButton.Hide()

	def ShowStatusPlusButtonList(self):
		for (statePlusKey, statusPlusButton) in self.statusPlusButtonDict.items():
			statusPlusButton.Show()

	def HideStatusPlusButtonList(self):
		for (statePlusKey, statusPlusButton) in self.statusPlusButtonDict.items():
			statusPlusButton.Hide()


	def ShowStatusPlusButtonList2(self):
		for (statePlusKey2, statusPlusButton2) in self.statusPlusButtonDict2.items():
			statusPlusButton2.Show()

	def HideStatusPlusButtonList2(self):
		for (statePlusKey2, statusPlusButton2) in self.statusPlusButtonDict2.items():
			statusPlusButton2.Hide()

	def SelectSkill(self, skillSlotIndex):
		mouseController = mouseModule.mouseController

		if FALSE == mouseController.isAttached():
			srcSlotIndex = self.__RealSkillSlotToSourceSlot(skillSlotIndex)
			selectedSkillIndex = player.GetSkillIndex(srcSlotIndex)

			if skill.CanUseSkill(selectedSkillIndex):
				if app.IsPressed(app.DIK_LCONTROL):
					player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_SKILL, srcSlotIndex)
					return

				mouseController.AttachObject(self, player.SLOT_TYPE_SKILL, srcSlotIndex, selectedSkillIndex)
		else:
			mouseController.DeattachObject()

	def SelectEmptySlot(self, SlotIndex):
		mouseModule.mouseController.DeattachObject()

	## ToolTip
	def OverInItem(self, slotNumber):
		if mouseModule.mouseController.isAttached():
			return

		if 0 == self.toolTipSkill:
			return

		srcSlotIndex = self.__RealSkillSlotToSourceSlot(slotNumber)
		skillIndex = player.GetSkillIndex(srcSlotIndex)
		skillLevel = player.GetSkillLevel(srcSlotIndex)
		skillGrade = player.GetSkillGrade(srcSlotIndex)
		skillType = skill.GetSkillType(skillIndex)

		## ACTIVE
		if skill.SKILL_TYPE_ACTIVE == skillType:
			overInSkillGrade = self.__GetSkillGradeFromSlot(slotNumber)

			if overInSkillGrade == skill.SKILL_GRADE_COUNT-1 and skillGrade == skill.SKILL_GRADE_COUNT:
				self.toolTipSkill.SetSkillNew(srcSlotIndex, skillIndex, skillGrade, skillLevel)
			elif overInSkillGrade == skillGrade:
				self.toolTipSkill.SetSkillNew(srcSlotIndex, skillIndex, overInSkillGrade, skillLevel)
			else:
				self.toolTipSkill.SetSkillOnlyName(srcSlotIndex, skillIndex, overInSkillGrade)

		else:
			self.toolTipSkill.SetSkillNew(srcSlotIndex, skillIndex, skillGrade, skillLevel)

	def OverOutItem(self):
		if 0 != self.toolTipSkill:
			if hasattr(self.toolTipSkill, 'IsShow') and self.toolTipSkill.IsShow():
				self.toolTipSkill.HideToolTip()
			elif hasattr(self.toolTipSkill, 'HideToolTip'):
				self.toolTipSkill.HideToolTip()

	## Quest
	def __SelectQuest(self, slotIndex):
		if app.ENABLE_RENEWAL_QUEST:
			questIndex = self.questIndexMap[slotIndex]

			if not questIndex in self.questClicked:
				self.questClicked.append(questIndex)
		else:
			questIndex = quest.GetQuestIndex(self.questShowingStartIndex + slotIndex)

		import event
		event.QuestButtonClick(-2147483648 + questIndex)

	def RefreshQuest(self):
		if app.ENABLE_RENEWAL_QUEST:
			if self.isLoaded == 0 or self.state != "QUEST":
				return

			for cat in self.questOpenedCategories:
				self.RefreshQuestCategory(cat)

			self.RefreshQuestCategoriesCount()
		else:
			if self.isLoaded==0:
				return

			self.OnQuestScroll()

			questCount = quest.GetQuestCount()
			questRange = range(quest.QUEST_MAX_NUM)

			if questCount > quest.QUEST_MAX_NUM:
				self.questScrollBar.Show()
			else:
				self.questScrollBar.Hide()

			for i in questRange[:questCount]:
				(questName, questIcon, questCounterName, questCounterValue) = quest.GetQuestData(self.questShowingStartIndex + i)

				self.questNameList[i].SetText(questName)
				self.questNameList[i].Show()
				self.questLastCountList[i].Show()
				self.questLastTimeList[i].Show()

				if len(questCounterName) > 0:
					self.questLastCountList[i].SetText("%s : %d" % (questCounterName, questCounterValue))
				else:
					self.questLastCountList[i].SetText("")

				## Icon
				self.questSlot.SetSlot(i, i, 1, 1, questIcon)

			for i in questRange[questCount:]:
				self.questNameList[i].Hide()
				self.questLastTimeList[i].Hide()
				self.questLastCountList[i].Hide()
				self.questSlot.ClearSlot(i)
				self.questSlot.HideSlotBaseImage(i)

			self.__UpdateQuestClock()

	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			self.questScrollBar.OnUp()
		else:
			self.questScrollBar.OnDown()

		if app.ENABLE_RENEWAL_BONUS_BOARD:
			if self.ElementDictionary.has_key("scrollBar"):
				self.scrollBar = self.ElementDictionary["scrollBar"]
				if self.scrollBar.IsShow():
					if nLen > 0:
						self.scrollBar.OnUp()
					else:
						self.scrollBar.OnDown()
					return TRUE
			return FALSE

	def __UpdateQuestClock(self):
		if "QUEST" == self.state:
			if app.ENABLE_RENEWAL_QUEST:
				for clock in self.questClockList:
					clockText = localeInfo.QUEST_UNLIMITED_TIME

					if clock.GetProperty("idx"):
						(lastName, lastTime) = quest.GetQuestLastTime(clock.GetProperty("idx"))

						if len(lastName) > 0:
							if lastTime <= 0:
								clockText = localeInfo.QUEST_TIMEOVER
							else:
								questLastMinute = lastTime / 60
								questLastSecond = lastTime % 60

								clockText = lastName + " : "

								if questLastMinute > 0:
									clockText += str(questLastMinute) + localeInfo.QUEST_MIN
									if questLastSecond > 0:
										clockText += " "

								if questLastSecond > 0:
									clockText += str(questLastSecond) + localeInfo.QUEST_SEC

					clock.SetText(clockText)
			else:
				for i in xrange(min(quest.GetQuestCount(), quest.QUEST_MAX_NUM)):
					(lastName, lastTime) = quest.GetQuestLastTime(i + self.questShowingStartIndex)

					clockText = localeInfo.QUEST_UNLIMITED_TIME
					if len(lastName) > 0:

						if lastTime <= 0:
							clockText = localeInfo.QUEST_TIMEOVER
						else:
							questLastMinute = lastTime / 60
							questLastSecond = lastTime % 60

							clockText = lastName + " : "

							if questLastMinute > 0:
								clockText += str(questLastMinute) + localeInfo.QUEST_MIN
								if questLastSecond > 0:
									clockText += " "

							if questLastSecond > 0:
								clockText += str(questLastSecond) + localeInfo.QUEST_SEC

					self.questLastTimeList[i].SetText(clockText)

	def __GetStatMinusPoint(self):
		POINT_STAT_RESET_COUNT = 112
		return player.GetStatus(POINT_STAT_RESET_COUNT)

	def __OverInStatMinusButton(self, stat):
		try:
			self.__ShowStatToolTip(self.STAT_MINUS_DESCRIPTION[stat] % self.__GetStatMinusPoint())
		except KeyError:
			pass

		self.refreshToolTip = lambda arg = stat: self.__OverInStatMinusButton(arg)

	def __OverOutStatMinusButton(self):
		self.__HideStatToolTip()
		self.refreshToolTip = 0

	def __OverInCharacterButton(self, stat):
		# Bonus tooltip'i kapat
		if app.ENABLE_RENEWAL_BONUS_BOARD:
			if self.BonusToolTip and hasattr(self.BonusToolTip, 'HideToolTip'):
				self.BonusToolTip.HideToolTip()
		
		m_text_tooltip = [localeInfo.STAT_TOOLTIP_STATUS, localeInfo.STAT_TOOLTIP_BONUS, localeInfo.STAT_TOOLTIP_STATS]
		self.toolTip.ClearToolTip()
		self.toolTip.AppendTextLine(m_text_tooltip[stat])
		self.toolTip.Show()

	def __OverOutCharacterButton(self):
		self.__HideStatToolTip()

	def __OverInStatButton(self, stat):
		try:
			self.__ShowStatToolTip(self.STAT_DESCRIPTION[stat], localeInfo.STAT_TOOLTIP_ADD, TRUE)
		except KeyError:
			pass

	def __OverInStatButton2(self, stat):
		try:
			self.__ShowStatToolTip(self.STAT_DESCRIPTION[stat], localeInfo.STAT_TOOLTIP_ADD_2, TRUE)
		except KeyError:
			pass

	def __OverOutStatButton(self):
		self.__HideStatToolTip()

	def __ShowStatToolTip(self, statDesc, statDesc2 = FALSE, arg2 = FALSE):
		# Bonus tooltip'i kapat
		if app.ENABLE_RENEWAL_BONUS_BOARD:
			if self.BonusToolTip and hasattr(self.BonusToolTip, 'HideToolTip'):
				self.BonusToolTip.HideToolTip()
		
		self.toolTip.ClearToolTip()
		self.toolTip.AppendTextLine(statDesc)

		if arg2 == TRUE:
			self.toolTip.AppendTextLine(statDesc2)

		self.toolTip.Show()

	def __HideStatToolTip(self):
		self.toolTip.Hide()
		# Bonus tooltip'i de kapat (eðer açýksa)
		if app.ENABLE_RENEWAL_BONUS_BOARD:
			if self.BonusToolTip and hasattr(self.BonusToolTip, 'IsShow') and self.BonusToolTip.IsShow():
				if hasattr(self.BonusToolTip, 'HideToolTip'):
					self.BonusToolTip.HideToolTip()

	def OnPressEscapeKey(self):
		# ESC ile kapatýldýðýnda tüm tooltip'leri kapat
		from uiToolTip import ToolTip
		for tooltip in ToolTip._allToolTips:
			if tooltip and hasattr(tooltip, 'IsShow') and tooltip.IsShow():
				if hasattr(tooltip, 'HideToolTip'):
					tooltip.HideToolTip()
				elif hasattr(tooltip, 'Hide'):
					tooltip.Hide()

		if app.ENABLE_RENEWAL_QUEST:
			if self.questSlideWndNewKey > 0:
				if self.questSlideWnd[self.questSlideWndNewKey-1] is not None:
					self.questSlideWnd[self.questSlideWndNewKey-1].OnPressEscapeKey()

		self.Close()
		return TRUE

	def OnUpdate(self):
		self.__UpdateQuestClock()

		if app.ENABLE_SKILL_COLOR_SYSTEM:
			if self.skillColorWnd:
				self.__UpdateSkillColorPosition()

		if app.ENABLE_RENEWAL_BONUS_BOARD:
			self.Refresh()

		# Tooltip'lerin mouse pozisyonunu takip etmesi ve tooltip alanýndan çýkýldýðýnda gizlenmesi
		try:
			import wndMgr
			(x, y) = wndMgr.GetMousePosition()
			
			# Karakter penceresinin üzerinde mi kontrol et
			onWindow = False
			if self.IsShow():
				try:
					(wx, wy) = self.GetGlobalPosition()
					ww, wh = self.GetWidth(), self.GetHeight()
					if wx <= x <= wx + ww and wy <= y <= wy + wh:
						onWindow = True
				except:
					pass
			
			# Tüm tooltip'leri kontrol et
			tooltips_to_check = []
			if self.toolTip:
				tooltips_to_check.append(self.toolTip)
			if self.toolTipJob:
				tooltips_to_check.append(self.toolTipJob)
			if self.toolTipAlignment:
				tooltips_to_check.append(self.toolTipAlignment)
			if self.toolTipCharacterBoard:
				tooltips_to_check.append(self.toolTipCharacterBoard)
			if self.emotionToolTip:
				tooltips_to_check.append(self.emotionToolTip)
			if app.ENABLE_RENEWAL_BONUS_BOARD:
				if self.BonusToolTip:
					tooltips_to_check.append(self.BonusToolTip)
			
			# Karakter penceresinin üzerinde mi kontrol et
			onWindow = False
			if self.IsShow():
				try:
					(wx, wy) = self.GetGlobalPosition()
					ww, wh = self.GetWidth(), self.GetHeight()
					if wx <= x <= wx + ww and wy <= y <= wy + wh:
						onWindow = True
				except:
					pass
			
			# Her tooltip'i kontrol et
			for tooltip in tooltips_to_check:
				if tooltip and hasattr(tooltip, 'IsShow') and tooltip.IsShow():
					try:
						(tx, ty) = tooltip.GetGlobalPosition()
						tw, th = tooltip.GetWidth(), tooltip.GetHeight()
						onTooltip = (tx <= x <= tx + tw and ty <= y <= ty + th)
						
						# Ne tooltip'in üzerinde ne de karakter penceresinin üzerinde deðilse kapat
						if not onTooltip and not onWindow:
							if hasattr(tooltip, 'HideToolTip'):
								tooltip.HideToolTip()
							elif hasattr(tooltip, 'Hide'):
								tooltip.Hide()
					except:
						pass
			
			# toolTipSkill kontrolü (harici tooltip)
			if self.toolTipSkill and self.toolTipSkill != 0:
				if hasattr(self.toolTipSkill, 'IsShow') and self.toolTipSkill.IsShow():
					try:
						(tx, ty) = self.toolTipSkill.GetGlobalPosition()
						tw, th = self.toolTipSkill.GetWidth(), self.toolTipSkill.GetHeight()
						onTooltip = (tx <= x <= tx + tw and ty <= y <= ty + th)
						
						# Ne tooltip'in üzerinde ne de karakter penceresinin üzerinde deðilse kapat
						if not onTooltip and not onWindow:
							if hasattr(self.toolTipSkill, 'HideToolTip'):
								self.toolTipSkill.HideToolTip()
					except:
						pass
		except:
			pass

	## Skill Process
	def __RefreshSkillPage(self, name, slotCount):
		global SHOW_LIMIT_SUPPORT_SKILL_LIST

		skillPage = self.skillPageDict[name]

		startSlotIndex = skillPage.GetStartIndex()
		if "ACTIVE" == name:
			if self.PAGE_HORSE == self.curSelectedSkillGroup:
				startSlotIndex += slotCount

		getSkillType = skill.GetSkillType
		getSkillIndex = player.GetSkillIndex
		getSkillGrade = player.GetSkillGrade
		getSkillLevel = player.GetSkillLevel
		getSkillLevelUpPoint = skill.GetSkillLevelUpPoint
		getSkillMaxLevel = skill.GetSkillMaxLevel

		for i in xrange(slotCount+1):
			slotIndex = i + startSlotIndex
			skillIndex = getSkillIndex(slotIndex)

			for j in xrange(skill.SKILL_GRADE_COUNT):
				skillPage.ClearSlot(self.__GetRealSkillSlot(j, i))

			if 0 == skillIndex:
				continue

			skillGrade = getSkillGrade(slotIndex)
			skillLevel = getSkillLevel(slotIndex)
			skillType = getSkillType(skillIndex)

			## MountSkill
			if player.SKILL_INDEX_RIDING == skillIndex:
				if skillGrade == 1:
					skillLevel += 19
				elif skillGrade == 2:
					skillLevel += 29
				elif skillGrade == 3:
					skillLevel = 40

				skillPage.SetSkillSlotNew(slotIndex, skillIndex, max(skillLevel - 1, 0), skillLevel)
				skillPage.SetSlotCount(slotIndex, skillLevel)

			## ACTIVE
			elif skill.SKILL_TYPE_ACTIVE == skillType:
				for j in xrange(skill.SKILL_GRADE_COUNT):
					realSlotIndex = self.__GetRealSkillSlot(j, slotIndex)
					skillPage.SetSkillSlotNew(realSlotIndex, skillIndex, j, skillLevel)
					skillPage.SetCoverButton(realSlotIndex)

					if (skillGrade == skill.SKILL_GRADE_COUNT) and j == (skill.SKILL_GRADE_COUNT-1):
						skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)
					elif (not self.__CanUseSkillNow()) or (skillGrade != j):
						skillPage.SetSlotCount(realSlotIndex, 0)
						skillPage.DisableCoverButton(realSlotIndex)
						skillPage.DeactivateSlot(realSlotIndex) # hotfix
					else:
						skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)

					if player.IsSkillActive(slotIndex) and (skillGrade == j): # hotfix
						skillPage.ActivateSlot(realSlotIndex, wndMgr.COLOR_TYPE_WHITE)
			## SupportSkill
			else:
				if not SHOW_LIMIT_SUPPORT_SKILL_LIST or skillIndex in SHOW_LIMIT_SUPPORT_SKILL_LIST:
					realSlotIndex = self.__GetETCSkillRealSlotIndex(slotIndex)
					skillPage.SetSkillSlot(realSlotIndex, skillIndex, skillLevel)
					skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)

					if skill.CanUseSkill(skillIndex):
						skillPage.SetCoverButton(realSlotIndex)

					if player.IsSkillActive(slotIndex): # hotfix
						skillPage.ActivateSlot(realSlotIndex, wndMgr.COLOR_TYPE_WHITE)
					else:
						skillPage.DeactivateSlot(realSlotIndex)

			skillPage.RefreshSlot()

		self.__RestoreSlotCoolTime(skillPage)

		if app.ENABLE_SKILL_COLOR_SYSTEM:
			if "ACTIVE" == name:
				self.__CreateSkillColorButton(skillPage)

	def __RestoreSlotCoolTime(self, skillPage):
		restoreType = skill.SKILL_TYPE_NONE
		if self.PAGE_HORSE == self.curSelectedSkillGroup:
			restoreType = skill.SKILL_TYPE_HORSE
		else:
			restoreType = skill.SKILL_TYPE_ACTIVE

		skillPage.RestoreSlotCoolTime(restoreType)

	def RefreshSkill(self):
		if self.isLoaded == 0:
			return

		if self.__IsChangedHorseRidingSkillLevel():
			self.RefreshCharacter()
			return

		global SHOW_ONLY_ACTIVE_SKILL
		if SHOW_ONLY_ACTIVE_SKILL:
			self.__RefreshSkillPage("ACTIVE", self.ACTIVE_PAGE_SLOT_COUNT)
		else:
			self.__RefreshSkillPage("ACTIVE", self.ACTIVE_PAGE_SLOT_COUNT)
			self.__RefreshSkillPage("SUPPORT", self.SUPPORT_PAGE_SLOT_COUNT)

		self.RefreshSkillPlusButtonList()

	def CanShowPlusButton(self, skillIndex, skillLevel, curStatPoint):
		if 0 == skillIndex:
			return FALSE

		if not skill.CanLevelUpSkill(skillIndex, skillLevel):
			return FALSE

		return TRUE

	def __RefreshSkillPlusButton(self, name):
		global HIDE_SUPPORT_SKILL_POINT
		if HIDE_SUPPORT_SKILL_POINT and "SUPPORT" == name:
			return

		slotWindow = self.skillPageDict[name]
		slotWindow.HideAllSlotButton()

		labelWindow = self.labelPageStatDict[name]
		slotStatType = self.skillPageStatDict[name]
		if 0 == slotStatType:
			return

		statPoint = player.GetStatus(slotStatType)
		startSlotIndex = slotWindow.GetStartIndex()
		if "HORSE" == name:
			startSlotIndex += self.ACTIVE_PAGE_SLOT_COUNT

		if statPoint > 0:
			for i in xrange(self.PAGE_SLOT_COUNT):
				slotIndex = i + startSlotIndex
				skillIndex = player.GetSkillIndex(slotIndex)
				skillGrade = player.GetSkillGrade(slotIndex)
				skillLevel = player.GetSkillLevel(slotIndex)

				if skillIndex == 0:
					continue
				if skillGrade != 0:
					continue

				if name == "HORSE":
					if player.GetStatus(player.LEVEL) >= skill.GetSkillLevelLimit(skillIndex):
						if skillLevel < 20:
							slotWindow.ShowSlotButton(self.__GetETCSkillRealSlotIndex(slotIndex))
				else:
					if "SUPPORT" == name:
						if not SHOW_LIMIT_SUPPORT_SKILL_LIST or skillIndex in SHOW_LIMIT_SUPPORT_SKILL_LIST:
							if self.CanShowPlusButton(skillIndex, skillLevel, statPoint):
								slotWindow.ShowSlotButton(slotIndex)
					else:
						if self.CanShowPlusButton(skillIndex, skillLevel, statPoint):
							slotWindow.ShowSlotButton(slotIndex)
		else:
			labelWindow.Hide()

	if app.ENABLE_SKILL_COLOR_SYSTEM:
		def __CreateSkillColorButton(self, parent):
			self.skillColorButton = []

			xPos, yPos = 0, 0
			for idx in xrange(self.PAGE_SLOT_COUNT):
				skillSlot = idx
				if skillSlot < 6:
					if (skillSlot % 2) == 0:
						xPos = 75
						yPos = 4 + (skillSlot / 2 * 36)
					else:
						xPos = 187
						yPos = 4 + (skillSlot / 2 * 36)

					skillIndex = player.GetSkillIndex(skillSlot + 1)
					skillMaxGrade = 3

					if len(self.skillColorButton) == skillSlot:
						self.skillColorButton.append([])
						self.skillColorButton[skillSlot] = ui.Button()
						self.skillColorButton[skillSlot].SetParent(parent)
						self.skillColorButton[skillSlot].SetUpVisual("d:/ymir work/ui/game/skill_color/skill_color_button_default.tga")
						self.skillColorButton[skillSlot].SetOverVisual("d:/ymir work/ui/game/skill_color/skill_color_button_over.tga")
						self.skillColorButton[skillSlot].SetDownVisual("d:/ymir work/ui/game/skill_color/skill_color_button_down.tga")
						self.skillColorButton[skillSlot].SetPosition(xPos, yPos)
						self.skillColorButton[skillSlot].SetEvent(lambda arg = skillSlot, arg2 = skillIndex: self.__OnPressSkillColorButton(arg, arg2))
						if player.GetSkillGrade(skillSlot + 1) >= skillMaxGrade and (chr.IsPremium or chr.IsGameMaster):
							self.skillColorButton[skillSlot].Show()
						else:
							self.skillColorButton[skillSlot].Hide()
					else:
						self.skillColorButton[skillSlot].SetPosition(xPos, yPos)

		def __UpdateSkillColorPosition(self):
			x, y = self.GetGlobalPosition()
			self.skillColorWnd.SetPosition(x + 250, y)

		def __OnPressSkillColorButton(self, skillSlot, skillIndex):
			self.skillColorWnd = uiSkillColor.SkillColorWindow(skillSlot, skillIndex)

			if self.skillColorWnd and not self.skillColorWnd.IsShow():
				self.skillColorWnd.Show()

	def RefreshSkillPlusButtonList(self):
		if self.isLoaded==0:
			return

		self.RefreshSkillPlusPointLabel()

		if not self.__CanUseSkillNow():
			return

		try:
			if self.PAGE_HORSE == self.curSelectedSkillGroup:
				self.__RefreshSkillPlusButton("HORSE")
			else:
				self.__RefreshSkillPlusButton("ACTIVE")

			self.__RefreshSkillPlusButton("SUPPORT")

		except:
			import exception
			exception.Abort("CharacterWindow.RefreshSkillPlusButtonList.BindObject")

	def RefreshSkillPlusPointLabel(self):
		if self.isLoaded==0:
			return

		if self.PAGE_HORSE == self.curSelectedSkillGroup:
			activeStatPoint = player.GetStatus(player.SKILL_HORSE)
			self.activeSkillPointValue.SetText(str(activeStatPoint))

		else:
			activeStatPoint = player.GetStatus(player.SKILL_ACTIVE)
			self.activeSkillPointValue.SetText(str(activeStatPoint))

		supportStatPoint = max(0, player.GetStatus(player.SKILL_SUPPORT))
		self.supportSkillPointValue.SetText(str(supportStatPoint))

	## Skill Level Up Button
	def OnPressedSlotButton(self, slotNumber):
		srcSlotIndex = self.__RealSkillSlotToSourceSlot(slotNumber)

		skillIndex = player.GetSkillIndex(srcSlotIndex)
		curLevel = player.GetSkillLevel(srcSlotIndex)
		maxLevel = skill.GetSkillMaxLevel(skillIndex)

		net.SendChatPacket("/skillup " + str(skillIndex))

	## Use Skill
	def ClickSkillSlot(self, slotIndex):
		srcSlotIndex = self.__RealSkillSlotToSourceSlot(slotIndex)
		skillIndex = player.GetSkillIndex(srcSlotIndex)
		skillType = skill.GetSkillType(skillIndex)

		if not self.__CanUseSkillNow():
			if skill.SKILL_TYPE_ACTIVE == skillType:
				return

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				if skill.CanUseSkill(skillIndex):
					player.ClickSkillSlot(srcSlotIndex)
					return

		mouseModule.mouseController.DeattachObject()

	def OnUseSkill(self, slotIndex, coolTime):
		skillIndex = player.GetSkillIndex(slotIndex)
		skillType = skill.GetSkillType(skillIndex)

		## ACTIVE
		if skill.SKILL_TYPE_ACTIVE == skillType:
			skillGrade = player.GetSkillGrade(slotIndex)
			slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)
		## ETC
		else:
			slotIndex = self.__GetETCSkillRealSlotIndex(slotIndex)

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				slotWindow.StoreSlotCoolTime(skillType, slotIndex, coolTime)
				self.__RestoreSlotCoolTime(slotWindow)
				#slotWindow.SetSlotCoolTime(slotIndex, coolTime)
				return

	def OnActivateSkill(self, slotIndex):
		skillGrade = player.GetSkillGrade(slotIndex)
		slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				slotWindow.ActivateSlot(slotIndex, wndMgr.COLOR_TYPE_WHITE)
				return

		self.RefreshSkill()

	def OnDeactivateSkill(self, slotIndex):

		skillGrade = player.GetSkillGrade(slotIndex)
		slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				slotWindow.DeactivateSlot(slotIndex)
				return

		self.RefreshSkill()

	def __ShowJobToolTip(self):
		# Bonus tooltip'i kapat
		if app.ENABLE_RENEWAL_BONUS_BOARD:
			if self.BonusToolTip and hasattr(self.BonusToolTip, 'HideToolTip'):
				self.BonusToolTip.HideToolTip()
		
		self.toolTipJob.ShowToolTip()

	def SkillClearCoolTime(self, slotIndex):
		slotIndex = self.__GetRealSkillSlot(player.GetSkillGrade(slotIndex), slotIndex)
		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				slotWindow.SetSlotCoolTime(slotIndex, 0)

	def __HideJobToolTip(self):
		self.toolTipJob.HideToolTip()

	def __SetJobText(self, mainJob, subJob):
		if player.GetStatus(player.LEVEL) <5:
			subJob = 0

	def __ShowAlignmentToolTip(self):
		# Bonus tooltip'i kapat
		if app.ENABLE_RENEWAL_BONUS_BOARD:
			if self.BonusToolTip and hasattr(self.BonusToolTip, 'HideToolTip'):
				self.BonusToolTip.HideToolTip()
		
		self.toolTipAlignment.ShowToolTip()

	def __HideAlignmentToolTip(self):
		self.toolTipAlignment.HideToolTip()

	def __ShowHTHToolTip(self):
		# Bonus tooltip'i kapat
		if app.ENABLE_RENEWAL_BONUS_BOARD:
			if self.BonusToolTip and hasattr(self.BonusToolTip, 'HideToolTip'):
				self.BonusToolTip.HideToolTip()
		
		self.toolTipCharacterBoard.ClearToolTip()
		self.toolTipCharacterBoard.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_IMG_CON)
		self.toolTipCharacterBoard.AlignHorizonalCenter()

		self.toolTipCharacterBoard.ShowToolTip()

	def __HideHTHToolTip(self):
		self.toolTipCharacterBoard.HideToolTip()

	def __ShowINTToolTip(self):
		# Bonus tooltip'i kapat
		if app.ENABLE_RENEWAL_BONUS_BOARD:
			if self.BonusToolTip and hasattr(self.BonusToolTip, 'HideToolTip'):
				self.BonusToolTip.HideToolTip()
		
		self.toolTipCharacterBoard.ClearToolTip()
		self.toolTipCharacterBoard.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_IMG_INT)
		self.toolTipCharacterBoard.AlignHorizonalCenter()

		self.toolTipCharacterBoard.ShowToolTip()

	def __HideINTToolTip(self):
		self.toolTipCharacterBoard.HideToolTip()

	def __ShowSTRToolTip(self):
		# Bonus tooltip'i kapat
		if app.ENABLE_RENEWAL_BONUS_BOARD:
			if self.BonusToolTip and hasattr(self.BonusToolTip, 'HideToolTip'):
				self.BonusToolTip.HideToolTip()
		
		self.toolTipCharacterBoard.ClearToolTip()
		self.toolTipCharacterBoard.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_IMG_STR)
		self.toolTipCharacterBoard.AlignHorizonalCenter()

		self.toolTipCharacterBoard.ShowToolTip()

	def __HideSTRToolTip(self):
		self.toolTipCharacterBoard.HideToolTip()

	def __ShowDEXToolTip(self):
		# Bonus tooltip'i kapat
		if app.ENABLE_RENEWAL_BONUS_BOARD:
			if self.BonusToolTip and hasattr(self.BonusToolTip, 'HideToolTip'):
				self.BonusToolTip.HideToolTip()
		
		self.toolTipCharacterBoard.ClearToolTip()
		self.toolTipCharacterBoard.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_IMG_DEX)
		self.toolTipCharacterBoard.AlignHorizonalCenter()

		self.toolTipCharacterBoard.ShowToolTip()

	def __HideDEXToolTip(self):
		self.toolTipCharacterBoard.HideToolTip()

	def __ShowHELToolTip(self):
		# Bonus tooltip'i kapat
		if app.ENABLE_RENEWAL_BONUS_BOARD:
			if self.BonusToolTip and hasattr(self.BonusToolTip, 'HideToolTip'):
				self.BonusToolTip.HideToolTip()
		
		self.toolTipCharacterBoard.ClearToolTip()
		self.toolTipCharacterBoard.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_IMG_HEL)
		self.toolTipCharacterBoard.AlignHorizonalCenter()

		self.toolTipCharacterBoard.ShowToolTip()

	def __HideHELToolTip(self):
		self.toolTipCharacterBoard.HideToolTip()

	def __ShowSPToolTip(self):
		# Bonus tooltip'i kapat
		if app.ENABLE_RENEWAL_BONUS_BOARD:
			if self.BonusToolTip and hasattr(self.BonusToolTip, 'HideToolTip'):
				self.BonusToolTip.HideToolTip()
		
		self.toolTipCharacterBoard.ClearToolTip()
		self.toolTipCharacterBoard.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_IMG_SP)
		self.toolTipCharacterBoard.AlignHorizonalCenter()

		self.toolTipCharacterBoard.ShowToolTip()

	def __HideSPToolTip(self):
		self.toolTipCharacterBoard.HideToolTip()

	def __ShowATTToolTip(self):
		# Bonus tooltip'i kapat
		if app.ENABLE_RENEWAL_BONUS_BOARD:
			if self.BonusToolTip and hasattr(self.BonusToolTip, 'HideToolTip'):
				self.BonusToolTip.HideToolTip()
		
		self.toolTipCharacterBoard.ClearToolTip()
		self.toolTipCharacterBoard.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_IMG_ATT)
		self.toolTipCharacterBoard.AlignHorizonalCenter()

		self.toolTipCharacterBoard.ShowToolTip()

	def __HideATTToolTip(self):
		self.toolTipCharacterBoard.HideToolTip()

	def __ShowDEFToolTip(self):
		# Bonus tooltip'i kapat
		if app.ENABLE_RENEWAL_BONUS_BOARD:
			if self.BonusToolTip and hasattr(self.BonusToolTip, 'HideToolTip'):
				self.BonusToolTip.HideToolTip()
		
		self.toolTipCharacterBoard.ClearToolTip()
		self.toolTipCharacterBoard.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_IMG_DEF)
		self.toolTipCharacterBoard.AlignHorizonalCenter()

		self.toolTipCharacterBoard.ShowToolTip()

	def __HideDEFToolTip(self):
		self.toolTipCharacterBoard.HideToolTip()

	def __ShowMSPDToolTip(self):
		# Bonus tooltip'i kapat
		if app.ENABLE_RENEWAL_BONUS_BOARD:
			if self.BonusToolTip and hasattr(self.BonusToolTip, 'HideToolTip'):
				self.BonusToolTip.HideToolTip()
		
		self.toolTipCharacterBoard.ClearToolTip()
		self.toolTipCharacterBoard.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_MOVE_SPEED)
		self.toolTipCharacterBoard.AlignHorizonalCenter()

		self.toolTipCharacterBoard.ShowToolTip()

	def __HideMSPDToolTip(self):
		self.toolTipCharacterBoard.HideToolTip()

	def __ShowASPDToolTip(self):
		# Bonus tooltip'i kapat
		if app.ENABLE_RENEWAL_BONUS_BOARD:
			if self.BonusToolTip and hasattr(self.BonusToolTip, 'HideToolTip'):
				self.BonusToolTip.HideToolTip()
		
		self.toolTipCharacterBoard.ClearToolTip()
		self.toolTipCharacterBoard.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_ATT_SPEED)
		self.toolTipCharacterBoard.AlignHorizonalCenter()

		self.toolTipCharacterBoard.ShowToolTip()

	def __HideASPDToolTip(self):
		self.toolTipCharacterBoard.HideToolTip()

	def __ShowCSPDToolTip(self):
		# Bonus tooltip'i kapat
		if app.ENABLE_RENEWAL_BONUS_BOARD:
			if self.BonusToolTip and hasattr(self.BonusToolTip, 'HideToolTip'):
				self.BonusToolTip.HideToolTip()
		
		self.toolTipCharacterBoard.ClearToolTip()
		self.toolTipCharacterBoard.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_CAST_SPEED)
		self.toolTipCharacterBoard.AlignHorizonalCenter()

		self.toolTipCharacterBoard.ShowToolTip()

	def __HideCSPDToolTip(self):
		self.toolTipCharacterBoard.HideToolTip()

	def __ShowMATTToolTip(self):
		# Bonus tooltip'i kapat
		if app.ENABLE_RENEWAL_BONUS_BOARD:
			if self.BonusToolTip and hasattr(self.BonusToolTip, 'HideToolTip'):
				self.BonusToolTip.HideToolTip()
		
		self.toolTipCharacterBoard.ClearToolTip()
		self.toolTipCharacterBoard.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_MAG_ATT)
		self.toolTipCharacterBoard.AlignHorizonalCenter()

		self.toolTipCharacterBoard.ShowToolTip()

	def __HideMATTToolTip(self):
		self.toolTipCharacterBoard.HideToolTip()

	def __ShowMDEFToolTip(self):
		# Bonus tooltip'i kapat
		if app.ENABLE_RENEWAL_BONUS_BOARD:
			if self.BonusToolTip and hasattr(self.BonusToolTip, 'HideToolTip'):
				self.BonusToolTip.HideToolTip()
		
		self.toolTipCharacterBoard.ClearToolTip()
		self.toolTipCharacterBoard.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_MAG_DEF)
		self.toolTipCharacterBoard.AlignHorizonalCenter()

		self.toolTipCharacterBoard.ShowToolTip()

	def __HideMDEFToolTip(self):
		self.toolTipCharacterBoard.HideToolTip()

	def __ShowERToolTip(self):
		# Bonus tooltip'i kapat
		if app.ENABLE_RENEWAL_BONUS_BOARD:
			if self.BonusToolTip and hasattr(self.BonusToolTip, 'HideToolTip'):
				self.BonusToolTip.HideToolTip()
		
		self.toolTipCharacterBoard.ClearToolTip()
		self.toolTipCharacterBoard.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_MAG_ER)
		self.toolTipCharacterBoard.AlignHorizonalCenter()

		self.toolTipCharacterBoard.ShowToolTip()

	def __HideERToolTip(self):
		self.toolTipCharacterBoard.HideToolTip()

	def RefreshCharacter(self):
		if self.isLoaded == 0:
			return

		## Name
		try:
			characterName = player.GetName()
			guildName = player.GetGuildName()
			self.characterNameValue.SetText(characterName)
			self.guildNameValue.SetText(guildName)
			if not guildName:
				self.characterNameSlot.SetPosition(109, 34)

				self.guildNameSlot.Hide()
			else:
				self.characterNameSlot.SetPosition(153, 34)
				self.guildNameSlot.Show()
		except:
			import exception
			exception.Abort("CharacterWindow.RefreshCharacter.BindObject")

		race = net.GetMainActorRace()
		group = net.GetMainActorSkillGroup()
		empire = net.GetMainActorEmpire()

		## Job Text
		job = chr.RaceToJob(race)
		self.__SetJobText(job, group)

		## FaceImage
		try:
			faceImageName = FACE_IMAGE_DICT[race]

			try:
				self.faceImage.LoadImage(faceImageName)
			except:
				print "CharacterWindow.RefreshCharacter(race=%d, faceImageName=%s)" % (race, faceImageName)
				self.faceImage.Hide()

		except KeyError:
			self.faceImage.Hide()

		## GroupName
		self.__SetSkillGroupName(race, group)

		## Skill
		if 0 == group:
			self.__SelectSkillGroup(0)

		else:
			self.__SetSkillSlotData(race, group, empire)

			if self.__CanUseHorseSkill():
				self.__SelectSkillGroup(0)

	def __SetSkillGroupName(self, race, group):

		job = chr.RaceToJob(race)

		if not self.SKILL_GROUP_NAME_DICT.has_key(job):
			return

		nameList = self.SKILL_GROUP_NAME_DICT[job]

		if 0 == group:
			self.skillGroupButton1.SetText(nameList[1])
			self.skillGroupButton2.SetText(nameList[2])
			self.skillGroupButton1.Show()
			self.skillGroupButton2.Show()
			self.activeSkillGroupName.Hide()
		else:
			if self.__CanUseHorseSkill():
				self.activeSkillGroupName.Show()	#orjinal Hide()
				self.skillGroupButton1.SetText(nameList.get(group, "Noname"))
				self.skillGroupButton2.SetText(localeInfo.SKILL_GROUP_HORSE)
				self.skillGroupButton1.Hide()	#orjinal Show()
				self.skillGroupButton2.Hide()	#orjinal Show()
			else:
				self.activeSkillGroupName.SetText(nameList.get(group, "Noname"))
				self.activeSkillGroupName.Show()
				self.skillGroupButton1.Hide()
				self.skillGroupButton2.Hide()

	def __SetSkillSlotData(self, race, group, empire=0):
		## SkillIndex
		net.RegisterSkills(race, group, empire)

		## Event
		self.__SetSkillSlotEvent()

		## Refresh
		self.RefreshSkill()

	def __SelectSkillGroup(self, index):
		for btn in self.skillGroupButton:
			btn.SetUp()
		self.skillGroupButton[index].Down()

		if self.__CanUseHorseSkill():
			if 0 == index:
				index = net.GetMainActorSkillGroup() - 1
			elif 1 == index:
				index = self.PAGE_HORSE

		self.curSelectedSkillGroup = index
		self.__SetSkillSlotData(net.GetMainActorRace(), index+1, net.GetMainActorEmpire())

	def __CanUseSkillNow(self):
		if 0 == net.GetMainActorSkillGroup():
			return FALSE

		return TRUE

	def __CanUseHorseSkill(self):
		slotIndex = player.GetSkillSlotIndex(player.SKILL_INDEX_RIDING)

		if not slotIndex:
			return FALSE

		grade = player.GetSkillGrade(slotIndex) # hotfix
		level = player.GetSkillLevel(slotIndex)

		if level < 0:
			level *= -1

		if level >= 20:
			return TRUE

		if grade >= 1 and level >= 1: # hotfix
			return True

		return FALSE

	def __IsChangedHorseRidingSkillLevel(self):
		ret = FALSE

		if -1 == self.canUseHorseSkill:
			self.canUseHorseSkill = self.__CanUseHorseSkill()

		if self.canUseHorseSkill != self.__CanUseHorseSkill():
			ret = TRUE

		self.canUseHorseSkill = self.__CanUseHorseSkill()
		return ret

	def __GetRealSkillSlot(self, skillGrade, skillSlot):
		return skillSlot + min(skill.SKILL_GRADE_COUNT-1, skillGrade) * skill.SKILL_GRADE_STEP_COUNT

	def __GetETCSkillRealSlotIndex(self, skillSlot):
		if skillSlot > 100:
			return skillSlot
		return skillSlot % self.ACTIVE_PAGE_SLOT_COUNT

	def __RealSkillSlotToSourceSlot(self, realSkillSlot):
		if realSkillSlot > 100:
			return realSkillSlot
		if self.PAGE_HORSE == self.curSelectedSkillGroup:
			return realSkillSlot + self.ACTIVE_PAGE_SLOT_COUNT
		return realSkillSlot % skill.SKILL_GRADE_STEP_COUNT

	def __GetSkillGradeFromSlot(self, skillSlot):
		return int(skillSlot / skill.SKILL_GRADE_STEP_COUNT)

	def SelectSkillGroup(self, index):
		self.__SelectSkillGroup(index)

	def OnQuestScroll(self):
		questCount = quest.GetQuestCount()
		scrollLineCount = max(0, questCount - quest.QUEST_MAX_NUM)
		startIndex = int(scrollLineCount * self.questScrollBar.GetPos())

		if startIndex != self.questShowingStartIndex:
			self.questShowingStartIndex = startIndex
			self.RefreshQuest()

	if app.ENABLE_RENEWAL_QUEST:
		def __OnScrollQuest(self):
			if self.state != "QUEST":
				return

			curPos = self.questScrollBar.GetPos()
			if math.fabs(curPos - self.questLastScrollPosition) >= 0.001:
				self.RerenderQuestPage()
				self.questLastScrollPosition = curPos

		def ResetQuestScroll(self):
			self.questScrollBar.Hide()

			if self.questScrollBar.GetPos() != 0:
				self.questScrollBar.SetPos(0)

		def RerenderQuestPage(self):
			overflowingY = self.displayY - self.MAX_QUEST_PAGE_HEIGHT
			if overflowingY < 0:
				overflowingY = 0

			self.baseCutY = math.ceil(overflowingY * self.questScrollBar.GetPos())
			self.displayY = 0
			self.RearrangeQuestCategories(xrange(quest.QUEST_CATEGORY_MAX_NUM))
			self.RefreshQuestCategory()

			if overflowingY > 0:
				if (len(self.questOpenedCategories)) == 0:
					self.ResetQuestScroll()
				else:
					self.questScrollBar.Show()
			else:
				self.ResetQuestScroll()

		def __LoadQuestCategory(self):
			self.questPage.Show()

			if self.isLoaded == 0:
				return

			for i in xrange(quest.QUEST_CATEGORY_MAX_NUM):
				category = self.questCategoryList[i]

				categoryName = category.GetProperty("name")
				if not categoryName:
					category.SetProperty("name", category.GetText())
					categoryName = category.GetText()

				questCount = self.GetQuestCountInCategory(i)
				self.questCategoryList[i].SetTextAlignLeft(categoryName + " (" + str(questCount) + ")")
				self.questCategoryList[i].SetTextColor(self.GetQuestCategoryColor(i))
				self.questCategoryList[i].SetQuestLabel(quest_lable_expend_img_path_dict[i], self.GetQuestCountInCategory(i))
				self.questCategoryList[i].Show()

			self.RefreshQuestCategory()
			if self.isQuestCategoryLoad == FALSE:
				self.questScrollBar.Hide()
			else:
				self.RerenderQuestPage()

			self.isQuestCategoryLoad = TRUE

		def GetQuestCategoryColor(self, category):
			return self.questColorList["default_title"]

		def GetQuestProperties(self, questName):
			findString = {
				"*" : "blue",
				"&" : "green",
				"~" : "golden"
			}

			if questName[0] in findString:
				return (questName[1:], findString[questName[0]])

			return (questName, None)

		def IsQuestCategoryOpen(self, category):
			return (category in self.questOpenedCategories)

		def ToggleCategory(self, category):
			if self.IsQuestCategoryOpen(category):
				self.CloseQuestCategory(category)
			else:
				self.OpenQuestCategory(category)

		def RearrangeQuestCategories(self, categoryRange):
			i = 0
			for i in categoryRange:
				if (self.displayY - self.baseCutY) >= 0 and (self.displayY - self.baseCutY) < self.MAX_QUEST_PAGE_HEIGHT - 20:
					self.questCategoryList[i].SetPosition(13, (self.displayY - self.baseCutY) + 10)
					self.questCategoryList[i].Show()
				else:
					self.questCategoryList[i].Hide()

				self.displayY += 20
				self.questCategoryRenderPos[i] = self.displayY

		def CloseQuestCategory(self, category):
			self.questCategoryList[category].CloseCategory(self.GetQuestCountInCategory(category))

			if category in self.questOpenedCategories:
				self.questOpenedCategories.remove(category)

			for currentSlot in self.questSlotList:
				if currentSlot.GetProperty("category") == category:
					currentSlot.Hide()
					self.displayY -= currentSlot.GetHeight()

			self.RerenderQuestPage()

		def OpenQuestCategory(self, category):
			if self.GetQuestCountInCategory(category) == 0:
				return

			while len(self.questOpenedCategories) >= self.questMaxOpenedCategories:
				openedCategories = self.questOpenedCategories.pop()
				self.CloseQuestCategory(openedCategories)

			self.questCategoryList[category].OpenCategory(self.GetQuestCountInCategory(category))
			self.questOpenedCategories.append(category)
			self.RefreshQuestCategory(category)
			self.RerenderQuestPage()

		def RefreshQuestCategory(self, category = -1):
			if self.isLoaded == 0 or self.state != "QUEST":
				return

			categories = []
			if category == -1:
				categories = self.questOpenedCategories
			elif not category in self.questOpenedCategories:
				self.OpenQuestCategory(category)
				return
			else:
				categories.append(category)

			for currentCategory in categories:
				self.displayY = self.questCategoryRenderPos[currentCategory]

				self.LoadCategory(currentCategory)
				self.RearrangeQuestCategories(xrange(currentCategory + 1, quest.QUEST_CATEGORY_MAX_NUM))

		def RefreshQuestCategoriesCount(self):
			for category in xrange(quest.QUEST_CATEGORY_MAX_NUM):
				categoryName = self.questCategoryList[category].GetProperty("name")
				questCount = self.GetQuestCountInCategory(category)
				self.questCategoryList[category].SetTextAlignLeft(categoryName + " (" + str(questCount) + ")")

		def RefreshQuest(self):
			if self.isLoaded == 0 or self.state != "QUEST":
				return

			for category in self.questOpenedCategories:
				self.RefreshQuestCategory(category)

			self.RefreshQuestCategoriesCount()

		def CreateQuestSlot(self, name):
			for questSlot in self.questSlotList:
				if questSlot.GetWindowName() == name:
					return questSlot

			pyScrLoader = ui.PythonScriptLoader()
			slot = ui.ListBar()
			pyScrLoader.LoadElementListBar(slot, quest_slot_listbar, self.questPage)

			slot.SetParent(self.quest_page_board_window)
			slot.SetWindowName(name)
			slot.Hide()
			self.questSlotList.append(slot)
			return slot

		def SetQuest(self, slot, questID, questName, questCounterName, questCounterValue):
			(name, color) = self.GetQuestProperties(questName)
			slot.SetTextAlignLeft(name, 20)
			if color:
				slot.SetTextColor(self.questColorList[color])
			slot.SetEvent(ui.__mem_func__(self.__SelectQuest), questID)
			slot.SetWindowHorizontalAlignLeft()
			slot.Show()

		def LoadCategory(self, category):
			self.questIndexMap = {}
			self.questCounterList = []
			self.questClockList = []
			self.questSeparatorList = []

			for questSlot in self.questSlotList:
				questSlot.Hide()

			questCount = 0
			for questIdx in self.GetQuestsInCategory(category):
				questCount += 1
				(questID, questIndex, questName, questCategory, _, questCounterName, questCounterValue) = questIdx
				(lastName, lastTime) = quest.GetQuestLastTime(questID)

				slot = self.CreateQuestSlot("QuestSlotList_" + str(questCategory) + "_" + str(questID))

				slot.SetPosition(0, (self.displayY - self.baseCutY))
				slot.SetParent(self.quest_page_board_window)
				baseDisplayY = self.displayY

				## -- Quest Counter
				hasCounter = FALSE
				if questCounterName != "":
					self.displayY += 15

					counter = ui.TextLine()
					counter.SetParent(slot)
					counter.SetPosition(20, 20 - 2.5)
					counter.SetText(questCounterName + ": " + str(questCounterValue))
					counter.Show()

					self.questCounterList.append(counter)
					hasCounter = TRUE
				## -- Quest Counter

				## -- Quest Clock
				self.displayY += 15

				clockText = localeInfo.QUEST_UNLIMITED_TIME
				if len(lastName) > 0:
					if lastTime <= 0:
						clockText = localeInfo.QUEST_TIMEOVER
					else:
						questLastMinute = lastTime / 60
						questLastSecond = lastTime % 60

						clockText = lastName + " : "

						if questLastMinute > 0:
							clockText += str(questLastMinute) + localeInfo.QUEST_MIN
							if questLastSecond > 0:
								clockText += " "

						if questLastSecond > 0:
							clockText += str(questLastSecond) + localeInfo.QUEST_SEC

				clock = ui.TextLine()
				clock.SetParent(slot)
				clock.SetPosition(20, 20 + (int(hasCounter) * 14) - 2.5)
				clock.SetText(clockText)
				clock.SetProperty("idx", questID)
				self.questClockList.append(clock)
				clock.Show()
				## -- Quest Clock

				## -- Quest Separator
				self.displayY += 5
				if questCount < self.GetQuestCountInCategory(category):
					seperator = ui.ImageBox()
					seperator.SetParent(slot)
					seperator.SetPosition(4, 20 + (int(hasCounter) * 14 - 2.5) + 15)
					seperator.LoadImage("d:/ymir work/ui/quest_re/quest_list_line_01.tga")
					seperator.Show()
					self.questSeparatorList.append(seperator)
				## -- Quest Separator

				slot.SetProperty("category", questCategory)

				if questIndex in self.questClicked:
					slot.OnClickEvent()

				if (baseDisplayY - self.baseCutY) + 2 >= 0 and (baseDisplayY - self.baseCutY) + 2 < self.MAX_QUEST_PAGE_HEIGHT - 30:
					self.questIndexMap[questID] = questIndex
					self.SetQuest(slot, questID, questName, questCounterName, questCounterValue)

				self.displayY += 15

			newList = []
			for questSlot in self.questSlotList:
				if questSlot.IsShow():
					newList.append(questSlot)

			self.questSlotList = newList

		def __OnClickQuestCategoryButton(self, category):
			self.ToggleCategory(category)

		def GetQuestsInCategory(self, category, retCount = FALSE):
			questList = []
			count = 0
			for i in xrange(quest.GetQuestCount()):
				(questIndex, questName, questCategory, questIcon, questCounterName, questCounterValue) = quest.GetQuestData(i)
				if questCategory == category:
					count += 1
					questList.append((i, questIndex, questName, questCategory, questIcon, questCounterName, questCounterValue))

			if retCount:
				return count

			return questList

		def GetQuestCountInCategory(self, category):
			return self.GetQuestsInCategory(category, TRUE)

	def OnMoveWindow(self, x, y):
		pass
