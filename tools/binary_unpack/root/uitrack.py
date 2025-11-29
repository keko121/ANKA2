if __USE_DYNAMIC_MODULE__:
	import pyapi

app = __import__(pyapi.GetModuleName("app"))
net = __import__(pyapi.GetModuleName("net"))

import ui
import _weakref
import item
import nonplayer
import localeInfo
import systemSetting
import constInfo

import uiToolTip

IMG_DIR_AVATAR = "d:/ymir work/ui/game/dungeon_track/avatar/"
IMG_DIR = "d:/ymir work/ui/game/dungeon_track/"

def calculateRect(curValue, maxValue):
	try:
		return -1.0 + float(curValue) / float(maxValue)
	except:
		return 0.0

def FormatTime(seconds):
	if seconds <= 0:
		return "0s"
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	d, h = divmod(h, 24)
	timeText = ""
	if d > 0:
		timeText += "{}d ".format(d)
	if h > 0:
		timeText += "{}h ".format(h)
	if m > 0:
		timeText += "{}m ".format(m)
	if s > 0:
		timeText += "{}s ".format(s)
	return timeText if timeText != "" else "0s"

class TrackWindow(ui.ScriptWindow):
	class TrackItem(ui.ScriptWindow):
		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def Destroy(self):
			self.ClearDictionary()
			self.__dataDict = {}

			self.interface = None

		def __init__(self, parent, __dataDict):
			ui.ScriptWindow.__init__(self)
			self.Destroy()
			self.SetParent(parent)

			self.parent = parent
			self.__dataDict = __dataDict
			self.__fileName = ""

			self.interface = None

			self.tooltipItem = uiToolTip.ItemToolTip()
			self.tooltipItem.Hide()

			self.__LoadWindow()

		def __LoadWindow(self):
			try:
				pyScrLoader = ui.PythonScriptLoader()
				pyScrLoader.LoadScriptFile(self, "uiscript/dungeontrackitem.py")
			except:
				import exception
				exception.Abort("TrackWindow.__LoadWindow.LoadObject")

			GetObject = self.GetChild
			GetObject("avatar").LoadImage(self.__dataDict["img"])
			GetObject("avatar").SetPosition(5, 5)
			GetObject("teleport_button").SetEvent(self.__ClickTeleport)

			trackType = self.__dataDict["trackType"]

			if trackType == 0:
				ticketImageList = [GetObject("itemwall{}".format(i)) for i in xrange(3)]
				map(lambda x : x.Hide(), ticketImageList)
				(ticketList, ticketListLen) = (self.__dataDict["tickets"], len(self.__dataDict["tickets"]))
				startX = (self.GetWidth()-114)+63 if ticketListLen == 1 else (self.GetWidth()-114)+15 if ticketListLen == 2 else (self.GetWidth()-114)
				for i in xrange(len(ticketList)):
					(itemVnum, itemCount) = tuple(ticketList[i])
					item.SelectItem(itemVnum)
					ticketImage = GetObject("item{}".format(i))
					ticketImage.LoadImage(item.GetIconImageFileName())
					ticketImage.SAFE_SetStringEvent("MOUSE_OVER_IN",self.OnMouseOverInTicket, itemVnum)
					ticketImage.SAFE_SetStringEvent("MOUSE_OVER_OUT",self.OnMouseOverOutTicket)
					ticketImage.Show()
					ticketImageList[i].SetPosition(startX+(i*32), 36)
					ticketImageList[i].Show()
					if itemCount > 1:
						GetObject("itemcount{}".format(i)).SetText(str(itemCount))
						GetObject("itemcount{}".format(i)).Show()
					else:
						GetObject("itemcount{}".format(i)).Hide()
			else:
				ticketImageList = ["itemwall{}".format(i) for i in xrange(3)]
				ticketImageList.append("dungeon_key")
				for t in ticketImageList:
					self.ElementDictionary[t].Hide()
					self.ElementDictionary[t].Destroy()
					self.ElementDictionary[t] = None
					del self.ElementDictionary[t]

			GetObject("name_field").SetText(self.__dataDict["name"])
			GetObject("level_field").SetText((localeInfo.TRACK_DUNGEON_LEVEL_FIELD if trackType == 0 else localeInfo.TRACK_BOSS_LEVEL_FIELD) % (self.__dataDict["level_range"][0], self.__dataDict["level_range"][1]))
			GetObject("group_field").SetText((localeInfo.TRACK_DUNGEON_PARTY_FIELD if trackType == 0 else localeInfo.TRACK_BOSS_PARTY_FIELD) % ((localeInfo.TRACK_DUNGEON_PARTY_NOT_NEED if not self.__dataDict["group"] else localeInfo.TRACK_DUNGEON_PARTY_NEED) if trackType == 0 else (FormatTime(self.__dataDict["cooldown"]))))
			GetObject("cooldown_field").SetText((localeInfo.TRACK_DUNGEON_COOLDOWN_FIELD if trackType == 0 else localeInfo.TRACK_BOSS_COOLDOWN_FIELD) % (FormatTime(self.__dataDict["cooldown"]) if trackType == 0 else self.__dataDict["mapName"]))

			self.__fileName = IMG_DIR + "dungeon_closed.tga"
			self.__dataDict["status"] = TRUE if app.GetGlobalTimeStamp() > self.__dataDict["server_cooldown"] else FALSE

			GetObject("status_field").SetText(localeInfo.TRACK_STATUS_FIELD % ("|cFF{}{}".format("6AFF84" if self.__dataDict["status"] else "FF6E79", FormatTime(self.__dataDict["server_cooldown"]-app.GetGlobalTimeStamp()) if not self.__dataDict["status"] else localeInfo.TRACK_STATUS_AVAILABLE if trackType == 0 else (localeInfo.TRACK_STATUS_ALIVE % self.__dataDict["channel"]))))

		def BindInterfaceClass(self, interface):
			from _weakref import proxy
			self.interface = proxy(interface)

		def OnMouseOverOutTicket(self):
			if self.tooltipItem:
				if self.tooltipItem.IsShow():
					self.tooltipItem.HideToolTip()

		def OnMouseOverInTicket(self, itemVnum):
			if self.tooltipItem:
				self.tooltipItem.SetItemToolTip(itemVnum)

		def __ClickTeleport(self):
			net.SendChatPacket("/track_window teleport {}".format(self.__dataDict["bossVnum"]))

		def OnUpdate(self):
			# Tooltip kontrolü: Track window'daki item tooltip'lerinin ekranda kalmasýný önle
			if self.tooltipItem and self.tooltipItem.IsShow():
				try:
					import wndMgr
					(x, y) = wndMgr.GetMousePosition()
					(tx, ty) = self.tooltipItem.GetGlobalPosition()
					tw, th = self.tooltipItem.GetWidth(), self.tooltipItem.GetHeight()
					onTooltip = (tx <= x <= tx + tw and ty <= y <= ty + th)
					
					# Ticket icon'larýnýn üzerinde mi kontrol et
					onTicketIcon = False
					if self.__dataDict["trackType"] == 0:
						ticketList = self.__dataDict.get("tickets", [])
						for i in xrange(len(ticketList)):
							try:
								ticketImage = self.GetChild("item{}".format(i))
								if ticketImage and ticketImage.IsShow():
									(ix, iy) = ticketImage.GetGlobalPosition()
									iw, ih = ticketImage.GetWidth(), ticketImage.GetHeight()
									if ix <= x <= ix + iw and iy <= y <= iy + ih:
										onTicketIcon = True
										break
							except:
								pass
					
					# Ne tooltip'in üzerinde ne de ticket icon'unun üzerinde deðilse kapat
					if not onTooltip and not onTicketIcon:
						self.tooltipItem.HideToolTip()
				except:
					pass
			
			if not self.__dataDict["status"]:
				leftTime = self.__dataDict["server_cooldown"]-app.GetGlobalTimeStamp()
				if leftTime <= 1:
					self.__dataDict["status"] = TRUE
					self.__dataDict["deactiveType"] = 0

					if ((systemSetting.GetDungeonTrack() == 1 and self.__dataDict["trackType"] == 0) or (systemSetting.GetBossTrack() == 1 and self.__dataDict["trackType"] == 1)):
						if self.interface:
							self.interface.TrackRecvInfo((localeInfo.TRACK_DUNGEON_READY if self.__dataDict["trackType"] == 0 else localeInfo.TRACK_BOSS_READY) % self.__dataDict["name"])

				self.GetChild("status_field").SetText(localeInfo.TRACK_STATUS_FIELD % ("|cFF{}{}".format("6AFF84" if self.__dataDict["status"] else "FF6E79" if self.__dataDict["deactiveType"] == 0 else "FFDC66", (localeInfo.TRACK_STATUS_FIELD_GO_BACK if self.__dataDict["deactiveType"] != 0 else "") + FormatTime(self.__dataDict["server_cooldown"]-app.GetGlobalTimeStamp()) if not self.__dataDict["status"] else localeInfo.TRACK_STATUS_AVAILABLE if self.__dataDict["trackType"] == 0 else (localeInfo.TRACK_STATUS_ALIVE % self.__dataDict["channel"]))))

			img = IMG_DIR + "dungeon_available.tga" if self.__dataDict["status"] else IMG_DIR + "dungeon_closed.tga" if self.__dataDict["deactiveType"] == 0 else IMG_DIR + "dungeon_re_enter.tga"
			if self.__fileName != img:
				self.GetChild("board").LoadImage(img)
				self.__fileName = img
			else:
				if self.__dataDict["status"] and IMG_DIR + "dungeon_available.tga" != self.__fileName:
					self.GetChild("board").LoadImage(IMG_DIR + "dungeon_available.tga")
					self.__fileName = IMG_DIR + "dungeon_available.tga"

		def OnRender(self):
			_wy = self.parent.GetGlobalPosition()[1]
			_height = self.parent.GetHeight()
			for chilname, childItem in self.ElementDictionary.items():
				if isinstance(childItem, ui.TextLine):
					(_x,_y) = childItem.GetGlobalPosition()
					childHeight = childItem.GetHeight()
					if _y < _wy:
						if childItem.IsShow():
							childItem.Hide()
						continue
					if _y+childHeight > (_wy+_height-20):
						if childItem.IsShow():
							childItem.Hide()
						continue
					if not childItem.IsShow():
						childItem.Show()

				if isinstance(childItem, ui.ToggleButton) or isinstance(childItem, ui.Button) or isinstance(childItem, ui.ExpandedImageBox):
					topRender = 0
					bottomRender = 0
					itsRendered = FALSE
					(_x,_y) = childItem.GetGlobalPosition()
					childHeight = childItem.GetHeight()
					if _y < _wy:
						topRender = _y-_wy
						itsRendered = TRUE
					if _y+childHeight > (_wy+_height-2):
						bottomRender = (_wy+_height-2)-(_y+childHeight)
						itsRendered = TRUE
					if itsRendered:
						childItem.SetRenderingRect(0,calculateRect(childHeight-abs(topRender), childHeight),0,calculateRect(childHeight-abs(bottomRender),childHeight))
					else:
						childItem.SetRenderingRect(0, 0, 0, 0)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()
		self.__dataDict = {}
		self.__trackType = 0
		self.__packetSended = FALSE

		self.interface = None

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.Destroy()
		self.__LoadWindow()

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/dungeontrackwindow.py")
		except:
			import exception
			exception.Abort("TrackWindow.__LoadWindow.LoadObject")
		GetObject = self.GetChild

		GetObject("board").SetCloseEvent(self.Close)

		scrollBar = ScrollBarNew()
		scrollBar.SetParent(GetObject("board"))
		scrollBar.SetScrollBarSize(452)
		scrollBar.SetMiddleBarSize(1.0)
		scrollBar.SetPosition(self.GetWidth()-25, 75)
		scrollBar.Show()
		self.ElementDictionary["scrollBar"] = scrollBar

		GetObject("listbox").SetExtraScrollLen(112)
		GetObject("listbox").SetScrollBar(_weakref.proxy(scrollBar))

		GetObject("dungeon_info").SAFE_SetEvent(self.SetTrackType, 0)
		GetObject("worldboss_info").SAFE_SetEvent(self.SetTrackType, 1)

		GetObject("dungeon_info_notice").SetToggleUpEvent(self.SetOptions, 0)
		GetObject("dungeon_info_notice").SetToggleDownEvent(self.SetOptions, 0)

		GetObject("worldboss_info_notice").SetToggleUpEvent(self.SetOptions, 1)
		GetObject("worldboss_info_notice").SetToggleDownEvent(self.SetOptions, 1)

		self.__dataDict = {
			# Dungeon
			0 : [\
				{
					"trackType": 0,
					"name": localeInfo.MAP_DEVILTOWER1,
					"level_range": [40, 95],
					"group": FALSE,
					"cooldown": 60*60,
					"server_cooldown": 0,
					"img": IMG_DIR_AVATAR + "demon_tower.tga",
					"tickets": [[71095, 1]],
					"bossVnum": 1093,
					"status" : FALSE,
					"deactiveType" : 0,
				},
				{
					"trackType": 0,
					"name": localeInfo.MAP_SPIDERDUNGEON_03,
					"level_range": [70, 90],
					"group": FALSE,
					"cooldown": 60*60,
					"server_cooldown": 0,
					"img": IMG_DIR_AVATAR + "baroness.tga",
					"tickets": [[30324, 1]],
					"bossVnum": 2092,
					"status" : FALSE,
					"deactiveType" : 0,
				},
				{
					"trackType": 0,
					"name": localeInfo.MAP_SKIPIA_DUNGEON_BOSS,
					"level_range": [75, 105],
					"group": FALSE,
					"cooldown": 60*60,
					"server_cooldown": 0,
					"img": IMG_DIR_AVATAR + "beran.tga",
					"tickets": [[30179, 3]],
					"bossVnum": 2493,
					"status" : FALSE,
					"deactiveType" : 0,
				},
				{
					"trackType": 0,
					"name": localeInfo.MAP_DEVILCATACOMB,
					"level_range": [80, 105],
					"group": FALSE,
					"cooldown": 60*60,
					"server_cooldown": 0,
					"img": IMG_DIR_AVATAR + "azrael.tga",
					"tickets": [[30319, 1]],
					"bossVnum": 2598,
					"status" : FALSE,
					"deactiveType" : 0,
				},
				{
					"trackType": 0,
					"name": localeInfo.MAP_N_FLAME_DUNGEON_01,
					"level_range": [90, 120],
					"group": FALSE,
					"cooldown": 60*60*1,
					"server_cooldown": 0,
					"img": IMG_DIR_AVATAR + "razador.tga",
					"tickets": [[71095, 1]],
					"bossVnum": 6091,
					"status" : FALSE,
					"deactiveType" : 0,
				},
				{
					"trackType": 0,
					"name": localeInfo.MAP_N_SNOW_DUNGEON_01,
					"level_range": [90, 120],
					"group": FALSE,
					"cooldown": 60*60*1,
					"server_cooldown": 0,
					"img": IMG_DIR_AVATAR + "nemere.tga",
					"tickets": [[71095, 1]],
					"bossVnum": 6191,
					"status" : FALSE,
					"deactiveType" : 0,
				},
				{
					"trackType": 0,
					"name": localeInfo.DEFENSAWE_HYDRA,
					"level_range": [105, 120],
					"group": FALSE,
					"cooldown": 60*60*3,
					"server_cooldown": 0,
					"img": IMG_DIR_AVATAR + "hidra.tga",
					"tickets": [[71095, 1]],
					"bossVnum": 9018,
					"status" : FALSE,
					"deactiveType" : 0,
				},
				# {
					# "trackType": 0,
					# "name": localeInfo.MELEYDUNGEON,
					# "level_range": [110, 120],
					# "group": TRUE,
					# "cooldown": 60*60*3,
					# "server_cooldown": 0,
					# "img": IMG_DIR_AVATAR + "meley.tga",
					# "tickets": [[71095, 1]],
					# "bossVnum": 20442,
					# "status" : FALSE,
					# "deactiveType" : 0,
				# },
			],
			# WorldBoss
			1 : [\
				# {
					# "name": localeInfo.TRACK_WB_2,
					# "trackType": 1,
					# "level_range": [40, 60],
					# "cooldown": 60*60*48,
					# "server_cooldown": 0,
					# "img": IMG_DIR_AVATAR + "you.tga",
					# "bossVnum": 9836,
					# "mapName": localeInfo.TRACK_WB_1_MAP,
					# "channel": 99,
					# "status" : FALSE,
					# "regen_id" : 1,
					# "deactiveType" : 0,
				# },
				{
					"name": localeInfo.DEFENSAWE_HYDRA,
					"trackType": 1,
					"level_range": [65, 85],
					"cooldown": 60*60*48,
					"server_cooldown": 0,
					"img": IMG_DIR_AVATAR + "shadow_tower.tga",
					"bossVnum": 9844,
					"mapName": localeInfo.MAP_DEVILTOWER2,
					"channel": 99,
					"status" : FALSE,
					"regen_id" : 0,
					"deactiveType" : 0,
				},
				# {
					# "name": localeInfo.TRACK_WB_3,
					# "trackType": 1,
					# "level_range": [80, 100],
					# "cooldown": 60 * 60 * 48,
					# "server_cooldown": 0,
					# "img": IMG_DIR_AVATAR+"chou.tga",
					# "bossVnum": 9838,
					# "mapName": localeInfo.TRACK_WB_1_MAP,
					# "channel": 99,
					# "status" : FALSE,
					# "regen_id" : 2,
					# "deactiveType" : 0,
				# },
				# {
					# "name": localeInfo.TRACK_WB_4,
					# "trackType": 1,
					# "level_range": [95, 115],
					# "cooldown": 60 * 60 * 48,
					# "server_cooldown": 0,
					# "img": IMG_DIR_AVATAR+"xu.tga",
					# "bossVnum": 9840,
					# "mapName": localeInfo.TRACK_WB_1_MAP,
					# "channel": 99,
					# "status" : FALSE,
					# "regen_id" : 3,
					# "deactiveType" : 0,
				# },
				# {
					# "name": localeInfo.TRACK_WB_5,
					# "trackType": 1,
					# "level_range": [105, 120],
					# "cooldown": 60 * 60 * 48,
					# "server_cooldown": 0,
					# "img": IMG_DIR_AVATAR+"chen.tga",
					# "bossVnum": 9842,
					# "mapName": localeInfo.TRACK_WB_1_MAP,
					# "channel": 99,
					# "status" : FALSE,
					# "regen_id" : 4,
					# "deactiveType" : 0,
				# },
			],
		}
		self.SetTrackType(0)
		self.SetCenterPosition()

	def BindInterfaceClass(self, interface):
		from _weakref import proxy
		self.interface = proxy(interface)

	def SetOptions(self, type):
		if type == 0:
			systemSetting.SetDungeonTrack(not systemSetting.GetDungeonTrack())
		elif type == 1:
			systemSetting.SetBossTrack(not systemSetting.GetBossTrack())
		self.RefreshOptions()

	def RefreshOptions(self):
		if systemSetting.GetDungeonTrack():
			self.GetChild("dungeon_info_notice").Down()
		else:
			self.GetChild("dungeon_info_notice").SetUp()

		if systemSetting.GetBossTrack():
			self.GetChild("worldboss_info_notice").Down()
		else:
			self.GetChild("worldboss_info_notice").SetUp()

	def SetTrackType(self, trackType):
		self.__trackType = trackType

		btnList = [self.GetChild("dungeon_info"), self.GetChild("worldboss_info")]
		btnList[trackType].Down()
		btnList[not trackType].SetUp()

		self.Refresh()

	def Refresh(self):
		listbox = self.GetChild("listbox")
		listbox.RemoveAllItems()

		trackDataList = self.__dataDict[self.__trackType] if self.__dataDict.has_key(self.__trackType) else []
		yItemCount = 0
		for data in trackDataList:
			trackItem = self.TrackItem(_weakref.proxy(listbox), data)
			trackItem.SetPosition(0, yItemCount * trackItem.GetHeight(), TRUE)
			listbox.AppendItem(trackItem)
			trackItem.Show()
			yItemCount+=1

		listbox.RefreshAll()

	def TrackBossInfo(self, bossID, bossLeftTime, bossChannel):
		trackDataList = self.__dataDict[1] if self.__dataDict.has_key(1) else []
		for data in trackDataList:
			if data["regen_id"] == bossID:
				data["server_cooldown"] = app.GetGlobalTimeStamp()+bossLeftTime if bossLeftTime != 65535 else 0
				data["status"] = FALSE if bossLeftTime != 65535 else TRUE

	def TrackDungeonInfo(self, cmdData):
		trackDataList = self.__dataDict[0] if self.__dataDict.has_key(0) else []
		if len(cmdData) != 0:
			cmdTokenList = cmdData[:len(cmdData)-1].split("#")
			for cmd in cmdTokenList:
				cooldown = cmd.split("|")
				if len(cooldown) == 3:
					bossVnum = int(cooldown[0])
					for data in trackDataList:
						if data["bossVnum"] == bossVnum:
							data["server_cooldown"] = app.GetGlobalTimeStamp()+int(cooldown[1])
							data["deactiveType"] = int(cooldown[2])
							data["status"] = FALSE

	def CheckPacket(self):
		if not self.__packetSended:
			self.__packetSended = TRUE
			command = "/track_window load"
			trackDataList = self.__dataDict[1] if self.__dataDict.has_key(1) else []
			for data in trackDataList:
				command += " {}".format(data["regen_id"])
			net.SendChatPacket(command)

	def Open(self):
		self.Show()
		self.SetTop()

		if not self.__packetSended:
			self.__packetSended = TRUE
			command = "/track_window load"
			trackDataList = self.__dataDict[1] if self.__dataDict.has_key(1) else []
			for data in trackDataList:
				command += " {}".format(data["regen_id"])

			net.SendChatPacket(command)

		self.RefreshOptions()

	def OnRunMouseWheel(self, nLen):
		if self.ElementDictionary.has_key("scrollBar"):
			self.scrollBar = self.ElementDictionary["scrollBar"]
			if self.scrollBar.IsShow():
				if nLen > 0:
					self.scrollBar.OnUp()
				else:
					self.scrollBar.OnDown()
				return TRUE
		return FALSE

	def Close(self):
		self.Hide()
		return TRUE

	def OnPressEscapeKey(self):
		# ESC ile kapatýldýðýnda tüm tooltip'leri kapat
		from uiToolTip import ToolTip
		for tooltip in ToolTip._allToolTips:
			if tooltip and hasattr(tooltip, 'IsShow') and tooltip.IsShow():
				if hasattr(tooltip, 'HideToolTip'):
					tooltip.HideToolTip()
				elif hasattr(tooltip, 'Hide'):
					tooltip.Hide()
		
		return self.Close()

