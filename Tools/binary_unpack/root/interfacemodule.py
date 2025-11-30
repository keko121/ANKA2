if __USE_DYNAMIC_MODULE__:
	import pyapi

app = __import__(pyapi.GetModuleName("app"))
chr = __import__(pyapi.GetModuleName("chr"))
player = __import__(pyapi.GetModuleName("player"))
net = __import__(pyapi.GetModuleName("net"))

import constInfo
import systemSetting
import wndMgr
import os
import chat
import uiTaskBar
import uiCharacter
import uiInventory
import uiChat
import uiMessenger
import guild

import ui
import uiWhisper
import uiPointReset
import uiShop
import uiExchange
import uiSystem
import uiRestart
import uiToolTip
import uiMiniMap
import uiParty
import uiSafebox
import uiGuild
import uiQuest
import uiPrivateShopBuilder
import uiCommon
import uiRefine
import uiEquipmentDialog
import uiGameButton
import uiTip
import uiCube
import miniMap
import uiselectitem
import uiScriptLocale

import shop
import event
import localeInfo

if app.ENABLE_GUILD_RANK_SYSTEM:
	import uiGuildRanking

if app.ENABLE_RENEWAL_SWITCHBOT:
	import uiSwitchbot

if app.ENABLE_ACCE_COSTUME_SYSTEM:
	import uiAcce

if app.ENABLE_BIOLOG_SYSTEM:
	import uiBiologManager

if app.ENABLE_VIEW_CHEST_DROP:
	import uiChestDrop

if app.ENABLE_SPECIAL_INVENTORY:
	import uiSpecialInventory

if app.ENABLE_EVENT_MANAGER:
	import uiEvent

if app.ENABLE_MINIGAME_OKEY_CARDS_SYSTEM:
	import uiCards

if app.ENABLE_RENEWAL_BATTLE_PASS:
	import uiBattlePass

if app.ENABLE_RENDER_TARGET:
	import uiRenderTarget

if app.ENABLE_RENEWAL_OFFLINESHOP:
	import uiOfflineShopBuilder
	import uiOfflineShop

if app.ENABLE_OFFLINESHOP_SEARCH_SYSTEM:
	import uiPrivateShopSearch

if app.ENABLE_INGAME_WIKI_SYSTEM:
	import uiWiki

if app.ENABLE_RENEWAL_SKILL_SELECT:
	import uiSkillSelect

if app.ENABLE_NEW_DUNGEON_LIB:
	import uiDungeonTimer

if app.ENABLE_RENEWAL_INGAME_ITEMSHOP:
	import uiItemShop

if app.ENABLE_AURA_COSTUME_SYSTEM:
	import uiAura

if app.ENABLE_GUILDBANK_LOG:
	import uiGuildBank
	
if app.ENABLE_FISH_GAME:
	import uiFishGame

if app.ENABLE_GROWTH_PET_SYSTEM:
	import uiPetInfo

if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
	import uiTeleport

if app.ENABLE_DUNGEON_TRACKING_SYSTEM:
	import uiTrack

if app.ENABLE_RENEWAL_SPECIAL_CHAT:
	import uiSpecialChat

if app.ENABLE_CHANGE_LOOK_SYSTEM:
	import uiChangeLook

if app.ENABLE_HUNTING_SYSTEM:
	import uiHunting

if app.ENABLE_RIDING_EXTENDED:
	import uiMountUpGrade

if app.__AUTO_HUNT__:
	import uiAutoHunt

if app.ENABLE_AUTO_SELL_SYSTEM:
	import uiautosell

