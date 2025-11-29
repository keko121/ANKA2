if __USE_DYNAMIC_MODULE__:
	import pyapi

app = __import__(pyapi.GetModuleName("app"))
chr = __import__(pyapi.GetModuleName("chr"))
chrmgr = __import__(pyapi.GetModuleName("chrmgr"))
player = __import__(pyapi.GetModuleName("player"))
net = __import__(pyapi.GetModuleName("net"))

import dbg
import snd
import wndMgr

import background
import playerSettingModule

import ui
import uiPhaseCurtain
import constInfo
import localeInfo

class PopupDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.CloseEvent = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		PythonScriptLoader = ui.PythonScriptLoader()
		PythonScriptLoader.LoadScriptFile(self, "UIScript/PopupDialog.py")

	def Open(self, Message, event = 0, ButtonName = localeInfo.UI_CANCEL):

		if TRUE == self.IsShow():
			self.Close()

		self.Lock()
		self.SetTop()
		self.CloseEvent = event

		AcceptButton = self.GetChild("accept")
		# AcceptButton.SetText(ButtonName)
		AcceptButton.SetEvent(ui.__mem_func__(self.Close))

		self.GetChild("message").SetText(Message)
		self.Show()

	def Close(self):

		if FALSE == self.IsShow():
			self.CloseEvent = 0
			return

		self.Unlock()
		self.Hide()

		if 0 != self.CloseEvent:
			self.CloseEvent()
			self.CloseEvent = 0

	def Destroy(self):
		self.Close()
		self.ClearDictionary()

	def OnPressEscapeKey(self):
		self.Close()
		return TRUE

	def OnIMEReturn(self):
		self.Close()
		return TRUE