class ScrollBarNew(ui.Window):
	SCROLLBAR_WIDTH = 10
	SCROLL_BTN_XDIST = 2
	SCROLL_BTN_YDIST = 2

	class MiddleBar(ui.DragButton):
		def __init__(self):
			ui.DragButton.__init__(self)
			self.AddFlag("movable")
			self.SetWindowName("scrollbar_middlebar")

		def MakeImage(self):
			top = ui.ExpandedImageBox()
			top.SetParent(self)
			top.LoadImage(IMG_DIR+"scrollbar_ex/scrollbar_top.tga")
			top.AddFlag("not_pick")
			top.Show()

			topScale = ui.ExpandedImageBox()
			topScale.SetParent(self)
			topScale.SetPosition(0, top.GetHeight())
			topScale.LoadImage(IMG_DIR+"scrollbar_ex/scrollbar_scale.tga")
			topScale.AddFlag("not_pick")
			topScale.Show()

			bottom = ui.ExpandedImageBox()
			bottom.SetParent(self)
			bottom.LoadImage(IMG_DIR+"scrollbar_ex/scrollbar_bottom.tga")
			bottom.AddFlag("not_pick")
			bottom.Show()
			bottomScale = ui.ExpandedImageBox()
			bottomScale.SetParent(self)
			bottomScale.LoadImage(IMG_DIR+"scrollbar_ex/scrollbar_scale.tga")
			bottomScale.AddFlag("not_pick")
			bottomScale.Show()

			middle = ui.ExpandedImageBox()
			middle.SetParent(self)
			middle.LoadImage(IMG_DIR+"scrollbar_ex/scrollbar_mid.tga")
			middle.AddFlag("not_pick")
			middle.Show()

			self.top = top
			self.topScale = topScale
			self.bottom = bottom
			self.bottomScale = bottomScale
			self.middle = middle

		def SetSize(self, height):
			minHeight = self.top.GetHeight() + self.bottom.GetHeight() + self.middle.GetHeight()
			height = max(minHeight, height)
			ui.DragButton.SetSize(self, 10, height)
			scale = (height - minHeight) / 2 
			extraScale = 0
			if (height - minHeight) % 2 == 1:
				extraScale = 1
			self.topScale.SetRenderingRect(0, 0, 0, scale - 1)
			self.middle.SetPosition(0, self.top.GetHeight() + scale)
			self.bottomScale.SetPosition(0, self.middle.GetBottom())
			self.bottomScale.SetRenderingRect(0, 0, 0, scale - 1 + extraScale)
			self.bottom.SetPosition(0, height - self.bottom.GetHeight())

	def __init__(self):
		ui.Window.__init__(self)
		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = None
		self.eventArgs = None
		self.lockFlag = FALSE
		self.CreateScrollBar()
		self.SetScrollBarSize(0)
		self.scrollStep = 0.2
		self.SetWindowName("NONAME_ScrollBar")

	def __del__(self):
		ui.Window.__del__(self)

	def CreateScrollBar(self):
		topImage = ui.ExpandedImageBox()
		topImage.SetParent(self)
		topImage.AddFlag("not_pick")
		topImage.LoadImage(IMG_DIR+"scrollbar_ex/scroll_top.tga")
		topImage.Show()

		bottomImage = ui.ExpandedImageBox()
		bottomImage.SetParent(self)
		bottomImage.AddFlag("not_pick")
		bottomImage.LoadImage(IMG_DIR+"scrollbar_ex/scroll_bottom.tga")
		bottomImage.Show()

		middleImage = ui.ExpandedImageBox()
		middleImage.SetParent(self)
		middleImage.AddFlag("not_pick")
		middleImage.SetPosition(0, topImage.GetHeight())
		middleImage.LoadImage(IMG_DIR+"scrollbar_ex/scroll_mid.tga")
		middleImage.Show()

		self.topImage = topImage
		self.bottomImage = bottomImage
		self.middleImage = middleImage
		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(ui.__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.MakeImage()
		middleBar.SetSize(12)
		self.middleBar = middleBar

	def Destroy(self):
		self.eventScroll = None
		self.eventArgs = None

	def SetScrollEvent(self, event, *args):
		self.eventScroll = event
		self.eventArgs = args

	def SetMiddleBarSize(self, pageScale):
		self.middleBar.SetSize(int(pageScale * float(self.GetHeight() - (self.SCROLL_BTN_YDIST*2))))
		realHeight = self.GetHeight() - (self.SCROLL_BTN_YDIST*2) - self.middleBar.GetHeight()
		self.pageSize = realHeight

	def SetScrollBarSize(self, height):
		self.SetSize(self.SCROLLBAR_WIDTH, height)
		self.pageSize = height - self.SCROLL_BTN_YDIST*2 - self.middleBar.GetHeight()
		middleImageScale = float((height - self.SCROLL_BTN_YDIST*2) - self.middleImage.GetHeight()) / float(self.middleImage.GetHeight())

		self.middleImage.SetRenderingRect(0, 0, 0, middleImageScale)
		self.bottomImage.SetPosition(0, height - self.bottomImage.GetHeight())
		self.middleBar.SetRestrictMovementArea(self.SCROLL_BTN_XDIST, self.SCROLL_BTN_YDIST, self.middleBar.GetWidth(), height - self.SCROLL_BTN_YDIST * 2)
		self.middleBar.SetPosition(self.SCROLL_BTN_XDIST, self.SCROLL_BTN_YDIST)

	def SetScrollStep(self, step):
		self.scrollStep = step

	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep)

	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep)

	def GetScrollStep(self):
		return self.scrollStep

	def GetPos(self):
		return self.curPos

	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep)

	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep)

	def SetPos(self, pos, moveEvent = TRUE):
		pos = max(0.0, pos)
		pos = min(1.0, pos)
		newPos = float(self.pageSize) * pos
		self.middleBar.SetPosition(self.SCROLL_BTN_XDIST, int(newPos) + self.SCROLL_BTN_YDIST)

		if moveEvent == TRUE:
			self.OnMove()

	def OnMove(self):
		if self.lockFlag:
			return
		if 0 == self.pageSize:
			return
		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(yLocal - self.SCROLL_BTN_YDIST) / float(self.pageSize)
		if self.eventScroll:
			apply(self.eventScroll, self.eventArgs)

	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		newPos = float(yMouseLocalPosition) / float(self.GetHeight())
		self.SetPos(newPos)

	def LockScroll(self):
		self.lockFlag = TRUE

	def UnlockScroll(self):
		self.lockFlag = FALSE