IsQBHide = 0
class Interface(object):
	CHARACTER_STATUS_TAB = 1
	CHARACTER_SKILL_TAB = 2

	def __init__(self):
		systemSetting.SetInterfaceHandler(self)
		self.windowOpenPosition = 0
		self.dlgWhisperWithoutTarget = None
		self.inputDialog = None
		self.tipBoard = None
		self.bigBoard = None

		if app.ENABLE_RENEWAL_OX_EVENT:
			self.bigBoardControl = None

		if app.ENABLE_AUTO_SELL_SYSTEM:
			self.wndAutoSell = None

		self.mallPageDlg = None

		self.wndWeb = None
		self.wndTaskBar = None
		self.wndCharacter = None
		self.wndInventory = None
		self.wndExpandedTaskBar = None
		self.wndChat = None
		self.wndMessenger = None
		self.wndMiniMap = None
		self.wndGuild = None
		self.wndGuildBuilding = None

		if app.ENABLE_RENEWAL_SWITCHBOT:
			self.wndSwitchbot = None

		if app.ENABLE_RENEWAL_CUBE:
			self.wndCubeRenewal = None

		if app.ENABLE_BIOLOG_SYSTEM:
			self.wndBiologManager = {}

		if app.ENABLE_VIEW_CHEST_DROP:
			self.dlgChestDrop = None

		if app.ENABLE_SPECIAL_INVENTORY:
			self.wndSpecialInventory = None

		if app.ENABLE_EVENT_MANAGER:
			self.wndEventOverview = None

		if app.ENABLE_RENEWAL_BATTLE_PASS:
			self.wndBattlePassExtended = None
			self.isFirstOpeningExtBattlePass = FALSE

		if app.ENABLE_RENDER_TARGET:
			self.wndRenderTarget = None

		if app.ENABLE_RENEWAL_OFFLINESHOP:
			self.dlgOfflineShop = None
			self.dlgOfflineShopPanel = None
			self.offlineShopBuilder = None
			self.dlgShopMessage = None

		if app.ENABLE_OFFLINESHOP_SEARCH_SYSTEM:
			self.wndPrivateShopSearch = None

		if app.ENABLE_INGAME_WIKI_SYSTEM:
			self.wndWiki = None

		if app.ENABLE_NEW_DUNGEON_LIB:
			self.wndDungeonTimer = None

		if app.ENABLE_RENEWAL_INGAME_ITEMSHOP:
			self.wndItemShop = None

		if app.ENABLE_SLOT_MARKING_SYSTEM:
			self.OnTopWindow = None
			self.dlgShop = None
			self.dlgExchange = None
			self.privateShopBuilder = None
			self.wndSafebox = None
			self.dlgRefineNew = None

		if app.ENABLE_RIDING_EXTENDED:
			self.wndMountUpGrade = None

		if app.ENABLE_FISH_GAME:
			self.wndFishGame = None

		if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
			self.wndWarpWindow = None

		if app.ENABLE_DUNGEON_TRACKING_SYSTEM:
			self.wndTrackWindow = None

		if app.ENABLE_RENEWAL_SPECIAL_CHAT:
			self.wndSpecialChat = None

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			self.wndChangeLook = None

		if app.ENABLE_HUNTING_SYSTEM:
			self.wndHunting = None
			self.wndHuntingSelect = None
			self.wndHuntingReward = None

		if app.__AUTO_HUNT__:
			self.wndAutoHunt = None

		self.listGMName = {}
		self.wndQuestWindow = {}
		self.wndQuestWindowNewKey = 0
		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}

		self.OpenLinkQuestionDialog = None

		self.wndExpandedMoneyTaskBar = None

		event.SetInterfaceWindow(self)

	def __del__(self):
		systemSetting.DestroyInterfaceHandler()
		event.SetInterfaceWindow(None)

	################################
	## Make Windows & Dialogs
	def __MakeUICurtain(self):
		wndUICurtain = ui.Bar("TOP_MOST")
		wndUICurtain.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		wndUICurtain.SetColor(0x77000000)
		wndUICurtain.Hide()
		self.wndUICurtain = wndUICurtain

	def __MakeMessengerWindow(self):
		self.wndMessenger = uiMessenger.MessengerWindow()

		from _weakref import proxy
		self.wndMessenger.SetWhisperButtonEvent(lambda n,i=proxy(self):i.OpenWhisperDialog(n))
		self.wndMessenger.SetGuildButtonEvent(ui.__mem_func__(self.ToggleGuildWindow))

	def __MakeGuildWindow(self):
		self.wndGuild = uiGuild.GuildWindow()

	def __MakeChatWindow(self):
		wndChat = uiChat.ChatWindow()
		wndChat.SetSize(wndChat.CHAT_WINDOW_WIDTH, 0)
		wndChat.SetPosition(wndMgr.GetScreenWidth()/2 - wndChat.CHAT_WINDOW_WIDTH/2, wndMgr.GetScreenHeight() - wndChat.EDIT_LINE_HEIGHT - 37)
		wndChat.SetHeight(200)
		wndChat.Refresh()
		wndChat.Show()

		self.wndChat = wndChat
		self.wndChat.BindInterface(self)
		self.wndChat.SetSendWhisperEvent(ui.__mem_func__(self.OpenWhisperDialogWithoutTarget))
		self.wndChat.SetOpenChatLogEvent(ui.__mem_func__(self.ToggleChatLogWindow))

	def __MakeTaskBar(self):
		wndTaskBar = uiTaskBar.TaskBar()
		wndTaskBar.BindInterfaceClass(self)
		wndTaskBar.LoadWindow()
		self.wndTaskBar = wndTaskBar
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHARACTER, ui.__mem_func__(self.ToggleCharacterWindowStatusPage))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_INVENTORY, ui.__mem_func__(self.ToggleInventoryWindow))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_MESSENGER, ui.__mem_func__(self.ToggleMessenger))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_SYSTEM, ui.__mem_func__(self.ToggleSystemDialog))
		if uiTaskBar.TaskBar.IS_EXPANDED:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_EXPAND, ui.__mem_func__(self.ToggleExpandedButton))
			self.wndExpandedTaskBar = uiTaskBar.ExpandedTaskBar()
			self.wndExpandedTaskBar.LoadWindow()
			# Interface class'ýný baðla
			self.wndExpandedTaskBar.BindInterfaceClass(self)

			if app.ENABLE_GROWTH_PET_SYSTEM:
				self.PetInformationActivate()
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_PET_INFO, ui.__mem_func__(self.TogglePetInformationWindow))
			if app.ENABLE_HUNTING_SYSTEM:
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_HUNTING, ui.__mem_func__(self.ToggleHuntingWindow))
			if app.__AUTO_HUNT__:
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_AUTO_WINDOW, ui.__mem_func__(self.ToggleAutoHuntWindow))
			if app.ENABLE_AUTO_SELL_SYSTEM:
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_AUTO_SELL, ui.__mem_func__(self.ToggleAutoSellWindow))

			# Sidebar buton event'lerini ExpandedTaskBar'daki metodlara ata
			if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
				self.wndExpandedTaskBar.SetSidebarButtonEvent(uiTaskBar.ExpandedTaskBar.SIDEBAR_TELEPORT, ui.__mem_func__(self.wndExpandedTaskBar.OnClickSidebarTeleport))

			if app.ENABLE_SPECIAL_INVENTORY:
				self.wndExpandedTaskBar.SetSidebarButtonEvent(uiTaskBar.ExpandedTaskBar.SIDEBAR_SPECIAL_DEP, ui.__mem_func__(self.wndExpandedTaskBar.OnClickSidebarSpecialDep))

			if app.ENABLE_RENEWAL_OFFLINESHOP:
				self.wndExpandedTaskBar.SetSidebarButtonEvent(uiTaskBar.ExpandedTaskBar.SIDEBAR_OFFLINE_SHOP, ui.__mem_func__(self.wndExpandedTaskBar.OnClickSidebarOfflineShop))

			if app.ENABLE_RENEWAL_SWITCHBOT:
				self.wndExpandedTaskBar.SetSidebarButtonEvent(uiTaskBar.ExpandedTaskBar.SIDEBAR_SWITCHBOT, ui.__mem_func__(self.wndExpandedTaskBar.OnClickSidebarSwitchbot))

			self.wndExpandedTaskBar.SetSidebarButtonEvent(uiTaskBar.ExpandedTaskBar.SIDEBAR_POTIONS, ui.__mem_func__(self.wndExpandedTaskBar.OnClickSidebarPotions))

			if app.ENABLE_INGAME_WIKI_SYSTEM:
				self.wndExpandedTaskBar.SetSidebarButtonEvent(uiTaskBar.ExpandedTaskBar.SIDEBAR_WIKIPEDIA, ui.__mem_func__(self.wndExpandedTaskBar.OnClickSidebarWikipedia))
		else:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHAT, ui.__mem_func__(self.ToggleChat))

		self.wndExpandedMoneyTaskBar = uiTaskBar.ExpandedMoneyTaskBar()
		self.wndExpandedMoneyTaskBar.LoadWindow()

		if self.wndInventory:
			self.wndInventory.SetExpandedMoneyBar(self.wndExpandedMoneyTaskBar)

	def __MakeParty(self):
		wndParty = uiParty.PartyWindow()
		wndParty.Hide()
		self.wndParty = wndParty

	def __MakeGameButtonWindow(self):
		wndGameButton = uiGameButton.GameButtonWindow()
		wndGameButton.SetTop()
		wndGameButton.Show()
		wndGameButton.SetButtonEvent("STATUS", ui.__mem_func__(self.__OnClickStatusPlusButton))
		wndGameButton.SetButtonEvent("SKILL", ui.__mem_func__(self.__OnClickSkillPlusButton))
		wndGameButton.SetButtonEvent("QUEST", ui.__mem_func__(self.__OnClickQuestButton))
		wndGameButton.SetButtonEvent("BUILD", ui.__mem_func__(self.__OnClickBuildButton))

		self.wndGameButton = wndGameButton

	def __IsChatOpen(self):
		return TRUE

	def __MakeWindows(self):
		wndCharacter = uiCharacter.CharacterWindow()

		wndInventory = uiInventory.InventoryWindow()
		wndInventory.BindInterfaceClass(self)

		# Sidebar butonlarý artýk ExpandedTaskBar'da, bu çaðrýlar kaldýrýldý

		wndMiniMap = uiMiniMap.MiniMap()
		wndMiniMap.BindInterfaceClass(self)

		if not app.ENABLE_SPECIAL_INVENTORY:
			wndSafebox = uiSafebox.SafeboxWindow()
			if app.ENABLE_SLOT_MARKING_SYSTEM:
				wndSafebox.BindInterface(self)

			wndMall = uiSafebox.MallWindow()
			self.wndMall = wndMall

		wndChatLog = uiChat.ChatLogWindow()
		wndChatLog.BindInterface(self)


		if app.ENABLE_GUILDBANK_LOG:
			self.wndGuildBank = uiGuildBank.GuildBankLogDialog()

		self.wndCharacter = wndCharacter
		self.wndInventory = wndInventory
		self.wndMiniMap = wndMiniMap

		if not app.ENABLE_SPECIAL_INVENTORY:
			self.wndSafebox = wndSafebox

		self.wndChatLog = wndChatLog

		if app.ENABLE_RIDING_EXTENDED:
			self.wndMountUpGrade = uiMountUpGrade.MountUpGradeWindow()

		if app.ENABLE_GUILD_RANK_SYSTEM:
			self.wndGuildRanking = uiGuildRanking.GuildRankingDialog()

		if app.ENABLE_RENEWAL_SWITCHBOT:
			self.wndSwitchbot = uiSwitchbot.SwitchbotWindow()

		if app.ENABLE_BIOLOG_SYSTEM:
			self.wndBiologManager["PANEL"] = uiBiologManager.BiologManager()
			self.wndBiologManager["ALERT"] = uiBiologManager.BiologManager_Alert()

		if app.ENABLE_VIEW_CHEST_DROP:
			self.dlgChestDrop = uiChestDrop.ChestDropWindow()

		if app.ENABLE_SPECIAL_INVENTORY:
			self.wndSpecialInventory = uiSpecialInventory.SpecialInventoryWindow()
			self.wndSpecialInventory.BindInterfaceClass(self)
			self.wndSafebox = uiSafebox.SafeboxWindow(self.wndSpecialInventory)
			self.wndMall = uiSafebox.MallWindow(self.wndSpecialInventory)
			self.wndSpecialInventory.BindSafeboxAndMallClass(self.wndSafebox, self.wndMall)

		if app.ENABLE_EVENT_MANAGER:
			self.wndEventOverview = uiEvent.EventOverview()
			self.wndEventOverview.BindInterface(self)

		if app.ENABLE_AURA_COSTUME_SYSTEM:
			wndAura = uiAura.AuraWindow()
			self.wndAura = wndAura

		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.wndPetInfoWindow = uiPetInfo.PetInformationWindow()
			self.wndPetInfoWindow.BindInterfaceClass(self)
			self.wndInventory.SetPetHatchingWindow(self.wndPetInfoWindow.GetPetHatchingWindow())
			self.wndInventory.SetPetFeedWindow(self.wndPetInfoWindow.GetPetFeedWindow())
			self.wndInventory.SetPetNameChangeWindow(self.wndPetInfoWindow.GetPetNameChangeWindow())

		if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
			self.wndWarpWindow = uiTeleport.TeleportWindow()

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			self.wndChangeLook = uiChangeLook.ChangeLookWindow()

	def __MakeDialogs(self):
		self.dlgExchange = uiExchange.ExchangeDialog()
		self.dlgExchange.LoadDialog()
		self.dlgExchange.SetCenterPosition()
		if app.ENABLE_SLOT_MARKING_SYSTEM:
			self.dlgExchange.BindInterface(self)
		self.dlgExchange.Hide()

		self.dlgPointReset = uiPointReset.PointResetDialog()
		self.dlgPointReset.LoadDialog()
		self.dlgPointReset.Hide()

		self.dlgShop = uiShop.ShopDialog()
		self.dlgShop.LoadDialog()
		if app.ENABLE_SLOT_MARKING_SYSTEM:
			self.dlgShop.BindInterface(self)
		self.dlgShop.Hide()

		self.dlgRestart = uiRestart.RestartDialog()
		self.dlgRestart.LoadDialog()
		self.dlgRestart.Hide()

		self.dlgSystem = uiSystem.SystemDialog()
		self.dlgSystem.BindInterfaceClass(self)
		self.dlgSystem.LoadDialog()
		self.dlgSystem.Hide()

		self.dlgPassword = uiSafebox.PasswordDialog()
		self.dlgPassword.Hide()

		self.hyperlinkItemTooltip = uiToolTip.HyperlinkItemToolTip()
		self.hyperlinkItemTooltip.Hide()

		self.tooltipItem = uiToolTip.ItemToolTip()
		if app.ENABLE_SLOT_MARKING_SYSTEM:
			self.tooltipItem.BindInterface(self)
		self.tooltipItem.Hide()

		self.tooltipSkill = uiToolTip.SkillToolTip()
		self.tooltipSkill.Hide()

		self.privateShopBuilder = uiPrivateShopBuilder.PrivateShopBuilder()
		if app.ENABLE_SLOT_MARKING_SYSTEM:
			self.privateShopBuilder.BindInterface(self)
		self.privateShopBuilder.Hide()

		self.dlgRefineNew = uiRefine.RefineDialogNew()
		if app.ENABLE_SLOT_MARKING_SYSTEM:
			self.dlgRefineNew.SetInven(self.wndInventory)
		self.dlgRefineNew.Hide()

		if app.ENABLE_RENEWAL_BATTLE_PASS:
			self.wndBattlePassExtended = uiBattlePass.BattlePassWindow()

		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.tooltipPetSkill = uiToolTip.PetSkillToolTip()
			self.tooltipPetSkill.Hide()

		if app.ENABLE_RENEWAL_SPECIAL_CHAT:
			self.wndSpecialChat = uiSpecialChat.SpecialChat()
			self.wndSpecialChat.Hide()

		if app.ENABLE_HUNTING_SYSTEM:
			self.wndHunting = uiHunting.HuntingWindow()
			self.wndHuntingSelect = uiHunting.HuntingSelectWindow()
			self.wndHuntingReward = uiHunting.HuntingRewardWindow()

	def __MakeTipBoard(self):
		self.tipBoard = uiTip.TipBoardNew()
		self.tipBoard.Hide()

		self.bigBoard = uiTip.BigBoard()
		self.bigBoard.Hide()

		if app.ENABLE_RENEWAL_OX_EVENT:
			self.bigBoardControl = uiTip.BigBoardControl()
			self.bigBoardControl.Hide()

	def __MakeWebWindow(self):
		if constInfo.IN_GAME_SHOP_ENABLE:
			import uiWeb
			self.wndWeb = uiWeb.WebWindow()
			self.wndWeb.LoadWindow()
			self.wndWeb.Hide()

	def __MakeCubeWindow(self):
		self.wndCube = uiCube.CubeWindow()
		self.wndCube.LoadWindow()
		self.wndCube.Hide()

	def __MakeCubeResultWindow(self):
		self.wndCubeResult = uiCube.CubeResultWindow()
		self.wndCubeResult.LoadWindow()
		self.wndCubeResult.Hide()

	def __MakeItemSelectWindow(self):
		self.wndItemSelect = uiselectitem.SelectItemWindow()
		self.wndItemSelect.Hide()

	if app.ENABLE_RENEWAL_CUBE:
		def __MakeCubeRenewal(self):
			import uicuberenewal
			self.wndCubeRenewal = uicuberenewal.CubeRenewalWindows()
			self.wndCubeRenewal.Hide()

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def __MakeAcceWindow(self):
			self.wndAcceCombine = uiAcce.CombineWindow()
			self.wndAcceCombine.LoadWindow()
			if app.ENABLE_SLOT_MARKING_SYSTEM:
				self.wndAcceCombine.BindInterface(self)
				if self.wndInventory:
					self.wndAcceCombine.SetInven(self.wndInventory)
			self.wndAcceCombine.Hide()

			self.wndAcceAbsorption = uiAcce.AbsorbWindow()
			self.wndAcceAbsorption.LoadWindow()
			if app.ENABLE_SLOT_MARKING_SYSTEM:
				self.wndAcceAbsorption.BindInterface(self)
				if self.wndInventory:
					self.wndAcceAbsorption.SetInven(self.wndInventory)
			self.wndAcceAbsorption.Hide()

			if self.wndInventory:
				self.wndInventory.SetAcceWindow(self.wndAcceCombine, self.wndAcceAbsorption)

	if app.ENABLE_MINIGAME_OKEY_CARDS_SYSTEM:
		def __MakeCardsInfoWindow(self):
			self.wndCardsInfo = uiCards.CardsInfoWindow()
			self.wndCardsInfo.LoadWindow()
			self.wndCardsInfo.Hide()

		def __MakeCardsWindow(self):
			self.wndCards = uiCards.CardsWindow()
			self.wndCards.LoadWindow()
			self.wndCards.Hide()

		def __MakeCardsIconWindow(self):
			self.wndCardsIcon = uiCards.IngameWindow()
			self.wndCardsIcon.LoadWindow()
			self.wndCardsIcon.Hide()

	if app.ENABLE_RENEWAL_SKILL_SELECT:
		def __MakeSkillSelectWindow(self):
			self.wndSkillSelect = uiSkillSelect.SkillSelectWindow()
			self.wndSkillSelect.LoadWindow()
			self.wndSkillSelect.Hide()

	def MakeInterface(self):
		self.__MakeMessengerWindow()
		self.__MakeGuildWindow()
		self.__MakeChatWindow()
		self.__MakeParty()
		self.__MakeWindows()
		self.__MakeDialogs()

		self.__MakeUICurtain()
		self.__MakeTaskBar()
		self.__MakeGameButtonWindow()
		self.__MakeTipBoard()
		self.__MakeWebWindow()
		self.__MakeCubeWindow()
		self.__MakeCubeResultWindow()
		self.__MakeItemSelectWindow()

		if app.ENABLE_RENEWAL_CUBE:
			self.__MakeCubeRenewal()

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.__MakeAcceWindow()

		if app.ENABLE_MINIGAME_OKEY_CARDS_SYSTEM:
			self.__MakeCardsInfoWindow()
			self.__MakeCardsWindow()
			self.__MakeCardsIconWindow()

		if app.ENABLE_RENEWAL_SKILL_SELECT:
			self.__MakeSkillSelectWindow()

		if app.ENABLE_AUTO_SELL_SYSTEM:
			self.__MakeAutoSellWindow()

		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}

		self.wndInventory.SetItemToolTip(self.tooltipItem)
		self.wndSafebox.SetItemToolTip(self.tooltipItem)
		self.wndCube.SetItemToolTip(self.tooltipItem)
		self.wndCubeResult.SetItemToolTip(self.tooltipItem)


		if app.ENABLE_GUILDBANK_LOG:
			self.wndGuildBank.SetItemToolTip(self.tooltipItem)

		# ITEM_MALL
		self.wndMall.SetItemToolTip(self.tooltipItem)
		# END_OF_ITEM_MALL
		self.wndCharacter.SetSkillToolTip(self.tooltipSkill)
		self.wndTaskBar.SetItemToolTip(self.tooltipItem)
		self.wndTaskBar.SetSkillToolTip(self.tooltipSkill)
		self.wndGuild.SetSkillToolTip(self.tooltipSkill)
		self.wndItemSelect.SetItemToolTip(self.tooltipItem)
		self.dlgShop.SetItemToolTip(self.tooltipItem)
		self.dlgExchange.SetItemToolTip(self.tooltipItem)
		self.privateShopBuilder.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_RENEWAL_SWITCHBOT:
			self.wndSwitchbot.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.wndAcceCombine.SetItemToolTip(self.tooltipItem)
			self.wndAcceAbsorption.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_BIOLOG_SYSTEM:
			self.wndBiologManager["PANEL"].SetItemToolTip(self.tooltipItem)

		if app.ENABLE_VIEW_CHEST_DROP:
			self.dlgChestDrop.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_SPECIAL_INVENTORY:
			self.wndSpecialInventory.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_AURA_COSTUME_SYSTEM:
			self.wndAura.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_SLOT_MARKING_SYSTEM:
			self.privateShopBuilder.SetInven(self.wndInventory)
			self.dlgExchange.SetInven(self.wndInventory)
			if app.ENABLE_SPECIAL_INVENTORY:
				self.privateShopBuilder.SetSpecialInven(self.wndSpecialInventory)
				self.dlgExchange.SetSpecialInven(self.wndSpecialInventory)

		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.wndPetInfoWindow.SetItemToolTip(self.tooltipItem)
			self.wndPetInfoWindow.SetInven(self.wndInventory)
			self.wndPetInfoWindow.SetPetSkillToolTip(self.tooltipPetSkill)

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			self.wndChangeLook.SetItemToolTip(self.tooltipItem)

		self.__InitWhisper()

	def AnswerOpenLink(self, answer):
		if not self.OpenLinkQuestionDialog:
			return

		self.OpenLinkQuestionDialog.Close()
		self.OpenLinkQuestionDialog = None

		if not answer:
			return

		link = constInfo.link
		os.system(link)

	if app.ENABLE_AUTO_SELL_SYSTEM:
		def __MakeAutoSellWindow(self):
			if not hasattr(self, "wndAutoSell") or self.wndAutoSell is None:
				self.wndAutoSell = uiautosell.AutoSellWindow()
				self.wndAutoSell.Hide()
	
		def ToggleAutoSellWindow(self):
			self.__MakeAutoSellWindow()
			if self.wndAutoSell.IsShow():
				self.wndAutoSell.Hide()
			else:
				self.wndAutoSell.Show()
				self.wndAutoSell.SetTop()
				net.SendChatPacket("/autosell_info 1")

	def MakeHyperlinkTooltip(self, hyperlink):
		tokens = hyperlink.split(":")
		if tokens and len(tokens):
			type = tokens[0]
			if "item" == type:
				self.hyperlinkItemTooltip.SetHyperlinkItem(tokens)
			elif "pm" == type and str(tokens[1]) != player.GetMainCharacterName():
				self.OpenWhisperDialog(str(tokens[1]))
			elif "web" == type and tokens[1].startswith("httpXxX") or "web" == type and tokens[1].startswith("httpsXxX"):
					OpenLinkQuestionDialog = uiCommon.QuestionDialog2()
					OpenLinkQuestionDialog.SetText1(localeInfo.CHAT_OPEN_LINK_DANGER)
					OpenLinkQuestionDialog.SetText2(localeInfo.CHAT_OPEN_LINK)
					OpenLinkQuestionDialog.SetAcceptEvent(lambda arg=TRUE: self.AnswerOpenLink(arg))
					OpenLinkQuestionDialog.SetCancelEvent(lambda arg=FALSE: self.AnswerOpenLink(arg))
					constInfo.link = "start " + tokens[1].replace("XxX", "://").replace("&","^&")
					OpenLinkQuestionDialog.Open()
					self.OpenLinkQuestionDialog = OpenLinkQuestionDialog
			elif "sysweb" == type:
				os.system("start " + tokens[1].replace("XxX", "://"))
			elif "petitem" == type and app.ENABLE_GROWTH_PET_SYSTEM:
				self.hyperlinkItemTooltip.SetHyperlinkPetItem(tokens)

	## Make Windows & Dialogs
	################################

	def Close(self):
		if self.dlgWhisperWithoutTarget:
			self.dlgWhisperWithoutTarget.Destroy()
			del self.dlgWhisperWithoutTarget

		if uiQuest.QuestDialog.__dict__.has_key("QuestCurtain"):
			uiQuest.QuestDialog.QuestCurtain.Close()

		if self.wndQuestWindow:
			for key, eachQuestWindow in self.wndQuestWindow.items():
				eachQuestWindow.nextCurtainMode = -1
				eachQuestWindow.CloseSelf()
				eachQuestWindow = None
		self.wndQuestWindow = {}

		if self.wndChat:
			self.wndChat.Destroy()

		if self.wndTaskBar:
			self.wndTaskBar.Destroy()

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Destroy()

		if self.wndExpandedMoneyTaskBar:
			self.wndExpandedMoneyTaskBar.Destroy()

		if self.wndCharacter:
			self.wndCharacter.Destroy()

		if self.wndInventory:
			self.wndInventory.Hide()
			self.wndInventory.Destroy()

		if self.dlgExchange:
			self.dlgExchange.Destroy()

		if self.dlgPointReset:
			self.dlgPointReset.Destroy()

		if self.dlgShop:
			self.dlgShop.Destroy()

		if self.dlgRestart:
			self.dlgRestart.Destroy()

		if self.dlgSystem:
			self.dlgSystem.Destroy()

		if self.dlgPassword:
			self.dlgPassword.Destroy()

		if self.wndMiniMap:
			self.wndMiniMap.Destroy()

		if self.wndSafebox:
			self.wndSafebox.Destroy()

		if self.wndWeb:
			self.wndWeb.Destroy()
			self.wndWeb = None

		if self.wndMall:
			self.wndMall.Destroy()

		if self.wndParty:
			self.wndParty.Destroy()

		if self.wndCube:
			self.wndCube.Destroy()

		if self.wndCubeResult:
			self.wndCubeResult.Destroy()

		if self.wndMessenger:
			self.wndMessenger.Destroy()

		if self.wndGuild:
			self.wndGuild.Destroy()

		if self.privateShopBuilder:
			self.privateShopBuilder.Destroy()

		if self.dlgRefineNew:
			self.dlgRefineNew.Destroy()

		if self.wndGuildBuilding:
			self.wndGuildBuilding.Destroy()

		if self.wndGameButton:
			self.wndGameButton.Destroy()

		if app.ENABLE_HUNTING_SYSTEM:
			if self.wndHunting:
				self.wndHunting.Destroy()
				del self.wndHunting
			if self.wndHuntingSelect:
				self.wndHuntingSelect.Destroy()
				del self.wndHuntingSelect
			if self.wndHuntingReward:
				self.wndHuntingReward.Destroy()
				del self.wndHuntingReward

		if app.__AUTO_HUNT__:
			if self.wndAutoHunt:
				self.wndAutoHunt.Close()
				self.wndAutoHunt.Destroy()
				self.wndAutoHunt = None

		# ITEM_MALL
		if self.mallPageDlg:
			self.mallPageDlg.Destroy()
		# END_OF_ITEM_MALL

		# ACCESSORY_REFINE_ADD_METIN_STONE
		if self.wndItemSelect:
			self.wndItemSelect.Destroy()
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

		if app.ENABLE_GUILD_RANK_SYSTEM:
			if self.wndGuildRanking:
				self.wndGuildRanking.Destory()

		if app.ENABLE_RENEWAL_SWITCHBOT:
			if self.wndSwitchbot:
				self.wndSwitchbot.Hide()
				self.wndSwitchbot.Destroy()

		if app.ENABLE_RENEWAL_CUBE:
			if self.wndCubeRenewal:
				self.wndCubeRenewal.Destroy()
				self.wndCubeRenewal.Close()

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if self.wndAcceCombine:
				self.wndAcceCombine.Destroy()

			if self.wndAcceAbsorption:
				self.wndAcceAbsorption.Destroy()

		if app.ENABLE_BIOLOG_SYSTEM:
			if self.wndBiologManager:
				for wnd in self.wndBiologManager.values():
					wnd.Destroy()

		if app.ENABLE_GUILDBANK_LOG:
			if self.wndGuildBank:
				self.wndGuildBank.Destroy()
				self.wndGuildBank.Close()

		if app.ENABLE_VIEW_CHEST_DROP:
			if self.dlgChestDrop:
				self.dlgChestDrop.Destroy()

		if app.ENABLE_SPECIAL_INVENTORY:
			if self.wndSpecialInventory:
				self.wndSpecialInventory.Hide()
				self.wndSpecialInventory.Destroy()

		if app.ENABLE_EVENT_MANAGER:
			if self.wndEventOverview:
				self.wndEventOverview.Hide()
				self.wndEventOverview.Destroy()

		if app.ENABLE_MINIGAME_OKEY_CARDS_SYSTEM:
			if self.wndCardsInfo:
				self.wndCardsInfo.Destroy()

			if self.wndCards:
				self.wndCards.Destroy()

			if self.wndCardsIcon:
				self.wndCardsIcon.Destroy()

		if app.ENABLE_RENEWAL_BATTLE_PASS:
			if self.wndBattlePassExtended:
				self.wndBattlePassExtended.Destroy()

		if app.ENABLE_RENDER_TARGET:
			if self.wndRenderTarget:
				self.wndRenderTarget.Close()
				self.wndRenderTarget.Destroy()
				self.wndRenderTarget = None

		if app.ENABLE_RENEWAL_OFFLINESHOP:
			if self.dlgOfflineShop:
				self.dlgOfflineShop.Hide()
				self.dlgOfflineShop.Destroy()
				del self.dlgOfflineShop

			if self.dlgOfflineShopPanel:
				self.dlgOfflineShopPanel.Hide()
				self.dlgOfflineShopPanel.Destroy()
				del self.dlgOfflineShopPanel

			if self.offlineShopBuilder:
				self.offlineShopBuilder.Hide()
				self.offlineShopBuilder.Destroy()
				del self.offlineShopBuilder

			if self.dlgShopMessage:
				self.dlgShopMessage.Hide()
				self.dlgShopMessage.Destroy()
				self.dlgShopMessage = None

		if app.ENABLE_OFFLINESHOP_SEARCH_SYSTEM:
			if self.wndPrivateShopSearch:
				self.wndPrivateShopSearch.Hide()
				self.wndPrivateShopSearch.Destroy()
				del self.wndPrivateShopSearch
				self.wndPrivateShopSearch = 0

		if app.ENABLE_INGAME_WIKI_SYSTEM:
			if self.wndWiki:
				self.wndWiki.Close()
				self.wndWiki.Destroy()
				del self.wndWiki
				self.wndWiki = None

		if app.ENABLE_RENEWAL_SKILL_SELECT:
			if self.wndSkillSelect:
				self.wndSkillSelect.Destroy()

		if app.ENABLE_RENEWAL_INGAME_ITEMSHOP:
			if self.wndItemShop:
				self.wndItemShop.Hide()
				self.wndItemShop.Destroy()
				self.wndItemShop = None

		if app.ENABLE_AURA_COSTUME_SYSTEM:
			if self.wndAura:
				self.wndAura.Destroy()
			del self.wndAura

		if app.ENABLE_FISH_GAME:
			if self.wndFishGame:
				self.wndFishGame.Hide()
				self.wndFishGame.Destroy()
				self.wndFishGame = None

		if app.ENABLE_GROWTH_PET_SYSTEM:
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.Destroy()

		if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
			if self.wndWarpWindow:
				self.wndWarpWindow.Destroy()

		if app.ENABLE_DUNGEON_TRACKING_SYSTEM:
			if self.wndTrackWindow:
				self.wndTrackWindow.Close()
				self.wndTrackWindow.Destroy()
				self.wndTrackWindow = None

		if app.ENABLE_RENEWAL_SPECIAL_CHAT:
			if self.wndSpecialChat:
				self.wndSpecialChat.Destroy()

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			if self.wndChangeLook:
				del self.wndChangeLook

		if app.ENABLE_RIDING_EXTENDED:
			if self.wndMountUpGrade:
				self.wndMountUpGrade.Destroy()
				del self.wndMountUpGrade

		self.wndChatLog.Destroy()
		for btn in self.questButtonList:
			btn.SetEvent(0)
		for btn in self.whisperButtonList:
			btn.SetEvent(0)
		for dlg in self.whisperDialogDict.itervalues():
			dlg.Destroy()
		for brd in self.guildScoreBoardDict.itervalues():
			brd.Destroy()
		for dlg in self.equipmentDialogDict.itervalues():
			dlg.Destroy()

		# ITEM_MALL
		del self.mallPageDlg
		# END_OF_ITEM_MALL

		del self.wndGuild
		del self.wndMessenger
		del self.wndUICurtain
		del self.wndChat
		del self.wndTaskBar
		if self.wndExpandedTaskBar:
			del self.wndExpandedTaskBar

		if self.wndExpandedMoneyTaskBar:
			del self.wndExpandedMoneyTaskBar
		del self.wndCharacter
		del self.wndInventory
		del self.dlgExchange
		del self.dlgPointReset
		del self.dlgShop
		del self.dlgRestart
		del self.dlgSystem
		del self.dlgPassword
		del self.hyperlinkItemTooltip
		del self.tooltipItem
		del self.tooltipSkill
		del self.wndMiniMap
		del self.wndSafebox
		del self.wndMall
		del self.wndParty
		del self.wndCube
		del self.wndCubeResult
		del self.privateShopBuilder
		del self.inputDialog
		del self.wndChatLog
		del self.dlgRefineNew
		del self.wndGuildBuilding
		del self.wndGameButton
		del self.tipBoard
		del self.bigBoard
		del self.wndItemSelect

		if app.ENABLE_GUILD_RANK_SYSTEM:
			del self.wndGuildRanking

		if app.ENABLE_RENEWAL_SWITCHBOT:
			del self.wndSwitchbot

		if app.ENABLE_RENEWAL_CUBE:
			del self.wndCubeRenewal

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			del self.wndAcceCombine
			del self.wndAcceAbsorption

		if app.ENABLE_BIOLOG_SYSTEM:
			for wnd in self.wndBiologManager.values():
				del wnd

		if app.ENABLE_VIEW_CHEST_DROP:
			if self.dlgChestDrop:
				del self.dlgChestDrop

		if app.ENABLE_SPECIAL_INVENTORY:
			if self.wndSpecialInventory:
				del self.wndSpecialInventory

		if app.ENABLE_EVENT_MANAGER:
			del self.wndEventOverview


		if app.ENABLE_GUILDBANK_LOG:
			del self.wndGuildBank

		if app.ENABLE_MINIGAME_OKEY_CARDS_SYSTEM:
			del self.wndCardsInfo
			del self.wndCards
			del self.wndCardsIcon

		if app.ENABLE_RENEWAL_BATTLE_PASS:
			del self.wndBattlePassExtended

		if app.ENABLE_RENEWAL_OX_EVENT:
			del self.bigBoardControl

		if app.ENABLE_RENEWAL_SKILL_SELECT:
			del self.wndSkillSelect

		if app.ENABLE_NEW_DUNGEON_LIB:
			if self.wndDungeonTimer:
				self.wndDungeonTimer.Hide()
				self.wndDungeonTimer = 0

		if app.ENABLE_GROWTH_PET_SYSTEM:
			if self.wndPetInfoWindow:
				del self.wndPetInfoWindow
			self.wndPetInfoWindow = None
			del self.tooltipPetSkill

		if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
			del self.wndWarpWindow

		if app.ENABLE_RENEWAL_SPECIAL_CHAT:
			del self.wndSpecialChat

		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}

		uiChat.DestroyChatInputSetWindow()

	## Skill
	def OnUseSkill(self, slotIndex, coolTime):
		self.wndCharacter.OnUseSkill(slotIndex, coolTime)
		self.wndTaskBar.OnUseSkill(slotIndex, coolTime)
		self.wndGuild.OnUseSkill(slotIndex, coolTime)

	def OnActivateSkill(self, slotIndex):
		self.wndCharacter.OnActivateSkill(slotIndex)
		self.wndTaskBar.OnActivateSkill(slotIndex)

	def OnDeactivateSkill(self, slotIndex):
		self.wndCharacter.OnDeactivateSkill(slotIndex)
		self.wndTaskBar.OnDeactivateSkill(slotIndex)

	def OnChangeCurrentSkill(self, skillSlotNumber):
		self.wndTaskBar.OnChangeCurrentSkill(skillSlotNumber)

	def SkillClearCoolTime(self, slotIndex):
		self.wndCharacter.SkillClearCoolTime(slotIndex)
		self.wndTaskBar.SkillClearCoolTime(slotIndex)

	def SelectMouseButtonEvent(self, dir, event):
		self.wndTaskBar.SelectMouseButtonEvent(dir, event)

	## Refresh
	def RefreshAlignment(self):
		self.wndCharacter.RefreshAlignment()

	def RefreshStatus(self):
		self.wndTaskBar.RefreshStatus()
		self.wndCharacter.RefreshStatus()
		self.wndInventory.RefreshStatus()

		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.wndPetInfoWindow.RefreshStatus()

	def RefreshStamina(self):
		self.wndTaskBar.RefreshStamina()

	def RefreshSkill(self):
		self.wndCharacter.RefreshSkill()
		self.wndTaskBar.RefreshSkill()

	def RefreshInventory(self):
		self.wndTaskBar.RefreshQuickSlot()
		self.wndInventory.RefreshItemSlot()

		if app.ENABLE_SPECIAL_INVENTORY:
			self.wndSpecialInventory.RefreshItemSlot()

		if app.ENABLE_AURA_COSTUME_SYSTEM:
			if player.IsAuraRefineWindowOpen():
				if self.wndAura and self.wndAura.IsShow():
					self.wndAura.RefreshAuraWindow()

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			if player.GetChangeLookWindowOpen() == 1:
				self.wndChangeLook.RefreshChangeLookWindow()

	def RefreshCharacter(self):
		self.wndCharacter.RefreshCharacter()
		self.wndTaskBar.RefreshQuickSlot()

	def RefreshQuest(self):
		self.wndCharacter.RefreshQuest()

	def RefreshSafebox(self):
		self.wndSafebox.RefreshSafebox()

	if app.ENABLE_GUILD_RANK_SYSTEM:
		def OpenGuildRanking(self):
			self.wndGuildRanking.Open()

	# ITEM_MALL
	def RefreshMall(self):
		self.wndMall.RefreshMall()

	def OpenItemMall(self):
		if not self.mallPageDlg:
			self.mallPageDlg = uiShop.MallPageDialog()

		self.mallPageDlg.Open()
	# END_OF_ITEM_MALL

	def RefreshMessenger(self):
		self.wndMessenger.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.wndGuild.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.wndGuild.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.wndGuild.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.wndGuild.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.wndGuild.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.wndGuild.RefreshGuildGradePage()

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		## guild_renewal
		def RefreshGuildBaseInfoPage(self):
			self.wndGuild.RefreshGuildBaseInfoPage()

		## GuildBaseInfoBankGold
		def RefreshGuildBaseInfoPageBankGold(self):
			self.wndGuild.RefreshGuildBaseInfoPageBankGold()

		## guild_renewal_war
		def RefreshGuildWarInfoPage(self):
			self.wndGuild.RefreshGuildWarInfoPage()

	def DeleteGuild(self):
		self.wndMessenger.ClearGuildMember()
		self.wndGuild.DeleteGuild()

	def OnBlockMode(self, mode):
		self.dlgSystem.OnBlockMode(mode)

	## Calling Functions
	# PointReset
	def OpenPointResetDialog(self):
		self.dlgPointReset.Show()
		self.dlgPointReset.SetTop()

	def ClosePointResetDialog(self):
		self.dlgPointReset.Close()

	# Shop
	def OpenShopDialog(self, vid):
		self.wndInventory.Show()
		self.wndInventory.SetTop()
		self.dlgShop.Open(vid)
		self.dlgShop.SetTop()

	def CloseShopDialog(self):
		self.dlgShop.Close()

	def RefreshShopDialog(self):
		self.dlgShop.Refresh()

	if app.ENABLE_VIEW_CHEST_DROP:
		def AddChestDropInfo(self, chestVnum, pageIndex, slotIndex, itemVnum, itemCount):
			self.dlgChestDrop.AddChestDropItem(int(chestVnum), int(pageIndex), int(slotIndex), int(itemVnum), int(itemCount))

		def RefreshChestDropInfo(self, chestVnum):
			self.dlgChestDrop.RefreshItems(chestVnum)

	## Quest
	def OpenCharacterWindowQuestPage(self):
		self.wndCharacter.Show()
		self.wndCharacter.SetState("QUEST")

	def OpenQuestWindow(self, skin, idx):

		wnds = ()

		q = uiQuest.QuestDialog(skin, idx)
		q.SetWindowName("QuestWindow" + str(idx))
		q.Show()
		if skin:
			q.Lock()
			wnds = self.__HideWindows()

			# UNKNOWN_UPDATE
			q.AddOnDoneEvent(lambda tmp_self, args=wnds: self.__ShowWindows(args))
			# END_OF_UNKNOWN_UPDATE

		if skin:
			q.AddOnCloseEvent(q.Unlock)
		q.AddOnCloseEvent(lambda key = self.wndQuestWindowNewKey:ui.__mem_func__(self.RemoveQuestDialog)(key))
		self.wndQuestWindow[self.wndQuestWindowNewKey] = q

		self.wndQuestWindowNewKey = self.wndQuestWindowNewKey + 1

		# END_OF_UNKNOWN_UPDATE
		
	def RemoveQuestDialog(self, key):
		del self.wndQuestWindow[key]

	## Exchange
	def StartExchange(self):
		self.dlgExchange.OpenDialog()
		self.dlgExchange.Refresh()

	def EndExchange(self):
		self.dlgExchange.CloseDialog()

	def RefreshExchange(self):
		self.dlgExchange.Refresh()

	if app.ENABLE_SLOT_MARKING_SYSTEM:
		def AddExchangeItemSlotIndex(self, idx):
			self.dlgExchange.AddExchangeItemSlotIndex(idx)

	## Party
	def AddPartyMember(self, pid, name):
		self.wndParty.AddPartyMember(pid, name)

		self.__ArrangeQuestButton()

	def UpdatePartyMemberInfo(self, pid):
		self.wndParty.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.wndParty.RemovePartyMember(pid)
		self.__ArrangeQuestButton()

	def LinkPartyMember(self, pid, vid):
		self.wndParty.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.wndParty.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.wndParty.UnlinkAllPartyMember()

	def ExitParty(self):
		self.wndParty.ExitParty()
		self.__ArrangeQuestButton()

	def PartyHealReady(self):
		self.wndParty.PartyHealReady()

	def ChangePartyParameter(self, distributionMode):
		self.wndParty.ChangePartyParameter(distributionMode)

	## Safebox
	def AskSafeboxPassword(self):
		if self.wndSafebox.IsShow():
			return

		# SAFEBOX_PASSWORD
		self.dlgPassword.SetTitle(localeInfo.PASSWORD_TITLE)
		self.dlgPassword.SetSendMessage("/safebox_password ")
		# END_OF_SAFEBOX_PASSWORD

		self.dlgPassword.ShowDialog()

	def OpenSafeboxWindow(self, size):
		if app.ENABLE_SPECIAL_INVENTORY:
			self.wndSpecialInventory.ShowSafeboxWindow(size)

		self.dlgPassword.CloseDialog()
		self.wndSafebox.ShowWindow(size)

	def RefreshSafeboxMoney(self):
		self.wndSafebox.RefreshSafeboxMoney()

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def OpenGuildScoreWindow(self):
			import chat
			chat.AppendChat(chat.CHAT_TYPE_INFO, "OpenGuildScoreWindow")
			self.wndGuild.OpenGuildScoreWindow()

	def CommandCloseSafebox(self):
		if app.ENABLE_SPECIAL_INVENTORY:
			self.wndSpecialInventory.CommandCloseSafebox()

		self.wndSafebox.CommandCloseSafebox()

	# ITEM_MALL
	def AskMallPassword(self):
		if self.wndMall.IsShow():
			return
		self.dlgPassword.SetTitle(localeInfo.MALL_PASSWORD_TITLE)
		self.dlgPassword.SetSendMessage("/mall_password ")
		self.dlgPassword.ShowDialog()

	def OpenMallWindow(self, size):
		if app.ENABLE_SPECIAL_INVENTORY:
			self.wndSpecialInventory.ShowMallWindow(size)

		self.dlgPassword.CloseDialog()
		self.wndMall.ShowWindow(size)

	def CommandCloseMall(self):
		if app.ENABLE_SPECIAL_INVENTORY:
			self.wndSpecialInventory.CommandCloseMall()

		self.wndMall.CommandCloseMall()
	# END_OF_ITEM_MALL

	## Guild
	def OnStartGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnStartGuildWar(guildSelf, guildOpp)

		guildWarScoreBoard = uiGuild.GuildWarScoreBoard()
		guildWarScoreBoard.Open(guildSelf, guildOpp)
		guildWarScoreBoard.Show()
		if app.ENABLE_GUILDRENEWAL_SYSTEM:
			self.wndGuild.GuildWarOppGuildNameSetting(guildSelf, guildOpp)
		self.guildScoreBoardDict[uiGuild.GetGVGKey(guildSelf, guildOpp)] = guildWarScoreBoard

	def OnEndGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnEndGuildWar(guildSelf, guildOpp)

		key = uiGuild.GetGVGKey(guildSelf, guildOpp)

		if not self.guildScoreBoardDict.has_key(key):
			return

		self.guildScoreBoardDict[key].Destroy()
		del self.guildScoreBoardDict[key]

	# GUILDWAR_MEMBER_COUNT
	def UpdateMemberCount(self, gulidID1, memberCount1, guildID2, memberCount2):
		key = uiGuild.GetGVGKey(gulidID1, guildID2)

		if not self.guildScoreBoardDict.has_key(key):
			return

		self.guildScoreBoardDict[key].UpdateMemberCount(gulidID1, memberCount1, guildID2, memberCount2)
	# END_OF_GUILDWAR_MEMBER_COUNT

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def OnRecvGuildWarPoint(self, gainGuildID, opponentGuildID, point, winpoint):
			key = uiGuild.GetGVGKey(gainGuildID, opponentGuildID)
			if not self.guildScoreBoardDict.has_key(key):
				return

			guildBoard = self.guildScoreBoardDict[key]
			guildBoard.SetScore(gainGuildID, opponentGuildID, point)
			import chat
			chat.AppendChat(1, "OnRecvGuildWarPoint - winpoint %d" % (winpoint))
			self.wndGuild.GuildWarScoreSetting(gainGuildID, opponentGuildID, point, winpoint)
	else:
		def OnRecvGuildWarPoint(self, gainGuildID, opponentGuildID, point):
			key = uiGuild.GetGVGKey(gainGuildID, opponentGuildID)
			if not self.guildScoreBoardDict.has_key(key):
				return

			guildBoard = self.guildScoreBoardDict[key]
			guildBoard.SetScore(gainGuildID, opponentGuildID, point)

	## PK Mode
	def OnChangePKMode(self):
		self.wndCharacter.RefreshAlignment()
		self.dlgSystem.OnChangePKMode()

	## Refine
	def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type):
		self.dlgRefineNew.Open(targetItemPos, nextGradeItemVnum, cost, prob, type)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.dlgRefineNew.AppendMaterial(vnum, count)

	if app.ENABLE_AUTO_REFINE:
		def CheckRefineDialog(self, isFail):
			self.dlgRefineNew.CheckRefine(isFail)

	## Show & Hide
	def ShowDefaultWindows(self):
		self.wndTaskBar.Show()
		self.wndMiniMap.Show()
		self.wndMiniMap.ShowMiniMap()

	def ShowAllWindows(self):
		self.wndTaskBar.Show()
		self.wndCharacter.Show()
		self.wndInventory.Show()
		self.wndChat.Show()
		self.wndMiniMap.Show()

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Show()
			self.wndExpandedTaskBar.SetTop()

		if self.wndExpandedMoneyTaskBar:
			self.wndExpandedMoneyTaskBar.Show()
			self.wndExpandedMoneyTaskBar.SetTop()

	def HideAllWindows(self):
		if self.wndTaskBar:
			self.wndTaskBar.Hide()

		if app.ENABLE_RENEWAL_BONUS_BOARD:
			if self.wndCharacter:
				self.wndCharacter.Close()
		else:
			if self.wndCharacter:
				self.wndCharacter.Hide()

		if self.wndInventory:
			self.wndInventory.Hide()

		if self.wndChat:
			self.wndChat.Hide()

		if self.wndMiniMap:
			self.wndMiniMap.Hide()

		if self.wndMessenger:
			self.wndMessenger.Hide()

		if self.wndGuild:
			self.wndGuild.Hide()

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Hide()

		if self.wndExpandedMoneyTaskBar:
			self.wndExpandedMoneyTaskBar.Hide()

		if app.ENABLE_RIDING_EXTENDED:
			if self.wndMountUpGrade:
				self.wndMountUpGrade.Hide()

		if app.ENABLE_RENEWAL_SWITCHBOT:
			if self.wndSwitchbot:
				self.wndSwitchbot.Hide()

		if app.ENABLE_BIOLOG_SYSTEM:
			if self.wndBiologManager:
				for wnd in self.wndBiologManager.values():
					wnd.Hide()

		if app.ENABLE_SPECIAL_INVENTORY:
			if self.wndSpecialInventory:
				self.wndSpecialInventory.Hide()

		if app.ENABLE_RENEWAL_BATTLE_PASS:
			if self.wndBattlePassExtended:
				self.wndBattlePassExtended.Hide()

		if app.ENABLE_AURA_COSTUME_SYSTEM:
			if self.wndAura:
				self.wndAura.Hide()

		if app.ENABLE_GROWTH_PET_SYSTEM:
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.Hide()
				if self.wndPetInfoWindow.wndPetMiniInfo:
					self.wndPetInfoWindow.wndPetMiniInfo.Hide()

		if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
			if self.wndWarpWindow:
				self.wndWarpWindow.Hide()

		if app.ENABLE_RENEWAL_SPECIAL_CHAT:
			if self.wndSpecialChat:
				self.wndSpecialChat.Hide()

		if app.ENABLE_HUNTING_SYSTEM:
			if self.wndHunting:
				self.wndHunting.Hide()

			if self.wndHuntingSelect:
				self.wndHuntingSelect.Hide()

			if self.wndHuntingReward:
				self.wndHuntingReward.Hide()

	def ShowMouseImage(self):
		self.wndTaskBar.ShowMouseImage()

	def HideMouseImage(self):
		self.wndTaskBar.HideMouseImage()

	def ToggleChat(self):
		if TRUE == self.wndChat.IsEditMode():
			self.wndChat.CloseChat()
		else:
			if self.wndWeb and self.wndWeb.IsShow():
				pass
			else:
				self.wndChat.OpenChat()

	def IsOpenChat(self):
		return self.wndChat.IsEditMode()

	def SetChatFocus(self):
		self.wndChat.SetChatFocus()

	if app.ENABLE_RENEWAL_DEAD_PACKET:
		def OpenRestartDialog(self, d_time):
			self.dlgRestart.OpenDialog(d_time)
			self.dlgRestart.SetTop()
	else:
		def OpenRestartDialog(self):
			self.dlgRestart.OpenDialog()
			self.dlgRestart.SetTop()

	def CloseRestartDialog(self):
		self.dlgRestart.Close()

	def ToggleSystemDialog(self):
		if FALSE == self.dlgSystem.IsShow():
			self.dlgSystem.OpenDialog()
			self.dlgSystem.SetTop()
		else:
			self.dlgSystem.Close()

	def OpenSystemDialog(self):
		self.dlgSystem.OpenDialog()
		self.dlgSystem.SetTop()

	def ToggleMessenger(self):
		if self.wndMessenger.IsShow():
			self.wndMessenger.Hide()
		else:
			self.wndMessenger.SetTop()
			self.wndMessenger.Show()

	def ToggleMiniMap(self):
		if app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT):
			if FALSE == self.wndMiniMap.isShowMiniMap():
				self.wndMiniMap.ShowMiniMap()
				self.wndMiniMap.SetTop()
			else:
				self.wndMiniMap.HideMiniMap()

		else:
			self.wndMiniMap.ToggleAtlasWindow()

	def PressMKey(self):
		if app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT):
			self.ToggleMessenger()

		else:
			self.ToggleMiniMap()

	def SetMapName(self, mapName):
		self.wndMiniMap.SetMapName(mapName)

	def MiniMapScaleUp(self):
		self.wndMiniMap.ScaleUp()

	def MiniMapScaleDown(self):
		self.wndMiniMap.ScaleDown()

	def ToggleCharacterWindow(self, state):
		if FALSE == player.IsObserverMode():
			if FALSE == self.wndCharacter.IsShow():
				self.OpenCharacterWindowWithState(state)
			else:
				if state == self.wndCharacter.GetState():
					self.wndCharacter.OverOutItem()
					if app.ENABLE_RENEWAL_BONUS_BOARD:
						self.wndCharacter.Close()
					else:
						self.wndCharacter.Hide()
				else:
					self.wndCharacter.SetState(state)

	def OpenCharacterWindowWithState(self, state):
		if FALSE == player.IsObserverMode():
			self.wndCharacter.SetState(state)
			self.wndCharacter.Show()
			self.wndCharacter.SetTop()

	def ToggleCharacterWindowStatusPage(self):
		self.ToggleCharacterWindow("STATUS")

	def ToggleInventoryWindow(self):
		if FALSE == player.IsObserverMode():
			if FALSE == self.wndInventory.IsShow():
				self.wndInventory.Show()
				self.wndInventory.SetTop()
			else:
				self.wndInventory.OverOutItem()
				self.wndInventory.Close()

	def ToggleExpandedButton(self):
		if False == player.IsObserverMode():
			if False == self.wndExpandedTaskBar.IsShow():
				self.wndExpandedTaskBar.Show()
				self.wndExpandedTaskBar.SetTop()
			else:
				self.wndExpandedTaskBar.Close()

	def ToggleExpandedMoneyButton(self):
		if FALSE == self.wndExpandedMoneyTaskBar.IsShow():
			self.wndExpandedMoneyTaskBar.Show()
			self.wndExpandedMoneyTaskBar.SetTop()
		else:
			self.wndExpandedMoneyTaskBar.Close()

	if app.ENABLE_GROWTH_PET_SYSTEM:
		def PetInformationActivate(self):
			if uiTaskBar.TaskBar.IS_EXPANDED:
				self.wndExpandedTaskBar.SetToolTipText(uiTaskBar.ExpandedTaskBar.BUTTON_PET_INFO, uiScriptLocale.TASKBAR_PET_INFO)

		def TogglePetInformationWindow(self):
			if False == player.IsObserverMode():
				if not self.wndPetInfoWindow.IsShow():
					self.wndPetInfoWindow.Show()
				else:
					self.wndPetInfoWindow.Close()

	def ToggleGuildWindow(self):
		if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM and app.ENABLE_GUILD_REQUEST:
			if not self.wndGuild.CanOpen():
				if self.wndGuild.GuildListDialogIsShow():
					self.wndGuild.CloseGuildListDialog()
				else:
					self.wndGuild.OpenGuildListDialog()
				return

		if not self.wndGuild.IsShow():
			if self.wndGuild.CanOpen():
				self.wndGuild.Open()
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GUILD_YOU_DO_NOT_JOIN)
		else:
			self.wndGuild.OverOutItem()
			self.wndGuild.Hide()

	def ToggleChatLogWindow(self):
		if self.wndChatLog.IsShow():
			self.wndChatLog.Hide()
		else:
			self.wndChatLog.Show()

	if app.ENABLE_RENEWAL_SWITCHBOT:
		def ToggleSwitchbotWindow(self):
			if self.wndSwitchbot.IsShow():
				self.wndSwitchbot.Close()
			else:
				self.wndSwitchbot.Open()

		def RefreshSwitchbotWindow(self):
			if self.wndSwitchbot and self.wndSwitchbot.IsShow():
				self.wndSwitchbot.RefreshSwitchbotWindow()

		def RefreshSwitchbotItem(self, slot):
			if self.wndSwitchbot and self.wndSwitchbot.IsShow():
				self.wndSwitchbot.RefreshSwitchbotItem(slot)

	if app.ENABLE_BIOLOG_SYSTEM:
		def ToggleBiologManager(self):
			if self.wndBiologManager["PANEL"].IsShow():
				self.wndBiologManager["PANEL"].Close()
			else:
				self.wndBiologManager["PANEL"].Open()

		def BiologManagerUpdate(self):
			self.wndBiologManager["PANEL"].RecvUpdate()

		def BiologManager_Alert(self):
			self.wndBiologManager["ALERT"].RecvUpdate(5)

		def BiologManagerClose(self):
			if self.wndBiologManager["PANEL"].IsShow():
				self.wndBiologManager["PANEL"].Close()

	if app.ENABLE_SPECIAL_INVENTORY:
		def ToggleSpecialInventoryWindow(self):
			if FALSE == player.IsObserverMode():
				if FALSE == self.wndSpecialInventory.IsShow():
					self.wndSpecialInventory.Show()
					self.wndSpecialInventory.SetTop()
				else:
					self.wndSpecialInventory.OverOutItem()
					self.wndSpecialInventory.Close()

		def OpenSpecialInventoryWindow(self, category = 0):
			if FALSE == player.IsObserverMode():
				if FALSE == self.wndSpecialInventory.IsShow():
					self.wndSpecialInventory.Show()
					self.wndSpecialInventory.SetTop()
					self.wndSpecialInventory.SetInventoryType(category)

	if app.ENABLE_EVENT_MANAGER:
		def ToggleInGameEvent(self):
			if FALSE == player.IsObserverMode():
				if FALSE == self.wndEventOverview.IsShow():
					self.wndEventOverview.Open()
				else:
					self.wndEventOverview.Close()

		def OpenInGameEvent(self):
			if self.wndEventOverview:
				if not self.wndEventOverview.IsShow():
					self.wndEventOverview.Open()

		def CloseInGameEvent(self):
			if self.wndEventOverview:
				if self.wndEventOverview.IsShow():
					self.wndEventOverview.Close()

	if app.ENABLE_RENEWAL_BATTLE_PASS:
		def ReciveOpenExtBattlePass(self):
			if FALSE == self.isFirstOpeningExtBattlePass:
				self.isFirstOpeningExtBattlePass = TRUE
				self.wndBattlePassExtended.SetPage("NORMAL")
			if FALSE == self.wndBattlePassExtended.IsShow():
				self.ToggleBattlePassExtended()
			else:
				self.wndBattlePassExtended.SetPage(self.wndBattlePassExtended.GetPage())

		def ToggleBattlePassExtended(self):
			if FALSE == self.isFirstOpeningExtBattlePass:
				net.SendExtBattlePassAction(1)
			if FALSE == self.wndBattlePassExtended.IsShow():
				self.wndBattlePassExtended.Show()
				self.wndBattlePassExtended.SetTop()
			else:
				self.wndBattlePassExtended.Close()

		def AddExtendedBattleGeneralInfo(self, BattlePassType, BattlePassName, BattlePassID, battlePassStartTime, battlePassEndTime):
			if self.wndBattlePassExtended:
				self.wndBattlePassExtended.RecvGeneralInfo(BattlePassType, BattlePassName, BattlePassID, battlePassStartTime, battlePassEndTime)

		def AddExtendedBattlePassMission(self, battlepassType, battlepassID, missionIndex, missionType, missionInfo1, missionInfo2, missionInfo3):
			if self.wndBattlePassExtended:
				self.wndBattlePassExtended.AddMission(battlepassType, battlepassID, missionIndex, missionType, missionInfo1, missionInfo2, missionInfo3)

		def UpdateExtendedBattlePassMission(self, battlepassType, missionIndex, missionType, newProgress):
			if self.wndBattlePassExtended:
				self.wndBattlePassExtended.UpdateMission(battlepassType, missionIndex, missionType, newProgress)

		def AddExtendedBattlePassMissionReward(self, battlepassType, battlepassID, missionIndex, missionType, itemVnum, itemCount):
			if self.wndBattlePassExtended:
				self.wndBattlePassExtended.AddMissionReward(battlepassType, battlepassID, missionIndex, missionType, itemVnum, itemCount)

		def AddExtendedBattlePassReward(self, battlepassType, battlepassID, itemVnum, itemCount):
			if self.wndBattlePassExtended:
				self.wndBattlePassExtended.AddReward(battlepassType, battlepassID, itemVnum, itemCount)

		def AddExtBattlePassRanklistEntry(self, playername, battlepassType, battlepassID, startTime, endTime):
			if self.wndBattlePassExtended:
				self.wndBattlePassExtended.AddRankingEntry(playername, battlepassType, battlepassID, startTime, endTime)

	if app.ENABLE_RENEWAL_SPECIAL_CHAT:
		def OnPickItem(self, item):
			item_vnum = int(item)
			self.SpecialChatOnPick(0, item_vnum)

		def SpecialChatOnPick(self, money = 0, item_vnum = 0):
			if money > 0:
				money_str = localeInfo.NumberToMoneyString(money)
				self.wndSpecialChat.AddSpecialChatLine(localeInfo.SPECIAL_CHAT_PICK % (money_str))

			if item_vnum > 0:
				import item
				item.SelectItem(item_vnum)
				self.wndSpecialChat.AddSpecialChatLine(localeInfo.SPECIAL_CHAT_PICK % (item.GetItemName()))

	def Highligt_Item(self, inven_type, inven_pos):
		if app.ENABLE_PICKUP_ITEM_EFFECT and player.INVENTORY == inven_type:
			self.wndInventory.HighlightSlot(inven_pos)
			if app.ENABLE_SPECIAL_INVENTORY:
				self.wndSpecialInventory.HighlightSlot(inven_pos)

	def CheckGameButton(self):
		if self.wndGameButton:
			self.wndGameButton.CheckGameButton()

	def __OnClickStatusPlusButton(self):
		self.ToggleCharacterWindow("STATUS")

	def __OnClickSkillPlusButton(self):
		self.ToggleCharacterWindow("SKILL")

	def __OnClickQuestButton(self):
		self.ToggleCharacterWindow("QUEST")

	def __OnClickBuildButton(self):
		self.BUILD_OpenWindow()

	def OpenWebWindow(self, url):
		self.wndWeb.Open(url)
		self.wndChat.CloseChat()

	def ShowGift(self):
		self.wndTaskBar.ShowGift()

	def CloseWbWindow(self):
		self.wndWeb.Close()

	if app.ENABLE_RENEWAL_CUBE:
		def BINARY_CUBE_RENEWAL_OPEN(self):
			self.wndCubeRenewal.Show()

	def OpenCubeWindow(self):
		self.wndCube.Open()

		if FALSE == self.wndInventory.IsShow():
			self.wndInventory.Show()

	def UpdateCubeInfo(self, gold, itemVnum, count):
		self.wndCube.UpdateInfo(gold, itemVnum, count)

	def CloseCubeWindow(self):
		self.wndCube.Close()

	def FailedCubeWork(self):
		self.wndCube.Refresh()

	def SucceedCubeWork(self, itemVnum, count):
		self.wndCube.Clear()

		if 0:
			self.wndCubeResult.SetPosition(*self.wndCube.GetGlobalPosition())
			self.wndCubeResult.SetCubeResultItem(itemVnum, count)
			self.wndCubeResult.Open()
			self.wndCubeResult.SetTop()

	if constInfo.ENABLE_EXPANDED_TASKBAR:
		def PressExpandedTaskbar(self):
			if self.wndExpandedTaskBar.IsShow():
				self.wndExpandedTaskBar.Hide()
			else:
				self.wndExpandedTaskBar.Show()

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def ActAcce(self, iAct, bWindow):
			board = (self.wndAcceAbsorption,self.wndAcceCombine)[int(bWindow)]
			if iAct == 1:
				self.ActAcceOpen(board)
			elif iAct == 2:
				self.ActAcceClose(board)
			elif iAct == 3 or iAct == 4:
				self.ActAcceRefresh(board, iAct)

		def ActAcceOpen(self,board):
			if not board.IsOpened():
				board.Open()
			if not self.wndInventory.IsShow():
				self.wndInventory.Show()
			self.wndInventory.RefreshBagSlotWindow()

		def ActAcceClose(self,board):
			if board.IsOpened():
				board.Close()
			self.wndInventory.RefreshBagSlotWindow()

		def ActAcceRefresh(self,board,iAct):
			if board.IsOpened():
				board.Refresh(iAct)
			self.wndInventory.RefreshBagSlotWindow()

	if app.ENABLE_GUILDBANK_LOG:
		def OpenGuildBankInfo(self):
			self.wndGuildBank.Show()

		def GuildBankLogInfoRefresh(self):
			self.wndGuildBank.RefreshGuildBankInfo()

	if app.ENABLE_GUILDRENEWAL_SYSTEM and app.ENABLE_GUILD_DONATE_ATTENDANCE:
		def GuildDonateInfoRefresh(self):
			guildDonateBoard = uiGuild.DonateGuildDialog()
			guildDonateBoard.RefreshGuildDonateInfo()

	if app.ENABLE_MINIGAME_OKEY_CARDS_SYSTEM:
		def OpenCardsInfoWindow(self):
			self.wndCardsInfo.Open()

		def OpenCardsWindow(self, safemode):
			self.wndCards.Open(safemode)

		def UpdateCardsInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points):
			self.wndCards.UpdateCardsInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points)

		def UpdateCardsFieldInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
			self.wndCards.UpdateCardsFieldInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)

		def CardsPutReward(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
			self.wndCards.CardsPutReward(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)

		def CardsShowIcon(self):
			self.wndCardsIcon.Show()

	def __HideWindows(self):
		hideWindows = self.wndTaskBar,\
						self.wndCharacter,\
						self.wndInventory,\
						self.wndMiniMap,\
						self.wndGuild,\
						self.wndMessenger,\
						self.wndChat,\
						self.wndParty,\
						self.wndGameButton,

		if self.wndExpandedTaskBar:
			hideWindows += self.wndExpandedTaskBar,

		if self.wndExpandedMoneyTaskBar:
			hideWindows += self.wndExpandedMoneyTaskBar,

		if app.ENABLE_RIDING_EXTENDED and self.wndMountUpGrade:
			hideWindows += self.wndMountUpGrade,

		if app.ENABLE_RENEWAL_SWITCHBOT:
			if self.wndSwitchbot:
				hideWindows += self.wndSwitchbot,

		if app.ENABLE_SPECIAL_INVENTORY:
			if self.wndSpecialInventory:
				hideWindows += self.wndSpecialInventory,

		if app.ENABLE_RENEWAL_BATTLE_PASS:
			if self.wndBattlePassExtended:
				hideWindows += self.wndBattlePassExtended,

		if app.ENABLE_GROWTH_PET_SYSTEM:
			if self.wndPetInfoWindow:
				hideWindows += self.wndPetInfoWindow,

		if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
			if self.wndWarpWindow:
				hideWindows += self.wndWarpWindow,

		if app.ENABLE_RENEWAL_SPECIAL_CHAT:
			if self.wndSpecialChat:
				hideWindows += self.wndSpecialChat,

		if app.ENABLE_HUNTING_SYSTEM:
			if self.wndHunting:
				hideWindows += self.wndHunting,

			if self.wndHuntingSelect:
				hideWindows += self.wndHuntingSelect,

			if self.wndHuntingReward:
				hideWindows += self.wndHuntingReward,

		hideWindows = filter(lambda x:x.IsShow(), hideWindows)
		map(lambda x:x.Hide(), hideWindows)
		import sys

		self.HideAllQuestButton()
		self.HideAllWhisperButton()

		if self.wndChat.IsEditMode():
			self.wndChat.CloseChat()

		return hideWindows

	def __ShowWindows(self, wnds):
		import sys
		map(lambda x:x.Show(), wnds)
		global IsQBHide
		if not IsQBHide:
			self.ShowAllQuestButton()
		else:
			self.HideAllQuestButton()

		self.ShowAllWhisperButton()

	def BINARY_OpenAtlasWindow(self):
		if self.wndMiniMap:
			self.wndMiniMap.ShowAtlas()

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def BINARY_SetObserverMode(self, flag, isbuttonshow):
			self.wndGameButton.SetObserverMode(flag,isbuttonshow)
	else:
		def BINARY_SetObserverMode(self, flag):
			self.wndGameButton.SetObserverMode(flag)

	# ACCESSORY_REFINE_ADD_METIN_STONE
	def BINARY_OpenSelectItemWindow(self):
		self.wndItemSelect.Open()
	# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

	def OpenPrivateShopInputNameDialog(self):
		if app.ENABLE_AURA_COSTUME_SYSTEM:
			if self.wndAura and self.wndAura.IsShow():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_OPEN_OTHER_WINDOW)
				return

		if app.ENABLE_GROWTH_PET_SYSTEM:
			pet_id = player.GetActivePetItemId()
			if pet_id:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_OPEN_SHOP_BECAUSE_SUMMON)
				return

		inputDialog = uiCommon.InputDialog()
		inputDialog.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_NAME_DIALOG_TITLE)
		inputDialog.SetMaxLength(32)
		inputDialog.SetAcceptEvent(ui.__mem_func__(self.OpenPrivateShopBuilder))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.ClosePrivateShopInputNameDialog))
		inputDialog.Open()
		self.inputDialog = inputDialog

	def ClosePrivateShopInputNameDialog(self):
		self.inputDialog = None
		return TRUE

	def OpenPrivateShopBuilder(self):
		if app.ENABLE_AURA_COSTUME_SYSTEM:
			if self.wndAura and self.wndAura.IsShow():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_OPEN_OTHER_WINDOW)
				return

		if app.ENABLE_GROWTH_PET_SYSTEM:
			pet_id = player.GetActivePetItemId()
			if pet_id:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_OPEN_SHOP_BECAUSE_SUMMON)
				return

		if not self.inputDialog:
			return TRUE

		if not len(self.inputDialog.GetText()):
			return TRUE

		self.privateShopBuilder.Open(self.inputDialog.GetText())
		self.ClosePrivateShopInputNameDialog()
		return TRUE

	def AppearPrivateShop(self, vid, text):

		board = uiPrivateShopBuilder.PrivateShopAdvertisementBoard()
		board.Open(vid, text)

		self.privateShopAdvertisementBoardDict[vid] = board

	def DisappearPrivateShop(self, vid):
		if not self.privateShopAdvertisementBoardDict.has_key(vid):
			return

		del self.privateShopAdvertisementBoardDict[vid]
		uiPrivateShopBuilder.DeleteADBoard(vid)

	def OpenEquipmentDialog(self, vid):
		dlg = uiEquipmentDialog.EquipmentDialog()
		dlg.SetItemToolTip(self.tooltipItem)
		dlg.SetCloseEvent(ui.__mem_func__(self.CloseEquipmentDialog))
		dlg.Open(vid)

		self.equipmentDialogDict[vid] = dlg

	if app.ENABLE_CHANGE_LOOK_SYSTEM:
		def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count, dwChangeLookVnum):
			if not vid in self.equipmentDialogDict:
				return
			self.equipmentDialogDict[vid].SetEquipmentDialogItem(slotIndex, vnum, count, dwChangeLookVnum)
	else:
		def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
			if not vid in self.equipmentDialogDict:
				return
			self.equipmentDialogDict[vid].SetEquipmentDialogItem(slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogSocket(slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogAttr(slotIndex, attrIndex, type, value)

	def CloseEquipmentDialog(self, vid):
		if not vid in self.equipmentDialogDict:
			return
		del self.equipmentDialogDict[vid]

	def BINARY_ClearQuest(self, index):
		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

	def RecvQuest(self, index, name):
		self.BINARY_RecvQuest(index, name, "file", localeInfo.GetLetterImageName())

	def BINARY_RecvQuest(self, index, name, iconType, iconName):

		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

		btn = uiWhisper.WhisperButton()

		import item
		if "item"==iconType:
			item.SelectItem(int(iconName))
			buttonImageFileName=item.GetIconImageFileName()
		else:
			buttonImageFileName=iconName
			btn.SetUpVisual(localeInfo.GetLetterCloseImageName())
			btn.SetOverVisual(localeInfo.GetLetterOpenImageName())
			btn.SetDownVisual(localeInfo.GetLetterOpenImageName())

		if not app.ENABLE_RENEWAL_QUEST:
			btn.SetToolTipText(name, -20, 35)
			btn.ToolTipText.SetHorizontalAlignLeft()

			btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)
			btn.Show()
		else:
			btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)

		btn.index = index
		btn.name = name

		self.questButtonList.insert(0, btn)
		self.__ArrangeQuestButton()

	def __ArrangeQuestButton(self):

		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		if self.wndParty.IsShow():
			xPos = 100 + 30
		else:
			xPos = 20

		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63

		count = 0
		for btn in self.questButtonList:
			if app.ENABLE_RENEWAL_QUEST:
				btn.SetToolTipText(str(len(self.questButtonList)))
				btn.ToolTipText.SetHorizontalAlignCenter()

			btn.SetPosition(xPos + (int(count/yCount) * 100), yPos + (count%yCount * 63))
			count += 1

			global IsQBHide
			if IsQBHide:
				btn.Hide()
			else:
				if app.ENABLE_RENEWAL_QUEST and count > 0:
					btn.Hide()
				else:
					btn.Show()

	def __StartQuest(self, btn):
		if app.ENABLE_RENEWAL_QUEST:
			self.__OnClickQuestButton()
			self.HideAllQuestButton()
		else:
			event.QuestButtonClick(btn.index)
			self.__DestroyQuestButton(btn)

	def __FindQuestButton(self, index):
		for btn in self.questButtonList:
			if btn.index == index:
				return btn

		return 0

	def __DestroyQuestButton(self, btn):
		btn.SetEvent(0)
		self.questButtonList.remove(btn)
		self.__ArrangeQuestButton()

	def HideAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Hide()

	def ShowAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Show()
			if app.ENABLE_RENEWAL_QUEST:
				break

	def __InitWhisper(self):
		chat.InitWhisper(self)

	def OpenWhisperDialogWithoutTarget(self):
		if not self.dlgWhisperWithoutTarget:
			dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
			dlgWhisper.BindInterface(self)
			dlgWhisper.LoadDialog()
			dlgWhisper.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)
			dlgWhisper.SetPosition(self.windowOpenPosition * 30,self.windowOpenPosition * 30)
			dlgWhisper.Show()
			self.dlgWhisperWithoutTarget = dlgWhisper

			self.windowOpenPosition = (self.windowOpenPosition + 1) % 5

		else:
			self.dlgWhisperWithoutTarget.SetTop()
			self.dlgWhisperWithoutTarget.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)

	def RegisterTemporaryWhisperDialog(self, name):
		if not self.dlgWhisperWithoutTarget:
			return

		btn = self.__FindWhisperButton(name)
		if 0 != btn:
			self.__DestroyWhisperButton(btn)

		elif self.whisperDialogDict.has_key(name):
			oldDialog = self.whisperDialogDict[name]
			oldDialog.Destroy()
			del self.whisperDialogDict[name]

		self.whisperDialogDict[name] = self.dlgWhisperWithoutTarget
		self.dlgWhisperWithoutTarget.OpenWithTarget(name)
		self.dlgWhisperWithoutTarget = None
		self.__CheckGameMaster(name)

	if app.ENABLE_EXTENDED_WHISPER_DETAILS and app.ENABLE_MULTI_LANGUAGE_SYSTEM:
		def RecieveWhisperDetails(self, name, country):
			if self.whisperDialogDict.has_key(name):
				self.whisperDialogDict[name].SetCountryFlag(country)
			else:
				btn = self.__FindWhisperButton(name)
				if btn != 0:
					btn.countryID = country

	def OpenWhisperDialog(self, name):
		if not self.whisperDialogDict.has_key(name):
			dlg = self.__MakeWhisperDialog(name)
			dlg.OpenWithTarget(name)
			dlg.chatLine.SetFocus()
			dlg.Show()

			self.__CheckGameMaster(name)
			btn = self.__FindWhisperButton(name)
			if 0 != btn:
				self.__DestroyWhisperButton(btn)

	def RecvWhisper(self, name):
		if not self.whisperDialogDict.has_key(name):
			btn = self.__FindWhisperButton(name)
			if 0 == btn:
				btn = self.__MakeWhisperButton(name)
				btn.Flash()

				if app.ENABLE_BLINK_ALERT:
					app.FlashApplication()

				chat.AppendChat(chat.CHAT_TYPE_NOTICE, localeInfo.RECEIVE_MESSAGE % (name))

			else:
				btn.Flash()

				if app.ENABLE_BLINK_ALERT:
					app.FlashApplication()

		elif self.IsGameMasterName(name):
			dlg = self.whisperDialogDict[name]
			dlg.SetGameMasterLook()

	def MakeWhisperButton(self, name):
		self.__MakeWhisperButton(name)

	def ShowWhisperDialog(self, btn):
		try:
			self.__MakeWhisperDialog(btn.name)
			dlgWhisper = self.whisperDialogDict[btn.name]
			dlgWhisper.OpenWithTarget(btn.name)
			dlgWhisper.Show()
			self.__CheckGameMaster(btn.name)
		except:
			import dbg
			dbg.TraceError("interface.ShowWhisperDialog - Failed to find key")

		self.__DestroyWhisperButton(btn)

	def MinimizeWhisperDialog(self, name):

		if 0 != name:
			self.__MakeWhisperButton(name)

		self.CloseWhisperDialog(name)

	def CloseWhisperDialog(self, name):

		if 0 == name:

			if self.dlgWhisperWithoutTarget:
				self.dlgWhisperWithoutTarget.Destroy()
				self.dlgWhisperWithoutTarget = None

			return

		try:
			dlgWhisper = self.whisperDialogDict[name]
			dlgWhisper.Destroy()
			del self.whisperDialogDict[name]
		except:
			import dbg
			dbg.TraceError("interface.CloseWhisperDialog - Failed to find key")

	def __ArrangeWhisperButton(self):

		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		xPos = screenWidth - 70
		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63

		count = 0
		for button in self.whisperButtonList:

			button.SetPosition(xPos + (int(count/yCount) * -50), yPos + (count%yCount * 63))
			count += 1

	def __FindWhisperButton(self, name):
		for button in self.whisperButtonList:
			if button.name == name:
				return button

		return 0

	def __MakeWhisperDialog(self, name):
		dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
		dlgWhisper.BindInterface(self)
		dlgWhisper.LoadDialog()
		dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
		self.whisperDialogDict[name] = dlgWhisper

		self.windowOpenPosition = (self.windowOpenPosition+1) % 5

		return dlgWhisper

	def __MakeWhisperButton(self, name):
		whisperButton = uiWhisper.WhisperButton()
		whisperButton.SetUpVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
		whisperButton.SetOverVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
		whisperButton.SetDownVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
		if self.IsGameMasterName(name):
			whisperButton.SetToolTipTextWithColor(name, 0xffffa200)
		else:
			whisperButton.SetToolTipText(name)
		whisperButton.ToolTipText.SetHorizontalAlignCenter()
		whisperButton.SetEvent(ui.__mem_func__(self.ShowWhisperDialog), whisperButton)
		whisperButton.Show()
		whisperButton.name = name

		self.whisperButtonList.insert(0, whisperButton)
		self.__ArrangeWhisperButton()

		return whisperButton

	def __DestroyWhisperButton(self, button):
		button.SetEvent(0)
		self.whisperButtonList.remove(button)
		self.__ArrangeWhisperButton()

	def HideAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Hide()

	def ShowAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Show()

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def RefreshVisibleCostume(self):
			self.wndInventory.RefreshVisibleCostume()

	if app.ENABLE_SPECIAL_INVENTORY:
		def CloseLoadSafeboxEvent(self):
			if not self.wndSpecialInventory:
				return

			self.wndSpecialInventory.CloseLoadSafeboxEvent()

		def CloseLoadMallEvent(self):
			if not self.wndSpecialInventory:
				return

			self.wndSpecialInventory.CloseLoadMallEvent()

	def __CheckGameMaster(self, name):
		if not self.listGMName.has_key(name):
			return
		if self.whisperDialogDict.has_key(name):
			dlg = self.whisperDialogDict[name]
			dlg.SetGameMasterLook()

	def RegisterGameMasterName(self, name):
		if self.listGMName.has_key(name):
			return
		self.listGMName[name] = "GM"

	def IsGameMasterName(self, name):
		if self.listGMName.has_key(name):
			return TRUE
		else:
			return FALSE

	### Guild Building ###

	def BUILD_OpenWindow(self):
		self.wndGuildBuilding = uiGuild.BuildGuildBuildingWindow()
		self.wndGuildBuilding.Open()
		self.wndGuildBuilding.wnds = self.__HideWindows()
		self.wndGuildBuilding.SetCloseEvent(ui.__mem_func__(self.BUILD_CloseWindow))

	def BUILD_CloseWindow(self):
		self.__ShowWindows(self.wndGuildBuilding.wnds)
		self.wndGuildBuilding = None

	def BUILD_OnUpdate(self):
		if not self.wndGuildBuilding:
			return

		if self.wndGuildBuilding.IsPositioningMode():
			import background
			x, y, z = background.GetPickingPoint()
			self.wndGuildBuilding.SetBuildingPosition(x, y, z)

	def BUILD_OnMouseLeftButtonDown(self):
		if not self.wndGuildBuilding:
			return

		# GUILD_BUILDING
		if self.wndGuildBuilding.IsPositioningMode():
			self.wndGuildBuilding.SettleCurrentPosition()
			return TRUE
		elif self.wndGuildBuilding.IsPreviewMode():
			pass
		else:
			return TRUE
		# END_OF_GUILD_BUILDING
		return FALSE

	def BUILD_OnMouseLeftButtonUp(self):
		if not self.wndGuildBuilding:
			return

		if not self.wndGuildBuilding.IsPreviewMode():
			return TRUE

		return FALSE

	def BULID_EnterGuildArea(self, areaID):
		# GUILD_BUILDING
		mainCharacterName = player.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()

		if mainCharacterName != masterName:
			return

		if areaID != player.GetGuildID():
			return
		# END_OF_GUILD_BUILDING

		self.wndGameButton.ShowBuildButton()

	def BULID_ExitGuildArea(self, areaID):
		self.wndGameButton.HideBuildButton()

	def IsEditLineFocus(self):
		if self.ChatWindow.chatLine.IsFocus():
			return 1

		if self.ChatWindow.chatToLine.IsFocus():
			return 1

		return 0

	def AttachItemFromSafebox(self, slotIndex, itemIndex):
		if self.wndInventory and self.wndInventory.IsShow():
			self.wndInventory.AttachItemFromSafebox(slotIndex, itemIndex)

		return TRUE

	def AttachInvenItemToOtherWindowSlot(self, slotWindow, slotIndex):
		if self.wndSafebox and self.wndSafebox.IsShow():
			return self.wndSafebox.AttachItemFromInventory(slotWindow, slotIndex)

		return FALSE

	def EmptyFunction(self):
		pass

	def IsShowDlgQuestionWindow(self):
		if self.wndInventory.IsDlgQuestionShow():
			return TRUE
		else:
			return FALSE

	def CloseDlgQuestionWindow(self):
		if self.wndInventory.IsDlgQuestionShow():
			self.wndInventory.CancelDlgQuestion()

	def DeactivateSlot(self, slotindex, type):
		self.wndInventory.DeactivateSlot(slotindex, type)

	def ActivateSlot(self, slotindex, type):
		self.wndInventory.ActivateSlot(slotindex, type)

	if app.ENABLE_RENDER_TARGET:
		def MakeRenderTargetWindow(self):
			if self.wndRenderTarget == None:
				self.wndRenderTarget = uiRenderTarget.RenderTargetWindow()

		def OpenRenderTargetWindow(self, renderType = 0, renderVnum = 11299):
			self.MakeRenderTargetWindow()
			self.wndRenderTarget.Open(renderType, renderVnum)

	if app.ENABLE_RENEWAL_OFFLINESHOP:
		def MakeOfflineShopMessage(self):
			if self.dlgShopMessage == None:
				self.dlgShopMessage = ui.MessageWindow()

		def AddOfflineShopMessage(self, itemVnum, itemCount, itemPrice):
			itemVnum, itemCount, itemPrice = (int(itemVnum), int(itemCount), int(itemPrice))
			self.MakeOfflineShopMessage()
			item.SelectItem(itemVnum)

			if itemCount > 1:
				self.dlgShopMessage.AddMessage(localeInfo.OFFLINESHOP_ITEM_SOLD_MESSAGE_WITH_COUNT % (itemCount, item.GetItemName(), localeInfo.NumberToMoneyString(itemPrice)), 5)
			else:
				self.dlgShopMessage.AddMessage(localeInfo.OFFLINESHOP_ITEM_SOLD_MESSAGE % (item.GetItemName(), localeInfo.NumberToMoneyString(itemPrice)), 5)

		def OpenOfflineShopDialog(self, vid, isOwner):
			self.wndInventory.Show()
			self.wndInventory.SetTop()

			if isOwner:
				self.OpenOfflineShopPanel()
			else:
				if self.dlgOfflineShop == None:
					self.MakeOfflineShop()

				if self.dlgOfflineShop:
					self.dlgOfflineShop.Open(vid)
					self.dlgOfflineShop.SetCenterPosition()
					self.dlgOfflineShop.SetTop()

		def OpenOfflineShopPanel(self):
			if self.dlgOfflineShopPanel == None:
				self.MakeOfflineShopPanel()

			self.dlgOfflineShopPanel.Open()
			self.dlgOfflineShopPanel.SetTop()
			self.dlgOfflineShopPanel.SetCenterPosition()

		def OpenOfflineShopBuilder(self):
			if self.offlineShopBuilder == None:
				self.MakeOfflineShopBuilder()

			self.offlineShopBuilder.Open(".....")
			self.offlineShopBuilder.SetTop()

		def DisappearOfflineShop(self, vid):
			uiOfflineShopBuilder.HideADBoardWithKey(vid)

		def AppearOfflineShop(self, vid, text):
			type = 0
			if text[0].isdigit():
				type = int(text[0])
				text = text[1:]
			if uiOfflineShopBuilder.ShowADBoardWithKey(vid) == FALSE:
				board = uiOfflineShopBuilder.OfflineShopAdvertisementBoard(type)
				board.Open(vid, text)
			else:
				uiOfflineShopBuilder.UpdateADText(vid, type, text)

		def MakeOfflineShopBuilder(self):
			self.offlineShopBuilder = uiOfflineShopBuilder.OfflineShopBuilder()
			self.offlineShopBuilder.BindInterfaceClass(self)
			self.offlineShopBuilder.Hide()

		def MakeOfflineShop(self):
			self.dlgOfflineShop = uiOfflineShop.OfflineShopDialog()
			self.dlgOfflineShop.BindInterfaceClass(self)
			self.dlgOfflineShop.LoadDialog()
			self.dlgOfflineShop.Hide()

		def MakeOfflineShopPanel(self):
			self.dlgOfflineShopPanel = uiOfflineShop.OfflineMyShop()
			self.dlgOfflineShopPanel.BindInterfaceClass(self)
			self.dlgOfflineShopPanel.LoadWindow()

		def AppendLogOfflineShopPanel(self, name, date, itemvnum, itemcount, price):
			if self.dlgOfflineShopPanel == None:
				self.MakeOfflineShopPanel()

			self.dlgOfflineShopPanel.AppendLog(name, date, itemvnum, itemcount, price)

		def AppendLogOfflineShopPanelFirst(self, name, date, itemvnum, itemcount, price):
			if self.dlgOfflineShopPanel == None:
				self.MakeOfflineShopPanel()

			self.dlgOfflineShopPanel.AppendLogFirst(name, date, itemvnum, itemcount, price)

		def ToggleOfflineShopWindow(self):
			if self.dlgOfflineShopPanel:
				if self.dlgOfflineShopPanel.IsShow():
					self.dlgOfflineShopPanel.CloseReal()
					return

			if self.offlineShopBuilder:
				if self.offlineShopBuilder.IsShow():
					self.offlineShopBuilder.CloseReal()
					return

			net.SendOfflineShopButton()

	if app.ENABLE_OFFLINESHOP_SEARCH_SYSTEM:
		def __MakePrivateShopSearchWindow(self):
			self.wndPrivateShopSearch = uiPrivateShopSearch.PrivateShopSearchDialog()
			self.wndPrivateShopSearch.BindInterfaceClass(self)
			self.wndPrivateShopSearch.LoadWindow()

		def OfflineShopBuyed(self, itemID):
			if self.wndPrivateShopSearch:
				self.wndPrivateShopSearch.SetItemBuyStatus(int(itemID))

		def OpenPrivateShopSearch(self, type = 0):
			if self.wndPrivateShopSearch == None:
				self.__MakePrivateShopSearchWindow()
				self.wndPrivateShopSearch.Open(type)
				return

			if self.wndPrivateShopSearch.IsShow():
				self.wndPrivateShopSearch.Hide()
			else:
				self.wndPrivateShopSearch.Open(type)

		def RefreshShopSearch(self):
			if self.wndPrivateShopSearch == None:
				self.__MakePrivateShopSearchWindow()

			self.wndPrivateShopSearch.RefreshMe()
			self.wndPrivateShopSearch.RefreshList()

	if app.ENABLE_INGAME_WIKI_SYSTEM:
		def __MakeWiki(self):
			if self.wndWiki == None:
				self.wndWiki = uiWiki.EncyclopediaofGame()

		def OpenWikiWindow(self):
			self.__MakeWiki()
			if self.wndWiki.IsShow():
				self.wndWiki.Close()
			else:
				self.wndWiki.Open()

	if app.ENABLE_AUTOMATIC_PICK_UP_SYSTEM:
		def OnChangePickUPMode(self):
			self.dlgSystem.OnChangePickUPMode()

	if app.ENABLE_RENEWAL_SKILL_SELECT:
		def OpenSkillSelectWindow(self, job):
			self.wndSkillSelect.Open(job)

	if app.ENABLE_NEW_DUNGEON_LIB:
		def MakeDungeonTimerWindow(self):
			self.wndDungeonTimer = uiDungeonTimer.Cooldown()
			self.wndDungeonTimer.Hide()

	if app.ENABLE_RENEWAL_INGAME_ITEMSHOP:
		def MakeItemShopWindow(self):
			if self.wndItemShop == None:
				self.wndItemShop = uiItemShop.ItemShopWindow()
				self.wndItemShop.BindInterfaceClass(self)

		def OpenItemShopWindow(self):
			self.MakeItemShopWindow()
			if self.wndItemShop.IsShow():
				self.wndItemShop.Close()
			else:
				self.wndItemShop.Open()

		def OpenItemShopMainWindow(self):
			self.MakeItemShopWindow()
			self.wndItemShop.Open()
			self.wndItemShop.LoadFirstOpening()

		def ItemShopHideLoading(self):
			self.MakeItemShopWindow()
			self.wndItemShop.Open()
			self.wndItemShop.CloseLoading()

		def ItemShopPurchasesWindow(self):
			self.MakeItemShopWindow()
			self.wndItemShop.Open()
			self.wndItemShop.OpenPurchasesWindow()

		def ItemShopUpdateItem(self, itemID, itemMaxSellingCount):
			self.MakeItemShopWindow()
			self.wndItemShop.UpdateItem(itemID, itemMaxSellingCount)

		def ItemShopSetDragonCoin(self,dragonCoin):
			self.MakeItemShopWindow()
			self.wndItemShop.SetDragonCoin(dragonCoin)

		def SetWheelItemData(self, cmd):
			self.MakeItemShopWindow()
			self.wndItemShop.SetWheelItemData(str(cmd))

		def OnSetWhell(self, giftIndex):
			self.MakeItemShopWindow()
			self.wndItemShop.OnSetWhell(int(giftIndex))

		def GetWheelGiftData(self, itemVnum, itemCount):
			self.MakeItemShopWindow()
			self.wndItemShop.GetWheelGiftData(int(itemVnum), int(itemCount))

	if app.ENABLE_SLOT_MARKING_SYSTEM:
		def MarkUnusableInvenSlotOnTopWnd(self, onTopWnd, InvenSlot):
			if app.ENABLE_SLOT_MARKING_SYSTEM:
				if onTopWnd == player.ON_TOP_WND_SHOP and self.dlgShop and self.dlgShop.CantSellInvenItem(InvenSlot):
					return TRUE
				elif onTopWnd == player.ON_TOP_WND_SAFEBOX and self.wndSafebox and self.wndSafebox.CantCheckInItem(InvenSlot):
					return TRUE
				elif onTopWnd == player.ON_TOP_WND_PRIVATE_SHOP and self.privateShopBuilder and self.privateShopBuilder.CantTradableItem(InvenSlot):
					return TRUE
				elif onTopWnd == player.ON_TOP_WND_EXCHANGE and self.dlgExchange and self.dlgExchange.CantTradableItem(InvenSlot):
					return TRUE

			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				if onTopWnd == player.ON_TOP_WND_ACCE_COMBINE and self.wndAcceCombine and self.wndAcceCombine.CantTradableItem(InvenSlot):
					return TRUE
				elif onTopWnd == player.ON_TOP_WND_ACCE_ABSORB and self.wndAcceAbsorption and self.wndAcceAbsorption.CantTradableItem(InvenSlot):
					return TRUE

			return FALSE

		def SetOnTopWindow(self, onTopWnd):
			self.OnTopWindow = onTopWnd

		def GetOnTopWindow(self):
			return self.OnTopWindow

		def RefreshMarkInventoryBag(self):
			if self.wndInventory and self.wndInventory.IsShow():
				self.wndInventory.RefreshBagSlotWindow()

			if app.ENABLE_SPECIAL_INVENTORY:
				if self.wndSpecialInventory and self.wndSpecialInventory.IsShow():
					self.wndSpecialInventory.RefreshBagSlotWindow()

	if app.ENABLE_AURA_COSTUME_SYSTEM:
		def AuraWindowOpen(self, type):
			if self.wndAura.IsShow():
				return

			if self.inputDialog or self.privateShopBuilder.IsShow():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ACCE_NOT_OPEN_PRIVATE_SHOP)
				return

			if self.dlgRefineNew and self.dlgRefineNew.IsShow():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ACCE_NOT_OPEN_REFINE)
				return

			self.wndAura.Open(type)

			if not self.wndInventory.IsShow():
				self.wndInventory.Show()

		def AuraWindowClose(self):
			if not self.wndAura.IsShow():
				return

			self.wndAura.CloseWindow()

	if app.ENABLE_FISH_GAME:
		def MakeFishGameWindow(self):
			if self.wndFishGame == None:
				self.wndFishGame = uiFishGame.FishGameWindow()

		def OpenFishGameWindow(self, gameKey):
			self.MakeFishGameWindow()
			self.wndFishGame.Open(int(gameKey))

		def SetFishGameGoal(self, goalCount):
			self.MakeFishGameWindow()
			self.wndFishGame.SetFishScore(int(goalCount))

		def CloseFishGame(self):
			self.MakeFishGameWindow()
			self.wndFishGame.Hide()

	if app.ENABLE_GROWTH_PET_SYSTEM:
		def PetHatchingWindowCommand(self, command):
			if self.wndPetInfoWindow:
				if self.wndPetInfoWindow.wndPetHatching:
					self.wndPetInfoWindow.wndPetHatching.PetHatchingWindowCommand(command)

		def PetNameChangeWindowCommand(self, command):
			if self.wndPetInfoWindow:
				if self.wndPetInfoWindow.wndPetNameChange:
					self.wndPetInfoWindow.wndPetNameChange.PetNameChangeWindowCommand(command)

		def PetSkillUpgradeDlgOpen(self, slot, index, gold):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.OpenPetSkillUpGradeQuestionDialog(slot, index, gold)

		def PetFlashEvent(self, index):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetFlashEvent(index)

		def PetInfoBindAffectShower(self, affect_shower):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetInfoBindAffectShower(affect_shower)

		def PetAffectShowerRefresh(self):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetAffectShowerRefresh()

		def PetFeedReuslt(self, result):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetFeedReuslt(result)

		def PetAttrDetermineResult(self, byType):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetAttrDetermineResult(byType)

		def PetAttrChangeResult(self, slotIndex, byType):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetAttrChangeResult(slotIndex, byType)

		def PetReviveResult(self, result):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetReviveResult(result)

		def PetWindowTypeResult(self, result):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetWindowTypeResult(result)

		def TogglePetInformationWindow(self):
			if FALSE == player.IsObserverMode():
				if not self.wndPetInfoWindow.IsShow():
					self.wndPetInfoWindow.Show()
				else:
					self.wndPetInfoWindow.Close()

	if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
		def OpenWarpWindow(self):
			if self.wndWarpWindow.IsShow():
				self.wndWarpWindow.Close()
			else:
				self.wndWarpWindow.Open()

	if app.ENABLE_DUNGEON_TRACKING_SYSTEM:
		def TrackWindowCheckPacket(self):
			self.wndTrackWindow.CheckPacket()

		def MakeTrackWindow(self):
			if self.wndTrackWindow == None:
				self.wndTrackWindow = uiTrack.TrackWindow()
				self.wndTrackWindow.BindInterfaceClass(self)

		def OpenTrackWindow(self):
			self.MakeTrackWindow()
			if self.wndTrackWindow.IsShow():
				self.wndTrackWindow.Close()
			else:
				self.wndTrackWindow.Open()

		def TrackDungeonInfo(self, cmdData):
			self.MakeTrackWindow()
			self.wndTrackWindow.TrackDungeonInfo(cmdData)

		def TrackBossInfo(self, bossID, bossLeftTime, bossChannel):
			self.MakeTrackWindow()
			self.wndTrackWindow.TrackBossInfo(int(bossID), int(bossLeftTime), int(bossChannel))

		def TrackRecvInfo(self, content):
			content = content.replace("$", " ")
			self.RegisterGameMasterName(localeInfo.SYSTEM_WHISPER)
			chat.AppendWhisper(chat.WHISPER_TYPE_CHAT, localeInfo.SYSTEM_WHISPER, content)
			self.RecvWhisper(localeInfo.SYSTEM_WHISPER)

	if app.ENABLE_CHANGE_LOOK_SYSTEM:
		def ChangeWindowOpen(self, type):
			if self.wndChangeLook:
				self.wndChangeLook.Open(type)

		def IsShowDlgQuestionWindow(self):
			if self.wndInventory.IsDlgQuestionShow():
				return TRUE
			else:
				return FALSE

		def CloseDlgQuestionWindow(self):
			if self.wndInventory.IsDlgQuestionShow():
				self.wndInventory.CancelDlgQuestion()

	if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
		if app.ENABLE_GUILD_REQUEST:
			def RefreshGuildRankingList(self, issearch):
				if self.wndGuild:
					self.wndGuild.RefreshGuildRankingList(issearch)

			def CloseGuildRankWindow(self):
				if self.wndGuild:
					self.wndGuild.CloseGuildListDialog()

		def ShowGuildWarButton(self):
			if self.wndGameButton:
				self.wndGameButton.ShowGuildWarButton()

		def HideGuildWarButton(self):
			if self.wndGameButton:
				self.wndGameButton.HideGuildWarButton()

	if app.ENABLE_HUNTING_SYSTEM:
		def ToggleHuntingWindow(self):
			if self.wndHunting.IsShow():
				self.wndHunting.Close()
			elif self.wndHuntingSelect.IsShow():
				self.wndHuntingSelect.Close()
			else:
				net.SendHuntingAction(1, 0)

		def OpenHuntingWindowMain(self, level, monster, cur_count, dest_count, money_min, money_max, exp_min, exp_max, race_item, race_item_count):
			if self.wndHunting:
				self.wndHunting.OpenMain(level, monster, cur_count, dest_count, money_min, money_max, exp_min, exp_max, race_item, race_item_count)
				self.wndHunting.SetTop()
				constInfo.HUNTING_BUTTON_FLASH = 0

		def OpenHuntingWindowSelect(self, level, type ,monster, count, money_min, money_max, exp_min, exp_max, race_item, race_item_count):
			if self.wndHunting and self.wndHunting.IsShow():
				self.wndHunting.CloseWithMini()
			self.wndHuntingSelect.OpenSelect(level, type ,monster, count, money_min, money_max, exp_min, exp_max, race_item, race_item_count)
			constInfo.HUNTING_BUTTON_FLASH = 0

		def OpenHuntingWindowReward(self, level, reward, reward_count, random_reward, random_reward_count, money, exp):
			if False == self.wndHuntingReward.IsShow():
				self.wndHuntingReward.OpenReward(level, reward, reward_count, random_reward, random_reward_count, money, exp)
				self.wndHuntingReward.SetTop()

		def UpdateHuntingMission(self, count):
			if self.wndHunting:
				self.wndHunting.UpdateMission(count)

		def HuntingSetRandomItemsMain(self, item_vnum, item_count):
			if self.wndHunting:
				self.wndHunting.SetRandomItemTable(item_vnum, item_count)

		def HuntingSetRandomItemsSelect(self, item_vnum, item_count):
			if self.wndHuntingSelect:
				self.wndHuntingSelect.SetRandomItemTable(item_vnum, item_count)

	if app.ENABLE_RIDING_EXTENDED:
		def MountUpGradeWindow(self):
			if not player.IsObserverMode():
				if not self.wndMountUpGrade.IsShow():
					self.wndMountUpGrade.Open()
				else:
					self.wndMountUpGrade.Close()

	if app.__AUTO_HUNT__:
		def AutoHuntStatus(self, status):
			if self.wndAutoHunt:
				self.wndAutoHunt.SetStatus(True if int(status) else False)
		def CheckAutoLogin(self):
			if self.wndAutoHunt == None:
				self.wndAutoHunt = uiAutoHunt.Window()
			self.wndAutoHunt.CheckAutoLogin()
		def OpenAutoHunt(self):
			if self.wndAutoHunt == None:
				self.wndAutoHunt = uiAutoHunt.Window()
			if self.wndAutoHunt.IsShow():
				self.wndAutoHunt.Close()
			else:
				self.wndAutoHunt.Open()
		def ToggleAutoHuntWindow(self):
			if self.wndAutoHunt == None:
				self.wndAutoHunt = uiAutoHunt.Window()
			if self.wndAutoHunt.IsShow():
				self.wndAutoHunt.Close()
			else:
				self.wndAutoHunt.Open()
