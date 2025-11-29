if __USE_DYNAMIC_MODULE__:
	import pyapi

app = __import__(pyapi.GetModuleName("app"))
chr = __import__(pyapi.GetModuleName("chr"))
chrmgr = __import__(pyapi.GetModuleName("chrmgr"))
player = __import__(pyapi.GetModuleName("player"))
net = __import__(pyapi.GetModuleName("net"))

import os
import dbg
import grp
import item
import background
import event
import snd
import chat
import textTail
import snd
import effect
import wndMgr
import fly
import systemSetting
import quest
import guild
import skill
import messenger
import serverInfo
import localeInfo
import constInfo
import exchange
import ime

import ui
import uiCommon
import uiPhaseCurtain
import uiMapNameShower
import uiAffectShower
import uiPlayerGauge
import uiCharacter
import uiTarget
import uiPrivateShopBuilder

import mouseModule
import consoleModule
import localeInfo

import playerSettingModule
import interfaceModule

import musicInfo
import debugInfo
import stringCommander

# if app.ENABLE_GUILDRENEWAL_SYSTEM:
	# import uiGuildPopup
	# import uiGuildBank
if app.ENABLE_BIOLOG_SYSTEM:
	import biologmgr

if app.ENABLE_RENEWAL_OFFLINESHOP:
	import uiOfflineShopBuilder
	import shop

if app.ENABLE_MAINTENANCE_SYSTEM:
	import uiMaintenance

if app.ENABLE_RENEWAL_INGAME_ITEMSHOP:
	import uiItemShop

if app.ENABLE_SHIP_DEFENCE_DUNGEON:
	import uiShipMastHP

if app.ENABLE_SKILL_BOOK_READING:
	import uibkoku

if app.ENABLE_SPIRIT_STONE_READING:
	import uiruhtasi

from _weakref import proxy

SCREENSHOT_CWDSAVE = TRUE
SCREENSHOT_DIR = None

cameraDistance = 1550.0
cameraPitch = 27.0
cameraRotation = 0.0
cameraHeight = 100.0

testAlignment = 0

