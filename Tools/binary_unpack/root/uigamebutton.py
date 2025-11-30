if __USE_DYNAMIC_MODULE__:
	import pyapi

app = __import__(pyapi.GetModuleName("app"))
player = __import__(pyapi.GetModuleName("player"))
net = __import__(pyapi.GetModuleName("net"))

import ui

if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
	import uiCommon
	import localeInfo

class GameButtonWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow("UIScript/gamewindow.py")
		if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
			self.popup = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self, filename):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, filename)
		except Exception, msg:
			import dbg
			dbg.TraceError("GameButtonWindow.LoadScript - %s" % (msg))
			app.Abort()
			return FALSE

		try:
			self.gameButtonDict={
				"STATUS" : self.GetChild("StatusPlusButton"),
				"SKILL" : self.GetChild("SkillPlusButton"),
				"QUEST" : self.GetChild("QuestButton"),
				"BUILD" : self.GetChild("BuildGuildBuilding"),
				"EXIT_OBSERVER" : self.GetChild("ExitObserver"),
			}

			if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
				self.gameButtonDict["GUILDWAR"] = self.GetChild("GuildWarButton")
				self.gameButtonDict["GUILDWAR"].SetEvent(ui.__mem_func__(self.__RequestGuildWarEnter))

			self.gameButtonDict["EXIT_OBSERVER"].SetEvent(ui.__mem_func__(self.__OnClickExitObserver))

		except Exception, msg:
			import dbg
			dbg.TraceError("GameButtonWindow.LoadScript - %s" % (msg))
			app.Abort()
			return FALSE

		self.__HideAllGameButton()
		if app.ENABLE_GUILDRENEWAL_SYSTEM:
			self.SetObserverMode(player.IsObserverMode(),True)
		else:
			self.SetObserverMode(player.IsObserverMode())
		return TRUE

	if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
		def __RequestGuildWarEnter(self):
			questionDialog = uiCommon.QuestionDialog()
			questionDialog.SetText(localeInfo.GAME_GUILDWAR_NOW_JOIN)
			questionDialog.SetAcceptEvent(ui.__mem_func__(self.AcceptGuildWarEnter))
			questionDialog.SetCancelEvent(ui.__mem_func__(self.ClosePopUpDialog))
			questionDialog.Open()
			self.popup = questionDialog

		def AcceptGuildWarEnter(self):
			m2netm2g.SendChatPacket("/guildwar_request_enter")
			if self.popup:
				self.popup.Close()
			self.popup = None

		def ClosePopUpDialog(self):
			if self.popup:
				self.popup.Close()
			self.popup = None

		def ShowGuildWarButton(self):
			self.gameButtonDict["GUILDWAR"].Show()

		def HideGuildWarButton(self):
			self.gameButtonDict["GUILDWAR"].Hide()

	def Destroy(self):
		for key in self.gameButtonDict:
			self.gameButtonDict[key].SetEvent(0)

		self.gameButtonDict={}

		if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
			self.popup = None

	def SetButtonEvent(self, name, event):
		try:
			self.gameButtonDict[name].SetEvent(event)
		except Exception, msg:
			print "GameButtonWindow.LoadScript - %s" % (msg)
			app.Abort()
			return

	def ShowBuildButton(self):
		self.gameButtonDict["BUILD"].Show()

	def HideBuildButton(self):
		self.gameButtonDict["BUILD"].Hide()

	def CheckGameButton(self):

		if not self.IsShow():
			return

		statusPlusButton = self.gameButtonDict["STATUS"]
		skillPlusButton = self.gameButtonDict["SKILL"]

		if player.GetStatus(player.STAT) > 0:
			statusPlusButton.Show()
		else:
			statusPlusButton.Hide()

		if self.__IsSkillStat():
			skillPlusButton.Show()
		else:
			skillPlusButton.Hide()

	def __IsSkillStat(self):
		if player.GetStatus(player.SKILL_ACTIVE) > 0:
			return TRUE

		return FALSE

	def __OnClickExitObserver(self):
		net.SendChatPacket("/observer_exit")

	def __HideAllGameButton(self):
		for btn in self.gameButtonDict.values():
			btn.Hide()

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def SetObserverMode(self, isEnable, isButtonShow):
			if isButtonShow:
				if isEnable:
					self.gameButtonDict["EXIT_OBSERVER"].Show()
				else:
					self.gameButtonDict["EXIT_OBSERVER"].Hide()
	else:
		def SetObserverMode(self, isEnable):
			if isEnable:
				self.gameButtonDict["EXIT_OBSERVER"].Show()
			else:
				self.gameButtonDict["EXIT_OBSERVER"].Hide()