class MainStream(object):
	isChrData=0	

	def __init__(self):
		print "NEWMAIN STREAM ----------------------------------------------------------------------------"
		net.SetHandler(self)
		net.SetTCPRecvBufferSize(128*1024)
		net.SetTCPSendBufferSize(4096)
		net.SetUDPRecvBufferSize(4096)

		self.id = ""
		self.pwd = ""
		self.addr = ""
		self.port = 0
		self.account_addr = 0
		self.account_port = 0
		self.slot = 0
		self.isAutoSelect = 0
		self.isAutoLogin = 0

		# self.curtain = 0
		self.curPhaseWindow = 0
		self.newPhaseWindow = 0

	def __del__(self):
		print "---------------------------------------------------------------------------- DELETE MAIN STREAM "

	def Destroy(self):
		if self.curPhaseWindow:
			self.curPhaseWindow.Close()
			self.curPhaseWindow = 0

		if self.newPhaseWindow:
			self.newPhaseWindow.Close()
			self.newPhaseWindow = 0

		self.popupWindow.Destroy()
		self.popupWindow = 0

		# self.curtain = 0

	def Create(self):
		self.CreatePopupDialog()

	def SetPhaseWindow(self, newPhaseWindow):
		self.newPhaseWindow = newPhaseWindow
		self.__ChangePhaseWindow()

	def __ChangePhaseWindow(self):
		oldPhaseWindow = self.curPhaseWindow
		newPhaseWindow = self.newPhaseWindow
		self.curPhaseWindow = 0
		self.newPhaseWindow = 0

		if oldPhaseWindow:
			oldPhaseWindow.Close()

		if newPhaseWindow:
			newPhaseWindow.Open()

		self.curPhaseWindow = newPhaseWindow

		if not self.curPhaseWindow:
			app.Exit()

	def CreatePopupDialog(self):
		self.popupWindow = PopupDialog()
		self.popupWindow.LoadDialog()
		self.popupWindow.SetCenterPosition()
		self.popupWindow.Hide()

	def SetLogoPhase(self):
		net.Disconnect()

		import introLogo
		self.SetPhaseWindow(introLogo.LogoWindow(self))

	def SetLoginPhase(self):
		net.Disconnect()

		import introLogin
		self.SetPhaseWindow(introLogin.LoginWindow(self))

	def SameLogin_SetLoginPhase(self):
		net.Disconnect()

		import introLogin
		introInst = introLogin.LoginWindow(self)
		self.SetPhaseWindow(introInst)
		introInst.SameLogin_OpenUI()

	def SetSelectEmpirePhase(self):
		try:
			import introEmpire
			self.SetPhaseWindow(introEmpire.SelectEmpireWindow(self))
		except:
			import exception
			exception.Abort("networkModule.SetSelectEmpirePhase")

	def SetReselectEmpirePhase(self):
		try:
			import introEmpire
			self.SetPhaseWindow(introEmpire.ReselectEmpireWindow(self))
		except:
			import exception
			exception.Abort("networkModule.SetReselectEmpirePhase")

	def SetSelectCharacterPhase(self):
		try:
			localeInfo.LoadLocaleData()
			import introSelect
			self.popupWindow.Close()
			self.SetPhaseWindow(introSelect.SelectCharacterWindow(self))
		except:
			import exception
			exception.Abort("networkModule.SetSelectCharacterPhase")

	def SetCreateCharacterPhase(self):
		try:
			import introCreate
			self.SetPhaseWindow(introCreate.CreateCharacterWindow(self))
		except:
			import exception
			exception.Abort("networkModule.SetCreateCharacterPhase")

	def SetLoadingPhase(self, isWarp = FALSE):
		try:
			class LoadingWindow:
				def __init__(self, stream, isWarp = FALSE):

					self.isWarp = isWarp

					if self.isWarp:
						self.LoadingImage = ui.AniImageBox()
						for x in xrange(14):
							self.LoadingImage.AppendImage("d:/ymir work/ui/intro/loading/%d.tga" % (x))
							self.LoadingImage.SetPosition(wndMgr.GetScreenWidth() / 2 - 170, wndMgr.GetScreenHeight() / 2 - 178)
							self.LoadingImage.Show()
					else:
						self.LoadingImage = ui.ExpandedImageBox()
						self.LoadingImage.LoadImage("d:/ymir work/ui/intro/common/background.png")
						width = float(wndMgr.GetScreenWidth()) / float(self.LoadingImage.GetWidth())
						height = float(wndMgr.GetScreenHeight()) / float(self.LoadingImage.GetHeight())
						self.LoadingImage.SetScale(width, height)
						self.LoadingImage.Show()

					chrSlot = stream.GetCharacterSlot()
					net.SendSelectCharacterPacket(chrSlot)
					playerSettingModule.LoadGameData("RACE_HEIGHT")
					background.SetViewDistanceSet(background.DISTANCE0, 25600)
					background.SelectViewDistanceNum(background.DISTANCE0)

					if self.isWarp:
						self.LoadingImage.OnEndFrame()

				def Open(self):
					pass

				def Close(self):
					pass

			self.SetPhaseWindow(LoadingWindow(self, isWarp))
		except:
			import exception
			exception.Abort("networkModule.SetLoadingPhase")

	def SetGamePhase(self):
		try:
			import game
			self.popupWindow.Close()
			self.SetPhaseWindow(game.GameWindow(self))
		except:
			raise
			import exception
			exception.Abort("networkModule.SetGamePhase")

	def Connect(self):
		import constInfo
		if constInfo.KEEP_ACCOUNT_CONNETION_ENABLE:
			net.ConnectToAccountServer(self.addr, self.port, self.account_addr, self.account_port)
		else:
			net.ConnectTCP(self.addr, self.port)

	def SetConnectInfo(self, addr, port, account_addr = 0, account_port = 0):
		self.addr = addr
		self.port = port
		self.account_addr = account_addr
		self.account_port = account_port

		if app.__AUTO_HUNT__:
			import constInfo
			constInfo.autoHuntAutoLoginDict["addr"] = self.addr
			constInfo.autoHuntAutoLoginDict["port"] = self.port
			constInfo.autoHuntAutoLoginDict["account_addr"] = self.account_addr
			constInfo.autoHuntAutoLoginDict["account_port"] = self.account_port

	def GetConnectAddr(self):
		return self.addr

	def SetLoginInfo(self, id, pwd):
		self.id = id
		self.pwd = pwd

		if app.__AUTO_HUNT__:
			import constInfo
			constInfo.autoHuntAutoLoginDict["id"] = self.id
			constInfo.autoHuntAutoLoginDict["pwd"] = self.pwd

		net.SetLoginInfo(id, pwd)

	def CancelEnterGame(self):
		pass

	def SetCharacterSlot(self, slot):
		self.slot = slot

		if app.__AUTO_HUNT__:
			import constInfo
			constInfo.autoHuntAutoLoginDict["slot"] = slot

	def GetCharacterSlot(self):
		return self.slot

	def EmptyFunction(self):
		pass