class GameWindow(ui.ScriptWindow):
	def __init__(self, stream):
		ui.ScriptWindow.__init__(self, "GAME")
		self.SetWindowName("game")
		net.SetPhaseWindow(net.PHASE_WINDOW_GAME, self)
		player.SetGameWindow(self)

		self.quickSlotPageIndex = 0
		self.lastPKModeSendedTime = 0
		self.pressNumber = None

		self.guildWarQuestionDialog = None
		self.interface = None
		self.targetBoard = None
		self.console = None
		self.mapNameShower = None
		self.affectShower = None
		self.playerGauge = None

		if app.ENABLE_AUTOMATIC_PICK_UP_SYSTEM:
			constInfo.PREMIUMMODE = [FALSE, 0]

		self.stream=stream
		self.interface = interfaceModule.Interface()
		self.interface.MakeInterface()
		self.interface.ShowDefaultWindows()

		self.curtain = uiPhaseCurtain.PhaseCurtain()
		self.curtain.speed = 0.03
		self.curtain.Hide()

		self.targetBoard = uiTarget.TargetBoard()
		self.targetBoard.SetWhisperEvent(ui.__mem_func__(self.interface.OpenWhisperDialog))
		self.targetBoard.Hide()

		self.console = consoleModule.ConsoleWindow()
		self.console.BindGameClass(self)
		self.console.SetConsoleSize(wndMgr.GetScreenWidth(), 200)
		self.console.Hide()

		self.mapNameShower = uiMapNameShower.MapNameShower()
		self.affectShower = uiAffectShower.AffectShower()


		if app.ENABLE_SPIRIT_STONE_READING:
			self.ruhtasi = uiruhtasi.RuhTasi()
			self.ruhtasi.Hide()

		if app.ENABLE_SKILL_BOOK_READING:
			self.bkoku = uibkoku.BKOku()
			self.bkoku.Hide()

		self.playerGauge = uiPlayerGauge.PlayerGauge(self)
		self.playerGauge.Hide()

		if app.ENABLE_MAINTENANCE_SYSTEM:
			self.wndMaintenance = uiMaintenance.MaintenanceClass()

		if app.ENABLE_SHIP_DEFENCE_DUNGEON:
			self.wndShipMastHP = uiShipMastHP.ShipMastHP()
			self.wndShipMastHP.Close()

		self.itemDropQuestionDialog = None

		self.__SetQuickSlotMode()

		self.__ServerCommand_Build()
		self.__ProcessPreservedServerCommand()

		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.interface.PetInfoBindAffectShower(self.affectShower)

	def __del__(self):
		player.SetGameWindow(0)
		net.ClearPhaseWindow(net.PHASE_WINDOW_GAME, self)
		ui.ScriptWindow.__del__(self)

	def Open(self):
		app.SetFrameSkip(1)

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())

		self.quickSlotPageIndex = 0
		self.PickingCharacterIndex = -1
		self.PickingItemIndex = -1
		self.consoleEnable = FALSE
		self.isShowDebugInfo = FALSE
		self.ShowNameFlag = FALSE

		self.enableXMasBoom = FALSE
		self.startTimeXMasBoom = 0.0
		self.indexXMasBoom = 0

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight

		app.SetCamera(cameraDistance, cameraPitch, cameraRotation, cameraHeight)

		constInfo.SET_DEFAULT_CAMERA_MAX_DISTANCE()
		constInfo.SET_DEFAULT_CHRNAME_COLOR()
		constInfo.SET_DEFAULT_FOG_LEVEL()
		constInfo.SET_DEFAULT_CONVERT_EMPIRE_LANGUAGE_ENABLE()
		constInfo.SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS()
		constInfo.SET_DEFAULT_USE_SKILL_EFFECT_ENABLE()
		constInfo.SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE()

		event.SetLeftTimeString(localeInfo.UI_LEFT_TIME)

		textTail.EnablePKTitle(constInfo.PVPMODE_ENABLE)

		if constInfo.PVPMODE_TEST_ENABLE:
			self.testPKMode = ui.TextLine()
			self.testPKMode.SetFontName(localeInfo.UI_DEF_FONT)
			self.testPKMode.SetPosition(0, 15)
			self.testPKMode.SetWindowHorizontalAlignCenter()
			self.testPKMode.SetHorizontalAlignCenter()
			self.testPKMode.SetFeather()
			self.testPKMode.SetOutline()
			self.testPKMode.Show()

			self.testAlignment = ui.TextLine()
			self.testAlignment.SetFontName(localeInfo.UI_DEF_FONT)
			self.testAlignment.SetPosition(0, 35)
			self.testAlignment.SetWindowHorizontalAlignCenter()
			self.testAlignment.SetHorizontalAlignCenter()
			self.testAlignment.SetFeather()
			self.testAlignment.SetOutline()
			self.testAlignment.Show()

		self.__BuildKeyDict()
		self.__BuildDebugInfo()

		uiPrivateShopBuilder.Clear()

		exchange.InitTrading()

		if app.ENABLE_RENEWAL_REGEN:
			player.LoadNewRegen()

		if debugInfo.IsDebugMode():
			self.ToggleDebugInfo()

		snd.SetMusicVolume(systemSetting.GetMusicVolume()*net.GetFieldMusicVolume())
		snd.SetSoundVolume(systemSetting.GetSoundVolume())

		netFieldMusicFileName = net.GetFieldMusicFileName()
		if netFieldMusicFileName:
			snd.FadeInMusic("BGM/" + netFieldMusicFileName)
		elif musicInfo.fieldMusic != "":
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

		self.__SetQuickSlotMode()
		self.__SelectQuickPage(self.quickSlotPageIndex)

		self.SetFocus()
		self.Show()
		app.ShowCursor()

		net.SendEnterGamePacket()

		if app.ENABLE_SHIP_DEFENCE_DUNGEON:
			if background.GetCurrentMapName() == "defensawe_hydra":
				self.__ShipMastHPShow()

		# START_GAME_ERROR_EXIT
		try:
			self.StartGame()
		except:
			import exception
			exception.Abort("GameWindow.Open")
		# END_OF_START_GAME_ERROR_EXIT

		self.cubeInformation = {}
		self.currentCubeNPC = 0

		if app.ENABLE_FOG_FIX:
			if systemSetting.IsFogMode():
				background.SetEnvironmentFog(TRUE)
			else:
				background.SetEnvironmentFog(FALSE)

	def Close(self):
		self.Hide()

		if app.ENABLE_MULTI_FARM_BLOCK:
			app.SetMultiFarmExeIcon(1)

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight
		(cameraDistance, cameraPitch, cameraRotation, cameraHeight) = app.GetCamera()

		if musicInfo.fieldMusic != "":
			snd.FadeOutMusic("BGM/"+ musicInfo.fieldMusic)

		self.onPressKeyDict = None
		self.onClickKeyDict = None

		chat.Close()
		snd.StopAllSound()
		grp.InitScreenEffect()
		chr.Destroy()
		textTail.Clear()
		quest.Clear()
		background.Destroy()
		guild.Destroy()
		messenger.Destroy()
		skill.ClearSkillData()
		wndMgr.Unlock()

		if app.ENABLE_RENEWAL_OFFLINESHOP:
			uiOfflineShopBuilder.Clear()
			shop.Clear()

		mouseModule.mouseController.DeattachObject()

		if self.guildWarQuestionDialog:
			self.guildWarQuestionDialog.Close()

		self.partyRequestQuestionDialog = None
		self.partyInviteQuestionDialog = None
		self.guildInviteQuestionDialog = None
		self.guildWarQuestionDialog = None
		self.messengerAddFriendQuestion = None

		self.itemDropQuestionDialog = None

		self.confirmDialog = None

		self.PrintCoord = None
		self.FrameRate = None
		self.Pitch = None
		self.Splat = None
		self.TextureNum = None
		self.ObjectNum = None
		self.ViewDistance = None
		self.PrintMousePos = None

		self.ClearDictionary()

		self.playerGauge = None
		self.mapNameShower = None
		self.affectShower = None

		if self.console:
			self.console.BindGameClass(0)
			self.console.Close()
			self.console = None

		if self.targetBoard:
			self.targetBoard.Destroy()
			self.targetBoard = None


		if app.ENABLE_SPIRIT_STONE_READING:
			if self.ruhtasi:
				self.ruhtasi.Destroy()
				self.ruhtasi = None

		if app.ENABLE_SKILL_BOOK_READING:
			if self.bkoku:
				self.bkoku.Destroy()
				self.bkoku = None

		if self.interface:
			self.interface.HideAllWindows()
			self.interface.Close()
			self.interface = None

		if app.ENABLE_MAINTENANCE_SYSTEM:
			if self.wndMaintenance.IsShow():
				self.wndMaintenance.Hide()

		if app.ENABLE_SHIP_DEFENCE_DUNGEON:
			if self.wndShipMastHP:
				self.wndShipMastHP.Close()
				self.wndShipMastHP = 0

		player.ClearSkillDict()
		player.ResetCameraRotation()

		self.KillFocus()
		app.HideCursor()

		print "---------------------------------------------------------------------------- CLOSE GAME WINDOW"

	if app.ENABLE_SPIRIT_STONE_READING:
		def ruhcac(self):
			self.ruhtasi.Show()

	if app.ENABLE_SKILL_BOOK_READING:
		def bkac(self):
			self.bkoku.Show()

	def __BuildKeyDict(self):
		onPressKeyDict = {}

		onPressKeyDict[app.DIK_1]	= lambda : self.__PressNumKey(1)
		onPressKeyDict[app.DIK_2]	= lambda : self.__PressNumKey(2)
		onPressKeyDict[app.DIK_3]	= lambda : self.__PressNumKey(3)
		onPressKeyDict[app.DIK_4]	= lambda : self.__PressNumKey(4)
		onPressKeyDict[app.DIK_5]	= lambda : self.__PressNumKey(5)
		onPressKeyDict[app.DIK_6]	= lambda : self.__PressNumKey(6)
		onPressKeyDict[app.DIK_7]	= lambda : self.__PressNumKey(7)
		onPressKeyDict[app.DIK_8]	= lambda : self.__PressNumKey(8)
		onPressKeyDict[app.DIK_9]	= lambda : self.__PressNumKey(9)
		onPressKeyDict[app.DIK_F1]	= lambda : self.__PressQuickSlot(4)
		onPressKeyDict[app.DIK_F2]	= lambda : self.__PressQuickSlot(5)
		onPressKeyDict[app.DIK_F3]	= lambda : self.__PressQuickSlot(6)
		onPressKeyDict[app.DIK_F4]	= lambda : self.__PressQuickSlot(7)

		if app.ENABLE_RENEWAL_SWITCHBOT:
			onPressKeyDict[app.DIK_F5]	= lambda : self.interface.ToggleSwitchbotWindow()

		if app.ENABLE_DUNGEON_TRACKING_SYSTEM:
			onPressKeyDict[app.DIK_F6]	= lambda : self.interface.OpenTrackWindow()

		if app.ENABLE_BIOLOG_SYSTEM:
			onPressKeyDict[app.DIK_F7]	= lambda : biologmgr.SendPacket(net.BIOLOG_MANAGER_OPEN)

		if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
			onPressKeyDict[app.DIK_F8]	= lambda : self.interface.OpenWarpWindow()

		if app.ENABLE_OFFLINESHOP_SEARCH_SYSTEM:
			onPressKeyDict[app.DIK_F9]	= lambda : self.interface.OpenPrivateShopSearch(0)

		if app.ENABLE_RENEWAL_BATTLE_PASS:
			onPressKeyDict[app.DIK_F10]	= lambda : self.interface.ToggleBattlePassExtended()

		if app.ENABLE_SPECIAL_INVENTORY:
			onPressKeyDict[app.DIK_K]	= lambda : self.interface.ToggleSpecialInventoryWindow()

		if app.__AUTO_HUNT__:
			onPressKeyDict[app.DIK_O]	= lambda : self.interface.OpenAutoHunt()

		if app.ENABLE_AUTO_SELL_SYSTEM:
			onPressKeyDict[app.DIK_U] = lambda : self.interface.ToggleAutoSellWindow()

		onPressKeyDict[app.DIK_LALT]		= lambda : self.ShowName()
		onPressKeyDict[app.DIK_LCONTROL]	= lambda : self.ShowMouseImage()
		onPressKeyDict[app.DIK_SYSRQ]		= lambda : self.SaveScreen()
		onPressKeyDict[app.DIK_SPACE]		= lambda : self.StartAttack()

		onPressKeyDict[app.DIK_UP]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_DOWN]		= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_LEFT]		= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_RIGHT]		= lambda : self.MoveRight()
		onPressKeyDict[app.DIK_W]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_S]			= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_A]			= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_D]			= lambda : self.MoveRight()

		onPressKeyDict[app.DIK_E]			= lambda: app.RotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_R]			= lambda: app.ZoomCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_T]			= lambda: app.PitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_G]			= self.__PressGKey
		onPressKeyDict[app.DIK_Q]			= self.__PressQKey

		onPressKeyDict[app.DIK_NUMPAD9]		= lambda: app.MovieResetCamera()
		onPressKeyDict[app.DIK_NUMPAD4]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD6]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_PGUP]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_PGDN]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_NUMPAD8]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD2]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_GRAVE]		= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_Z]			= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_C]			= lambda state = "STATUS": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_V]			= lambda state = "SKILL": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_N]			= lambda state = "QUEST": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_I]			= lambda : self.interface.ToggleInventoryWindow()
		if app.ENABLE_GROWTH_PET_SYSTEM:
			onPressKeyDict[app.DIK_P]		= lambda : self.interface.TogglePetInformationWindow()
		onPressKeyDict[app.DIK_M]			= lambda : self.interface.PressMKey()
		onPressKeyDict[app.DIK_ADD]			= lambda : self.interface.MiniMapScaleUp()
		onPressKeyDict[app.DIK_SUBTRACT]	= lambda : self.interface.MiniMapScaleDown()
		onPressKeyDict[app.DIK_L]			= lambda : self.interface.ToggleChatLogWindow()
		onPressKeyDict[app.DIK_COMMA]		= lambda : self.ShowConsole()
		onPressKeyDict[app.DIK_LSHIFT]		= lambda : self.__SetQuickPageMode()

		onPressKeyDict[app.DIK_J]			= lambda : self.__PressJKey()
		onPressKeyDict[app.DIK_H]			= lambda : self.__PressHKey()
		onPressKeyDict[app.DIK_B]			= lambda : self.__PressBKey()
		onPressKeyDict[app.DIK_F]			= lambda : self.__PressFKey()

		self.onPressKeyDict = onPressKeyDict

		onClickKeyDict = {}
		onClickKeyDict[app.DIK_UP] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_DOWN] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_LEFT] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_RIGHT] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_SPACE] = lambda : self.EndAttack()

		onClickKeyDict[app.DIK_W] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_S] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_A] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_D] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_Q] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_E] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_R] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_F] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_T] = lambda: app.PitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_G] = lambda: self.__ReleaseGKey()
		onClickKeyDict[app.DIK_NUMPAD4] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD6] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGUP] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGDN] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD8] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD2] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_LALT] = lambda: self.HideName()
		onClickKeyDict[app.DIK_LCONTROL] = lambda: self.HideMouseImage()
		onClickKeyDict[app.DIK_LSHIFT] = lambda: self.__SetQuickSlotMode()

		#if app.ENABLE_GUILDRENEWAL_SYSTEM:
		#	onClickKeyDict[app.DIK_TAB] = lambda: self.__PressTabKey()

		self.onClickKeyDict=onClickKeyDict

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def __PressTabKey(self):
			self.interface.OpenGuildScoreWindow()

	def __PressNumKey(self,num):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			
			if num >= 1 and num <= 9:
				if(chrmgr.IsPossibleEmoticon(-1)):
					chrmgr.SetEmoticon(-1,int(num)-1)
					net.SendEmoticon(int(num)-1)
		else:
			if num >= 1 and num <= 4:
				self.pressNumber(num-1)

	def __ClickBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			return
		else:
			if constInfo.PVPMODE_ACCELKEY_ENABLE:
				self.ChangePKMode()


	def	__PressJKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if player.IsMountingHorse():
				net.SendChatPacket("/unmount")
			else:
				if not uiPrivateShopBuilder.IsBuildingPrivateShop():
					for i in xrange(player.INVENTORY_PAGE_SIZE):
						if player.GetItemIndex(i) in (71114, 71116, 71118, 71120):
							net.SendItemUsePacket(i)
							break
	def	__PressHKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_ride")

	def	__PressBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_back")
		else:
			state = "EMOTICON"
			self.interface.ToggleCharacterWindow(state)

	def	__PressFKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_feed")	
		else:
			app.ZoomCamera(app.CAMERA_TO_POSITIVE)

	def __PressGKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/ride")	
		else:
			if self.ShowNameFlag:
				self.interface.ToggleGuildWindow()
			else:
				app.PitchCamera(app.CAMERA_TO_POSITIVE)

	def	__ReleaseGKey(self):
		app.PitchCamera(app.CAMERA_STOP)

	def __PressQKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if 0==interfaceModule.IsQBHide:
				interfaceModule.IsQBHide = 1
				self.interface.HideAllQuestButton()
			else:
				interfaceModule.IsQBHide = 0
				self.interface.ShowAllQuestButton()
		else:
			app.RotateCamera(app.CAMERA_TO_NEGATIVE)

	def __SetQuickSlotMode(self):
		self.pressNumber=ui.__mem_func__(self.__PressQuickSlot)

	def __SetQuickPageMode(self):
		self.pressNumber=ui.__mem_func__(self.__SelectQuickPage)

	def __PressQuickSlot(self, localSlotIndex):
		if app.ENABLE_GROWTH_PET_SYSTEM:
			result = player.CanUseGrowthPetQuickSlot(localSlotIndex)

			if player.QUICK_SLOT_POS_ERROR == result:
				return
			elif result in [player.QUICK_SLOT_ITEM_USE_SUCCESS, player.QUICK_SLOT_IS_NOT_ITEM, player.QUICK_SLOT_PET_ITEM_USE_SUCCESS]:
				player.RequestUseLocalQuickSlot(localSlotIndex)
			elif player.QUICK_SLOT_PET_ITEM_USE_FAILED == result:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_SUMMON_BECAUSE_LIFE_TIME_END)
			elif player.QUICK_SLOT_CAN_NOT_USE_PET_ITEM == result:
				return
		else:
			player.RequestUseLocalQuickSlot(localSlotIndex)

	if constInfo.ENABLE_EXPANDED_TASKBAR:
		def __PressExpandedTaskbar(self):
			self.interface.PressExpandedTaskbar()

	def __SelectQuickPage(self, pageIndex):
		self.quickSlotPageIndex = pageIndex
		player.SetQuickPage(pageIndex)

	def ToggleDebugInfo(self):
		self.isShowDebugInfo = not self.isShowDebugInfo

		if self.isShowDebugInfo:
			self.PrintCoord.Show()
			self.FrameRate.Show()
			self.Pitch.Show()
			self.Splat.Show()
			self.TextureNum.Show()
			self.ObjectNum.Show()
			self.ViewDistance.Show()
			self.PrintMousePos.Show()
		else:
			self.PrintCoord.Hide()
			self.FrameRate.Hide()
			self.Pitch.Hide()
			self.Splat.Hide()
			self.TextureNum.Hide()
			self.ObjectNum.Hide()
			self.ViewDistance.Hide()
			self.PrintMousePos.Hide()

	def __BuildDebugInfo(self):
		self.PrintCoord = ui.TextLine()
		self.PrintCoord.SetFontName(localeInfo.UI_DEF_FONT)
		self.PrintCoord.SetPosition(wndMgr.GetScreenWidth() - 270, 0)

		self.FrameRate = ui.TextLine()
		self.FrameRate.SetFontName(localeInfo.UI_DEF_FONT)
		self.FrameRate.SetPosition(wndMgr.GetScreenWidth() - 270, 20)

		self.Pitch = ui.TextLine()
		self.Pitch.SetFontName(localeInfo.UI_DEF_FONT)
		self.Pitch.SetPosition(wndMgr.GetScreenWidth() - 270, 40)

		self.Splat = ui.TextLine()
		self.Splat.SetFontName(localeInfo.UI_DEF_FONT)
		self.Splat.SetPosition(wndMgr.GetScreenWidth() - 270, 60)

		self.PrintMousePos = ui.TextLine()
		self.PrintMousePos.SetFontName(localeInfo.UI_DEF_FONT)
		self.PrintMousePos.SetPosition(wndMgr.GetScreenWidth() - 270, 80)

		self.TextureNum = ui.TextLine()
		self.TextureNum.SetFontName(localeInfo.UI_DEF_FONT)
		self.TextureNum.SetPosition(wndMgr.GetScreenWidth() - 270, 100)

		self.ObjectNum = ui.TextLine()
		self.ObjectNum.SetFontName(localeInfo.UI_DEF_FONT)
		self.ObjectNum.SetPosition(wndMgr.GetScreenWidth() - 270, 120)

		self.ViewDistance = ui.TextLine()
		self.ViewDistance.SetFontName(localeInfo.UI_DEF_FONT)
		self.ViewDistance.SetPosition(0, 0)

	def __NotifyError(self, msg):
		chat.AppendChat(chat.CHAT_TYPE_INFO, msg)

	def ChangePKMode(self):

		if not app.IsPressed(app.DIK_LCONTROL):
			return

		if player.GetStatus(player.LEVEL)<constInfo.PVPMODE_PROTECTED_LEVEL:
			self.__NotifyError(localeInfo.OPTION_PVPMODE_PROTECT % (constInfo.PVPMODE_PROTECTED_LEVEL))
			return

		curTime = app.GetTime()
		if curTime - self.lastPKModeSendedTime < constInfo.PVPMODE_ACCELKEY_DELAY:
			return

		self.lastPKModeSendedTime = curTime

		curPKMode = player.GetPKMode()
		nextPKMode = curPKMode + 1
		if nextPKMode == player.PK_MODE_PROTECT:
			if 0 == player.GetGuildID():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_CANNOT_SET_GUILD_MODE)
				nextPKMode = 0
			else:
				nextPKMode = player.PK_MODE_GUILD

		elif nextPKMode == player.PK_MODE_MAX_NUM:
			nextPKMode = 0

		net.SendChatPacket("/PKMode " + str(nextPKMode))
		print "/PKMode " + str(nextPKMode)

	def OnChangePKMode(self):

		self.interface.OnChangePKMode()

		try:
			self.__NotifyError(localeInfo.OPTION_PVPMODE_MESSAGE_DICT[player.GetPKMode()])
		except KeyError:
			print "UNKNOWN PVPMode[%d]" % (player.GetPKMode())

		if constInfo.PVPMODE_TEST_ENABLE:
			curPKMode = player.GetPKMode()
			alignment, grade = chr.testGetPKData()
			self.pkModeNameDict = { 0 : "PEACE", 1 : "REVENGE", 2 : "FREE", 3 : "PROTECT", }
			self.testPKMode.SetText("Current PK Mode : " + self.pkModeNameDict.get(curPKMode, "UNKNOWN"))
			self.testAlignment.SetText("Current Alignment : " + str(alignment) + " (" + localeInfo.TITLE_NAME_LIST[grade] + ")")

	def StartGame(self):
		self.RefreshInventory()
		self.RefreshEquipment()
		self.RefreshCharacter()
		self.RefreshSkill()

		if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
			systemSetting.SetSnowModeOption(systemSetting.GetSnowModeOption())
			systemSetting.SetSnowTextureModeOption(systemSetting.GetSnowTextureModeOption())

	def CheckGameButton(self):
		if self.interface:
			self.interface.CheckGameButton()

	def RefreshAlignment(self):
		self.interface.RefreshAlignment()

	def RefreshStatus(self):
		self.CheckGameButton()

		if self.interface:
			self.interface.RefreshStatus()

		if self.playerGauge:
			self.playerGauge.RefreshGauge()

	def RefreshStamina(self):
		self.interface.RefreshStamina()

	def RefreshSkill(self):
		self.CheckGameButton()
		if self.interface:
			self.interface.RefreshSkill()

	def RefreshQuest(self):
		self.interface.RefreshQuest()

	def RefreshMessenger(self):
		self.interface.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.interface.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.interface.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.interface.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.interface.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.interface.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.interface.RefreshGuildGradePage()

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def RefreshGuildBaseInfoPage(self):
			self.interface.RefreshGuildBaseInfoPage()

		def RefreshGuildBaseInfoPageBankGold(self):
			self.interface.RefreshGuildBaseInfoPageBankGold()

		def RefreshGuildWarInfoPage(self):
			self.interface.RefreshGuildWarInfoPage()

	def OnBlockMode(self, mode):
		self.interface.OnBlockMode(mode)

	def OpenQuestWindow(self, skin, idx):
		if constInfo.INPUT_IGNORE == 1:
			return
		self.interface.OpenQuestWindow(skin, idx)

	def PopupMessage(self, msg):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, 0, localeInfo.UI_OK)

	def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type=0):
		self.interface.OpenRefineDialog(targetItemPos, nextGradeItemVnum, cost, prob, type)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.interface.AppendMaterialToRefineDialog(vnum, count)

	def RunUseSkillEvent(self, slotIndex, coolTime):
		self.interface.OnUseSkill(slotIndex, coolTime)

	def ClearAffects(self):
		self.affectShower.ClearAffects()

	def SetAffect(self, affect):
		self.affectShower.SetAffect(affect)

	def ResetAffect(self, affect):
		self.affectShower.ResetAffect(affect)

	def BINARY_NEW_AddAffect(self, type, pointIdx, value, duration):
		self.affectShower.BINARY_NEW_AddAffect(type, pointIdx, value, duration)

		if app.__AUTO_HUNT__:
			if constInfo.autoHuntAutoLoginDict["status"] == 1 and constInfo.autoHuntAutoLoginDict["leftTime"] == -2:
				constInfo.autoHuntAutoLoginDict["leftTime"] = app.GetGlobalTimeStamp() + 2

		if app.ENABLE_AUTOMATIC_PICK_UP_SYSTEM:
			if chr.NEW_AFFECT_AUTO_PICK_UP == type:
				constInfo.PREMIUMMODE = [TRUE, app.GetGlobalTimeStamp() + int(duration)]
				self.interface.OnChangePickUPMode()

	def BINARY_NEW_RemoveAffect(self, type, pointIdx):
		self.affectShower.BINARY_NEW_RemoveAffect(type, pointIdx)

		if app.ENABLE_AUTOMATIC_PICK_UP_SYSTEM:
			if chr.NEW_AFFECT_AUTO_PICK_UP == type:
				constInfo.PREMIUMMODE = [FALSE, 0]
				self.interface.OnChangePickUPMode()

		if app.__AUTO_HUNT__:
			if type == chr.NEW_AFFECT_AUTO_HUNT:
				net.SendChatPacket("/auto_hunt end")

	def BINARY_OpenInGameEvent(self):
		self.interface.OpenInGameEvent()

	def BINARY_CloseInGameEvent(self):
		self.interface.CloseInGameEvent()

	def ActivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnActivateSkill(slotIndex)

	def DeactivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnDeactivateSkill(slotIndex)

	def RefreshEquipment(self):
		if self.interface:
			self.interface.RefreshInventory()

	def RefreshInventory(self):
		if self.interface:
			self.interface.RefreshInventory()

	def RefreshCharacter(self):
		if self.interface:
			self.interface.RefreshCharacter()

	if app.ENABLE_RENEWAL_DEAD_PACKET:
		def OnGameOver(self, d_time):
			self.CloseTargetBoard()
			self.OpenRestartDialog(d_time)

		def OpenRestartDialog(self, d_time):
			self.interface.OpenRestartDialog(d_time)
	else:
		def OnGameOver(self):
			self.CloseTargetBoard()
			self.OpenRestartDialog()

		def OpenRestartDialog(self):
			self.interface.OpenRestartDialog()

	def ChangeCurrentSkill(self, skillSlotNumber):
		self.interface.OnChangeCurrentSkill(skillSlotNumber)

	def SetPCTargetBoard(self, vid, name):
		self.targetBoard.Open(vid, name)
		
		if app.IsPressed(app.DIK_LCONTROL):
			
			if not player.IsSameEmpire(vid):
				return

			if player.IsMainCharacterIndex(vid):
				return		
			elif chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(vid):
				return

			self.interface.OpenWhisperDialog(name)
			

	def RefreshTargetBoardByVID(self, vid):
		self.targetBoard.RefreshByVID(vid)

	def RefreshTargetBoardByName(self, name):
		self.targetBoard.RefreshByName(name)
		
	def __RefreshTargetBoard(self):
		self.targetBoard.Refresh()

	if app.ENABLE_VIEW_TARGET_DECIMAL_HP:
		def SetHPTargetBoard(self, vid, hpPercentage, iMinHP, iMaxHP):
			if vid != self.targetBoard.GetTargetVID():
				self.targetBoard.ResetTargetBoard()
				self.targetBoard.SetEnemyVID(vid)
			
			self.targetBoard.SetHP(hpPercentage, iMinHP, iMaxHP)
			self.targetBoard.Show()
	else:
		def SetHPTargetBoard(self, vid, hpPercentage):
			if vid != self.targetBoard.GetTargetVID():
				self.targetBoard.ResetTargetBoard()
				self.targetBoard.SetEnemyVID(vid)

			self.targetBoard.SetHP(hpPercentage)
			self.targetBoard.Show()

	def CloseTargetBoardIfDifferent(self, vid):
		if vid != self.targetBoard.GetTargetVID():
			self.targetBoard.Close()

	def CloseTargetBoard(self):
		self.targetBoard.Close()

	def OpenEquipmentDialog(self, vid):
		self.interface.OpenEquipmentDialog(vid)

	if app.ENABLE_CHANGE_LOOK_SYSTEM:
		def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count, dwChangeLookVnum):
			self.interface.SetEquipmentDialogItem(vid, slotIndex, vnum, count, dwChangeLookVnum)
	else:
		def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
			self.interface.SetEquipmentDialogItem(vid, slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		self.interface.SetEquipmentDialogSocket(vid, slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		self.interface.SetEquipmentDialogAttr(vid, slotIndex, attrIndex, type, value)

	def ShowMapName(self, mapName, x, y):
		if self.mapNameShower:
			self.mapNameShower.ShowMapName(mapName, x, y)

		if self.interface:
			self.interface.SetMapName(mapName)

	def BINARY_OpenAtlasWindow(self):
		self.interface.BINARY_OpenAtlasWindow()

	def OnRecvWhisper(self, mode, name, line):
		if mode == chat.WHISPER_TYPE_GM:
			self.interface.RegisterGameMasterName(name)
		chat.AppendWhisper(mode, name, line)
		self.interface.RecvWhisper(name)

	def OnRecvWhisperSystemMessage(self, mode, name, line):
		chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, line)
		self.interface.RecvWhisper(name)

	def OnRecvWhisperError(self, mode, name, line):
		if localeInfo.WHISPER_ERROR.has_key(mode):
			chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, localeInfo.WHISPER_ERROR[mode](name))
		else:
			chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, "Whisper Unknown Error(mode=%d, name=%s)" % (mode, name))
		self.interface.RecvWhisper(name)

	def RecvWhisper(self, name):
		self.interface.RecvWhisper(name)

	def OnPickMoney(self, money):
		if app.ENABLE_RENEWAL_SPECIAL_CHAT:
			self.interface.SpecialChatOnPick(money, 0)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_PICK_MONEY % (money))

	if app.ENABLE_SPECIAL_INVENTORY:
		def OpenSpecialInventoryWindow(self, category):
			self.interface.OpenSpecialInventoryWindow(int(category))

	def OnShopError(self, type):
		try:
			self.PopupMessage(localeInfo.SHOP_ERROR_DICT[type])
		except KeyError:
			self.PopupMessage(localeInfo.SHOP_ERROR_UNKNOWN % (type))

	def OnSafeBoxError(self):
		self.PopupMessage(localeInfo.SAFEBOX_ERROR)

	def OnFishingSuccess(self, isFish, fishName):
		chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeInfo.FISHING_SUCCESS(isFish, fishName), 2000)

	# ADD_FISHING_MESSAGE
	def OnFishingNotifyUnknown(self):
		# chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_UNKNOWN)
		self.noticeBox = ui.NoticeBoxBoard(localeInfo.FISHING_UNKNOWN)

	def OnFishingWrongPlace(self):
		# chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_WRONG_PLACE)
		self.noticeBox = ui.NoticeBoxBoard(localeInfo.FISHING_WRONG_PLACE)
	# END_OF_ADD_FISHING_MESSAGE

	def OnFishingNotify(self, isFish, fishName):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_NOTIFY(isFish, fishName))

	def OnFishingFailure(self):
		chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeInfo.FISHING_FAILURE, 2000)

	def OnCannotPickItem(self):
		# chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_PICK_ITEM)
		self.noticeBox = ui.NoticeBoxBoard(localeInfo.GAME_CANNOT_PICK_ITEM)

	# MINING
	def OnCannotMining(self):
		# chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_MINING)
		self.noticeBox = ui.NoticeBoxBoard(localeInfo.GAME_CANNOT_MINING)
	# END_OF_MINING

	def OnCannotUseSkill(self, vid, type):
		if localeInfo.USE_SKILL_ERROR_TAIL_DICT.has_key(type):
			# textTail.RegisterInfoTail(vid, localeInfo.USE_SKILL_ERROR_TAIL_DICT[type])
			self.noticeBox = ui.NoticeBoxBoard(localeInfo.USE_SKILL_ERROR_TAIL_DICT[type])
		if localeInfo.USE_SKILL_ERROR_CHAT_DICT.has_key(type):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_SKILL_ERROR_CHAT_DICT[type])
			self.noticeBox = ui.NoticeBoxBoard(localeInfo.USE_SKILL_ERROR_CHAT_DICT[type])

	def	OnCannotShotError(self, vid, type):
		# textTail.RegisterInfoTail(vid, localeInfo.SHOT_ERROR_TAIL_DICT.get(type, localeInfo.SHOT_ERROR_UNKNOWN % (type)))
		msg = localeInfo.SHOT_ERROR_TAIL_DICT.get(type, localeInfo.SHOT_ERROR_UNKNOWN % (type))
		self.noticeBox = ui.NoticeBoxBoard(msg)

	def StartPointReset(self):
		self.interface.OpenPointResetDialog()

	def StartShop(self, vid):
		self.interface.OpenShopDialog(vid)

	def EndShop(self):
		self.interface.CloseShopDialog()

	def RefreshShop(self):
		self.interface.RefreshShopDialog()

	def SetShopSellingPrice(self, Price):
		pass

	def StartExchange(self):
		self.interface.StartExchange()

	def EndExchange(self):
		self.interface.EndExchange()

	def RefreshExchange(self):
		self.interface.RefreshExchange()

	def RecvPartyInviteQuestion(self, leaderVID, leaderName):
		partyInviteQuestionDialog = uiCommon.QuestionDialogWithTimeLimit2()
		partyInviteQuestionDialog.SetText1(leaderName + localeInfo.PARTY_DO_YOU_JOIN)
		partyInviteQuestionDialog.SetTimeOverMsg(localeInfo.PARTY_ANSWER_TIMEOVER)
		partyInviteQuestionDialog.SetTimeOverEvent(self.AnswerPartyInvite, FALSE)
		partyInviteQuestionDialog.SetAcceptEvent(lambda arg=TRUE: self.AnswerPartyInvite(arg))
		partyInviteQuestionDialog.SetCancelEvent(lambda arg=FALSE: self.AnswerPartyInvite(arg))
		partyInviteQuestionDialog.Open(10)
		partyInviteQuestionDialog.partyLeaderVID = leaderVID
		self.partyInviteQuestionDialog = partyInviteQuestionDialog

	def AnswerPartyInvite(self, answer):

		if not self.partyInviteQuestionDialog:
			return

		partyLeaderVID = self.partyInviteQuestionDialog.partyLeaderVID

		distance = player.GetCharacterDistance(partyLeaderVID)
		if distance < 0.0 or distance > 5000:
			answer = FALSE

		net.SendPartyInviteAnswerPacket(partyLeaderVID, answer)

		self.partyInviteQuestionDialog.Close()
		self.partyInviteQuestionDialog = None

	def AddPartyMember(self, pid, name):
		self.interface.AddPartyMember(pid, name)

	def UpdatePartyMemberInfo(self, pid):
		self.interface.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.interface.RemovePartyMember(pid)
		self.__RefreshTargetBoard()

	def LinkPartyMember(self, pid, vid):
		self.interface.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.interface.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.interface.UnlinkAllPartyMember()

	def ExitParty(self):
		self.interface.ExitParty()
		self.RefreshTargetBoardByVID(self.targetBoard.GetTargetVID())

	def ChangePartyParameter(self, distributionMode):
		self.interface.ChangePartyParameter(distributionMode)

	def OnMessengerAddFriendQuestion(self, name):
		messengerAddFriendQuestion = uiCommon.QuestionDialogWithTimeLimit2()
		messengerAddFriendQuestion.SetText1(localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND % (name))
		messengerAddFriendQuestion.SetTimeOverMsg(localeInfo.MESSENGER_ADD_FRIEND_ANSWER_TIMEOVER)
		messengerAddFriendQuestion.SetTimeOverEvent(self.OnDenyAddFriend)
		messengerAddFriendQuestion.SetAcceptEvent(ui.__mem_func__(self.OnAcceptAddFriend))
		messengerAddFriendQuestion.SetCancelEvent(ui.__mem_func__(self.OnDenyAddFriend))
		messengerAddFriendQuestion.Open(10)
		messengerAddFriendQuestion.name = name
		self.messengerAddFriendQuestion = messengerAddFriendQuestion

	def OnAcceptAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		net.SendChatPacket("/messenger_auth y " + name)
		self.OnCloseAddFriendQuestionDialog()
		return TRUE

	def OnDenyAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		net.SendChatPacket("/messenger_auth n " + name)
		self.OnCloseAddFriendQuestionDialog()
		return TRUE

	def OnCloseAddFriendQuestionDialog(self):
		self.messengerAddFriendQuestion.Close()
		self.messengerAddFriendQuestion = None
		return TRUE

	def OpenSafeboxWindow(self, size):
		self.interface.OpenSafeboxWindow(size)

	def RefreshSafebox(self):
		self.interface.RefreshSafebox()

	def RefreshSafeboxMoney(self):
		self.interface.RefreshSafeboxMoney()

	# ITEM_MALL
	def OpenMallWindow(self, size):
		self.interface.OpenMallWindow(size)

	def RefreshMall(self):
		self.interface.RefreshMall()
	# END_OF_ITEM_MALL

	## Guild
	if app.ENABLE_GUILDBANK_LOG:
		def OpenGuildBankInfo(self):
			self.interface.OpenGuildBankInfo()

		def GuildBankLogInfoRefresh(self):
			self.interface.GuildBankLogInfoRefresh()

	if app.ENABLE_GUILDRENEWAL_SYSTEM and app.ENABLE_GUILD_DONATE_ATTENDANCE:
		def GuildDonateInfoRefresh(self):
			self.interface.GuildDonateInfoRefresh()

	def RecvGuildInviteQuestion(self, guildID, guildName):
		guildInviteQuestionDialog = uiCommon.QuestionDialog()
		guildInviteQuestionDialog.SetText(guildName + localeInfo.GUILD_DO_YOU_JOIN)
		guildInviteQuestionDialog.SetAcceptEvent(lambda arg=TRUE: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.SetCancelEvent(lambda arg=FALSE: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.Open()
		guildInviteQuestionDialog.guildID = guildID
		self.guildInviteQuestionDialog = guildInviteQuestionDialog

	def AnswerGuildInvite(self, answer):
		if not self.guildInviteQuestionDialog:
			return

		guildLeaderVID = self.guildInviteQuestionDialog.guildID
		net.SendGuildInviteAnswerPacket(guildLeaderVID, answer)

		self.guildInviteQuestionDialog.Close()
		self.guildInviteQuestionDialog = None


	def DeleteGuild(self):
		self.interface.DeleteGuild()

	# if app.ENABLE_GUILDRENEWAL_SYSTEM:
		# def SetGuildWarType(self, index):
			# self.interface.SetGuildWarType(index)

		# def OpenGuildBankWindow(self, size):
			# self.interface.OpenGuildBankWindow(size)

		# def OpenGuildGoldInOutWindow(self, inout):
			# self.interface.OpenGuildGoldInOutWindow(inout)

		# def RefreshGuildBank(self):
			# self.interface.RefreshGuildBank()

		# def RefreshGuildBankInfo(self):
			# self.interface.RefreshGuildBankInfo()

		# def OpenGuildBankInfo(self):
			# self.interface.OpenGuildBankInfo()

	## Clock
	def ShowClock(self, second):
		self.interface.ShowClock(second)

	def HideClock(self):
		self.interface.HideClock()

	## Emotion
	def BINARY_ActEmotion(self, emotionIndex):
		if self.interface.wndCharacter:
			self.interface.wndCharacter.ActEmotion(emotionIndex)

	def CheckFocus(self):
		if FALSE == self.IsFocus():
			if TRUE == self.interface.IsOpenChat():
				self.interface.ToggleChat()

			self.SetFocus()

	def SaveScreen(self):
		print "save screen"

		if SCREENSHOT_CWDSAVE:
			if not os.path.exists(os.getcwd()+os.sep+"screenshot"):
				os.mkdir(os.getcwd()+os.sep+"screenshot")

			(succeeded, name) = grp.SaveScreenShotToPath(os.getcwd()+os.sep+"screenshot"+os.sep)
		elif SCREENSHOT_DIR:
			(succeeded, name) = grp.SaveScreenShot(SCREENSHOT_DIR)
		else:
			(succeeded, name) = grp.SaveScreenShot()

		if succeeded:
			pass
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SCREENSHOT_SAVE_FAILURE)

	def ShowConsole(self):
		if debugInfo.IsDebugMode() or TRUE == self.consoleEnable:
			player.EndKeyWalkingImmediately()
			self.console.OpenWindow()

	def ShowName(self):
		self.ShowNameFlag = TRUE
		self.playerGauge.EnableShowAlways()
		player.SetQuickPage(self.quickSlotPageIndex+1)

	def __IsShowName(self):

		if systemSetting.IsAlwaysShowName():
			return TRUE

		if self.ShowNameFlag:
			return TRUE

		return FALSE

	def HideName(self):
		self.ShowNameFlag = FALSE
		self.playerGauge.DisableShowAlways()
		player.SetQuickPage(self.quickSlotPageIndex)

	def ShowMouseImage(self):
		self.interface.ShowMouseImage()

	def HideMouseImage(self):
		self.interface.HideMouseImage()

	def StartAttack(self):
		player.SetAttackKeyState(TRUE)

	def EndAttack(self):
		player.SetAttackKeyState(FALSE)

	def MoveUp(self):
		player.SetSingleDIKKeyState(app.DIK_UP, TRUE)

	def MoveDown(self):
		player.SetSingleDIKKeyState(app.DIK_DOWN, TRUE)

	def MoveLeft(self):
		player.SetSingleDIKKeyState(app.DIK_LEFT, TRUE)

	def MoveRight(self):
		player.SetSingleDIKKeyState(app.DIK_RIGHT, TRUE)

	def StopUp(self):
		player.SetSingleDIKKeyState(app.DIK_UP, FALSE)

	def StopDown(self):
		player.SetSingleDIKKeyState(app.DIK_DOWN, FALSE)

	def StopLeft(self):
		player.SetSingleDIKKeyState(app.DIK_LEFT, FALSE)

	def StopRight(self):
		player.SetSingleDIKKeyState(app.DIK_RIGHT, FALSE)

	def PickUpItem(self):
		if app.ENABLE_AUTOMATIC_PICK_UP_SYSTEM:
			if (constInfo.PICKUPMODE & player.AUTOMATIC_PICK_UP_ACTIVATE):
				player.PickCloseItemAutoVector()
			else:
				player.PickCloseItemVector()
		else:
			if app.ENABLE_INSTANT_PICKUP:
				player.PickCloseItemVector()
			else:
				player.PickCloseItem()

	def OnKeyDown(self, key):
		if self.interface.wndWeb and self.interface.wndWeb.IsShow():
			return

		if key == app.DIK_ESC:
			self.RequestDropItem(FALSE)
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

		try:
			self.onPressKeyDict[key]()
		except KeyError:
			pass
		except:
			raise

		return TRUE

	def OnKeyUp(self, key):
		try:
			self.onClickKeyDict[key]()
		except KeyError:
			pass
		except:
			raise

		return TRUE

	def OnMouseLeftButtonDown(self):
		if self.interface.BUILD_OnMouseLeftButtonDown():
			return

		if mouseModule.mouseController.isAttached():
			self.CheckFocus()
		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				return
			else:
				self.CheckFocus()
				player.SetMouseState(player.MBT_LEFT, player.MBS_PRESS);

		return TRUE

	def OnMouseLeftButtonUp(self):
		if self.interface.BUILD_OnMouseLeftButtonUp():
			return

		if mouseModule.mouseController.isAttached():
			attachedType = mouseModule.mouseController.GetAttachedType()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
			attachedItemSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()

			if player.SLOT_TYPE_QUICK_SLOT == attachedType:
				player.RequestDeleteGlobalQuickSlot(attachedItemSlotPos)

			elif player.SLOT_TYPE_INVENTORY == attachedType or\
				(player.SLOT_TYPE_SKILL_BOOK_INVENTORY == attachedType or\
				player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY == attachedType or\
				player.SLOT_TYPE_STONE_INVENTORY == attachedType or\
				player.SLOT_TYPE_GIFT_BOX_INVENTORY == attachedType or\
				player.SLOT_TYPE_CHANGERS_INVENTORY == attachedType and app.ENABLE_SPECIAL_INVENTORY):

				if player.ITEM_MONEY == attachedItemIndex:
					self.__PutMoney(attachedType, attachedItemCount, self.PickingCharacterIndex)
				else:
					self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			elif app.ENABLE_AURA_COSTUME_SYSTEM and player.SLOT_TYPE_AURA == attachedType:
				self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				if player.SLOT_TYPE_CHANGE_LOOK == attachedType:
					self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			mouseModule.mouseController.DeattachObject()

		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				if app.IsPressed(app.DIK_LALT):
					link = chat.GetLinkFromHyperlink(hyperlink)
					ime.PasteString(link)
				else:
					self.interface.MakeHyperlinkTooltip(hyperlink)
				return
			else:
				player.SetMouseState(player.MBT_LEFT, player.MBS_CLICK)

		return TRUE

	def __PutItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, dstChrID):
		if player.SLOT_TYPE_INVENTORY == attachedType or player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType or\
			(player.SLOT_TYPE_SKILL_BOOK_INVENTORY == attachedType or\
			player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY == attachedType or\
			player.SLOT_TYPE_STONE_INVENTORY == attachedType or\
			player.SLOT_TYPE_GIFT_BOX_INVENTORY == attachedType or\
			player.SLOT_TYPE_CHANGERS_INVENTORY == attachedType and app.ENABLE_SPECIAL_INVENTORY):

			attachedInvenType = player.SlotTypeToInvenType(attachedType)
			if TRUE == chr.HasInstance(self.PickingCharacterIndex) and player.GetMainCharacterIndex() != dstChrID:
				if player.IsEquipmentSlot(attachedItemSlotPos) and player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedType:
					self.stream.popupWindow.Close()
					self.stream.popupWindow.Open(localeInfo.EXCHANGE_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)
				else:
					if chr.IsNPC(dstChrID):
						if app.ENABLE_AUTO_REFINE:
							constInfo.AUTO_REFINE_TYPE = 2
							constInfo.AUTO_REFINE_DATA["NPC"][0] = dstChrID
							constInfo.AUTO_REFINE_DATA["NPC"][1] = attachedInvenType
							constInfo.AUTO_REFINE_DATA["NPC"][2] = attachedItemSlotPos
							constInfo.AUTO_REFINE_DATA["NPC"][3] = attachedItemCount
						net.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount)
					else:
						net.SendExchangeStartPacket(dstChrID)
						net.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
			else:
				self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)

		if app.ENABLE_AURA_COSTUME_SYSTEM:
			if player.SLOT_TYPE_AURA == attachedType:
				self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			if player.SLOT_TYPE_CHANGE_LOOK == attachedType:
				self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)

	def __PutMoney(self, attachedType, attachedMoney, dstChrID):
		if TRUE == chr.HasInstance(dstChrID) and player.GetMainCharacterIndex() != dstChrID:
			net.SendExchangeStartPacket(dstChrID)
			net.SendExchangeElkAddPacket(attachedMoney)
		else:
			self.__DropMoney(attachedType, attachedMoney)

	def __DropMoney(self, attachedType, attachedMoney):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return

		if attachedMoney>=1000:
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.DROP_MONEY_FAILURE_1000_OVER, 0, localeInfo.UI_OK)
			return

		itemDropQuestionDialog = uiCommon.QuestionDialog("thin")
		itemDropQuestionDialog.SetText(localeInfo.DO_YOU_DROP_MONEY % (attachedMoney))
		itemDropQuestionDialog.SetAcceptEvent(lambda arg=TRUE: self.RequestDropItem(arg))
		itemDropQuestionDialog.SetCancelEvent(lambda arg=FALSE: self.RequestDropItem(arg))
		itemDropQuestionDialog.Open()
		itemDropQuestionDialog.dropType = attachedType
		itemDropQuestionDialog.dropCount = attachedMoney
		itemDropQuestionDialog.dropNumber = player.ITEM_MONEY
		self.itemDropQuestionDialog = itemDropQuestionDialog

	def __DropItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return

		if player.SLOT_TYPE_INVENTORY == attachedType and player.IsEquipmentSlot(attachedItemSlotPos):
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.DROP_ITEM_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)

		else:
			if player.SLOT_TYPE_INVENTORY == attachedType or\
				(player.SLOT_TYPE_SKILL_BOOK_INVENTORY == attachedType or\
				player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY == attachedType or\
				player.SLOT_TYPE_STONE_INVENTORY == attachedType or\
				player.SLOT_TYPE_GIFT_BOX_INVENTORY == attachedType or\
				player.SLOT_TYPE_CHANGERS_INVENTORY == attachedType and app.ENABLE_SPECIAL_INVENTORY):

				dropItemIndex = player.GetItemIndex(attachedItemSlotPos)

				item.SelectItem(dropItemIndex)
				dropItemName = item.GetItemName()

				questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

				itemDropQuestionDialog = uiCommon.ItemQuestionDialog()
				itemDropQuestionDialog.SetAcceptEvent(lambda arg=TRUE: self.RequestDropItem(arg))
				itemDropQuestionDialog.SetCancelEvent(lambda arg=FALSE: self.RequestDropItem(arg))
				itemDropQuestionDialog.SetSellEvent(lambda arg=TRUE: self.RequestSellItem(arg))
				if app.ENABLE_DESTROY_DIALOG:
					itemDropQuestionDialog.SetDestroyEvent(lambda arg=TRUE: self.RequestDestroyItem(arg))
				itemDropQuestionDialog.Open(dropItemIndex, attachedItemSlotPos, 0, questionText)
				itemDropQuestionDialog.dropType = attachedType
				itemDropQuestionDialog.dropNumber = attachedItemSlotPos
				itemDropQuestionDialog.dropCount = attachedItemCount
				self.itemDropQuestionDialog = itemDropQuestionDialog

				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

			if app.ENABLE_AURA_COSTUME_SYSTEM:
				if player.SLOT_TYPE_AURA == attachedType:
					net.SendAuraRefineCheckOut(attachedItemSlotPos, player.GetAuraRefineWindowType())

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				if player.SLOT_TYPE_CHANGE_LOOK == attachedType:
					net.SendChangeLookCheckOut(attachedItemSlotPos)

	def RequestDropItem(self, answer):
		if not self.itemDropQuestionDialog:
			return

		if answer:
			dropType = self.itemDropQuestionDialog.dropType
			dropCount = self.itemDropQuestionDialog.dropCount
			dropNumber = self.itemDropQuestionDialog.dropNumber

			if player.SLOT_TYPE_INVENTORY == dropType or\
				(player.SLOT_TYPE_SKILL_BOOK_INVENTORY == dropType or\
				player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY == dropType or\
				player.SLOT_TYPE_STONE_INVENTORY == dropType or\
				player.SLOT_TYPE_GIFT_BOX_INVENTORY == dropType or\
				player.SLOT_TYPE_CHANGERS_INVENTORY == dropType and app.ENABLE_SPECIAL_INVENTORY):

				if dropNumber == player.ITEM_MONEY:
					net.SendGoldDropPacketNew(dropCount)
					snd.PlaySound("sound/ui/money.wav")
				else:
					self.__SendDropItemPacket(dropNumber, dropCount)

		self.itemDropQuestionDialog.Close()
		self.itemDropQuestionDialog = None

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	if app.ENABLE_DESTROY_DIALOG:
		def RequestDestroyItem(self, answer):
			if not self.itemDropQuestionDialog:
				return

			if answer:
				dropType = self.itemDropQuestionDialog.dropType
				dropCount = self.itemDropQuestionDialog.dropCount
				dropNumber = self.itemDropQuestionDialog.dropNumber
				self.itemDropQuestionDialog.Close()
				self.itemDropQuestionDialog = None
				questionText = localeInfo.DESTROY_ITEM_QUESTION
				itemDestroyQuestionDialog = uiCommon.QuestionDialog("thin")
				itemDestroyQuestionDialog.SetText(questionText)
				itemDestroyQuestionDialog.SetAcceptEvent(lambda arg=TRUE: self.RequestDestroyItemFinaly(arg))
				itemDestroyQuestionDialog.SetCancelEvent(lambda arg=FALSE: self.RequestDestroyItemFinaly(arg))
				itemDestroyQuestionDialog.dropType = dropType
				itemDestroyQuestionDialog.dropNumber = dropNumber
				itemDestroyQuestionDialog.dropCount = dropCount
				itemDestroyQuestionDialog.Open()
				self.itemDestroyQuestionDialog = itemDestroyQuestionDialog

		def RequestDestroyItemFinaly(self, answer):
			if not self.itemDestroyQuestionDialog:
				return

			if answer:
				dropType = self.itemDestroyQuestionDialog.dropType
				dropCount = self.itemDestroyQuestionDialog.dropCount
				dropNumber = self.itemDestroyQuestionDialog.dropNumber

				if player.SLOT_TYPE_INVENTORY == dropType or\
					(player.SLOT_TYPE_SKILL_BOOK_INVENTORY == dropType or\
					player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY == dropType or\
					player.SLOT_TYPE_STONE_INVENTORY == dropType or\
					player.SLOT_TYPE_GIFT_BOX_INVENTORY == dropType or\
					player.SLOT_TYPE_CHANGERS_INVENTORY == dropType and app.ENABLE_SPECIAL_INVENTORY):

					if dropNumber == player.ITEM_MONEY:
						return
					else:
						self.__SendDestroyItemPacket(dropNumber, dropCount)

			self.itemDestroyQuestionDialog.Close()
			self.itemDestroyQuestionDialog = None

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

		def __SendDestroyItemPacket(self, itemVNum, itemCount, itemInvenType = player.INVENTORY):
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
				return

			net.SendItemDestroyPacket(itemInvenType, itemVNum, itemCount)

	def RequestSellItem(self, answer):
		if not self.itemDropQuestionDialog:
			return

		if answer:
			dropType = self.itemDropQuestionDialog.dropType
			dropNumber = self.itemDropQuestionDialog.dropNumber
			dropCount = self.itemDropQuestionDialog.dropCount

			if player.SLOT_TYPE_INVENTORY == dropType or\
				(player.SLOT_TYPE_SKILL_BOOK_INVENTORY == dropType or\
				player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY == dropType or\
				player.SLOT_TYPE_STONE_INVENTORY == dropType or\
				player.SLOT_TYPE_GIFT_BOX_INVENTORY == dropType or\
				player.SLOT_TYPE_CHANGERS_INVENTORY == dropType and app.ENABLE_SPECIAL_INVENTORY):

				if dropNumber == player.ITEM_MONEY:
					return
				else:
					self.__SendSellItemPacket(dropNumber, dropCount)

		self.itemDropQuestionDialog.Close()
		self.itemDropQuestionDialog = None

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def __SendSellItemPacket(self, slot, count):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendShopSellPacketNew(slot, count)

	def __SendDropItemPacket(self, itemVNum, itemCount, itemInvenType = player.INVENTORY):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemDropPacketNew(itemInvenType, itemVNum, itemCount)

	def OnMouseRightButtonDown(self):

		self.CheckFocus()

		if TRUE == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		else:
			player.SetMouseState(player.MBT_RIGHT, player.MBS_PRESS)

		return TRUE

	def OnMouseRightButtonUp(self):
		if TRUE == mouseModule.mouseController.isAttached():
			return TRUE

		player.SetMouseState(player.MBT_RIGHT, player.MBS_CLICK)
		return TRUE

	def OnMouseMiddleButtonDown(self):
		player.SetMouseMiddleButtonState(player.MBS_PRESS)

	def OnMouseMiddleButtonUp(self):
		player.SetMouseMiddleButtonState(player.MBS_CLICK)

	def OnUpdate(self):
		app.UpdateGame()

		if self.mapNameShower.IsShow():
			self.mapNameShower.Update()

		if self.isShowDebugInfo:
			self.UpdateDebugInfo()

		if self.enableXMasBoom:
			self.__XMasBoom_Update()

		self.interface.BUILD_OnUpdate()

		if app.__AUTO_HUNT__:
			if constInfo.autoHuntAutoLoginDict["status"] == 1 and constInfo.autoHuntAutoLoginDict["leftTime"] > 0 and constInfo.autoHuntAutoLoginDict["leftTime"] < app.GetGlobalTimeStamp():
				constInfo.autoHuntAutoLoginDict["leftTime"] = 0
				self.interface.CheckAutoLogin()
			
			# Otomatik bineðe binme kontrolü
			if "mount_time" in constInfo.autoHuntAutoLoginDict and constInfo.autoHuntAutoLoginDict["mount_time"] > 0:
				currentTime = app.GetGlobalTimeStamp()
				if constInfo.autoHuntAutoLoginDict["mount_time"] <= currentTime:
					# Bineðe binme zamaný geldi
					# Karakter hazýr mý kontrol et (player objesi yüklenmiþ olmalý)
					try:
						if hasattr(player, 'IsMountingHorse'):
							if not player.IsMountingHorse():
								attempt = constInfo.autoHuntAutoLoginDict.get("mount_attempt", 0)
								if attempt < 15:  # Maksimum 15 deneme (daha fazla þans)
									# Binek için /ride komutunu gönder (CTRL + G ile ayný)
									# Karakter tam yüklendi mi kontrol et
									try:
										# Karakter pozisyonunu kontrol et (yüklenmiþse pozisyon alýnabilir)
										(x, y, z) = player.GetMainCharacterPosition()
										# Pozisyon alýnabiliyorsa karakter yüklenmiþ demektir
										net.SendChatPacket("/ride")
									except:
										# Karakter henüz yüklenmemiþ, bir sonraki frame'de tekrar dene
										pass
									# Deneme sayacýný artýr
									constInfo.autoHuntAutoLoginDict["mount_attempt"] = attempt + 1
									# Bir sonraki deneme için 2 saniye bekle (daha uzun gecikme)
									constInfo.autoHuntAutoLoginDict["mount_time"] = currentTime + 2
								else:
									# 10 denemeden sonra durdur
									constInfo.autoHuntAutoLoginDict["mount_time"] = 0
									constInfo.autoHuntAutoLoginDict["mount_attempt"] = 0
							else:
								# Zaten bineðe binmiþ, kontrolü sýfýrla
								constInfo.autoHuntAutoLoginDict["mount_time"] = 0
								constInfo.autoHuntAutoLoginDict["mount_attempt"] = 0
								if "mount_retry_time" in constInfo.autoHuntAutoLoginDict:
									constInfo.autoHuntAutoLoginDict["mount_retry_time"] = 0
					except:
						# Hata durumunda da kontrolü sýfýrla
						constInfo.autoHuntAutoLoginDict["mount_time"] = 0
						constInfo.autoHuntAutoLoginDict["mount_attempt"] = 0

		# Tooltip kontrolü: Sadece haritadaki item tooltip'lerinin ekranda kalmasýný önle
		# Envanter, shop gibi pencerelerdeki tooltip'leri etkilemez
		try:
			import uiToolTip
			
			# Interface üzerinden tooltip'e eriþ
			tooltipItem = None
			if self.interface and hasattr(self.interface, 'tooltipItem'):
				tooltipItem = self.interface.tooltipItem
			
			# Eðer interface'den bulamadýysak, global tooltipItem'i kontrol et
			if not tooltipItem and hasattr(uiToolTip, 'tooltipItem'):
				tooltipItem = uiToolTip.tooltipItem
			
			if tooltipItem and tooltipItem.IsShow():
				# Fare pozisyonunu al
				try:
					(x, y) = app.GetCursorPosition()
				except:
					try:
						(x, y) = wndMgr.GetMousePosition()
					except:
						return
				
				# Açýk pencerelerin üzerinde mi kontrol et
				onWindow = False
				onDungeonTimer = False
				if self.interface:
					# Tüm açýk pencereleri kontrol et (dungeon timer hariç - o haritada da açýk olabilir)
					windows_to_check = [
						'wndInventory', 'wndSafebox', 'wndMall', 'wndCube',
						'dlgShop', 'dlgExchange', 'wndItemSelect',
						'wndCharacter', 'wndTaskBar', 'wndGuild', 'wndMessenger',
						'wndMiniMap', 'wndGameButton', 'wndChat',
					]
					
					for attr_name in windows_to_check:
						if hasattr(self.interface, attr_name):
							window = getattr(self.interface, attr_name, None)
							if window and hasattr(window, 'IsShow') and window.IsShow():
								try:
									(wx, wy) = window.GetGlobalPosition()
									ww, wh = window.GetWidth(), window.GetHeight()
									if wx <= x <= wx + ww and wy <= y <= wy + wh:
										onWindow = True
										break
								except:
									pass
					
					# Dungeon timer'ý ayrý kontrol et (haritada da açýk olabilir)
					if hasattr(self.interface, 'wndDungeonTimer'):
						dungeonTimer = getattr(self.interface, 'wndDungeonTimer', None)
						if dungeonTimer and hasattr(dungeonTimer, 'IsShow') and dungeonTimer.IsShow():
							try:
								(dx, dy) = dungeonTimer.GetGlobalPosition()
								dw, dh = dungeonTimer.GetWidth(), dungeonTimer.GetHeight()
								if dx <= x <= dx + dw and dy <= y <= dy + dh:
									onDungeonTimer = True
							except:
								pass
				
				# Eðer hiçbir pencere açýk deðilse (yani haritadayýz) ve tooltip açýksa
				# Veya dungeon timer açýk ama fare üzerinde deðilse
				if not onWindow:
					# Tooltip'in pozisyonunu al
					try:
						(tx, ty) = tooltipItem.GetGlobalPosition()
						tw, th = tooltipItem.GetWidth(), tooltipItem.GetHeight()
						onTooltip = (tx <= x <= tx + tw and ty <= y <= ty + th)
						
						# Fare tooltip'in üzerinde deðilse kapat
						# Dungeon timer açýk olsa bile, fare tooltip'in üzerinde deðilse kapat
						if not onTooltip:
							# Eðer dungeon timer açýksa ve fare üzerindeyse, tooltip'i kapatma
							if onDungeonTimer:
								pass  # Dungeon timer üzerindeyse tooltip'i açýk býrak
							else:
								tooltipItem.HideToolTip()
					except:
						# Hata durumunda tooltip'i kapat
						try:
							tooltipItem.HideToolTip()
						except:
							pass
		except:
			pass

	def UpdateDebugInfo(self):
		(x, y, z) = player.GetMainCharacterPosition()
		nUpdateTime = app.GetUpdateTime()
		nUpdateFPS = app.GetUpdateFPS()
		nRenderFPS = app.GetRenderFPS()
		nFaceCount = app.GetFaceCount()
		fFaceSpeed = app.GetFaceSpeed()
		nST=background.GetRenderShadowTime()
		(fAveRT, nCurRT) =  app.GetRenderTime()
		(iNum, fFogStart, fFogEnd, fFarCilp) = background.GetDistanceSetInfo()
		(iPatch, iSplat, fSplatRatio, sTextureNum) = background.GetRenderedSplatNum()
		if iPatch == 0:
			iPatch = 1

		self.PrintCoord.SetText("Coordinate: %.2f %.2f %.2f ATM: %d" % (x, y, z, app.GetAvailableTextureMemory()/(1024*1024)))
		xMouse, yMouse = wndMgr.GetMousePosition()
		self.PrintMousePos.SetText("MousePosition: %d %d" % (xMouse, yMouse))

		self.FrameRate.SetText("UFPS: %3d UT: %3d FS %.2f" % (nUpdateFPS, nUpdateTime, fFaceSpeed))

		if fAveRT>1.0:
			self.Pitch.SetText("RFPS: %3d RT:%.2f(%3d) FC: %d(%.2f) " % (nRenderFPS, fAveRT, nCurRT, nFaceCount, nFaceCount/fAveRT))

		self.Splat.SetText("PATCH: %d SPLAT: %d BAD(%.2f)" % (iPatch, iSplat, fSplatRatio))
		self.ViewDistance.SetText("Num : %d, FS : %f, FE : %f, FC : %f" % (iNum, fFogStart, fFogEnd, fFarCilp))

	def OnRender(self):
		app.RenderGame()
		
		if self.console.Console.collision:
			background.RenderCollision()
			chr.RenderCollision()

		(x, y) = app.GetCursorPosition()

		textTail.UpdateAllTextTail()

		if TRUE == wndMgr.IsPickedWindow(self.hWnd):

			self.PickingCharacterIndex = chr.Pick()

			if -1 != self.PickingCharacterIndex:
				textTail.ShowCharacterTextTail(self.PickingCharacterIndex)
			if 0 != self.targetBoard.GetTargetVID():
				textTail.ShowCharacterTextTail(self.targetBoard.GetTargetVID())

			if not self.__IsShowName():
				self.PickingItemIndex = item.Pick()
				if -1 != self.PickingItemIndex:
					textTail.ShowItemTextTail(self.PickingItemIndex)

		if self.__IsShowName():
			textTail.ShowAllTextTail()
			self.PickingItemIndex = textTail.Pick(x, y)

		if app.ENABLE_GRAPHIC_ON_OFF:
			if systemSetting.IsShowSalesText():
				uiPrivateShopBuilder.UpdateADBoard()

		textTail.UpdateShowingTextTail()
		textTail.ArrangeTextTail()
		if -1 != self.PickingItemIndex:
			textTail.SelectItemName(self.PickingItemIndex)

		grp.PopState()
		grp.SetInterfaceRenderState()

		textTail.Render()
		textTail.HideAllTextTail()

	def OnPressEscapeKey(self):
		if app.TARGET == app.GetCursor():
			app.SetCursor(app.NORMAL)

		elif TRUE == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		else:
			self.interface.OpenSystemDialog()

		return TRUE

	def OnIMEReturn(self):
		if app.IsPressed(app.DIK_LSHIFT):
			self.interface.OpenWhisperDialogWithoutTarget()
		else:
			self.interface.ToggleChat()
		return TRUE

	def OnPressExitKey(self):
		self.interface.ToggleSystemDialog()
		return TRUE

	def BINARY_LoverInfo(self, name, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnAddLover(name, lovePoint)
		if self.affectShower:
			self.affectShower.SetLoverInfo(name, lovePoint)

	def BINARY_UpdateLovePoint(self, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnUpdateLovePoint(lovePoint)
		if self.affectShower:
			self.affectShower.OnUpdateLovePoint(lovePoint)

	if app.ENABLE_MOB_DROP_INFO:
		def BINARY_AddTargetMonsterDropInfo(self, raceNum, itemVnum, itemCount):
			if not raceNum in uiTarget.MONSTER_INFO_DATA:
				uiTarget.MONSTER_INFO_DATA.update({raceNum : {}})
				uiTarget.MONSTER_INFO_DATA[raceNum].update({"items" : []})
			curList = uiTarget.MONSTER_INFO_DATA[raceNum]["items"]

			isUpgradeable = FALSE
			isMetin = FALSE
			item.SelectItem(itemVnum)
			if item.GetItemType() == item.ITEM_TYPE_WEAPON or item.GetItemType() == item.ITEM_TYPE_ARMOR:
				isUpgradeable = TRUE
			elif item.GetItemType() == item.ITEM_TYPE_METIN:
				isMetin = TRUE

			for curItem in curList:
				if isUpgradeable:
					if curItem.has_key("vnum_list") and curItem["vnum_list"][0] / 10 * 10 == itemVnum / 10 * 10:
						if not (itemVnum in curItem["vnum_list"]):
							curItem["vnum_list"].append(itemVnum)
						return
				elif isMetin:
					if curItem.has_key("vnum_list"):
						baseVnum = curItem["vnum_list"][0]
					if curItem.has_key("vnum_list") and (baseVnum - baseVnum%1000) == (itemVnum - itemVnum%1000):
						if not (itemVnum in curItem["vnum_list"]):
							curItem["vnum_list"].append(itemVnum)
						return
				else:
					if curItem.has_key("vnum") and curItem["vnum"] == itemVnum and curItem["count"] == itemCount:
						return

			if isUpgradeable or isMetin:
				curList.append({"vnum_list":[itemVnum], "count":itemCount})
			else:
				curList.append({"vnum":itemVnum, "count":itemCount})

		def BINARY_RefreshTargetMonsterDropInfo(self, raceNum):
			self.targetBoard.RefreshMonsterInfoBoard()

	def BINARY_OnQuestConfirm(self, msg, timeout, pid):
		confirmDialog = uiCommon.QuestionDialogWithTimeLimit2()
		confirmDialog.SetText1(msg)
		confirmDialog.SetAcceptEvent(lambda answer=TRUE, pid=pid: net.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
		confirmDialog.SetCancelEvent(lambda answer=FALSE, pid=pid: net.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
		confirmDialog.Open(timeout)
		self.confirmDialog = confirmDialog

	def Gift_Show(self):
		self.interface.ShowGift()

	def BINARY_Cube_Open(self, npcVNUM):
		self.currentCubeNPC = npcVNUM
		self.interface.OpenCubeWindow()

		if npcVNUM not in self.cubeInformation:
			net.SendChatPacket("/cube r_info")
		else:
			cubeInfoList = self.cubeInformation[npcVNUM]

			i = 0
			for cubeInfo in cubeInfoList:
				self.interface.wndCube.AddCubeResultItem(cubeInfo["vnum"], cubeInfo["count"])

				j = 0
				for materialList in cubeInfo["materialList"]:
					for materialInfo in materialList:
						itemVnum, itemCount = materialInfo
						self.interface.wndCube.AddMaterialInfo(i, j, itemVnum, itemCount)
					j = j + 1

				i = i + 1

			self.interface.wndCube.Refresh()

	def BINARY_Cube_Close(self):
		self.interface.CloseCubeWindow()

	def BINARY_Cube_UpdateInfo(self, gold, itemVnum, count):
		self.interface.UpdateCubeInfo(gold, itemVnum, count)
		
	def BINARY_Cube_Succeed(self, itemVnum, count):
		print "Å¥ºê Á¦ÀÛ ¼º°ø"
		self.interface.SucceedCubeWork(itemVnum, count)
		pass

	def BINARY_Cube_Failed(self):
		print "Å¥ºê Á¦ÀÛ ½ÇÆ?"
		self.interface.FailedCubeWork()
		pass

	def BINARY_Cube_ResultList(self, npcVNUM, listText):
		if npcVNUM == 0:
			npcVNUM = self.currentCubeNPC
		
		self.cubeInformation[npcVNUM] = []
		
		try:
			for eachInfoText in listText.split("/"):
				eachInfo = eachInfoText.split(",")
				itemVnum	= int(eachInfo[0])
				itemCount	= int(eachInfo[1])

				self.cubeInformation[npcVNUM].append({"vnum": itemVnum, "count": itemCount})
				self.interface.wndCube.AddCubeResultItem(itemVnum, itemCount)
			
			resultCount = len(self.cubeInformation[npcVNUM])
			requestCount = 7
			modCount = resultCount % requestCount
			splitCount = resultCount / requestCount
			for i in xrange(splitCount):
				net.SendChatPacket("/cube r_info %d %d" % (i * requestCount, requestCount))
				
			if 0 < modCount:
				net.SendChatPacket("/cube r_info %d %d" % (splitCount * requestCount, modCount))

		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0
			
		pass
		
	def BINARY_Cube_MaterialInfo(self, startIndex, listCount, listText):
		try:
			if 3 > len(listText):
				dbg.TraceError("Wrong Cube Material Infomation")
				return 0

			eachResultList = listText.split("@")

			cubeInfo = self.cubeInformation[self.currentCubeNPC]

			itemIndex = 0
			for eachResultText in eachResultList:
				cubeInfo[startIndex + itemIndex]["materialList"] = [[], [], [], [], []]
				materialList = cubeInfo[startIndex + itemIndex]["materialList"]
				
				gold = 0
				splitResult = eachResultText.split("/")
				if 1 < len(splitResult):
					gold = int(splitResult[1])

				eachMaterialList = splitResult[0].split("&")

				i = 0
				for eachMaterialText in eachMaterialList:
					complicatedList = eachMaterialText.split("|")
					
					if 0 < len(complicatedList):
						for complicatedText in complicatedList:
							(itemVnum, itemCount) = complicatedText.split(",")
							itemVnum = int(itemVnum)
							itemCount = int(itemCount)
							self.interface.wndCube.AddMaterialInfo(itemIndex + startIndex, i, itemVnum, itemCount)

							materialList[i].append((itemVnum, itemCount))

					else:
						itemVnum, itemCount = eachMaterialText.split(",")
						itemVnum = int(itemVnum)
						itemCount = int(itemCount)
						self.interface.wndCube.AddMaterialInfo(itemIndex + startIndex, i, itemVnum, itemCount)

						materialList[i].append((itemVnum, itemCount))

					i = i + 1

				itemIndex = itemIndex + 1

			self.interface.wndCube.Refresh()

		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

		pass

	def BINARY_Highlight_Item(self, inven_type, inven_pos):
		if self.interface:
			self.interface.Highligt_Item(inven_type, inven_pos)

	def BINARY_SetBigMessage(self, message):
		self.interface.bigBoard.SetTip(message)

	def BINARY_SetTipMessage(self, message):
		self.interface.tipBoard.SetTip(message)

	if app.ENABLE_RENEWAL_OX_EVENT:
		def BINARY_SetBigControlMessage(self, message):
			self.interface.bigBoardControl.SetTip(message)

	if app.ENABLE_EXTENDED_WHISPER_DETAILS and app.ENABLE_MULTI_LANGUAGE_SYSTEM:
		def BINARY_RecieveWhisperDetails(self, name, country):
			if self.interface:
				self.interface.RecieveWhisperDetails(name, country)

	def BINARY_AppendNotifyMessage(self, type):
		if not type in localeInfo.NOTIFY_MESSAGE:
			return
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.NOTIFY_MESSAGE[type])

	def BINARY_Guild_EnterGuildArea(self, areaID):
		self.interface.BULID_EnterGuildArea(areaID)

	def BINARY_Guild_ExitGuildArea(self, areaID):
		self.interface.BULID_ExitGuildArea(areaID)

	def BINARY_GuildWar_OnSendDeclare(self, guildID):
		pass

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def BINARY_GuildWar_OnRecvDeclare(self, guildID, warType, winType, ScoreType, TimeType):
			mainCharacterName = player.GetMainCharacterName()
			masterName = guild.GetGuildMasterName()
			if mainCharacterName == masterName:
				self.__GuildWar_OpenAskDialog(guildID, warType, winType, ScoreType, TimeType)

		def BINARY_GuildWar_OnRecvPoint(self, gainGuildID, opponentGuildID, point, winpoint):
			self.interface.OnRecvGuildWarPoint(gainGuildID, opponentGuildID, point, winpoint)
	else:
		def BINARY_GuildWar_OnRecvDeclare(self, guildID, warType):
			mainCharacterName = player.GetMainCharacterName()
			masterName = guild.GetGuildMasterName()
			if mainCharacterName == masterName:
				self.__GuildWar_OpenAskDialog(guildID, warType)

		def BINARY_GuildWar_OnRecvPoint(self, gainGuildID, opponentGuildID, point):
			self.interface.OnRecvGuildWarPoint(gainGuildID, opponentGuildID, point)

	def BINARY_GuildWar_OnStart(self, guildSelf, guildOpp):
		self.interface.OnStartGuildWar(guildSelf, guildOpp)

	def BINARY_GuildWar_OnEnd(self, guildSelf, guildOpp):
		self.interface.OnEndGuildWar(guildSelf, guildOpp)
		if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
			if self.guildWarQuestionDialog:
				self.__GuildWar_CloseAskDialog()

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def BINARY_BettingGuildWar_SetObserverMode(self, isEnable,isButtonShow):
			self.interface.BINARY_SetObserverMode(isEnable,isButtonShow)
	else:
		def BINARY_BettingGuildWar_SetObserverMode(self, isEnable):
			self.interface.BINARY_SetObserverMode(isEnable)

	def BINARY_BettingGuildWar_UpdateObserverCount(self, observerCount):
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	def __GuildWar_UpdateMemberCount(self, guildID1, memberCount1, guildID2, memberCount2, observerCount):
		guildID1 = int(guildID1)
		guildID2 = int(guildID2)
		memberCount1 = int(memberCount1)
		memberCount2 = int(memberCount2)
		observerCount = int(observerCount)

		self.interface.UpdateMemberCount(guildID1, memberCount1, guildID2, memberCount2)
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def __GuildWar_OpenAskDialog(self, guildID, warType, winType, ScoreType, TimeType):
			guildName = guild.GetGuildName(guildID)

			# REMOVED_GUILD_BUG_FIX
			if "Noname" == guildName:
				return
			# END_OF_REMOVED_GUILD_BUG_FIX

			import uiGuild
			questionDialog = uiGuild.AcceptGuildWarDialog()
			questionDialog.SAFE_SetAcceptEvent(self.__GuildWar_OnAccept)
			questionDialog.SAFE_SetCancelEvent(self.__GuildWar_OnDecline)
			## [guild_renewal_war]
			questionDialog.Open(guildName, warType, winType, ScoreType, TimeType)

			self.guildWarQuestionDialog = questionDialog
	else:
		def __GuildWar_OpenAskDialog(self, guildID, warType):
			guildName = guild.GetGuildName(guildID)

			# REMOVED_GUILD_BUG_FIX
			if "Noname" == guildName:
				return
			# END_OF_REMOVED_GUILD_BUG_FIX

			import uiGuild
			questionDialog = uiGuild.AcceptGuildWarDialog()
			questionDialog.SAFE_SetAcceptEvent(self.__GuildWar_OnAccept)
			questionDialog.SAFE_SetCancelEvent(self.__GuildWar_OnDecline)
			questionDialog.Open(guildName, warType)

			self.guildWarQuestionDialog = questionDialog

	def __GuildWar_CloseAskDialog(self):
		self.guildWarQuestionDialog.Close()
		self.guildWarQuestionDialog = None

	def __GuildWar_OnAccept(self):

		guildName = self.guildWarQuestionDialog.GetGuildName()

		net.SendChatPacket("/war " + guildName)
		self.__GuildWar_CloseAskDialog()

		return 1

	def __GuildWar_OnDecline(self):

		guildName = self.guildWarQuestionDialog.GetGuildName()

		net.SendChatPacket("/nowar " + guildName)
		self.__GuildWar_CloseAskDialog()

		return 1

	def __ServerCommand_Build(self):
		serverCommandList={
			"ConsoleEnable"									: self.__Console_Enable,
			"DayMode"										: self.__DayMode_Update,
			"PRESERVE_DayMode"								: self.__PRESERVE_DayMode_Update,
			"CloseRestartWindow"							: self.__RestartDialog_Close,
			"OpenPrivateShop"								: self.__PrivateShop_Open,
			"PartyHealReady"								: self.PartyHealReady,
			"ShowMeSafeboxPassword"							: self.AskSafeboxPassword,
			"CloseSafebox"									: self.CommandCloseSafebox,

			"CloseMall"										: self.CommandCloseMall,
			"ShowMeMallPassword"							: self.AskMallPassword,
			"item_mall"										: self.__ItemMall_Open,

			"RefineSuceeded"								: self.RefineSuceededMessage,
			"RefineFailed"									: self.RefineFailedMessage,
			"xmas_snow"										: self.__XMasSnow_Enable,
			"xmas_boom"										: self.__XMasBoom_Enable,
			"xmas_song"										: self.__XMasSong_Enable,
			"xmas_tree"										: self.__XMasTree_Enable,
			"newyear_boom"									: self.__XMasBoom_Enable,
			"PartyRequest"									: self.__PartyRequestQuestion,
			"PartyRequestDenied"							: self.__PartyRequestDenied,
			"horse_state"									: self.__Horse_UpdateState,
			"hide_horse_state"								: self.__Horse_HideState,
			"WarUC"											: self.__GuildWar_UpdateMemberCount,
			"test_server"									: self.__EnableTestServerFlag,
			"mall"											: self.__InGameShop_Show,

			"lover_login"									: self.__LoginLover,
			"lover_logout"									: self.__LogoutLover,
			"lover_near"									: self.__LoverNear,
			"lover_far"										: self.__LoverFar,
			"lover_divorce"									: self.__LoverDivorce,
			"PlayMusic"										: self.__PlayMusic,

			"MyShopPriceList"								: self.__PrivateShop_PriceList,

			"getinputbegin"									: self.GetInputBegin,
			"getinputend"									: self.GetInputEnd,
			"getinput"										: self.GetInput,
		}

		if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM and app.ENABLE_GUILD_REQUEST:
			serverCommandList["clear_guildranking"] = self.__ClearGuildRanking
			serverCommandList["clear_applicant"] = self.__ClearApplicant
			serverCommandList["clear_applicantguild"] = self.__ClearApplicantGuild

		if app.ENABLE_SPIRIT_STONE_READING:
			serverCommandList["ruhtasiekranac"] = self.ruhcac

		if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
			serverCommandList["guild_war"] = self.__Check_Guild_War

		if app.ENABLE_SKILL_BOOK_READING:
			serverCommandList["bkekranac"] = self.bkac

		if app.ENABLE_AUTO_SELL_SYSTEM:
			serverCommandList["addAutoSellInfo"] = self.interface.wndAutoSell.AddItem
			serverCommandList["autosell_status"] = self.interface.wndAutoSell.SetMod

		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			serverCommandList.update({
				"SetBodyCostumeHidden"						: self.SetBodyCostumeHidden,
				"SetHairCostumeHidden"						: self.SetHairCostumeHidden,
			})

			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				serverCommandList.update({
					"SetAcceCostumeHidden"					: self.SetAcceCostumeHidden,
				})

			if app.ENABLE_WEAPON_COSTUME_SYSTEM:
				serverCommandList.update({
					"SetWeaponCostumeHidden"				: self.SetWeaponCostumeHidden,
				})

			if app.ENABLE_AURA_COSTUME_SYSTEM:
				serverCommandList.update({
					"SetAuraCostumeHidden"					: self.SetAuraCostumeHidden,
				})

		if app.ENABLE_SPECIAL_INVENTORY:
			serverCommandList.update({
				"OpenSpecialInventoryWindow"				: self.OpenSpecialInventoryWindow,
				"CloseLoadSafeboxEvent"						: self.__CloseLoadSafeboxEvent,
				"CloseLoadMallEvent"						: self.__CloseLoadMallEvent,
			})

		if app.ENABLE_ANTI_EXP:
			serverCommandList.update({
				"SetAntiExp"								: self.SetAntiExp,
			})

		if app.ENABLE_MULTI_FARM_BLOCK:
			serverCommandList.update({
				"UpdateMultiFarmAffect"						: self.UpdateMultiFarmAffect,
				"UpdateMultiFarmPlayer"						: self.UpdateMultiFarmPlayer,
			})

		if app.ENABLE_RENEWAL_OFFLINESHOP:
			serverCommandList.update({
				"OpenBackAllItem"							: self.OpenBackAllItem,
				"OpenOfflineShop"							: self.OpenOfflineShop,
				"RefreshOfflineShop"						: self.RefreshOfflineShop,
				"OpenOfflineShopPanel"						: self.OpenOfflineShopPanel,
				"ClearOfflineShopLog"						: self.ClearOfflineShopLog,
				"AppendShopLog"								: self.AppendShopLog,
				"OfflineShopSellMsg"						: self.interface.AddOfflineShopMessage,
			})

		if app.ENABLE_OFFLINESHOP_SEARCH_SYSTEM:
			serverCommandList.update({
				"OfflineShopBuyed"							: self.interface.OfflineShopBuyed,
			})

		if app.ENABLE_AUTOMATIC_PICK_UP_SYSTEM:
			serverCommandList.update({
				"PickUPMode"								: self.__PickUPMode,
			})

		if app.ENABLE_MAINTENANCE_SYSTEM:
			serverCommandList.update({
				"BINARY_Update_Maintenance"					: self.BINARY_Update_Maintenance,
			})

		if app.ENABLE_NEW_DUNGEON_LIB:
			serverCommandList.update({
				"RefreshDungeonFloor"						: self.RefreshDungeonFloor,
				"RefreshDungeonTimer"						: self.RefreshDungeonTimer,
			})

		if app.ENABLE_RENEWAL_INGAME_ITEMSHOP:
			serverCommandList.update({
				"SetWheelItemData"							: self.interface.SetWheelItemData,
				"OnSetWhell"								: self.interface.OnSetWhell,
				"GetWheelGiftData"							: self.interface.GetWheelGiftData,
				"SetDragonCoin"								: self.ItemShopSetDragonCoin,
				"ItemShopAppendLog"							: self.ItemShopAppendLogEx,
			})

		if app.ENABLE_FISH_GAME:
			serverCommandList.update({
				"OpenFishGameWindow"						: self.interface.OpenFishGameWindow,
				"SetFishGameGoal"							: self.interface.SetFishGameGoal,
				"CloseFishGame"								: self.interface.CloseFishGame,
			})

		if app.ENABLE_INVENTORY_EXPANSION_SYSTEM:
			serverCommandList.update({
				"ManagerInventoryUnlock"					: self.ManagerInventoryUnlock,
			})

		if app.ENABLE_SHIP_DEFENCE_DUNGEON:
			serverCommandList.update({
				"gethydrahp"								: self.__HydraGetHp,
			})

		if app.ENABLE_DUNGEON_TRACKING_SYSTEM:
			serverCommandList.update({
				"TrackDungeonInfo"							: self.interface.TrackDungeonInfo,
				"TrackBossInfo"								: self.interface.TrackBossInfo,
			})

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			serverCommandList.update({
				"ShowChangeDialog"							: self.__ChangeWindowOpen,
			})

		if app.ENABLE_HUNTING_SYSTEM:
			serverCommandList.update({
				"HuntingButtonFlash"						: self.SetHuntingButtonFlash,
			})

		if app.__AUTO_HUNT__:
			serverCommandList.update({"AutoHuntStatus" : self.interface.AutoHuntStatus})

		self.serverCommander = stringCommander.Analyzer()
		for serverCommandItem in serverCommandList.items():
			self.serverCommander.SAFE_RegisterCallBack(serverCommandItem[0], serverCommandItem[1])

		if app.ENABLE_TELEPORT_TO_A_FRIEND:
			self.serverCommander.SAFE_RegisterCallBack("RequestWarpToCharacter", self.RequestWarpToCharacter)

		if app.ENABLE_RENEWAL_SKILL_SELECT:
			self.serverCommander.SAFE_RegisterCallBack("RenewalSkillSelectWindow", self.__RenewalSkillSelectWindow)

	if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
		def __Check_Guild_War(self, enable):
			if self.interface:
				if int(enable) == 1:
					self.interface.ShowGuildWarButton()
				else:
					self.interface.HideGuildWarButton()

	if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM and app.ENABLE_GUILD_REQUEST:
		def __ClearGuildRanking(self):
			guild.ClearGuildRanking()

		def __ClearApplicant(self):
			guild.ClearApplicant()

		def __ClearApplicantGuild(self):
			guild.ClearApplicantGuild()

	if app.ENABLE_RENEWAL_CUBE:
		def BINARY_CUBE_RENEWAL_OPEN(self):
			if self.interface:
				self.interface.BINARY_CUBE_RENEWAL_OPEN()

	def BINARY_ServerCommand_Run(self, line):
		try:
			return self.serverCommander.Run(line)
		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

	def __ProcessPreservedServerCommand(self):
		try:
			command = net.GetPreservedServerCommand()
			while command:
				print " __ProcessPreservedServerCommand", command
				self.serverCommander.Run(command)
				command = net.GetPreservedServerCommand()
		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

	def GetInputBegin(self):
		constInfo.INPUT_IGNORE = 1

	def GetInputEnd(self):
		constInfo.INPUT_IGNORE = 0

	def GetInput(self):
		net.SendQuestInputStringPacket("1")

	def PartyHealReady(self):
		self.interface.PartyHealReady()

	if app.ENABLE_GUILD_RANK_SYSTEM:
		def BINARY_GUILD_RANK_OPEN(self):
			self.interface.OpenGuildRanking()

	def AskSafeboxPassword(self):
		self.interface.AskSafeboxPassword()

	def AskMallPassword(self):
		self.interface.AskMallPassword()

	def __ItemMall_Open(self):
		self.interface.OpenItemMall();

	def CommandCloseMall(self):
		self.interface.CommandCloseMall()

	def RefineSuceededMessage(self):
		snd.PlaySound("sound/ui/make_soket.wav")
		self.PopupMessage(localeInfo.REFINE_SUCCESS)
		if app.ENABLE_AUTO_REFINE:
			self.interface.CheckRefineDialog(FALSE)

	def RefineFailedMessage(self):
		snd.PlaySound("sound/ui/jaeryun_fail.wav")
		self.PopupMessage(localeInfo.REFINE_FAILURE)
		if app.ENABLE_AUTO_REFINE:
			self.interface.CheckRefineDialog(TRUE)

	def CommandCloseSafebox(self):
		self.interface.CommandCloseSafebox()

	def __PrivateShop_PriceList(self, itemVNum, itemPrice):
		uiPrivateShopBuilder.SetPrivateShopItemPrice(itemVNum, itemPrice)

	def __Horse_HideState(self):
		self.affectShower.SetHorseState(0, 0, 0)

	def __Horse_UpdateState(self, level, health, battery):
		self.affectShower.SetHorseState(int(level), int(health), int(battery))

	def __IsXMasMap(self):
		mapDict = (
			"metin2_map_n_flame_01",
			"metin2_map_n_desert_01",
			"metin2_map_spiderdungeon_01",
			"metin2_map_spiderdungeon_02",
			"metin2_map_spiderdungeon_03",
			"metin2_map_deviltower1",
			"metin2_map_empirewar03",
			"metin2_map_devilsCatacomb",
			"metin2_map_Mt_Thunder",
			"metin2_map_n_flame_dungeon_01",
			"metin2_map_dawnmist_dungeon_01",
			"metin2_map_Mt_Th_dungeon_01",
		)

		if background.GetCurrentMapName() in mapDict:
			return FALSE

		return TRUE

	def __XMasSnow_Enable(self, mode):
		self.__XMasSong_Enable(mode)

		if "1" == mode:
			if not self.__IsXMasMap():
				return
			background.EnableSnow(1)
		else:
			background.EnableSnow(0)

	def __XMasBoom_Enable(self, mode):
		if "1" == mode:
			if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
				if not background.IsBoomMap():
					return
			else:
				if not self.__IsXMasMap():
					return

			self.__DayMode_Update("dark")
			self.enableXMasBoom = TRUE
			self.startTimeXMasBoom = app.GetTime()
		else:
			self.__DayMode_Update("light")
			self.enableXMasBoom = FALSE

	def __XMasTree_Enable(self, grade):
		background.SetXMasTree(int(grade))

	def __XMasSong_Enable(self, mode):
		if "1" == mode:
			XMAS_BGM = "xmas.mp3"
			if app.IsExistFile("BGM/" + XMAS_BGM)==1:
				if musicInfo.fieldMusic != "":
					snd.FadeOutMusic("BGM/" + musicInfo.fieldMusic)

				musicInfo.fieldMusic=XMAS_BGM
				snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)
		else:
			if musicInfo.fieldMusic != "":
				snd.FadeOutMusic("BGM/" + musicInfo.fieldMusic)

			musicInfo.fieldMusic=musicInfo.METIN2THEMA
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	def __RestartDialog_Close(self):
		self.interface.CloseRestartDialog()

	def __Console_Enable(self):
		constInfo.CONSOLE_ENABLE = TRUE
		self.consoleEnable = TRUE
		app.EnableSpecialCameraMode()
		ui.EnablePaste(TRUE)

	def __PrivateShop_Open(self):
		self.interface.OpenPrivateShopInputNameDialog()

	def BINARY_PrivateShop_Appear(self, vid, text):
		self.interface.AppearPrivateShop(vid, text)

	def BINARY_PrivateShop_Disappear(self, vid):
		self.interface.DisappearPrivateShop(vid)

	def __PRESERVE_DayMode_Update(self, mode):
		if "light" == mode:
			background.SetEnvironmentData(0)
		elif "dark" == mode:
			if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
				if not background.IsBoomMap():
					return
			else:
				if not self.__IsXMasMap():
					return

			background.RegisterEnvironmentData(background.DAY_MODE_DARK, constInfo.ENVIRONMENT_NIGHT)
			background.SetEnvironmentData(background.DAY_MODE_DARK)

	def __DayMode_Update(self, mode):
		if "light" == mode:
			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToLight)
		elif "dark" == mode:
			if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
				if not background.IsBoomMap():
					return
			else:
				if not self.__IsXMasMap():
					return

			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToDark)

	def __DayMode_OnCompleteChangeToLight(self):
		background.SetEnvironmentData(0)
		self.curtain.FadeIn()

	def __DayMode_OnCompleteChangeToDark(self):
		background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
		background.SetEnvironmentData(1)
		self.curtain.FadeIn()

	def __XMasBoom_Update(self):

		self.BOOM_DATA_LIST = ( (2, 5), (5, 2), (7, 3), (10, 3), (20, 5) )
		if self.indexXMasBoom >= len(self.BOOM_DATA_LIST):
			return

		boomTime = self.BOOM_DATA_LIST[self.indexXMasBoom][0]
		boomCount = self.BOOM_DATA_LIST[self.indexXMasBoom][1]

		if app.GetTime() - self.startTimeXMasBoom > boomTime:

			self.indexXMasBoom += 1

			for i in xrange(boomCount):
				self.__XMasBoom_Boom()

	def __XMasBoom_Boom(self):
		x, y, z = player.GetMainCharacterPosition()
		randX = app.GetRandom(-150, 150)
		randY = app.GetRandom(-150, 150)

		snd.PlaySound3D(x+randX, -y+randY, z, "sound/common/etc/salute.mp3")

	def __PartyRequestQuestion(self, vid):
		vid = int(vid)
		partyRequestQuestionDialog = uiCommon.QuestionDialog("thin")
		partyRequestQuestionDialog.SetText(chr.GetNameByVID(vid) + localeInfo.PARTY_DO_YOU_ACCEPT)
		partyRequestQuestionDialog.SetAcceptText(localeInfo.UI_ACCEPT)
		partyRequestQuestionDialog.SetCancelText(localeInfo.UI_DENY)
		partyRequestQuestionDialog.SetAcceptEvent(lambda arg=TRUE: self.__AnswerPartyRequest(arg))
		partyRequestQuestionDialog.SetCancelEvent(lambda arg=FALSE: self.__AnswerPartyRequest(arg))
		partyRequestQuestionDialog.Open()
		partyRequestQuestionDialog.vid = vid
		self.partyRequestQuestionDialog = partyRequestQuestionDialog

	def __AnswerPartyRequest(self, answer):
		if not self.partyRequestQuestionDialog:
			return

		vid = self.partyRequestQuestionDialog.vid

		if answer:
			net.SendChatPacket("/party_request_accept " + str(vid))
		else:
			net.SendChatPacket("/party_request_deny " + str(vid))

		self.partyRequestQuestionDialog.Close()
		self.partyRequestQuestionDialog = None

	def __PartyRequestDenied(self):
		self.PopupMessage(localeInfo.PARTY_REQUEST_DENIED)

	def __EnableTestServerFlag(self):
		app.EnableTestServerFlag()

	def __InGameShop_Show(self, url):
		if constInfo.IN_GAME_SHOP_ENABLE:
			self.interface.OpenWebWindow(url)

	def __LoginLover(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLoginLover()

	def __LogoutLover(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLogoutLover()
		if self.affectShower:
			self.affectShower.HideLoverState()

	def __LoverNear(self):
		if self.affectShower:
			self.affectShower.ShowLoverState()

	def __LoverFar(self):
		if self.affectShower:
			self.affectShower.HideLoverState()

	def __LoverDivorce(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.ClearLoverInfo()
		if self.affectShower:
			self.affectShower.ClearLoverState()

	if app.ENABLE_CHANGE_CHANNEL:
		def __GetServerID(self):
			serverID = 1
			for i in serverInfo.REGION_DICT[0].keys():
				if serverInfo.REGION_DICT[0][i]["name"] == net.GetServerInfo().split(",")[0]:
					serverID = int(i)
					break

			return serverID

		def RefreshChannel(self, channel):
			channelName = ""
			serverName = serverInfo.REGION_DICT[0][self.__GetServerID()]["name"]
			if channel in serverInfo.REGION_DICT[0][self.__GetServerID()]["channel"]:
				channelName = serverInfo.REGION_DICT[0][self.__GetServerID()]["channel"][int(channel)]["name"]
			elif channel == 99:
				channelName = "Special CH"
			else:
				channelName = "Unknow CH"

			net.SetServerInfo("%s, %s" % (serverName,channelName))

			if self.interface:
				self.interface.wndMiniMap.serverInfo.SetText(net.GetServerInfo())

			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_CHANNEL_NOTICE % (channel))

	def __PlayMusic(self, flag, filename):
		flag = int(flag)
		if flag:
			snd.FadeOutAllMusic()
			musicInfo.SaveLastPlayFieldMusic()
			snd.FadeInMusic("BGM/" + filename)
		else:
			snd.FadeOutAllMusic()
			musicInfo.LoadLastPlayFieldMusic()
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	def SkillClearCoolTime(self, slotIndex):
		self.interface.SkillClearCoolTime(slotIndex)

	def DeactivateSlot(self, slotindex, type):
		self.interface.DeactivateSlot(slotindex, type)

	def ActivateSlot(self, slotindex, type):
		self.interface.ActivateSlot(slotindex, type)

	if app.ENABLE_RENEWAL_SWITCHBOT:
		def RefreshSwitchbotWindow(self):
			if self.interface:
				self.interface.RefreshSwitchbotWindow()

		def RefreshSwitchbotItem(self, slot):
			if self.interface:
				self.interface.RefreshSwitchbotItem(slot)

	if app.ENABLE_TELEPORT_TO_A_FRIEND:
		def RequestWarpToCharacter(self, name):
			questionDialogWarp = uiCommon.QuestionDialog("thin")
			questionDialogWarp.SetText(localeInfo.ACCEPT_WARP_FROM_YOUR_FRIEND_REQUEST % (name))
			questionDialogWarp.SetAcceptEvent(lambda: self.WarpAcceptEvent(name))
			questionDialogWarp.SetCancelEvent(lambda: self.WarpCancelEvent())
			questionDialogWarp.Open()
			self.questionDialogWarp = questionDialogWarp
			return

		def WarpAcceptEvent(self, name):
			net.SendMessengerSummonByNamePacket(name)
			self.questionDialogWarp.Close()

		def WarpCancelEvent(self):
			self.questionDialogWarp.Close()

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def SetBodyCostumeHidden(self, hidden):
			constInfo.HIDDEN_BODY_COSTUME = int(hidden)
			self.interface.RefreshVisibleCostume()

		def SetHairCostumeHidden(self, hidden):
			constInfo.HIDDEN_HAIR_COSTUME = int(hidden)
			self.interface.RefreshVisibleCostume()

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			def SetAcceCostumeHidden(self, hidden):
				constInfo.HIDDEN_ACCE_COSTUME = int(hidden)
				self.interface.RefreshVisibleCostume()

		if app.ENABLE_WEAPON_COSTUME_SYSTEM:
			def SetWeaponCostumeHidden(self, hidden):
				constInfo.HIDDEN_WEAPON_COSTUME = int(hidden)
				self.interface.RefreshVisibleCostume()

		if app.ENABLE_AURA_COSTUME_SYSTEM:
			def SetAuraCostumeHidden(self, hidden):
				constInfo.HIDDEN_AURA_COSTUME = int(hidden)
				self.interface.RefreshVisibleCostume()

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def ActAcce(self, iAct, bWindow):
			if self.interface:
				self.interface.ActAcce(iAct, bWindow)

		def AlertAcce(self, bWindow):
			snd.PlaySound("sound/ui/make_soket.wav")
			if bWindow:
				self.PopupMessage(localeInfo.ACCE_DEL_SERVEITEM)
			else:
				self.PopupMessage(localeInfo.ACCE_DEL_ABSORDITEM)

	if app.ENABLE_BIOLOG_SYSTEM:
		def BINARY_BiologManagerOpen(self):
			self.interface.ToggleBiologManager()

		def BINARY_BiologManagerUpdate(self):
			self.interface.BiologManagerUpdate()

		def BINARY_BiologManagerAlert(self):
			self.interface.BiologManager_Alert()
 
		def BINARY_BiologManagerClose(self):
			self.interface.BiologManagerClose()

	if app.ENABLE_VIEW_CHEST_DROP:
		def BINARY_AddChestDropInfo(self, chestVnum, pageIndex, slotIndex, itemVnum, itemCount):
			if self.interface:
				self.interface.AddChestDropInfo(chestVnum, pageIndex, slotIndex, itemVnum, itemCount)

		def BINARY_RefreshChestDropInfo(self, chestVnum):
			if self.interface:
				self.interface.RefreshChestDropInfo(chestVnum)

	if app.ENABLE_SPECIAL_INVENTORY:
		def __CloseLoadSafeboxEvent(self):
			self.interface.CloseLoadSafeboxEvent()

		def __CloseLoadMallEvent(self):
			self.interface.CloseLoadMallEvent()

	if app.ENABLE_ANTI_EXP:
		def SetAntiExp(self, flag):
			flag = int(flag)
			if self.interface:
				ptr = [self.interface.wndTaskBar]
				for gui in ptr:
					if gui:
						if flag:
							guiptr = gui.GetChild("AntiExpButton")
							guiptr.SetUpVisual("d:/ymir work/ui/game/taskbar/antiexp_button_01.tga")
							guiptr.SetOverVisual("d:/ymir work/ui/game/taskbar/antiexp_button_02.tga")
							guiptr.SetDownVisual("d:/ymir work/ui/game/taskbar/antiexp_button_03.tga")

							if gui.IsChild("RestExp_Value"):
								gui.GetChild("Exp_Value").Hide()
							if gui.IsChild("Exp_Value"):
								gui.GetChild("RestExp_Value").Hide()

							for j in range(1, 5):
								if gui.IsChild("EXPGauge_0%d" % j):
									gui.GetChild("EXPGauge_0%d" % j).SetDiffuseColor(104.0 / 255.0, 104.0 / 255.0, 104.0 / 255.0, 1)

						else:
							guiptr = gui.GetChild("AntiExpButton")
							guiptr.SetUpVisual("d:/ymir work/ui/game/taskbar/antiexp_button_04.tga")
							guiptr.SetOverVisual("d:/ymir work/ui/game/taskbar/antiexp_button_05.tga")
							guiptr.SetDownVisual("d:/ymir work/ui/game/taskbar/antiexp_button_06.tga")

							if gui.IsChild("RestExp_Value"):
								gui.GetChild("Exp_Value").Show()
							if gui.IsChild("Exp_Value"):
								gui.GetChild("RestExp_Value").Show()

							for j in range(1, 5):
								if gui.IsChild("EXPGauge_0%d" % j):
									gui.GetChild("EXPGauge_0%d" % j).SetDiffuseColor(201, 160, 51, 1)

	if app.ENABLE_MINIGAME_OKEY_CARDS_SYSTEM:
		def BINARY_Cards_UpdateInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points):
			self.interface.UpdateCardsInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points)

		def BINARY_Cards_FieldUpdateInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
			self.interface.UpdateCardsFieldInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)

		def BINARY_Cards_PutReward(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
			self.interface.CardsPutReward(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)

		def BINARY_Cards_ShowIcon(self):
			self.interface.CardsShowIcon()

		def BINARY_Cards_Open(self, safemode):
			self.interface.OpenCardsWindow(safemode)

	if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM and app.ENABLE_GUILD_REQUEST:
		def RefreshGuildRankingList(self, issearch):
			if self.interface:
				self.interface.RefreshGuildRankingList(issearch)

	if app.ENABLE_RENEWAL_BATTLE_PASS:
		def BINARY_ExtOpenBattlePass(self):
			if self.interface:
				self.interface.ReciveOpenExtBattlePass()

		def BINARY_ExtBattlePassAddGeneralInfo(self, BattlePassType, BattlePassName, BattlePassID, battlePassStartTime, battlePassEndTime):
			if self.interface:
				self.interface.AddExtendedBattleGeneralInfo(BattlePassType, BattlePassName, BattlePassID, battlePassStartTime, battlePassEndTime)

		def BINARY_ExtBattlePassAddMission(self, battlepassType, battlepassID, missionIndex, missionType, missionInfo1, missionInfo2, missionInfo3):
			if self.interface:
				self.interface.AddExtendedBattlePassMission(battlepassType, battlepassID, missionIndex, missionType, missionInfo1, missionInfo2, missionInfo3)

		def BINARY_ExtBattlePassAddMissionReward(self, battlepassType, battlepassID, missionIndex, missionType, itemVnum, itemCount):
			if self.interface:
				self.interface.AddExtendedBattlePassMissionReward(battlepassType, battlepassID, missionIndex, missionType, itemVnum, itemCount)

		def BINARY_ExtBattlePassUpdate(self, battlepassType, missionIndex, missionType, newProgress):
			if self.interface:
				self.interface.UpdateExtendedBattlePassMission(battlepassType, missionIndex, missionType, newProgress)

		def BINARY_ExtBattlePassAddReward(self, battlepassType, battlepassID, itemVnum, itemCount):
			if self.interface:
				self.interface.AddExtendedBattlePassReward(battlepassType, battlepassID, itemVnum, itemCount)

		def BINARY_ExtBattlePassAddRanklistEntry(self, playername, battlepassType, battlepassID, startTime, endTime):
			if self.interface:
				self.interface.AddExtBattlePassRanklistEntry(playername, battlepassType, battlepassID, startTime, endTime)

	if app.ENABLE_RENEWAL_SPECIAL_CHAT:
		def OnPickItem(self, item):
			item_vnum = int(item)
			if self.interface:
				self.interface.SpecialChatOnPick(0, item_vnum)

	if app.ENABLE_MULTI_FARM_BLOCK:
		def UpdateMultiFarmPlayer(self, multiFarmPlayer):
			self.affectShower.SetMultiFarmPlayer(str(multiFarmPlayer))

		def UpdateMultiFarmAffect(self, multiFarmStatus, isNewStatus):
			self.affectShower.SetMultiFarmInfo(int(multiFarmStatus))

			if int(isNewStatus) == 1:
				if int(multiFarmStatus) == 1:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MULTI_FARM_ACTIVE_CHAT)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MULTI_FARM_DEACTIVE_CHAT)

			app.SetMultiFarmExeIcon(int(multiFarmStatus))

	if app.ENABLE_RENEWAL_OFFLINESHOP:
		def StartOfflineShop(self, vid, isOwner):
			if self.interface:
				self.interface.OpenOfflineShopDialog(vid, isOwner)

		def StartOfflineShopPanel(self):
			if self.interface:
				self.interface.OpenOfflineShopPanel()

		def ClearOfflineShopLog(self):
			if self.interface:
				if self.interface.dlgOfflineShopPanel:
					if self.interface.dlgOfflineShopPanel.GetChild("ListBox"):
						self.interface.dlgOfflineShopPanel.GetChild("ListBox").RemoveAllItems()

		def AppendShopLog(self, name, date, itemvnum, itemcount, price):
			self.interface.AppendLogOfflineShopPanel(name, date, itemvnum, itemcount, price)

		def AppendShopLogFirst(self, name, date, itemvnum, itemcount, price):
			self.interface.AppendLogOfflineShopPanelFirst(str(name), str(date), int(itemvnum), int(itemcount), int(price))

		def EndOfflineShop(self):
			if self.interface:
				if self.interface.dlgOfflineShop:
					if self.interface.dlgOfflineShop.IsShow():
						self.interface.dlgOfflineShop.Close()

				if self.interface.dlgOfflineShopPanel:
					if self.interface.dlgOfflineShopPanel.IsShow():
						self.interface.dlgOfflineShopPanel.Close()

				if self.interface.offlineShopBuilder:
					if self.interface.offlineShopBuilder.IsShow():
						self.interface.offlineShopBuilder.Close()

		def RefreshOfflineShop(self):
			if self.interface:
				if self.interface.dlgOfflineShop:
					self.interface.dlgOfflineShop.Refresh()

				if self.interface.dlgOfflineShopPanel:
					if self.interface.dlgOfflineShopPanel.IsShow():
						self.interface.dlgOfflineShopPanel.Refresh()

				if self.interface.offlineShopBuilder:
					if self.interface.offlineShopBuilder.IsShow():
						self.interface.offlineShopBuilder.Refresh()

		def OpenOfflineShop(self):
			if self.interface:
				self.interface.OpenOfflineShopBuilder()

		def OpenBackAllItem(self):
			backItem = uiCommon.QuestionDialog("thin")
			backItem.SetText(localeInfo.OFFLINESHOP_DO_YOU_WANT_BACK)
			backItem.SetAcceptText(localeInfo.UI_ACCEPT)
			backItem.SetCancelText(localeInfo.UI_DENY)
			backItem.SetAcceptEvent(lambda arg=TRUE: self.__AnswerGetBackItems(arg))
			backItem.SetCancelEvent(lambda arg=FALSE: self.__AnswerGetBackItems(arg))
			backItem.Open()
			self.partyRequestQuestionDialog=backItem

		def __AnswerGetBackItems(self, answer):
			if not self.partyRequestQuestionDialog:
				return

			if answer:
				net.SendGetBackItems()

			self.partyRequestQuestionDialog.Close()
			self.partyRequestQuestionDialog = None

		def OpenOfflineShopPanel(self):
			if self.interface:
				self.interface.OpenOfflineShopPanel()

		def BINARY_OfflineShop_Appear(self, vid, text):
			if (chr.GetInstanceType(vid) == chr.INSTANCE_TYPE_NPC):
				if self.interface:
					self.interface.AppearOfflineShop(vid, text)

		def BINARY_OfflineShop_Disappear(self, vid):
			if (chr.GetInstanceType(vid) == chr.INSTANCE_TYPE_NPC):
				if self.interface:
					self.interface.DisappearOfflineShop(vid)

	if app.ENABLE_OFFLINESHOP_SEARCH_SYSTEM:
		def OpenPrivateShopSearch(self, type):
			if self.interface:
				self.interface.OpenPrivateShopSearch(type)

		def RefreshShopSearch(self):
			if self.interface:
				self.interface.RefreshShopSearch()

		def BuyShopSearch(self):
			self.interface.RefreshShopSearch()

		def BuyShopSearch2(self):
			if self.interface:
				if self.interface.wndPrivateShopSearch.IsShow():
					self.interface.wndPrivateShopSearch.StartSearch()

	if app.ENABLE_AUTOMATIC_PICK_UP_SYSTEM:
		def __PickUPMode(self, mode):
			constInfo.PICKUPMODE = int(mode)
			self.interface.OnChangePickUPMode()

	if app.ENABLE_MAINTENANCE_SYSTEM:
		def BINARY_Update_Maintenance(self, iTime, iDuration, iReason):
			sTime = int(iTime)
			sDuration = int(iDuration)
			sReason = str(iReason)

			if sTime != 0 and sDuration != 0:
				self.wndMaintenance.OpenMaintenance(int(iTime), int(iDuration), str(iReason))

	if app.ENABLE_RENEWAL_SKILL_SELECT: 
		def __RenewalSkillSelectWindow(self, job):
			self.interface.OpenSkillSelectWindow(job)

	if app.ENABLE_NEW_DUNGEON_LIB:
		def RefreshDungeonTimer(self, Floor, Time):
			if self.interface:
				if self.interface.wndMiniMap:
					self.interface.wndMiniMap.Hide()
				self.interface.MakeDungeonTimerWindow()
				if self.interface.wndDungeonTimer:
					self.interface.wndDungeonTimer.RefreshDungeonTimer(Time, Floor)

		def RefreshDungeonFloor(self, Floor2):
			if self.interface:
				if self.interface.wndMiniMap:
					self.interface.wndMiniMap.Hide()
				self.interface.MakeDungeonTimerWindow()
				if self.interface.wndDungeonTimer:
					self.interface.wndDungeonTimer.RefreshDungeonFloor(Floor2)

	if app.ENABLE_RENEWAL_INGAME_ITEMSHOP:
		def ItemShopClear(self, updateTime):
			uiItemShop.ItemShopClear(int(updateTime))

		def ItemShopUpdateItem(self, itemID, itemVnum, itemPrice, itemDiscount, itemOffertime, itemTopSelling, itemAddedTime, itemSellingCount, itemMaxSellingCount):
			uiItemShop.ItemShopUpdateItem(int(itemID), int(itemVnum), long(itemPrice), int(itemDiscount), int(itemOffertime), int(itemTopSelling), int(itemAddedTime), long(itemSellingCount), int(itemMaxSellingCount))
			self.interface.ItemShopUpdateItem(int(itemID), int(itemMaxSellingCount))

		def ItemShopAppendItem(self, categoryIndex, categorySubIndex, itemID, itemVnum, itemPrice, itemDiscount, itemOffertime, itemTopSelling, itemAddedTime, itemSellingCount, itemMaxSellingCount):
			uiItemShop.ItemShopAppendItem(int(categoryIndex), int(categorySubIndex), int(itemID), int(itemVnum), long(itemPrice), int(itemDiscount), int(itemOffertime), int(itemTopSelling), int(itemAddedTime), long(itemSellingCount), int(itemMaxSellingCount))

		def ItemShopHideLoading(self):
			self.interface.ItemShopHideLoading()

		def ItemShopOpenMainPage(self):
			self.interface.OpenItemShopMainWindow()

		def ItemShopLogClear(self):
			uiItemShop.ItemShopLogClear()

		def ItemShopAppendLog(self, dateText, dateTime, playerName, ipAdress, itemVnum, itemCount, itemPrice):
			uiItemShop.ItemShopAppendLog(str(dateText), int(dateTime), str(playerName), str(ipAdress), int(itemVnum), int(itemCount), long(itemPrice))

		def ItemShopPurchasesWindow(self):
			self.interface.ItemShopPurchasesWindow()

		def ItemShopSetDragonCoin(self, dragonCoin):
			self.interface.ItemShopSetDragonCoin(long(dragonCoin))

		def ItemShopAppendLogEx(self, dateText, dateText2,dateTime, playerName, ipAdress, itemVnum, itemCount, itemPrice):
			uiItemShop.ItemShopAppendLog(str(dateText)+" "+str(dateText2), int(dateTime), str(playerName), str(ipAdress), int(itemVnum), int(itemCount), long(itemPrice))

	if app.ENABLE_SLOT_MARKING_SYSTEM:
		def AddExchangeItemSlotIndex(self, idx):
			self.interface.AddExchangeItemSlotIndex(idx)

	if app.ENABLE_AURA_COSTUME_SYSTEM:
		def AuraWindowOpen(self, type):
			self.interface.AuraWindowOpen(type)

		def AuraWindowClose(self):
			self.interface.AuraWindowClose()

	if app.ENABLE_GROWTH_PET_SYSTEM:
		def PetHatchingWindowCommand(self, command):
			self.interface.PetHatchingWindowCommand(command)

		def PetNameChangeWindowCommand(self, command):
			self.interface.PetNameChangeWindowCommand(command)

		def PetSkillUpgradeDlgOpen(self, slot, index, gold):
			self.interface.PetSkillUpgradeDlgOpen(slot, index, gold)

		def PetFlashEvent(self, index):
			self.interface.PetFlashEvent(index)

		def PetAffectShowerRefresh(self):
			self.interface.PetAffectShowerRefresh()

		def PetFeedReuslt(self, result):
			self.interface.PetFeedReuslt(result)

		def PetAttrDetermineResult(self, byType):
			self.interface.PetAttrDetermineResult(byType)

		def PetAttrChangeResult(self, slotIndex, byType):
			self.interface.PetAttrChangeResult(slotIndex, byType)

		def PetReviveResult(self, result):
			self.interface.PetReviveResult(result)

		def PetWindowTypeResult(self, result):
			self.interface.PetWindowTypeResult(result)

	if app.ENABLE_INVENTORY_EXPANSION_SYSTEM:
		def ManagerInventoryUnlock(self, cmd):
			cmd = cmd.split("|")
			if cmd[0] == "Reload":
				net.SendChatPacket("/reload_inventory")
			elif cmd[0] == "Hide":
				constInfo.Inventory_Locked["Keys_Can_Unlock_%d" % (int(cmd[2]))] = int(cmd[1])
			elif cmd[0] == "Message":
				dbg.LogBox("You need "+str(cmd[1])+" items to unlock.")

	if app.ENABLE_SHIP_DEFENCE_DUNGEON:
		def __ShipMastHPShow(self):
			if self.wndShipMastHP:
				self.wndShipMastHP.Open(10000000, 10000000)

		def __HydraGetHp(self, curPoint):
			if self.wndShipMastHP:
				new = int(curPoint)
				self.wndShipMastHP.SetShipMastHP(new, 10000000)

	if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
		def BINARY_OpenWarpWindow(self):
			if self.interface:
				self.interface.OpenWarpWindow()

	if app.ENABLE_DUNGEON_TRACKING_SYSTEM:
		def TrackWindowUpdate(self):
			if systemSetting.GetDungeonTrack() or systemSetting.GetBossTrack():
				self.interface.MakeTrackWindow()
				self.interface.TrackWindowCheckPacket()

	if app.ENABLE_CHANGE_LOOK_SYSTEM:
		def __ChangeWindowOpen(self, type):
			self.interface.ChangeWindowOpen(type)

	if app.ENABLE_HUNTING_SYSTEM:
		def BINARY_OpenHuntingWindowMain(self, level, monster, cur_count, dest_count, money_min, money_max, exp_min, exp_max, race_item, race_item_count):
			if self.interface:
				self.interface.OpenHuntingWindowMain(level, monster, cur_count, dest_count, money_min, money_max, exp_min, exp_max, race_item, race_item_count)

		def BINARY_OpenHuntingWindowSelect(self, level, type, monster, count, money_min, money_max, exp_min, exp_max, race_item, race_item_count):
			if self.interface:
				self.interface.OpenHuntingWindowSelect(level, type ,monster, count, money_min, money_max, exp_min, exp_max, race_item, race_item_count)

		def BINARY_OpenHuntingWindowReward(self, level, reward, reward_count, random_reward, random_reward_count, money, exp):
			if self.interface:
				self.interface.OpenHuntingWindowReward(level, reward, reward_count, random_reward, random_reward_count, money, exp)

		def BINARY_UpdateHuntingMission(self, count):
			if self.interface:
				self.interface.UpdateHuntingMission(count)

		def BINARY_HuntingReciveRandomItem(self, window, item_vnum, item_count):
			if self.interface:
				if window == 0:
					self.interface.HuntingSetRandomItemsMain(item_vnum, item_count)
				if window == 1:
					self.interface.HuntingSetRandomItemsSelect(item_vnum, item_count)

		def SetHuntingButtonFlash(self):
			if constInfo.HUNTING_MAIN_UI_SHOW == 0:
				constInfo.HUNTING_BUTTON_FLASH = 1

	if app.ENABLE_RIDING_EXTENDED:
		def OpenMountUpGrade(self):
			if self.interface:
				self.interface.MountUpGradeWindow()
