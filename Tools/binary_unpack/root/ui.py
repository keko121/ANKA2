if __USE_DYNAMIC_MODULE__:
	import pyapi

app = __import__(pyapi.GetModuleName("app"))
chr = __import__(pyapi.GetModuleName("chr"))
player = __import__(pyapi.GetModuleName("player"))

import ime
import grp
import snd
import wndMgr
import item
import skill
import localeInfo
import dbg
# MARK_BUG_FIX
import guild
# END_OF_MARK_BUG_FIX

from _weakref import proxy

BACKGROUND_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 1.0)
DARK_COLOR = grp.GenerateColor(0.2, 0.2, 0.2, 1.0)
BRIGHT_COLOR = grp.GenerateColor(0.7, 0.7, 0.7, 1.0)

SELECT_COLOR = grp.GenerateColor(0.0, 0.0, 0.5, 0.3)

WHITE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.5)
HALF_WHITE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.2)

createToolTipWindowDict = {}
def RegisterCandidateWindowClass(codePage, candidateWindowClass):
	EditLine.candidateWindowClassDict[codePage]=candidateWindowClass
def RegisterToolTipWindow(type, createToolTipWindow):
	createToolTipWindowDict[type]=createToolTipWindow

app.SetDefaultFontName(localeInfo.UI_DEF_FONT)

class __mem_func__:
	class __noarg_call__:
		def __init__(self, cls, obj, func):
			self.cls=cls
			self.obj=proxy(obj)
			self.func=proxy(func)

		def __call__(self, *arg):
			return self.func(self.obj)

	class __arg_call__:
		def __init__(self, cls, obj, func):
			self.cls=cls
			self.obj=proxy(obj)
			self.func=proxy(func)

		def __call__(self, *arg):
			return self.func(self.obj, *arg)

	def __init__(self, mfunc):
		if mfunc.im_func.func_code.co_argcount>1:
			self.call=__mem_func__.__arg_call__(mfunc.im_class, mfunc.im_self, mfunc.im_func)
		else:
			self.call=__mem_func__.__noarg_call__(mfunc.im_class, mfunc.im_self, mfunc.im_func)

	def __call__(self, *arg):
		return self.call(*arg)


class Window(object):
	def NoneMethod(cls):
		pass

	NoneMethod = classmethod(NoneMethod)

	def __init__(self, layer = "UI"):
		self.hWnd = None
		self.parentWindow = 0
		self.onMouseLeftButtonUpEvent = None
		self.onRunMouseWheelEvent = None
		self.RegisterWindow(layer)
		self.Hide()

		self.exPos = (0, 0)

		if app.ENABLE_RENEWAL_QUEST:
			self.propertyList = {}

		if app.ENABLE_INGAME_WIKI_SYSTEM:
			self.itsRendered = FALSE
			self.itsNeedDoubleRender = FALSE
			self.sortIndex = 0

		if app.ENABLE_FISH_GAME:
			self.onMoveDoneFunc = None

		self.mouseLeftButtonDownEvent = None
		self.mouseLeftButtonDownArgs = None
		self.mouseLeftButtonUpEvent = None
		self.mouseLeftButtonUpArgs = None
		self.mouseLeftButtonDoubleClickEvent = None
		self.mouseRightButtonDownEvent = None
		self.mouseRightButtonDownArgs = None
		self.mouseRightButtonUpEvent = None
		self.mouseRightButtonUpArgs = None
		self.mouseOverInEvent = None
		self.mouseOverInArgs = None
		self.mouseOverOutEvent = None
		self.mouseOverOutArgs = None
		self.moveWindowEvent = None
		self.renderEvent = None
		self.renderArgs = None

		self.overInEvent = None
		self.overInArgs = None

		self.overOutEvent = None
		self.overOutArgs = None

		self.baseX = 0
		self.baseY = 0

		self.SetWindowName("NONAME_Window")

	def __del__(self):
		wndMgr.Destroy(self.hWnd)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.Register(self, layer)

	def Destroy(self):
		pass

	def GetWindowHandle(self):
		return self.hWnd

	def AddFlag(self, style):
		wndMgr.AddFlag(self.hWnd, style)

	def IsRTL(self):
		return wndMgr.IsRTL(self.hWnd)

	def SetWindowName(self, Name):
		wndMgr.SetName(self.hWnd, Name)

	def GetWindowName(self):
		return wndMgr.GetName(self.hWnd)

	def SetParent(self, parent):
		if parent:
			wndMgr.SetParent(self.hWnd, parent.hWnd)
		else:
			wndMgr.SetParent(self.hWnd, 0)

	def SetAttachParent(self, parent):
		wndMgr.SetAttachParent(self.hWnd, parent.hWnd)

	def SetParentProxy(self, parent):
		self.parentWindow=proxy(parent)
		wndMgr.SetParent(self.hWnd, parent.hWnd)

	def GetParentProxy(self):
		return self.parentWindow

	def SetPickAlways(self):
		wndMgr.SetPickAlways(self.hWnd)

	def SetWindowHorizontalAlignLeft(self):
		wndMgr.SetWindowHorizontalAlign(self.hWnd, wndMgr.HORIZONTAL_ALIGN_LEFT)

	def SetWindowHorizontalAlignCenter(self):
		wndMgr.SetWindowHorizontalAlign(self.hWnd, wndMgr.HORIZONTAL_ALIGN_CENTER)

	def SetWindowHorizontalAlignRight(self):
		wndMgr.SetWindowHorizontalAlign(self.hWnd, wndMgr.HORIZONTAL_ALIGN_RIGHT)

	def SetWindowVerticalAlignTop(self):
		wndMgr.SetWindowVerticalAlign(self.hWnd, wndMgr.VERTICAL_ALIGN_TOP)

	def SetWindowVerticalAlignCenter(self):
		wndMgr.SetWindowVerticalAlign(self.hWnd, wndMgr.VERTICAL_ALIGN_CENTER)

	def SetWindowVerticalAlignBottom(self):
		wndMgr.SetWindowVerticalAlign(self.hWnd, wndMgr.VERTICAL_ALIGN_BOTTOM)

	def SetTop(self):
		wndMgr.SetTop(self.hWnd)

	def Show(self):
		wndMgr.Show(self.hWnd)

	def Hide(self):
		wndMgr.Hide(self.hWnd)

	def SetVisible(self, is_show):
		if is_show:
			self.Show()
		else:
			self.Hide()

	def Lock(self):
		wndMgr.Lock(self.hWnd)

	def Unlock(self):
		wndMgr.Unlock(self.hWnd)

	def IsShow(self):
		return wndMgr.IsShow(self.hWnd)

	def UpdateRect(self):
		wndMgr.UpdateRect(self.hWnd)

	def SetSize(self, width, height):
		wndMgr.SetWindowSize(self.hWnd, width, height)

	def GetWidth(self):
		return wndMgr.GetWindowWidth(self.hWnd)

	def GetHeight(self):
		return wndMgr.GetWindowHeight(self.hWnd)

	def GetLocalPosition(self):
		return wndMgr.GetWindowLocalPosition(self.hWnd)

	def GetLeft(self):
		x, y = self.GetLocalPosition()
		return x

	def GetGlobalLeft(self):
		x, y = self.GetGlobalPosition()
		return x

	def GetTop(self):
		x, y = self.GetLocalPosition()
		return y

	def GetGlobalTop(self):
		x, y = self.GetGlobalPosition()
		return y

	def GetRight(self):
		return self.GetLeft() + self.GetWidth()

	def GetBottom(self):
		return self.GetTop() + self.GetHeight()

	def GetGlobalPosition(self):
		return wndMgr.GetWindowGlobalPosition(self.hWnd)

	def GetMouseLocalPosition(self):
		return wndMgr.GetMouseLocalPosition(self.hWnd)

	def GetRect(self):
		return wndMgr.GetWindowRect(self.hWnd)

	def SetLeft(self, x):
		wndMgr.SetWindowPosition(self.hWnd, x, self.GetTop())

	def SetPosition(self, x, y, flag = FALSE):
		if flag == TRUE:
			self.exPos = (x, y)
		wndMgr.SetWindowPosition(self.hWnd, x, y)

	def SetCenterPosition(self, x = 0, y = 0):
		self.SetPosition((wndMgr.GetScreenWidth() - self.GetWidth()) / 2 + x, (wndMgr.GetScreenHeight() - self.GetHeight()) / 2 + y)

	def SavePosition(self):
		self.baseX = self.GetLeft()
		self.baseY = self.GetTop()

	def UpdatePositionByScale(self, scale):
		self.SetPosition(self.baseX * scale, self.baseY * scale)

	def IsFocus(self):
		return wndMgr.IsFocus(self.hWnd)

	def SetFocus(self):
		wndMgr.SetFocus(self.hWnd)

	def KillFocus(self):
		wndMgr.KillFocus(self.hWnd)

	def GetChildCount(self):
		return wndMgr.GetChildCount(self.hWnd)

	def IsIn(self):
		return wndMgr.IsIn(self.hWnd)

	def SetMouseRightButtonUpEvent(self, event, *args):
		self.mouseRightButtonUpEvent = event
		self.mouseRightButtonUpArgs = args

	def OnMouseRightButtonUp(self):
		if self.mouseRightButtonUpEvent:
			apply(self.mouseRightButtonUpEvent, self.mouseRightButtonUpArgs)

	def SetOnMouseLeftButtonUpEvent(self, event):
		self.onMouseLeftButtonUpEvent = event

	def IsInPosition(self):
		xMouse, yMouse = wndMgr.GetMousePosition()
		x, y = self.GetGlobalPosition()
		return xMouse >= x and xMouse < x + self.GetWidth() and yMouse >= y and yMouse < y + self.GetHeight()

	def SetMouseLeftButtonDownEvent(self, event, *args):
		self.mouseLeftButtonDownEvent = event
		self.mouseLeftButtonDownArgs = args

	def SetMouseLeftButtonDoubleClickEvent(self, event):
		self.mouseLeftButtonDoubleClickEvent = event

	def OnMouseLeftButtonDoubleClick(self):
		if self.mouseLeftButtonDoubleClickEvent:
			self.mouseLeftButtonDoubleClickEvent()

	def SetMouseRightButtonDownEvent(self, event, *args):
		self.mouseRightButtonDownEvent = event
		self.mouseRightButtonDownArgs = args

	def OnMouseRightButtonDown(self):
		if self.mouseRightButtonDownEvent:
			apply(self.mouseRightButtonDownEvent, self.mouseRightButtonDownArgs)

	def SetMouseLeftButtonUpEvent(self, event, *args):
		self.mouseLeftButtonUpEvent = event
		self.mouseLeftButtonUpArgs = args

	def SetMouseOverInEvent(self, event, *args):
		self.mouseOverInEvent = event
		self.mouseOverInArgs = args

	def SetMouseOverOutEvent(self, event, *args):
		self.mouseOverOutEvent = event
		self.mouseOverOutArgs = args

	def SetMoveWindowEvent(self, event):
		self.moveWindowEvent = event

	def OnMoveWindow(self, x, y):
		if self.moveWindowEvent:
			self.moveWindowEvent(x, y)

	def SAFE_SetOverInEvent(self, func, *args):
		self.overInEvent = __mem_func__(func)
		self.overInArgs = args

	def SetOverInEvent(self, func, *args):
		self.overInEvent = func
		self.overInArgs = args

	def SAFE_SetOverOutEvent(self, func, *args):
		self.overOutEvent = __mem_func__(func)
		self.overOutArgs = args

	def SetOverOutEvent(self, func, *args):
		self.overOutEvent = func
		self.overOutArgs = args

	def OnMouseOverIn(self):
		if self.overInEvent:
			apply(self.overInEvent, self.overInArgs)

	def OnMouseOverOut(self):
		if self.overOutEvent:
			apply(self.overOutEvent, self.overOutArgs)

	def SAFE_SetRenderEvent(self, event, *args):
		self.renderEvent = __mem_func__(event)
		self.renderArgs = args

	def ClearRenderEvent(self):
		self.renderEvent = None
		self.renderArgs = None

	def OnRender(self):
		if self.renderEvent:
			apply(self.renderEvent, self.renderArgs)

	def OnMouseLeftButtonDown(self):
		if self.mouseLeftButtonDownEvent:
			apply(self.mouseLeftButtonDownEvent, self.mouseLeftButtonDownArgs)

	def OnMouseLeftButtonUp(self):
		if self.onMouseLeftButtonUpEvent:
			self.onMouseLeftButtonUpEvent()

	def SetOnRunMouseWheelEvent(self, event):
		self.onRunMouseWheelEvent = event

	def OnRunMouseWheel(self, nLen):
		if self.onRunMouseWheelEvent:
			apply(self.onRunMouseWheelEvent, (bool(nLen < 0), ))
			return TRUE

		return FALSE

	if app.ENABLE_RENEWAL_QUEST:
		def SetProperty(self, propName, propValue):
			self.propertyList[propName] = propValue

		def GetProperty(self, propName):
			if propName in self.propertyList:
				return self.propertyList[propName]

			return None

	if app.ENABLE_CLIP_MASKING:
		def SetClippingMaskRect(self, left, top, right, bottom):
			wndMgr.SetClippingMaskRect(self.hWnd, left, top, right, bottom)

		def SetClippingMaskWindow(self, clipping_mask_window):
			wndMgr.SetClippingMaskWindow(self.hWnd, clipping_mask_window.hWnd)

class ListBoxEx(Window):
	class Item(Window):
		def __init__(self):
			Window.__init__(self)

		def __del__(self):
			Window.__del__(self)

		def SetParent(self, parent):
			Window.SetParent(self, parent)
			self.parent=proxy(parent)

		def OnMouseLeftButtonDown(self):
			self.parent.SelectItem(self)

		def OnRender(self):
			if self.parent.GetSelectedItem()==self:
				self.OnSelectedRender()

		def OnSelectedRender(self):
			x, y = self.GetGlobalPosition()
			grp.SetColor(grp.GenerateColor(0.0, 0.0, 0.7, 0.7))
			grp.RenderBar(x, y, self.GetWidth(), self.GetHeight())

	def __init__(self):
		Window.__init__(self)

		self.viewItemCount = 10
		self.basePos = 0
		self.itemHeight = 16
		self.itemStep = 20
		self.selItem = 0
		self.itemList = []
		self.onSelectItemEvent = lambda *arg: None

		self.itemWidth = 100

		self.scrollBar = None
		self.__UpdateSize()

	def __del__(self):
		Window.__del__(self)

	def __UpdateSize(self):
		height=self.itemStep*self.__GetViewItemCount()

		self.SetSize(self.itemWidth, height)

	def IsEmpty(self):
		if len(self.itemList) == 0:
			return 1
		return 0

	def SetItemStep(self, itemStep):
		self.itemStep = itemStep
		self.__UpdateSize()

	def SetItemSize(self, itemWidth, itemHeight):
		self.itemWidth = itemWidth
		self.itemHeight = itemHeight
		self.__UpdateSize()

	def SetViewItemCount(self, viewItemCount):
		self.viewItemCount = viewItemCount

	def SetSelectEvent(self, event):
		self.onSelectItemEvent = event

	def SetBasePos(self, basePos):
		if app.ENABLE_CLIP_MASKING:
			self.basePos = basePos

			curbp = self.basePos

			itemheight = self.itemStep * len(self.itemList)
			myheight = self.GetHeight()

			if itemheight < myheight:
				curbp = 0

			fromPos = curbp
			curPos = 0
			toPos = curbp + self.GetHeight()
			for item in self.itemList:
				if curPos + self.itemStep < fromPos or curPos > toPos:
					item.Hide()
				else:
					item.Show()

				item.SetPosition(0, curPos - fromPos)
				curPos += self.itemStep
		else:
			for oldItem in self.itemList[self.basePos:self.basePos + self.viewItemCount]:
				oldItem.Hide()

			self.basePos = basePos

			pos=basePos
			for newItem in self.itemList[self.basePos:self.basePos + self.viewItemCount]:
				(x, y) = self.GetItemViewCoord(pos, newItem.GetWidth())
				newItem.SetPosition(x, y)
				newItem.Show()
				pos += 1

	def GetItemIndex(self, argItem):
		return self.itemList.index(argItem)

	def GetSelectedItem(self):
		return self.selItem

	def SelectIndex(self, index):

		if index >= len(self.itemList) or index < 0:
			self.selItem = None
			return

		try:
			self.selItem = self.itemList[index]
		except:
			pass

	def SelectItem(self, selItem):
		self.selItem = selItem
		self.onSelectItemEvent(selItem)

	def RemoveAllItems(self):
		self.selItem = None
		self.itemList = []

		if self.scrollBar:
			self.scrollBar.SetPos(0)

	if app.ENABLE_RENEWAL_SWITCHBOT:
		def GetItems(self):
			return self.itemList

	def RemoveItem(self, delItem):
		if delItem == self.selItem:
			self.selItem = None

		self.itemList.remove(delItem)

	def AppendItem(self, newItem):
		newItem.SetParent(self)
		newItem.SetSize(self.itemWidth, self.itemHeight)

		if app.ENABLE_CLIP_MASKING:
			newItem.SetClippingMaskWindow(self)

		pos = len(self.itemList)
		if self.__IsInViewRange(pos):
			(x, y) = self.GetItemViewCoord(pos, newItem.GetWidth())
			newItem.SetPosition(x, y)
			newItem.Show()
		else:
			newItem.Hide()

		self.itemList.append(newItem)

	if app.ENABLE_RENEWAL_OFFLINESHOP:
		def AppendItemWithIndex(self, index, newItem):
			newItem.SetParent(self)
			newItem.SetSize(self.itemWidth, self.itemHeight)

			pos=len(self.itemList)
			if self.__IsInViewRange(pos):
				(x, y) = self.GetItemViewCoord(pos, newItem.GetWidth())
				newItem.SetPosition(x, y)
				newItem.Show()
			else:
				newItem.Hide()

			self.itemList.insert(index, newItem)

	def SetScrollBar(self, scrollBar):
		scrollBar.SetScrollEvent(__mem_func__(self.__OnScroll))
		self.scrollBar = scrollBar

	def __OnScroll(self):
		if app.ENABLE_CLIP_MASKING:
			self.SetBasePos(int(self.scrollBar.GetPos() * (self.__GetItemCount() - 1) * self.itemStep))
		else:
			self.SetBasePos(int(self.scrollBar.GetPos() * self.__GetScrollLen()))

	def __GetScrollLen(self):
		scrollLen = self.__GetItemCount() - self.__GetViewItemCount()
		if scrollLen < 0:
			return 0

		return scrollLen

	def __GetViewItemCount(self):
		return self.viewItemCount

	def __GetItemCount(self):
		return len(self.itemList)

	def GetItemViewCoord(self, pos, itemWidth):
		return (0, (pos-self.basePos) * self.itemStep)

	def __IsInViewRange(self, pos):
		if pos < self.basePos:
			return 0
		if pos >= self.basePos+self.viewItemCount:
			return 0
		return 1

class CandidateListBox(ListBoxEx):

	HORIZONTAL_MODE = 0
	VERTICAL_MODE = 1

	class Item(ListBoxEx.Item):
		def __init__(self, text):
			ListBoxEx.Item.__init__(self)

			self.textBox=TextLine()
			self.textBox.SetParent(self)
			self.textBox.SetText(text)
			self.textBox.Show()

		def __del__(self):
			ListBoxEx.Item.__del__(self)

	def __init__(self, mode = HORIZONTAL_MODE):
		ListBoxEx.__init__(self)
		self.itemWidth=32
		self.itemHeight=32
		self.mode = mode

	def __del__(self):
		ListBoxEx.__del__(self)

	def SetMode(self, mode):
		self.mode = mode

	def AppendItem(self, newItem):
		ListBoxEx.AppendItem(self, newItem)

	def GetItemViewCoord(self, pos):
		if self.mode == self.HORIZONTAL_MODE:
			return ((pos-self.basePos)*self.itemStep, 0)
		elif self.mode == self.VERTICAL_MODE:
			return (0, (pos-self.basePos)*self.itemStep)

class TextLine(Window):
	def __init__(self):
		Window.__init__(self)
		self.max = 0
		self.SetFontName(localeInfo.UI_DEF_FONT)

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterTextLine(self, layer)

	def SetMax(self, max):
		wndMgr.SetMax(self.hWnd, max)

	def SetLimitWidth(self, width):
		wndMgr.SetLimitWidth(self.hWnd, width)

	def SetMultiLine(self):
		wndMgr.SetMultiLine(self.hWnd, TRUE)

	def SetHorizontalAlignArabic(self):
		wndMgr.SetHorizontalAlign(self.hWnd, wndMgr.TEXT_HORIZONTAL_ALIGN_ARABIC)

	def SetHorizontalAlignLeft(self):
		wndMgr.SetHorizontalAlign(self.hWnd, wndMgr.TEXT_HORIZONTAL_ALIGN_LEFT)

	def SetHorizontalAlignRight(self):
		wndMgr.SetHorizontalAlign(self.hWnd, wndMgr.TEXT_HORIZONTAL_ALIGN_RIGHT)

	def SetHorizontalAlignCenter(self):
		wndMgr.SetHorizontalAlign(self.hWnd, wndMgr.TEXT_HORIZONTAL_ALIGN_CENTER)

	def SetVerticalAlignTop(self):
		wndMgr.SetVerticalAlign(self.hWnd, wndMgr.TEXT_VERTICAL_ALIGN_TOP)

	def SetVerticalAlignBottom(self):
		wndMgr.SetVerticalAlign(self.hWnd, wndMgr.TEXT_VERTICAL_ALIGN_BOTTOM)

	def SetVerticalAlignCenter(self):
		wndMgr.SetVerticalAlign(self.hWnd, wndMgr.TEXT_VERTICAL_ALIGN_CENTER)

	def SetSecret(self, Value = TRUE):
		wndMgr.SetSecret(self.hWnd, Value)

	def SetOutline(self, Value = TRUE):
		wndMgr.SetOutline(self.hWnd, Value)

	def SetFeather(self, value = TRUE):
		wndMgr.SetFeather(self.hWnd, value)

	def SetFontName(self, fontName):
		wndMgr.SetFontName(self.hWnd, fontName)

	def SetDefaultFontName(self):
		wndMgr.SetFontName(self.hWnd, localeInfo.UI_DEF_FONT)

	def SetFontColor(self, red, green, blue):
		wndMgr.SetFontColor(self.hWnd, red, green, blue)

	def SetPackedFontColor(self, color):
		wndMgr.SetFontColor(self.hWnd, color)

	def SetTextColor(self, color):
		wndMgr.SetFontColor(self.hWnd, color)

	def SetText(self, text):
		wndMgr.SetText(self.hWnd, text)

	if app.ENABLE_MULTI_TEXTLINE:
		def GetTextLineCount(self):
			return wndMgr.GetTextLineCount(self.hWnd)

		def DisableEnterToken(self):
			wndMgr.DisableEnterToken(self.hWnd)

		def SetLineHeight(self, height):
			wndMgr.SetLineHeight(self.hWnd, height)

		def GetLineHeight(self):
			return wndMgr.GetLineHeight(self.hWnd)

	def GetText(self):
		return wndMgr.GetText(self.hWnd)

	def GetTextWidth(self):
		(w, h) = self.GetTextSize()
		return w

	def GetTextHeight(self):
		(w, h) = self.GetTextSize()
		return h

	def GetTextSize(self):
		return wndMgr.GetTextSize(self.hWnd)

class EmptyCandidateWindow(Window):
	def __init__(self):
		Window.__init__(self)

	def __del__(self):
		Window.__init__(self)

	def Load(self):
		pass

	def SetCandidatePosition(self, x, y, textCount):
		pass

	def Clear(self):
		pass

	def Append(self, text):
		pass

	def Refresh(self):
		pass

	def Select(self):
		pass

class TextLink(Window):

	NORMAL_COLOR =  0xffa08784
	OVER_COLOR = 0xffc8aa80
	DOWN_COLOR = 0xffefe4cd

	def __init__(self):
		Window.__init__(self)

		self.eventFunc = None
		self.eventArgs = None

		self.text = TextLine()
		self.text.SetParent(self)
		self.text.SetPackedFontColor(self.NORMAL_COLOR)
		self.text.Show()

		self.underline = TextLine()
		self.underline.SetParent(self)
		self.underline.SetPackedFontColor(self.NORMAL_COLOR)
		self.underline.Hide()

	def __del__(self):
		Window.__del__(self)

	def SetText(self, text):
		self.text.SetText(text)
		self.SetSize(self.text.GetTextSize()[0], self.text.GetTextSize()[1])
		self.underline.SetPosition(-20, self.text.GetTextSize()[1])
		self.underline.SetWindowHorizontalAlignCenter()
		self.underline.SetSize(self.text.GetTextSize()[0], 0)

	def OnMouseOverIn(self):
		self.text.SetPackedFontColor(self.OVER_COLOR)
		self.underline.Show()

	def OnMouseOverOut(self):
		self.text.SetPackedFontColor(self.NORMAL_COLOR)
		self.underline.Hide()

	def OnMouseLeftButtonDown(self):
		self.text.SetPackedFontColor(self.DOWN_COLOR)
		self.underline.SetPackedFontColor(self.DOWN_COLOR)
		self.underline.Show()

	def OnMouseLeftButtonUp(self):
		if self.eventFunc:
			apply(self.eventFunc, self.eventArgs)
		self.OnMouseOverOut()

	def SetEvent(self, event, *args):
		self.eventFunc = event
		self.eventArgs = args

class EditLine(TextLine):
	candidateWindowClassDict = {}

	def __init__(self):
		TextLine.__init__(self)

		self.eventReturn = Window.NoneMethod
		self.eventEscape = Window.NoneMethod
		self.eventTab = None
		self.eventUpdate = None
		self.numberMode = FALSE
		self.useIME = TRUE

		self.bCodePage = FALSE

		self.infoMsg = ""
		self.backText = None
		self.isNeedEmpty = TRUE

		self.candidateWindowClass = None
		self.candidateWindow = None
		self.SetCodePage(app.GetDefaultCodePage())

		self.readingWnd = ReadingWnd()
		self.readingWnd.Hide()

		self.overLay = TextLine()
		self.overLay.SetParent(self)
		self.overLay.SetPosition(0, 0)
		self.overLay.SetPackedFontColor(WHITE_COLOR)
		self.overLay.Hide()

	def __del__(self):
		TextLine.__del__(self)

		self.eventReturn = Window.NoneMethod
		self.eventEscape = Window.NoneMethod
		self.eventTab = None

	def SetCodePage(self, codePage):
		candidateWindowClass=EditLine.candidateWindowClassDict.get(codePage, EmptyCandidateWindow)
		self.__SetCandidateClass(candidateWindowClass)

	def __SetCandidateClass(self, candidateWindowClass):
		if self.candidateWindowClass==candidateWindowClass:
			return

		self.candidateWindowClass = candidateWindowClass
		self.candidateWindow = self.candidateWindowClass()
		self.candidateWindow.Load()
		self.candidateWindow.Hide()

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterTextLine(self, layer)

	def SAFE_SetReturnEvent(self, event):
		self.eventReturn = __mem_func__(event)

	def SetReturnEvent(self, event):
		self.eventReturn = event

	def SetEscapeEvent(self, event):
		self.eventEscape = event

	def SetTabEvent(self, event):
		self.eventTab = event

	def SetUpdateEvent(self, event):
		self.eventUpdate = event

	def SetOverlayText(self, text):
		self.overLay.SetText(text)
		self.__RefreshOverlay()

	def GetOverlayText(self):
		return self.overLay.GetText()

	def SetMax(self, max):
		self.max = max
		wndMgr.SetMax(self.hWnd, self.max)
		ime.SetMax(self.max)
		self.SetUserMax(self.max)

	if app.ENABLE_RENEWAL_SWITCHBOT:
		def SetMaxSizeMode(self, forceWidht = -1):
			self.max_size = self.GetWidth() if forceWidht == -1 else forceWidht

	def SetUserMax(self, max):
		self.userMax = max
		ime.SetUserMax(self.userMax)

	def SetNumberMode(self):
		self.numberMode = TRUE

	def SetInfoMessage(self, msg):
		self.infoMsg = msg
		if self.backText == None:
			self.backText = TextLine()
			self.backText.SetParent(self)
			self.backText.SetPosition(0, 0)
			self.backText.SetFontColor(128, 128, 128)

		self.backText.SetText(msg)

		if self.isNeedEmpty:
			if len(self.GetText()) > 0:
				self.backText.Hide()
			else:
				self.backText.Show()
		else:
			self.backText.Show()

	def GetDisplayText(self):
		if self.GetText():
			return self.GetText()
		else:
			return self.overLay.GetText()

	def __RefreshOverlay(self):
		if len(self.GetText()):
			self.overLay.Hide()
		else:
			self.overLay.Show()

	def HideOverLay(self):
		if self.overLay:
			self.overLay.Hide()

	def IsShowCursor(self):
		return wndMgr.IsShowCursor(self.hWnd)

	if app.ENABLE_RENEWAL_CUBE:
		def CanEdit(self, flag):
			self.CanClick = flag

	def SetIMEFlag(self, flag):
		self.useIME = flag

	if app.ENABLE_EMOTICONS_SYSTEM:
		def SetTextEmoji(self, text):
			wndMgr.SetText(self.hWnd, text)

	def SetText(self, text):
		wndMgr.SetText(self.hWnd, text)

		if self.IsFocus():
			ime.SetText(text)

		self.__RefreshOverlay()

	def Enable(self):
		wndMgr.ShowCursor(self.hWnd)

	def Disable(self):
		wndMgr.HideCursor(self.hWnd)

	def SetEndPosition(self):
		ime.MoveEnd()

	def OnSetFocus(self):
		Text = self.GetText()
		ime.SetText(Text)
		ime.SetMax(self.max)
		ime.SetUserMax(self.userMax)
		ime.SetCursorPosition(-1)
		if self.numberMode:
			ime.SetNumberMode()
		else:
			ime.SetStringMode()
		ime.EnableCaptureInput()
		if self.useIME:
			ime.EnableIME()
		else:
			ime.DisableIME()
		wndMgr.ShowCursor(self.hWnd, TRUE)
		self.__RefreshOverlay()

	def OnKillFocus(self):
		self.SetText(ime.GetText(self.bCodePage))
		self.OnIMECloseCandidateList()
		self.OnIMECloseReadingWnd()
		ime.DisableIME()
		ime.DisableCaptureInput()
		wndMgr.HideCursor(self.hWnd)
		self.__RefreshOverlay()

	def OnIMEChangeCodePage(self):
		self.SetCodePage(ime.GetCodePage())

	def OnIMEOpenCandidateList(self):
		self.candidateWindow.Show()
		self.candidateWindow.Clear()
		self.candidateWindow.Refresh()

		gx, gy = self.GetGlobalPosition()
		self.candidateWindow.SetCandidatePosition(gx, gy, len(self.GetText()))

		return TRUE

	def OnIMECloseCandidateList(self):
		self.candidateWindow.Hide()
		return TRUE

	def OnIMEOpenReadingWnd(self):
		gx, gy = self.GetGlobalPosition()
		textlen = len(self.GetText())-2
		reading = ime.GetReading()
		readinglen = len(reading)
		self.readingWnd.SetReadingPosition( gx + textlen*6-24-readinglen*6, gy )
		self.readingWnd.SetText(reading)
		if ime.GetReadingError() == 0:
			self.readingWnd.SetTextColor(0xffffffff)
		else:
			self.readingWnd.SetTextColor(0xffff0000)
		self.readingWnd.SetSize(readinglen * 6 + 4, 19)
		self.readingWnd.Show()
		return TRUE

	def OnIMECloseReadingWnd(self):
		self.readingWnd.Hide()
		return TRUE

	def OnIMEUpdate(self):
		snd.PlaySound("sound/ui/type.wav")
		TextLine.SetText(self, ime.GetText(self.bCodePage))

		self.__RefreshOverlay()

		if self.eventUpdate:
			self.eventUpdate()

		if self.backText:
			if self.isNeedEmpty:
				if len(self.GetText()) > 0:
					self.backText.Hide()
				else:
					self.backText.Show()
			else:
				self.backText.Show()

	def OnIMETab(self):
		if self.eventTab:
			self.eventTab()
			return TRUE

		return FALSE

	def OnIMEReturn(self):
		snd.PlaySound("sound/ui/click.wav")
		self.eventReturn()

		return TRUE

	def OnPressEscapeKey(self):
		self.eventEscape()
		return TRUE

	def OnKeyDown(self, key):
		if app.DIK_F1 == key:
			return FALSE
		if app.DIK_F2 == key:
			return FALSE
		if app.DIK_F3 == key:
			return FALSE
		if app.DIK_F4 == key:
			return FALSE
		if app.DIK_LALT == key:
			return FALSE
		if app.DIK_SYSRQ == key:
			return FALSE
		if app.DIK_LCONTROL == key:
			return FALSE
		if app.DIK_V == key:
			if app.IsPressed(app.DIK_LCONTROL):
				ime.PasteTextFromClipBoard()

		return TRUE

	def OnKeyUp(self, key):
		if app.DIK_F1 == key:
			return FALSE
		if app.DIK_F2 == key:
			return FALSE
		if app.DIK_F3 == key:
			return FALSE
		if app.DIK_F4 == key:
			return FALSE
		if app.DIK_LALT == key:
			return FALSE
		if app.DIK_SYSRQ == key:
			return FALSE
		if app.DIK_LCONTROL == key:
			return FALSE

		return TRUE

	def OnIMEKeyDown(self, key):
		# Left
		if app.VK_LEFT == key:
			ime.MoveLeft()
			return TRUE
		# Right
		if app.VK_RIGHT == key:
			ime.MoveRight()
			return TRUE

		# Home
		if app.VK_HOME == key:
			ime.MoveHome()
			return TRUE
		# End
		if app.VK_END == key:
			ime.MoveEnd()
			return TRUE

		# Delete
		if app.VK_DELETE == key:
			ime.Delete()
			TextLine.SetText(self, ime.GetText(self.bCodePage))
			return TRUE

		return TRUE

	def OnMouseLeftButtonDown(self):
		if FALSE == self.IsIn():
			return FALSE

		self.SetFocus()
		PixelPosition = wndMgr.GetCursorPosition(self.hWnd)
		ime.SetCursorPosition(PixelPosition)

class MarkBox(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterMarkBox(self, layer)

	def Load(self):
		wndMgr.MarkBox_Load(self.hWnd)

	def SetScale(self, scale):
		wndMgr.MarkBox_SetScale(self.hWnd, scale)

	def SetIndex(self, guildID):
		MarkID = guild.GuildIDToMarkID(guildID)
		wndMgr.MarkBox_SetImageFilename(self.hWnd, guild.GetMarkImageFilenameByMarkID(MarkID))
		wndMgr.MarkBox_SetIndex(self.hWnd, guild.GetMarkIndexByMarkID(MarkID))

	def SetAlpha(self, alpha):
		wndMgr.MarkBox_SetDiffuseColor(self.hWnd, 1.0, 1.0, 1.0, alpha)

class ImageBox(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.eventDict = {}
		self.eventFunc = {"mouse_click" : None, "mouse_over_in" : None, "mouse_over_out" : None}
		self.eventArgs = {"mouse_click" : None, "mouse_over_in" : None, "mouse_over_out" : None}

	def __del__(self):
		Window.__del__(self)

		self.eventFunc = None
		self.eventArgs = None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterImageBox(self, layer)

	def LoadImage(self, imageName):
		self.name = imageName
		wndMgr.LoadImage(self.hWnd, imageName)

		if len(self.eventDict)!=0:
			print "LOAD IMAGE", self, self.eventDict

	def SetDiffuseColor(self, r, g, b, a):
		wndMgr.SetDiffuseColor(self.hWnd, r, g, b, a)

	def SetAlpha(self, alpha):
		wndMgr.SetDiffuseColor(self.hWnd, 1.0, 1.0, 1.0, alpha)

	if app.ENABLE_RENEWAL_SWITCHBOT:
		def SetSwitchBotIconColor(self):
			wndMgr.SetDiffuseColor(self.hWnd, (79.0/255.0), (79.0/255.0),(79.0/255.0), 1.0)

	def GetWidth(self):
		return wndMgr.GetWidth(self.hWnd)

	def GetHeight(self):
		return wndMgr.GetHeight(self.hWnd)

	if app.ENABLE_NEW_DUNGEON_LIB:
		def SetCoolTime(self, time):
			wndMgr.SetCoolTimeImageBox(self.hWnd, time)

		def SetStartCoolTime(self, time):
			wndMgr.SetStartCoolTimeImageBox(self.hWnd, time)

	def SetStringEvent(self, event, func, *args):
		self.eventDict[event] = func
		self.eventArgs[event] = args

	def SAFE_SetStringEvent(self, event, func, *args):
		self.eventDict[event]=__mem_func__(func)
		self.eventArgs[event] = args

	def SetEvent(self, func, *args):
		self.eventFunc[args[0]] = func
		self.eventArgs[args[0]] = args

	def SAFE_SetEvent(self, func, *args):
		self.eventFunc[args[0]] = __mem_func__(func)
		self.eventArgs[args[0]] = args

	def OnMouseLeftButtonUp(self) :
		if self.eventFunc["mouse_click"]:
			apply(self.eventFunc["mouse_click"], self.eventArgs["mouse_click"])
		Window.OnMouseLeftButtonUp(self)

	def OnMouseOverIn(self) :
		if self.eventFunc["mouse_over_in"]:
			apply(self.eventFunc["mouse_over_in"], self.eventArgs["mouse_over_in"])

		if self.eventDict.has_key("MOUSE_OVER_IN"):
			if self.eventArgs["MOUSE_OVER_IN"]:
				apply(self.eventDict["MOUSE_OVER_IN"], self.eventArgs["MOUSE_OVER_IN"])
			else:
				self.eventDict["MOUSE_OVER_IN"]()

	def OnMouseOverOut(self):
		if self.eventFunc["mouse_over_out"]:
			apply(self.eventFunc["mouse_over_out"], self.eventArgs["mouse_over_out"])

	def LeftRightReverse(self):
		wndMgr.LeftRightReverseImageBox(self.hWnd)

		if self.eventDict.has_key("MOUSE_OVER_OUT"):
			if self.eventArgs["MOUSE_OVER_OUT"]:
				apply(self.eventDict["MOUSE_OVER_OUT"], self.eventArgs["MOUSE_OVER_OUT"])
			else:
				self.eventDict["MOUSE_OVER_OUT"]()

class NoticeBoxBoard(Window):
	CORNER_WIDTH = 11
	CORNER_HEIGHT = 11
	LINE_WIDTH = 11
	LINE_HEIGHT = 11
	BOARD_COLOR = grp.GenerateColor(0.165, 0.133, 0.098, 1.0)

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, msg, lifeTime= 2.0, layer="UI"):
		Window.__init__(self, layer)

		CornerFileNames = [
			"d:/ymir work/ui/pattern/notice_box/noti_box_left_top.png",
			"d:/ymir work/ui/pattern/notice_box/noti_box_left_bot.png",
			"d:/ymir work/ui/pattern/notice_box/noti_box_right_top.png",
			"d:/ymir work/ui/pattern/notice_box/noti_box_right_bot.png"
		]
		LineFileNames = [
			"d:/ymir work/ui/pattern/notice_box/noti_box_left.png",
			"d:/ymir work/ui/pattern/notice_box/noti_box_right.png",
			"d:/ymir work/ui/pattern/notice_box/noti_box_top.png",
			"d:/ymir work/ui/pattern/notice_box/noti_box_bot.png"
		]

		self.Corners = []
		for fn in CornerFileNames:
			corner = ExpandedImageBox()
			corner.AddFlag("attach")
			corner.AddFlag("not_pick")
			corner.LoadImage(fn)
			corner.SetParent(self)
			corner.Show()
			self.Corners.append(corner)

		self.Lines = []
		for fn in LineFileNames:
			line = ExpandedImageBox()
			line.AddFlag("attach")
			line.AddFlag("not_pick")
			line.LoadImage(fn)
			line.SetParent(self)
			line.Show()
			self.Lines.append(line)

		self.Base = Bar()
		self.Base.SetParent(self)
		self.Base.AddFlag("attach")
		self.Base.AddFlag("not_pick")
		self.Base.SetColor(self.BOARD_COLOR)
		self.Base.Show()

		self.SetSize(200, 32)
		self.SetCenterPosition()
		x, y = self.GetGlobalPosition()  # 
		self.SetPosition(x, y + 255) 
		self.AddFlag("float")
		self.Show()

		self.textLine = TextLine()
		self.textLine.SetParent(self)
		self.textLine.SetHorizontalAlignCenter()
		self.textLine.SetVerticalAlignCenter()
		self.textLine.SetPosition(self.GetWidth() / 2, self.GetHeight() / 2 -5 )
		self.textLine.SetText(msg)
		self.textLine.SetPackedFontColor(0xFFF5F5DC)
		self.textLine.Show()

		self.lifeTime = lifeTime
		self.startTime = app.GetTime()

	def SetSize(self, width, height):
		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Base.SetSize(width - self.CORNER_WIDTH*2, height - self.CORNER_HEIGHT*2)

	def OnUpdate(self):
		if self.lifeTime > 0 and (app.GetTime() - self.startTime > self.lifeTime):
			self.Hide()

class ExpandedImageBox(ImageBox):
	def __init__(self, layer = "UI"):
		ImageBox.__init__(self, layer)

	def __del__(self):
		ImageBox.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterExpandedImageBox(self, layer)

	def SetScale(self, xScale, yScale):
		wndMgr.SetScale(self.hWnd, xScale, yScale)

	def SetOrigin(self, x, y):
		wndMgr.SetOrigin(self.hWnd, x, y)

	def SetRotation(self, rotation):
		wndMgr.SetRotation(self.hWnd, rotation)

	def SetRenderingMode(self, mode):
		wndMgr.SetRenderingMode(self.hWnd, mode)

	def SetRenderingRect(self, left, top, right, bottom):
		wndMgr.SetRenderingRect(self.hWnd, left, top, right, bottom)

	if app.ENABLE_RENEWAL_BATTLE_PASS:
		def SetClipRect(self, left, top, right, bottom, isVertical = FALSE):
			wndMgr.SetClipRect(self.hWnd, left, top, right, bottom, isVertical)

	def SetPercentage(self, curValue, maxValue):
		if maxValue:
			self.SetRenderingRect(0.0, 0.0, -1.0 + float(curValue) / float(maxValue), 0.0)
		else:
			self.SetRenderingRect(0.0, 0.0, 0.0, 0.0)

	if app.ENABLE_RENEWAL_BATTLE_PASS:
		def SetPercentageEx(self, minValue, curValue, maxValue):
			if minValue and maxValue:
				self.SetRenderingRect(0.0, 0.0, -1.0 + (float(curValue) - float(minValue)) / (float(maxValue) - float(minValue)), 0.0)
			else:
				self.SetRenderingRect(0.0, 0.0, 0.0, 0.0)

	def GetWidth(self):
		return wndMgr.GetWindowWidth(self.hWnd)

	def GetHeight(self):
		return wndMgr.GetWindowHeight(self.hWnd)

class AniImageBox(Window):
	if app.ENABLE_FISH_GAME:
		def SetRotation(self, rotation):
			wndMgr.SetRotation(self.hWnd, rotation)

		def GetRotation(self):
			return wndMgr.GetRotation(self.hWnd)

		def MoveStart(self):
			wndMgr.MoveStart(self.hWnd)

		def MoveStop(self):
			wndMgr.MoveStop(self.hWnd)

		def SetMovePos(self, x, y):
			wndMgr.SetMovePos(self.hWnd, x, y)

		def SetMoveSpeed(self, speed):
			wndMgr.SetMoveSpeed(self.hWnd, speed)

		def OnMoveDone(self):
			if self.onMoveDoneFunc:
				self.onMoveDoneFunc()

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		if app.ENABLE_MINIGAME_OKEY_CARDS_SYSTEM:
			self.eventEndFrame = None

		if app.ENABLE_HUNTING_SYSTEM:
			self.endFrameEvent = None
			self.endFrameArgs = None

			self.keyFrameEvent = None

	def __del__(self):
		Window.__del__(self)

		if app.ENABLE_MINIGAME_OKEY_CARDS_SYSTEM:
			self.eventEndFrame = None

		if app.ENABLE_HUNTING_SYSTEM:
			self.endFrameEvent = None
			self.endFrameArgs = None

			self.keyFrameEvent = None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterAniImageBox(self, layer)

	def SetDelay(self, delay):
		wndMgr.SetDelay(self.hWnd, delay)

	def AppendImage(self, filename):
		wndMgr.AppendImage(self.hWnd, filename)

	def SetScale(self, xScale, yScale):
		wndMgr.SetAniImgScale(self.hWnd, xScale, yScale)

	def SetPercentage(self, curValue, maxValue):
		wndMgr.SetRenderingRect(self.hWnd, 0.0, 0.0, -1.0 + float(curValue) / float(maxValue), 0.0)

	def SetPercentageWithScale(self, curValue, maxValue):
		wndMgr.SetRenderingRectWithScale(self.hWnd, 0.0, 0.0, -1.0 + float(curValue) / float(maxValue), 0.0)

	if app.ENABLE_EVENT_MANAGER:
		def SetScale(self, xScale, yScale):
			wndMgr.SetAniImgScale(self.hWnd, xScale, yScale)

	if app.ENABLE_MINIGAME_OKEY_CARDS_SYSTEM:
		def ResetFrame(self):
			wndMgr.ResetFrame(self.hWnd)

		def SetOnEndFrame(self, event):
			self.eventEndFrame = event

		def OnEndFrame(self):
			if self.eventEndFrame:
				self.eventEndFrame()
	else:
		def OnEndFrame(self):
			pass

	if app.ENABLE_HUNTING_SYSTEM:
		def SetEndFrameEvent(self, event, *args):
			self.endFrameEvent = event
			self.endFrameArgs = args

		def SetKeyFrameEvent(self, event):
			self.keyFrameEvent = event

		def OnKeyFrame(self, curFrame):
			if self.keyFrameEvent:
				self.keyFrameEvent(curFrame)

class GifBox(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.eventDict={}
		self.arg = -1
		self.argOut = -1
		self.imageLoaded = False

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterGifImageBox(self, layer)

	def LoadImage(self, imageName):
		self.name=imageName
		wndMgr.LoadGif(self.hWnd, imageName)
		self.imageLoaded = True

		if len(self.eventDict)!=0:
			print "LOAD IMAGE", self, self.eventDict

	def UnloadImage(self):
		if self.imageLoaded:
			wndMgr.UnloadGif(self.hWnd)
			self.imageLoaded = False

	def SetAlpha(self, alpha):
		wndMgr.SetDiffuseColor(self.hWnd, 1.0, 1.0, 1.0, alpha)

	def SetDiffuseColor(self, r,g,b,a=1.0):
		wndMgr.SetDiffuseColor(self.hWnd, r,g,b,a)

	def SetAlphaColor(self, r,g,b,alpha=1.0):
		wndMgr.SetDiffuseColor(self.hWnd, r,g,b, alpha)

	def GetWidth(self):
		return wndMgr.GetWidth(self.hWnd)

	def GetHeight(self):
		return wndMgr.GetHeight(self.hWnd)

	def SetRenderingRect(self, left, top, right, bottom):
		wndMgr.SetRenderingRect(self.hWnd, left, top, right, bottom)

	def SetPercentage(self, curValue, maxValue):
		if maxValue:
			self.SetRenderingRect(0.0, 0.0, -1.0 + float(curValue) / float(maxValue), 0.0)
		else:
			self.SetRenderingRect(0.0, 0.0, 0.0, 0.0)

	def SetScale(self, xScale, yScale):
		wndMgr.SetScale(self.hWnd, xScale, yScale)

if app.ENABLE_AUTO_REFINE:
	class CheckBox(Window):
		def __init__(self):
			Window.__init__(self)

			self.backgroundImage = None
			self.checkImage = None

			self.eventFunc = { "ON_CHECK" : None, "ON_UNCKECK" : None, }
			self.eventArgs = { "ON_CHECK" : None, "ON_UNCKECK" : None, }

			self.CreateElements()

		def __del__(self):
			Window.__del__(self)

			self.backgroundImage = None
			self.checkImage = None

			self.eventFunc = { "ON_CHECK" : None, "ON_UNCKECK" : None, }
			self.eventArgs = { "ON_CHECK" : None, "ON_UNCKECK" : None, }

		def CreateElements(self):
			self.backgroundImage = ImageBox()
			self.backgroundImage.SetParent(self)
			self.backgroundImage.AddFlag("not_pick")
			self.backgroundImage.LoadImage("d:/ymir work/ui/game/refine/checkbox.tga")
			self.backgroundImage.Show()

			self.checkImage = ImageBox()
			self.checkImage.SetParent(self)
			self.checkImage.AddFlag("not_pick")
			self.checkImage.SetPosition(0, -4)
			self.checkImage.LoadImage("d:/ymir work/ui/game/refine/checked.tga")
			self.checkImage.Hide()

			self.textInfo = TextLine()
			self.textInfo.SetParent(self)
			self.textInfo.SetPosition(20, -2)
			self.textInfo.Show()

			self.SetSize(self.backgroundImage.GetWidth() + self.textInfo.GetTextSize()[0], self.backgroundImage.GetHeight() + self.textInfo.GetTextSize()[1])

		def SetTextInfo(self, info):
			if self.textInfo:
				self.textInfo.SetText(info)

			self.SetSize(self.backgroundImage.GetWidth() + self.textInfo.GetTextSize()[0], self.backgroundImage.GetHeight() + self.textInfo.GetTextSize()[1])

		def SetCheckStatus(self, flag):
			if flag:
				self.checkImage.Show()
			else:
				self.checkImage.Hide()

		def GetCheckStatus(self):
			if self.checkImage:
				return self.checkImage.IsShow()

			return FALSE

		def SetEvent(self, func, *args) :
			result = self.eventFunc.has_key(args[0])
			if result :
				self.eventFunc[args[0]] = func
				self.eventArgs[args[0]] = args
			else :
				print "[ERROR] ui.py SetEvent, Can`t Find has_key : %s" % args[0]

		def OnMouseLeftButtonUp(self):
			if self.checkImage:
				if self.checkImage.IsShow():
					self.checkImage.Hide()

					if self.eventFunc["ON_UNCKECK"]:
						apply(self.eventFunc["ON_UNCKECK"], self.eventArgs["ON_UNCKECK"])
				else:
					self.checkImage.Show()

					if self.eventFunc["ON_CHECK"]:
						apply(self.eventFunc["ON_CHECK"], self.eventArgs["ON_CHECK"])

class Button(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.eventFunc = None
		self.eventArgs = None

		self.TextChild = []

		if app.ENABLE_SKILL_COLOR_SYSTEM:
			self.overFunc = None
			self.overArgs = None
			self.overOutFunc = None
			self.overOutArgs = None

		self.ButtonText = None
		self.ToolTipText = None

		self.showTooltipEvent = None
		self.showTooltipArg = None
		self.hideTooltipEvent = None
		self.hideTooltipArg = None

	def __del__(self):
		Window.__del__(self)

		self.eventFunc = None
		self.eventArgs = None

		if app.ENABLE_SKILL_COLOR_SYSTEM:
			self.overFunc = None
			self.overArgs = None
			self.overOutFunc = None
			self.overOutArgs = None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterButton(self, layer)

	def SetUpVisual(self, filename):
		wndMgr.SetUpVisual(self.hWnd, filename)

	def SetOverVisual(self, filename):
		wndMgr.SetOverVisual(self.hWnd, filename)

	def SetDownVisual(self, filename):
		wndMgr.SetDownVisual(self.hWnd, filename)

	def SetDisableVisual(self, filename):
		wndMgr.SetDisableVisual(self.hWnd, filename)

	def GetUpVisualFileName(self):
		return wndMgr.GetUpVisualFileName(self.hWnd)

	def GetOverVisualFileName(self):
		return wndMgr.GetOverVisualFileName(self.hWnd)

	def GetDownVisualFileName(self):
		return wndMgr.GetDownVisualFileName(self.hWnd)

	def Flash(self):
		wndMgr.Flash(self.hWnd)

	def EnableFlash(self):
		wndMgr.EnableFlash(self.hWnd)

	def DisableFlash(self):
		wndMgr.DisableFlash(self.hWnd)

	def Enable(self):
		wndMgr.Enable(self.hWnd)

	def Disable(self):
		wndMgr.Disable(self.hWnd)

	def Down(self):
		wndMgr.Down(self.hWnd)

	def SetUp(self):
		wndMgr.SetUp(self.hWnd)

	def SAFE_SetEvent(self, func, *args):
		self.eventFunc = __mem_func__(func)
		self.eventArgs = args

	def SetEvent(self, func, *args):
		self.eventFunc = func
		self.eventArgs = args

	def LeftRightReverse(self) :
		wndMgr.LeftRightReverse(self.hWnd)

	def SetTextColor(self, color):
		if not self.ButtonText:
			return
		self.ButtonText.SetPackedFontColor(color)

	def SetOutline(self, Value=TRUE):
		if not self.ButtonText:
			return
		self.ButtonText.SetOutline(Value)

	def SetTextPosition(self, x, y):
		self.ButtonText.SetPosition(x, y)
		self.ButtonText.SetWindowHorizontalAlignCenter()
		self.ButtonText.SetWindowVerticalAlignCenter()

	def SetText(self, text, height = 4):

		if not self.ButtonText:
			textLine = TextLine()
			textLine.SetParent(self)
			textLine.SetPosition(self.GetWidth()/2, self.GetHeight()/2)
			textLine.SetVerticalAlignCenter()
			textLine.SetHorizontalAlignCenter()
			textLine.Show()
			self.ButtonText = textLine

		self.ButtonText.SetText(text)

	def AppendTextLineAllClear(self) : 
		self.TextChild = []

	def SetAppendTextChangeText(self, idx, text):
		if not len(self.TextChild) :
			return

			self.TextChild[idx].SetText(text)

	def SetAppendTextColor(self, idx, color) :
		if not len(self.TextChild) :
			return

		self.TextChild[idx].SetPackedFontColor(color)

	def AppendTextLine(self, text, font_size = localeInfo.UI_DEF_FONT, font_color = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0), text_sort = "center", pos_x = None, pos_y = None):
		textLine = TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(font_size)
		textLine.SetPackedFontColor(font_color)
		textLine.SetText(text)
		textLine.Show()

		if not pos_x and not pos_y :
			textLine.SetPosition(self.GetWidth()/2, self.GetHeight()/2)
		else :
			textLine.SetPosition(pos_x, pos_y)

		textLine.SetVerticalAlignCenter()
		if "center" == text_sort :
			textLine.SetHorizontalAlignCenter()
		elif "right" == text_sort :
			textLine.SetHorizontalAlignRight()
		elif "left" == 	text_sort :
			textLine.SetHorizontalAlignLeft()

		self.TextChild.append(textLine)

	def SetFormToolTipText(self, type, text, x, y):
		if not self.ToolTipText:
			toolTip=createToolTipWindowDict[type]()
			toolTip.SetParent(self)
			toolTip.SetSize(0, 0)
			toolTip.SetHorizontalAlignCenter()
			toolTip.SetOutline()
			toolTip.Hide()
			toolTip.SetPosition(x + self.GetWidth()/2, y)
			self.ToolTipText=toolTip

		self.ToolTipText.SetText(text)

	def SetToolTipWindow(self, toolTip):
		self.ToolTipText=toolTip
		self.ToolTipText.SetParentProxy(self)

	def SetToolTipText(self, text, x=0, y = -19):
		self.SetFormToolTipText("TEXT", text, x, y)

	def CallEvent(self):
		snd.PlaySound("sound/ui/click.wav")

		if self.eventFunc:
			apply(self.eventFunc, self.eventArgs)

	def ShowToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Show()

		if self.showTooltipEvent:
			apply(self.showTooltipEvent, self.showTooltipArg)

	def HideToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Hide()

		if self.hideTooltipEvent:
			apply(self.hideTooltipEvent, self.hideTooltipArg)

	def SetShowToolTipEvent(self, func, *args):
		self.showTooltipEvent = func
		self.showTooltipArg = args

	def SetHideToolTipEvent(self, func, *args):
		self.hideTooltipEvent = func
		self.hideTooltipArg = args

	def IsDown(self):
		return wndMgr.IsDown(self.hWnd)

	if app.ENABLE_EMOTICONS_SYSTEM:
		def SetButtonScale(self, xScale, yScale):
			wndMgr.SetButtonScale(self.hWnd, xScale, yScale)

	def ClearToolTip(self):
		self.TextChild = []
		self.ToolTipText = None

	if app.ENABLE_RENEWAL_QUEST:
		def GetText(self):
			if not self.ButtonText:
				return ""

			return self.ButtonText.GetText()

		def IsDIsable(self):
			return wndMgr.IsDIsable(self.hWnd)

		def SetTextAlignLeft(self, text, height = 4):
			if not self.ButtonText:
				textLine = TextLine()
				textLine.SetParent(self)
				textLine.SetPosition(27, self.GetHeight()/2)
				textLine.SetVerticalAlignCenter()
				textLine.SetHorizontalAlignLeft()
				textLine.Show()
				self.ButtonText = textLine

			self.ButtonText.SetText(text)
			self.ButtonText.SetPosition(27, self.GetHeight()/2)
			self.ButtonText.SetVerticalAlignCenter()
			self.ButtonText.SetHorizontalAlignLeft()

	if app.ENABLE_SKILL_COLOR_SYSTEM:
		def SetListText(self, text, x = 8):
			if not self.ButtonText:
				textLine = TextLine()
				textLine.SetParent(self)
				textLine.SetPosition(x, self.GetHeight()/2)
				textLine.SetVerticalAlignCenter()
				textLine.SetHorizontalAlignLeft()
				textLine.Show()
				self.ButtonText = textLine

			self.ButtonText.SetText(text)

		def OnMouseOverIn(self):
			if self.overFunc:
				apply(self.overFunc, self.overArgs)

		def OnMouseOverOut(self):
			if self.overOutFunc:
				apply(self.overOutFunc, self.overOutArgs)

		def SetOverEvent(self, func, *args):
			self.overFunc = func
			self.overArgs = args

		def SetOverOutEvent(self, func, *args):
			self.overOutFunc = func
			self.overOutArgs = args

	if app.ENABLE_DUNGEON_TRACKING_SYSTEM:
		def SetRenderingRect(self, left, top, right, bottom):
			wndMgr.SetRenderingRect(self.hWnd, left, top, right, bottom)

class RadioButton(Button):
	def __init__(self):
		Button.__init__(self)

	def __del__(self):
		Button.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterRadioButton(self, layer)

	def SetFontColor(self, color):
		if not self.ButtonText:
			return
		self.ButtonText.SetPackedFontColor(color)

	def SetOutline(self, Value=TRUE):
		if not self.ButtonText:
			return
		self.ButtonText.SetOutline(Value)

	def SetFontName(self, fontName):
		if not self.ButtonText:
			return
		self.ButtonText.SetFontName(fontName)

class RadioButtonGroup:
	def __init__(self):
		self.buttonGroup = []
		self.selectedBtnIdx = -1

	def __del__(self):
		self.buttonGroup = []
		self.selectedBtnIdx = -1

	def Show(self):
		for (button, selectEvent, unselectEvent) in self.buttonGroup:
			button.Show()

	def Hide(self):
		for (button, selectEvent, unselectEvent) in self.buttonGroup:
			button.Hide()

	def SetText(self, idx, text):
		if idx >= len(self.buttonGroup):
			return
		(button, selectEvent, unselectEvent) = self.buttonGroup[idx]
		button.SetText(text)

	def SetTextPosition(self, idx, x, y):
		if idx >= len(self.buttonGroup):
			return
		(button, selectEvent, unselectEvent) = self.buttonGroup[idx]
		button.SetTextPosition(x, y)

	def SetToolTipText(self, idx, text):
		if idx >= len(self.buttonGroup):
			return
		(button, selectEvent, unselectEvent) = self.buttonGroup[idx]
		button.SetToolTipText(text)

	def OnClick(self, btnIdx):
		if btnIdx == self.selectedBtnIdx:
			return

		(button, selectEvent, unselectEvent) = self.buttonGroup[self.selectedBtnIdx]

		if unselectEvent:
			unselectEvent(self.selectedBtnIdx)
		button.SetUp()

		self.selectedBtnIdx = btnIdx
		(button, selectEvent, unselectEvent) = self.buttonGroup[btnIdx]

		if selectEvent:
			selectEvent(btnIdx)

		button.Down()
 		
	def AddButton(self, button, selectEvent, unselectEvent):
		i = len(self.buttonGroup)
		button.SetEvent(__mem_func__(self.OnClick),i)
		self.buttonGroup.append([button, selectEvent, unselectEvent])
		button.SetUp()

	def Create(rawButtonGroup):
		radioGroup = RadioButtonGroup()
		for (button, selectEvent, unselectEvent) in rawButtonGroup:
			radioGroup.AddButton(button, selectEvent, unselectEvent)
		
		radioGroup.OnClick(0)
		
		return radioGroup
		
	Create=staticmethod(Create)

class ToggleButton(Button):
	def __init__(self):
		Button.__init__(self)

		self.eventUp = None
		self.eventDown = None

		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			self.eventUpArgs = None
			self.eventDownArgs = None

	def __del__(self):
		Button.__del__(self)

		self.eventUp = None
		self.eventDown = None

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def SetToggleUpEvent(self, event, *args):
			self.eventUp = event
			self.eventUpArgs = args

		def SetToggleDownEvent(self, event, *args):
			self.eventDown = event
			self.eventDownArgs = args
	else:
		def SetToggleUpEvent(self, event):
			self.eventUp = event

		def SetToggleDownEvent(self, event):
			self.eventDown = event

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterToggleButton(self, layer)

	def OnToggleUp(self):
		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			if self.eventUp:
				if self.eventUpArgs:
					apply(self.eventUp, self.eventUpArgs)
				else:
					self.eventUp()
		else:
			if self.eventUp:
				self.eventUp()

	def OnToggleDown(self):
		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			if self.eventDown:
				if self.eventDownArgs:
					apply(self.eventDown, self.eventDownArgs)
				else:
					self.eventDown()
		else:
			if self.eventDown:
				self.eventDown()

	def Enable(self):
		wndMgr.Enable(self.hWnd)

	def Disable(self):
		wndMgr.Disable(self.hWnd)

	def IsDisable(self):
		return wndMgr.IsDisable(self.hWnd)

class DragButton(Button):
	def __init__(self):
		Button.__init__(self)
		self.AddFlag("movable")

		self.callbackEnable = TRUE
		self.eventMove = lambda: None

	def __del__(self):
		Button.__del__(self)

		self.eventMove = lambda: None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterDragButton(self, layer)

	def SetMoveEvent(self, event):
		self.eventMove = event

	def SetRestrictMovementArea(self, x, y, width, height):
		wndMgr.SetRestrictMovementArea(self.hWnd, x, y, width, height)

	def TurnOnCallBack(self):
		self.callbackEnable = TRUE

	def TurnOffCallBack(self):
		self.callbackEnable = FALSE

	def OnMove(self):
		if self.callbackEnable:
			self.eventMove()

class NumberLine(Window):

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterNumberLine(self, layer)

	def SetHorizontalAlignCenter(self):
		wndMgr.SetNumberHorizontalAlignCenter(self.hWnd)

	def SetHorizontalAlignRight(self):
		wndMgr.SetNumberHorizontalAlignRight(self.hWnd)

	def SetPath(self, path):
		wndMgr.SetPath(self.hWnd, path)

	def SetNumber(self, number):
		wndMgr.SetNumber(self.hWnd, number)

###################################################################################################
## PythonScript Element
###################################################################################################

class Box(Window):

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterBox(self, layer)

	def SetColor(self, color):
		wndMgr.SetColor(self.hWnd, color)

class Bar(Window):

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterBar(self, layer)

	def SetColor(self, color):
		wndMgr.SetColor(self.hWnd, color)

class Line(Window):

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterLine(self, layer)

	def SetColor(self, color):
		wndMgr.SetColor(self.hWnd, color)

class SlotBar(Window):

	def __init__(self):
		Window.__init__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterBar3D(self, layer)

## Same with SlotBar
class Bar3D(Window):

	def __init__(self):
		Window.__init__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterBar3D(self, layer)

	def SetColor(self, left, right, center):
		wndMgr.SetColor(self.hWnd, left, right, center)

class SlotWindow(Window):

	def __init__(self):
		Window.__init__(self)

		self.StartIndex = 0

		self.eventSelectEmptySlot = None
		self.eventSelectItemSlot = None
		self.eventUnselectEmptySlot = None
		self.eventUnselectItemSlot = None
		self.eventUseSlot = None
		self.eventOverInItem = None
		self.eventOverOutItem = None
		self.eventPressedSlotButton = None

	def __del__(self):
		Window.__del__(self)

		self.eventSelectEmptySlot = None
		self.eventSelectItemSlot = None
		self.eventUnselectEmptySlot = None
		self.eventUnselectItemSlot = None
		self.eventUseSlot = None
		self.eventOverInItem = None
		self.eventOverOutItem = None
		self.eventPressedSlotButton = None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterSlotWindow(self, layer)

	def SetSlotStyle(self, style):
		wndMgr.SetSlotStyle(self.hWnd, style)

	def HasSlot(self, slotIndex):
		return wndMgr.HasSlot(self.hWnd, slotIndex)

	def SetSlotBaseImage(self, imageFileName, r, g, b, a):
		wndMgr.SetSlotBaseImage(self.hWnd, imageFileName, r, g, b, a)

	def SetCoverButton(self,\
						slotIndex,\
						upName="d:/ymir work/ui/public/slot_cover_button_01.sub",\
						overName="d:/ymir work/ui/public/slot_cover_button_02.sub",\
						downName="d:/ymir work/ui/public/slot_cover_button_03.sub",\
						disableName="d:/ymir work/ui/public/slot_cover_button_04.sub",\
						LeftButtonEnable = FALSE,\
						RightButtonEnable = TRUE):
		wndMgr.SetCoverButton(self.hWnd, slotIndex, upName, overName, downName, disableName, LeftButtonEnable, RightButtonEnable)

	def EnableCoverButton(self, slotIndex):
		wndMgr.EnableCoverButton(self.hWnd, slotIndex)

	def DisableCoverButton(self, slotIndex):
		wndMgr.DisableCoverButton(self.hWnd, slotIndex)
		
	def SetAlwaysRenderCoverButton(self, slotIndex, bAlwaysRender = TRUE):
		wndMgr.SetAlwaysRenderCoverButton(self.hWnd, slotIndex, bAlwaysRender)

	def AppendSlotButton(self, upName, overName, downName):
		wndMgr.AppendSlotButton(self.hWnd, upName, overName, downName)

	def ShowSlotButton(self, slotNumber):
		wndMgr.ShowSlotButton(self.hWnd, slotNumber)

	def HideAllSlotButton(self):
		wndMgr.HideAllSlotButton(self.hWnd)

	def AppendRequirementSignImage(self, filename):
		wndMgr.AppendRequirementSignImage(self.hWnd, filename)

	def ShowRequirementSign(self, slotNumber):
		wndMgr.ShowRequirementSign(self.hWnd, slotNumber)

	def HideRequirementSign(self, slotNumber):
		wndMgr.HideRequirementSign(self.hWnd, slotNumber)

	def ActivateSlot(self, slotNumber, colortype):
		wndMgr.ActivateSlot(self.hWnd, slotNumber, colortype)

	def DeactivateSlot(self, slotNumber):
		wndMgr.DeactivateSlot(self.hWnd, slotNumber)

	def ShowSlotBaseImage(self, slotNumber):
		wndMgr.ShowSlotBaseImage(self.hWnd, slotNumber)

	def HideSlotBaseImage(self, slotNumber):
		wndMgr.HideSlotBaseImage(self.hWnd, slotNumber)

	def SetSlotCoolTimeInverse(self, slotIndex, coolTime, elapsedTime = 0.0):
		wndMgr.SetSlotCoolTimeInverse(self.hWnd, slotIndex, coolTime, elapsedTime)

	def SetSlotScale(self, xScale, yScale):
		wndMgr.SetSlotScale(self.hWnd, xScale, yScale)

	def SAFE_SetButtonEvent(self, button, state, event):
		if "LEFT"==button:
			if "EMPTY"==state:
				self.eventSelectEmptySlot=__mem_func__(event)
			elif "EXIST"==state:
				self.eventSelectItemSlot=__mem_func__(event)
			elif "ALWAYS"==state:
				self.eventSelectEmptySlot=__mem_func__(event)
				self.eventSelectItemSlot=__mem_func__(event)
		elif "RIGHT"==button:
			if "EMPTY"==state:
				self.eventUnselectEmptySlot=__mem_func__(event)
			elif "EXIST"==state:
				self.eventUnselectItemSlot=__mem_func__(event)
			elif "ALWAYS"==state:
				self.eventUnselectEmptySlot=__mem_func__(event)
				self.eventUnselectItemSlot=__mem_func__(event)

	def SetSelectEmptySlotEvent(self, empty):
		self.eventSelectEmptySlot = empty

	def SetSelectItemSlotEvent(self, item):
		self.eventSelectItemSlot = item

	def SetUnselectEmptySlotEvent(self, empty):
		self.eventUnselectEmptySlot = empty

	def SetUnselectItemSlotEvent(self, item):
		self.eventUnselectItemSlot = item

	def SetUseSlotEvent(self, use):
		self.eventUseSlot = use

	def SetOverInItemEvent(self, event):
		self.eventOverInItem = event

	def SetOverOutItemEvent(self, event):
		self.eventOverOutItem = event

	def SetPressedSlotButtonEvent(self, event):
		self.eventPressedSlotButton = event

	def GetSlotCount(self):
		return wndMgr.GetSlotCount(self.hWnd)

	def SetUseMode(self, flag):
		wndMgr.SetUseMode(self.hWnd, flag)

	def SetUsableItem(self, flag): 
		wndMgr.SetUsableItem(self.hWnd, flag)

	if app.ENABLE_SLOT_MARKING_SYSTEM:
		def SetCanMouseEventSlot(self, slotIndex):
			wndMgr.SetCanMouseEventSlot(self.hWnd, slotIndex)

		def SetCantMouseEventSlot(self, slotIndex):
			wndMgr.SetCantMouseEventSlot(self.hWnd, slotIndex)

		def SetUsableSlotOnTopWnd(self, slotIndex):
			wndMgr.SetUsableSlotOnTopWnd(self.hWnd, slotIndex)

		def SetUnusableSlotOnTopWnd(self, slotIndex):
			wndMgr.SetUnusableSlotOnTopWnd(self.hWnd, slotIndex)

	def SetSlotCoolTime(self, slotIndex, coolTime, elapsedTime = 0.0):
		wndMgr.SetSlotCoolTime(self.hWnd, slotIndex, coolTime, elapsedTime)

	def StoreSlotCoolTime(self, key, slotIndex, coolTime, elapsedTime = 0.0):
		wndMgr.StoreSlotCoolTime(self.hWnd, key, slotIndex, coolTime, elapsedTime)

	def RestoreSlotCoolTime(self, key):
		wndMgr.RestoreSlotCoolTime(self.hWnd, key)

	def DisableSlot(self, slotIndex):
		wndMgr.DisableSlot(self.hWnd, slotIndex)

	def EnableSlot(self, slotIndex):
		wndMgr.EnableSlot(self.hWnd, slotIndex)

	def GetSlotNumber(self):
		return wndMgr.GetSlotNumber(self.hWnd)

	def LockSlot(self, slotIndex):
		wndMgr.LockSlot(self.hWnd, slotIndex)

	def UnlockSlot(self, slotIndex):
		wndMgr.UnlockSlot(self.hWnd, slotIndex)

	def RefreshSlot(self):
		wndMgr.RefreshSlot(self.hWnd)

	def ClearSlot(self, slotNumber):
		wndMgr.ClearSlot(self.hWnd, slotNumber)

	def ClearAllSlot(self):
		wndMgr.ClearAllSlot(self.hWnd)

	def AppendSlot(self, index, x, y, width, height):
		wndMgr.AppendSlot(self.hWnd, index, x, y, width, height)

	def SetSlot(self, slotIndex, itemIndex, width, height, icon, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
		wndMgr.SetSlot(self.hWnd, slotIndex, itemIndex, width, height, icon, diffuseColor)

	def SetSlotCount(self, slotNumber, count):
		wndMgr.SetSlotCount(self.hWnd, slotNumber, count)

	def SetSlotCountNew(self, slotNumber, grade, count):
		wndMgr.SetSlotCountNew(self.hWnd, slotNumber, grade, count)

	def SetRealSlotNumber(self, slotNumber, realSlotNumber):
		wndMgr.SetSlotRealNumber(self.hWnd, slotNumber, realSlotNumber)

	if app.ENABLE_MINIGAME_OKEY_CARDS_SYSTEM:
		def SetCardSlot(self, renderingSlotNumber, CardIndex, cardIcon, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
			if 0 == CardIndex or None == CardIndex:
				wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
				return

			item.SelectItem(CardIndex)
			(width, height) = item.GetItemSize()

			wndMgr.SetCardSlot(self.hWnd, renderingSlotNumber, CardIndex, width, height, cardIcon, diffuseColor)

	def SetItemSlot(self, renderingSlotNumber, ItemIndex, ItemCount = 0, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
		if 0 == ItemIndex or None == ItemIndex:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		item.SelectItem(ItemIndex)
		itemIcon = item.GetIconImage()

		item.SelectItem(ItemIndex)
		(width, height) = item.GetItemSize()

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, ItemIndex, width, height, itemIcon, diffuseColor)
		wndMgr.SetSlotCount(self.hWnd, renderingSlotNumber, ItemCount)

	def SetSkillSlot(self, renderingSlotNumber, skillIndex, skillLevel):

		skillIcon = skill.GetIconImage(skillIndex)

		if 0 == skillIcon:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, skillIndex, 1, 1, skillIcon)
		wndMgr.SetSlotCount(self.hWnd, renderingSlotNumber, skillLevel)

	def SetSkillSlotNew(self, renderingSlotNumber, skillIndex, skillGrade, skillLevel):

		skillIcon = skill.GetIconImageNew(skillIndex, skillGrade)

		if 0 == skillIcon:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, skillIndex, 1, 1, skillIcon)

	def SetEmotionSlot(self, renderingSlotNumber, emotionIndex):
		icon = player.GetEmotionIconImage(emotionIndex)

		if 0 == icon:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, emotionIndex, 1, 1, icon)

	## Event
	def OnSelectEmptySlot(self, slotNumber):
		if self.eventSelectEmptySlot:
			self.eventSelectEmptySlot(slotNumber)

	def OnSelectItemSlot(self, slotNumber):
		if self.eventSelectItemSlot:
			self.eventSelectItemSlot(slotNumber)

	def OnUnselectEmptySlot(self, slotNumber):
		if self.eventUnselectEmptySlot:
			self.eventUnselectEmptySlot(slotNumber)

	def OnUnselectItemSlot(self, slotNumber):
		if self.eventUnselectItemSlot:
			self.eventUnselectItemSlot(slotNumber)

	def OnUseSlot(self, slotNumber):
		if self.eventUseSlot:
			self.eventUseSlot(slotNumber)

	def OnOverInItem(self, slotNumber):
		if self.eventOverInItem:
			self.eventOverInItem(slotNumber)

	def OnOverOutItem(self):
		if self.eventOverOutItem:
			self.eventOverOutItem()

	def OnPressedSlotButton(self, slotNumber):
		if self.eventPressedSlotButton:
			self.eventPressedSlotButton(slotNumber)

	def GetStartIndex(self):
		return 0

	if app.ENABLE_GROWTH_PET_SYSTEM:
		def SetPetSkillSlotNew(self, renderingSlotNumber, petSkillIndex):

			petSkillIcon = skill.GetPetSkillIconImage(petSkillIndex)

			if 0 == petSkillIcon:
				wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
				return

			wndMgr.SetSlot(self.hWnd, renderingSlotNumber, petSkillIndex, 1, 1, petSkillIcon)

	if app.ENABLE_CHANGE_LOOK_SYSTEM:
		def SetSlotCoverImage(self, slotindex, filename):
			wndMgr.SetSlotCoverImage(self.hWnd, slotindex, filename)

		def EnableSlotCoverImage(self, slotindex, onoff):
			wndMgr.EnableSlotCoverImage(self.hWnd, slotindex, onoff)

class GridSlotWindow(SlotWindow):

	def __init__(self):
		SlotWindow.__init__(self)

		self.startIndex = 0

	def __del__(self):
		SlotWindow.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterGridSlotWindow(self, layer)

	def ArrangeSlot(self, StartIndex, xCount, yCount, xSize, ySize, xBlank, yBlank):

		self.startIndex = StartIndex

		wndMgr.ArrangeSlot(self.hWnd, StartIndex, xCount, yCount, xSize, ySize, xBlank, yBlank)
		self.startIndex = StartIndex

	def GetStartIndex(self):
		return self.startIndex

if app.ENABLE_RENEWAL_SWITCHBOT:
	class TitleBarWithoutButton(Window):
		BLOCK_WIDTH = 32
		BLOCK_HEIGHT = 23

		def __init__(self):
			Window.__init__(self)
			self.AddFlag("attach")

		def __del__(self):
			Window.__del__(self)

		def MakeTitleBar(self, width, color):
			width = max(64, width)

			imgLeft = ImageBox()
			imgCenter = ExpandedImageBox()
			imgRight = ImageBox()
			imgLeft.AddFlag("not_pick")
			imgCenter.AddFlag("not_pick")
			imgRight.AddFlag("not_pick")
			imgLeft.SetParent(self)
			imgCenter.SetParent(self)
			imgRight.SetParent(self)

			imgLeft.LoadImage("d:/ymir work/ui/pattern/titlebar_left.tga")
			imgCenter.LoadImage("d:/ymir work/ui/pattern/titlebar_center.tga")
			imgRight.LoadImage("d:/ymir work/ui/pattern/titlebar_right_02.tga")

			imgLeft.Show()
			imgCenter.Show()
			imgRight.Show()

			self.imgLeft = imgLeft
			self.imgCenter = imgCenter
			self.imgRight = imgRight

			self.SetWidth(width)

		def SetWidth(self, width):
			self.imgCenter.SetRenderingRect(0.0, 0.0, float((width - self.BLOCK_WIDTH*2) - self.BLOCK_WIDTH) / self.BLOCK_WIDTH, 0.0)
			self.imgCenter.SetPosition(self.BLOCK_WIDTH, 0)
			self.imgRight.SetPosition(width - self.BLOCK_WIDTH, 0)
				
			self.SetSize(width, self.BLOCK_HEIGHT)

class TitleBar(Window):

	BLOCK_WIDTH = 32
	BLOCK_HEIGHT = 23

	def __init__(self):
		Window.__init__(self)
		self.AddFlag("attach")

	def __del__(self):
		Window.__del__(self)

	def MakeTitleBar(self, width, color):

		width = max(64, width)

		imgLeft = ImageBox()
		imgCenter = ExpandedImageBox()
		imgRight = ImageBox()
		imgLeft.AddFlag("not_pick")
		imgCenter.AddFlag("not_pick")
		imgRight.AddFlag("not_pick")
		imgLeft.SetParent(self)
		imgCenter.SetParent(self)
		imgRight.SetParent(self)

		imgLeft.LoadImage("d:/ymir work/ui/pattern/titlebar_left.tga")
		imgCenter.LoadImage("d:/ymir work/ui/pattern/titlebar_center.tga")
		imgRight.LoadImage("d:/ymir work/ui/pattern/titlebar_right.tga")

		imgLeft.Show()
		imgCenter.Show()
		imgRight.Show()

		btnClose = Button()
		btnClose.SetParent(self)
		btnClose.SetUpVisual("d:/ymir work/ui/public/close_button_01.sub")
		btnClose.SetOverVisual("d:/ymir work/ui/public/close_button_02.sub")
		btnClose.SetDownVisual("d:/ymir work/ui/public/close_button_03.sub")
		btnClose.SetToolTipText(localeInfo.UI_CLOSE, 0, -23)
		btnClose.Show()

		self.imgLeft = imgLeft
		self.imgCenter = imgCenter
		self.imgRight = imgRight
		self.btnClose = btnClose

		self.SetWidth(width)

	def SetWidth(self, width):
		self.imgCenter.SetRenderingRect(0.0, 0.0, float((width - self.BLOCK_WIDTH*2) - self.BLOCK_WIDTH) / self.BLOCK_WIDTH, 0.0)
		self.imgCenter.SetPosition(self.BLOCK_WIDTH, 0)
		self.imgRight.SetPosition(width - self.BLOCK_WIDTH, 0)
		self.btnClose.SetPosition(width - self.btnClose.GetWidth() - 3, 3)
		self.SetSize(width, self.BLOCK_HEIGHT)

	def SetCloseEvent(self, event):
		self.btnClose.SetEvent(event)

	if app.ENABLE_RENEWAL_BONUS_BOARD:
		def CloseButton(self, command):
			if command == "hide":
				self.imgRight.LoadImage("d:/ymir work/ui/pattern/titlebar_right_02.tga")
				self.btnClose.Hide()
			elif command == "show":
				self.imgRight.LoadImage("d:/ymir work/ui/pattern/titlebar_right.tga")
				self.btnClose.Show()

if app.ENABLE_RENEWAL_QUEST:
	class SubTitleBar(Button):
		def __init__(self):
			Button.__init__(self)

		def __del__(self):
			Button.__del__(self)

		def MakeSubTitleBar(self, width, color):
			width = max(64, width)
			self.SetWidth(width)
			self.SetUpVisual("d:/ymir work/ui/quest_re/quest_tab_01.tga")
			self.SetOverVisual("d:/ymir work/ui/quest_re/quest_tab_01.tga")
			self.SetDownVisual("d:/ymir work/ui/quest_re/quest_tab_01.tga")
			self.Show()

			scrollImage = ImageBox()
			scrollImage.SetParent(self)
			scrollImage.LoadImage("d:/ymir work/ui/quest_re/quest_down.tga")
			scrollImage.SetPosition(5, 2.5)
			scrollImage.AddFlag("not_pick")
			scrollImage.Show()
			self.scrollImage = scrollImage

		def OpenCategory(self, qcount = 0):
			if qcount > 0:
				self.scrollImage.LoadImage("d:/ymir work/ui/quest_re/quest_up.tga")
			else:
				self.scrollImage.LoadImage("d:/ymir work/ui/quest_re/quest_down.tga")

		def CloseCategory(self, qcount = 0):
			self.scrollImage.LoadImage("d:/ymir work/ui/quest_re/quest_down.tga")

		def SetQuestLabel(self, filename, qcount):
			tabColor = ImageBox()
			tabColor.SetParent(self)
			tabColor.LoadImage(filename)
			tabColor.AddFlag("not_pick")
			tabColor.SetPosition(188, 12)
			if qcount > 0:
				tabColor.Show()
			else:
				tabColor.Hide()
			self.tabColor = tabColor

		def SetWidth(self, width):
			self.SetPosition(32, 0)
			self.SetSize(width, 23)

	class ListBar(Button):
		def __init__(self):
			Button.__init__(self)

		def __del__(self):
			Button.__del__(self)

		def MakeListBar(self, width, color):
			width = max(64, width)
			self.SetWidth(width)
			self.Show()

			checkbox = ImageBox()
			checkbox.SetParent(self)
			checkbox.LoadImage("d:/ymir work/ui/quest_re/quest_new.tga")
			checkbox.SetPosition(10, 9)
			checkbox.AddFlag("not_pick")
			checkbox.Show()
			self.checkbox = checkbox
			self.isChecked = FALSE

		def SetWidth(self, width):
			self.SetPosition(32, 0)
			self.SetSize(width, 23)

		def CallEvent(self):
			self.OnClickEvent()
			super(ListBar, self).CallEvent()

		def OnClickEvent(self):
			self.checkbox.Hide()
			self.isChecked = TRUE

		def SetSlot(self, slotIndex, itemIndex, width, height, icon, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
			wndMgr.SetSlot(self.hWnd, slotIndex, itemIndex, width, height, icon, diffuseColor)

class HorizontalBar(Window):

	BLOCK_WIDTH = 32
	BLOCK_HEIGHT = 17

	def __init__(self):
		Window.__init__(self)
		self.AddFlag("attach")

		if app.ENABLE_RENEWAL_BONUS_BOARD:
			self.ButtonText = None

	def __del__(self):
		Window.__del__(self)

	def Create(self, width):

		width = max(96, width)

		imgLeft = ImageBox()
		imgLeft.SetParent(self)
		imgLeft.AddFlag("not_pick")
		imgLeft.LoadImage("d:/ymir work/ui/pattern/horizontalbar_left.tga")
		imgLeft.Show()

		imgCenter = ExpandedImageBox()
		imgCenter.SetParent(self)
		imgCenter.AddFlag("not_pick")
		imgCenter.LoadImage("d:/ymir work/ui/pattern/horizontalbar_center.tga")
		imgCenter.Show()

		imgRight = ImageBox()
		imgRight.SetParent(self)
		imgRight.AddFlag("not_pick")
		imgRight.LoadImage("d:/ymir work/ui/pattern/horizontalbar_right.tga")
		imgRight.Show()

		self.imgLeft = imgLeft
		self.imgCenter = imgCenter
		self.imgRight = imgRight
		self.SetWidth(width)

	def SetWidth(self, width):
		self.imgCenter.SetRenderingRect(0.0, 0.0, float((width - self.BLOCK_WIDTH*2) - self.BLOCK_WIDTH) / self.BLOCK_WIDTH, 0.0)
		self.imgCenter.SetPosition(self.BLOCK_WIDTH, 0)
		self.imgRight.SetPosition(width - self.BLOCK_WIDTH, 0)
		self.SetSize(width, self.BLOCK_HEIGHT)

	if app.ENABLE_RENEWAL_BONUS_BOARD:
		def SetText(self, text):
			if not self.ButtonText:
				textLine = TextLine()
				textLine.SetParent(self)
				textLine.SetPosition(self.GetWidth()/2, self.GetHeight()/2)
				textLine.SetVerticalAlignCenter()
				textLine.SetHorizontalAlignCenter()
				textLine.Show()
				self.ButtonText = textLine

			self.ButtonText.SetText(text)

		def GetText(self):
			if not self.ButtonText:
				return ""
			return self.ButtonText.GetText()

class Gauge(Window):

	SLOT_WIDTH = 16
	SLOT_HEIGHT = 7

	GAUGE_TEMPORARY_PLACE = 12
	GAUGE_WIDTH = 16

	def __init__(self):
		Window.__init__(self)
		self.width = 0
	def __del__(self):
		Window.__del__(self)

	def MakeGauge(self, width, color):

		self.width = max(48, width)

		imgSlotLeft = ImageBox()
		imgSlotLeft.SetParent(self)
		imgSlotLeft.LoadImage("d:/ymir work/ui/pattern/gauge_slot_left.tga")
		imgSlotLeft.Show()

		imgSlotRight = ImageBox()
		imgSlotRight.SetParent(self)
		imgSlotRight.LoadImage("d:/ymir work/ui/pattern/gauge_slot_right.tga")
		imgSlotRight.Show()
		imgSlotRight.SetPosition(width - self.SLOT_WIDTH, 0)

		imgSlotCenter = ExpandedImageBox()
		imgSlotCenter.SetParent(self)
		imgSlotCenter.LoadImage("d:/ymir work/ui/pattern/gauge_slot_center.tga")
		imgSlotCenter.Show()
		imgSlotCenter.SetRenderingRect(0.0, 0.0, float((width - self.SLOT_WIDTH*2) - self.SLOT_WIDTH) / self.SLOT_WIDTH, 0.0)
		imgSlotCenter.SetPosition(self.SLOT_WIDTH, 0)

		imgGauge = ExpandedImageBox()
		imgGauge.SetParent(self)
		imgGauge.LoadImage("d:/ymir work/ui/pattern/gauge_" + color + ".tga")
		imgGauge.Show()
		imgGauge.SetRenderingRect(0.0, 0.0, 0.0, 0.0)
		imgGauge.SetPosition(self.GAUGE_TEMPORARY_PLACE, 0)

		imgSlotLeft.AddFlag("attach")
		imgSlotCenter.AddFlag("attach")
		imgSlotRight.AddFlag("attach")

		self.imgLeft = imgSlotLeft
		self.imgCenter = imgSlotCenter
		self.imgRight = imgSlotRight
		self.imgGauge = imgGauge

		self.SetSize(width, self.SLOT_HEIGHT)

	def SetPercentage(self, curValue, maxValue):

		# PERCENTAGE_MAX_VALUE_ZERO_DIVISION_ERROR
		if maxValue > 0.0:
			percentage = min(1.0, float(curValue)/float(maxValue))
		else:
			percentage = 0.0
		# END_OF_PERCENTAGE_MAX_VALUE_ZERO_DIVISION_ERROR

		gaugeSize = -1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2) * percentage / self.GAUGE_WIDTH
		self.imgGauge.SetRenderingRect(0.0, 0.0, gaugeSize, 0.0)

class Gauge2(Window):

	SLOT_WIDTH = 16
	SLOT_HEIGHT = 7

	GAUGE_TEMPORARY_PLACE = 14
	GAUGE_WIDTH = 16

	def __init__(self):
		Window.__init__(self)
		self.width = 0
	def __del__(self):
		Window.__del__(self)

	def MakeGauge(self, width):

		self.width = max(48, width)

		imgSlotLeft = ImageBox()
		imgSlotLeft.SetParent(self)
		imgSlotLeft.LoadImage("d:/ymir work/ui/intro/common/gauge/gauge_slot_left.png")
		imgSlotLeft.Show()

		imgSlotRight = ImageBox()
		imgSlotRight.SetParent(self)
		imgSlotRight.LoadImage("d:/ymir work/ui/intro/common/gauge/gauge_slot_right.png")
		imgSlotRight.Show()
		imgSlotRight.SetPosition(width - self.SLOT_WIDTH + 44, 0)

		imgSlotCenter = ExpandedImageBox()
		imgSlotCenter.SetParent(self)
		imgSlotCenter.LoadImage("d:/ymir work/ui/intro/common/gauge/gauge_slot_center.png")
		imgSlotCenter.Show()
		imgSlotCenter.SetRenderingRect(0.0, 0.0, float((width - self.SLOT_WIDTH*2) - self.SLOT_WIDTH) / self.SLOT_WIDTH, 0.0)
		imgSlotCenter.SetPosition(self.SLOT_WIDTH - 10, 0)

		imgGauge = ExpandedImageBox()
		imgGauge.SetParent(self)
		imgGauge.LoadImage("d:/ymir work/ui/intro/common/gauge/gauge_slot_full.png")
		imgGauge.Show()
		imgGauge.SetRenderingRect(0.0, 0.0, 0.0, 0.0)
		imgGauge.SetPosition(self.GAUGE_TEMPORARY_PLACE - 12, 0)

		imgSlotLeft.AddFlag("attach")
		imgSlotCenter.AddFlag("attach")
		imgSlotRight.AddFlag("attach")

		self.imgLeft = imgSlotLeft
		self.imgCenter = imgSlotCenter
		self.imgRight = imgSlotRight
		self.imgGauge = imgGauge

		self.SetSize(width, self.SLOT_HEIGHT)

	def SetPercentage(self, curValue, maxValue):

		# PERCENTAGE_MAX_VALUE_ZERO_DIVISION_ERROR
		if maxValue > 0.0:
			percentage = min(1.0, float(curValue)/float(maxValue))
		else:
			percentage = 0.0
		# END_OF_PERCENTAGE_MAX_VALUE_ZERO_DIVISION_ERROR

		gaugeSize = -1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2) * percentage / self.GAUGE_WIDTH
		self.imgGauge.SetRenderingRect(0.0, 0.0, gaugeSize, 0.0)

class DynamicGauge(Gauge):
	dynamicGaugePerc = None
	newGaugePerc = 0

	def __init__(self):
		Gauge. __init__(self)

	def __del__(self):
		Gauge. __del__(self)

	def MakeGauge(self, width, color1, color2):
		Gauge.MakeGauge(self, width, color2)

		imgGauge2 = ExpandedImageBox()
		imgGauge2.SetParent(self)
		imgGauge2.LoadImage( "d:/ymir work/ui/pattern/gauge_" + color1 + ".tga")
		imgGauge2.Show()
		imgGauge2.SetRenderingRect(0.0, 0.0, 0.0, 0.0)
		imgGauge2.SetPosition(self .GAUGE_TEMPORARY_PLACE, 0)

		self .imgGauge2 = imgGauge2

	def SetPercentage(self, curValue, maxValue):
		if maxValue > 0.0:
			percentage = min(1.0, float(curValue)/float(maxValue))
		else:
			percentage = 0.0

		gaugeSize = -1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2)*percentage/self .GAUGE_WIDTH

		if self.dynamicGaugePerc == None:
			self.imgGauge.SetRenderingRect(0.0, 0.0, (-1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2)*percentage/self.GAUGE_WIDTH), 0.0)
			self.dynamicGaugePerc = percentage
		elif self.dynamicGaugePerc + 0.2 < self.newGaugePerc:
			self.imgGauge.SetRenderingRect(0.0, 0.0, (-1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2)*self.newGaugePerc/self .GAUGE_WIDTH), 0.0)
			self.dynamicGaugePerc = self.newGaugePerc

		self.newGaugePerc = percentage
		self.imgGauge2.SetRenderingRect(0.0, 0.0, gaugeSize, 0.0)

		if percentage == 0:
			self.imgGauge.Hide()
		else:
			self.imgGauge.Show()

	def OnUpdate (self):
		if self.dynamicGaugePerc > self.newGaugePerc:
			self.dynamicGaugePerc = self.dynamicGaugePerc - 0.005
			self.imgGauge.SetRenderingRect(0.0, 0.0, (-1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2)*self.dynamicGaugePerc/self.GAUGE_WIDTH), 0.0)
		elif self.dynamicGaugePerc < self.newGaugePerc:
			self.dynamicGaugePerc = self.newGaugePerc
			self.imgGauge.SetRenderingRect(0.0, 0.0, (-1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2 )*self.dynamicGaugePerc/self.GAUGE_WIDTH), 0.0)

class Board(Window):
	CORNER_WIDTH = 32
	CORNER_HEIGHT = 32
	LINE_WIDTH = 128
	LINE_HEIGHT = 128

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	BASE_PATH = "d:/ymir work/ui/pattern"
	IMAGES = {
		'CORNER' : {
			0 : "Board_Corner_LeftTop",
			1 : "Board_Corner_LeftBottom",
			2 : "Board_Corner_RightTop",
			3 : "Board_Corner_RightBottom"
		},
		'BAR' : {
			0 : "Board_Line_Left",
			1 : "Board_Line_Right",
			2 : "Board_Line_Top",
			3 : "Board_Line_Bottom"
		},
		'FILL' : "Board_Base"
	}

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		self.skipMaxCheck = FALSE

		self.MakeBoard()

	def MakeBoard(self):
		CornerFileNames = [ ]
		LineFileNames = [ ]
		
		for imageDictKey in (['CORNER', 'BAR']):
			for x in xrange(len(self.IMAGES[imageDictKey])):
				if imageDictKey == "CORNER":
					CornerFileNames.append("%s/%s.tga" % (self.BASE_PATH, self.IMAGES[imageDictKey][x]))
				elif imageDictKey == "BAR":
					LineFileNames.append("%s/%s.tga" % (self.BASE_PATH, self.IMAGES[imageDictKey][x]))
		
		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

		self.Base = ExpandedImageBox()
		self.Base.AddFlag("not_pick")
		self.Base.LoadImage("%s/%s.tga" % (self.BASE_PATH, self.IMAGES['FILL']))
		self.Base.SetParent(self)
		self.Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Base.Show()

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):
		if not self.skipMaxCheck:
			width = max(self.CORNER_WIDTH*2, width)
			height = max(self.CORNER_HEIGHT*2, height)
			
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)

		if self.Base:
			self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)

class BorderA(Window):
	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16
	BOARD_COLOR = grp.GenerateColor(0.17, 0.027, 0.0, 0.70)

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		CornerFileNames = [ "d:/ymir work/ui/pattern/border_a/border_a_"+dir+".tga" for dir in ["Left_Top","Left_Bottom","Right_Top","Right_Bottom"] ]
		LineFileNames = [ "d:/ymir work/ui/pattern/border_a/border_a_"+dir+".tga" for dir in ["Left","Right","Top","Bottom"] ]

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		self.Base = ExpandedImageBox()
		self.Base.AddFlag("not_pick")
		self.Base.LoadImage("d:/ymir work/ui/pattern/border_a/border_a_center.tga")
		self.Base.SetParent(self)
		self.Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Base.Show()

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)

		if self.Base:
			self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)

	def ShowInternal(self):
		self.Base.Show()
		for wnd in self.Lines:
			wnd.Show()
		for wnd in self.Corners:
			wnd.Show()

	def HideInternal(self):
		self.Base.Hide()
		for wnd in self.Lines:
			wnd.Hide()
		for wnd in self.Corners:
			wnd.Hide()

class BorderB(Board):
	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16

	BASE_PATH = "d:/ymir work/ui/pattern/border_b"

	IMAGES = {
		'CORNER' : {
			0 : "border_b_left_top",
			1 : "border_b_left_bottom",
			2 : "border_b_right_top",
			3 : "border_b_right_bottom"
		},
		'BAR' : {
			0 : "border_b_left",
			1 : "border_b_right",
			2 : "border_b_top",
			3 : "border_b_bottom"
		},
		'FILL' : "border_b_center"
	}

	def __init__(self):
		Board.__init__(self)
			
		self.eventFunc = {
			"MOUSE_LEFT_BUTTON_UP" : None, 
		}
		self.eventArgs = {
			"MOUSE_LEFT_BUTTON_UP" : None, 
		}

	def __del__(self):
		Board.__del__(self)
		self.eventFunc = None
		self.eventArgs = None

	def SetSize(self, width, height):
		Board.SetSize(self, width, height)

	def SetEvent(self, func, *args) :
		result = self.eventFunc.has_key(args[0])
		if result :
			self.eventFunc[args[0]] = func
			self.eventArgs[args[0]] = args
		else :
			print "[ERROR] ui.py SetEvent, Can`t Find has_key : %s" % args[0]

	def OnMouseLeftButtonUp(self):
		if self.eventFunc["MOUSE_LEFT_BUTTON_UP"] :
			apply(self.eventFunc["MOUSE_LEFT_BUTTON_UP"], self.eventArgs["MOUSE_LEFT_BUTTON_UP"])

class BoardWithTitleBar(Board):
	def __init__(self):
		Board.__init__(self)

		titleBar = TitleBar()
		titleBar.SetParent(self)
		titleBar.MakeTitleBar(0, "red")
		titleBar.SetPosition(8, 7)
		titleBar.Show()

		titleName = TextLine()
		titleName.SetParent(titleBar)
		titleName.SetPosition(0, 4)
		titleName.SetWindowHorizontalAlignCenter()
		titleName.SetHorizontalAlignCenter()
		titleName.Show()

		self.titleBar = titleBar
		self.titleName = titleName

		self.SetCloseEvent(self.Hide)

	def __del__(self):
		Board.__del__(self)
		self.titleBar = None
		self.titleName = None

	def SetSize(self, width, height):
		self.titleBar.SetWidth(width - 15)
		#self.pickRestrictWindow.SetSize(width, height - 30)
		Board.SetSize(self, width, height)
		self.titleName.UpdateRect()

	def SetTitleColor(self, color):
		self.titleName.SetPackedFontColor(color)

	def SetTitleName(self, name):
		self.titleName.SetText(name)

	def SetCloseEvent(self, event):
		self.titleBar.SetCloseEvent(event)

if app.ENABLE_RENEWAL_SWITCHBOT:
	class NewBoard(Window):
		CORNER_WIDTH = 32
		CORNER_HEIGHT = 32
		LINE_WIDTH = 128
		LINE_HEIGHT = 128
		LT = 0
		LB = 1
		RT = 2
		RB = 3
		L = 0
		R = 1
		T = 2
		B = 3

		def __init__(self):
			Window.__init__(self)

			self.MakeBoard("d:/ymir work/ui/pattern/new_board/Board_Corner_", "d:/ymir work/ui/pattern/new_board/Board_Line_")
			self.MakeBase()

		def MakeBoard(self, cornerPath, linePath):

			CornerFileNames = [ cornerPath+dir+".tga" for dir in ("LeftTop", "LeftBottom", "RightTop", "RightBottom", ) ]
			LineFileNames = [ linePath+dir+".tga" for dir in ("Left", "Right", "Top", "Bottom", ) ]
			
			self.Corners = []
			for fileName in CornerFileNames:
				Corner = ExpandedImageBox()
				Corner.AddFlag("not_pick")
				Corner.LoadImage(fileName)
				Corner.SetParent(self)
				Corner.SetPosition(0, 0)
				Corner.Show()
				self.Corners.append(Corner)

			self.Lines = []
			for fileName in LineFileNames:
				Line = ExpandedImageBox()
				Line.AddFlag("not_pick")
				Line.LoadImage(fileName)
				Line.SetParent(self)
				Line.SetPosition(0, 0)
				Line.Show()
				self.Lines.append(Line)

			self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
			self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

		def MakeBase(self):
			self.Base = ExpandedImageBox()
			self.Base.AddFlag("not_pick")
			self.Base.LoadImage("d:/ymir work/ui/pattern/new_board/Board_Base.tga")
			self.Base.SetParent(self)
			self.Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
			self.Base.Show()

		def __del__(self):
			Window.__del__(self)

		def SetSize(self, width, height):
			width = max(self.CORNER_WIDTH*2, width)
			height = max(self.CORNER_HEIGHT*2, height)
			Window.SetSize(self, width, height)

			self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
			self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
			self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
			self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
			self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

			verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
			horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
			self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
			self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
			self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
			self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)

			if self.Base:
				self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)

	class NewBoardWithTitleBar(NewBoard):
		def __init__(self, withButton = FALSE):
			NewBoard.__init__(self)

			self.withButton = withButton
			titleBar = TitleBar()
			if self.withButton is TRUE:
				titleBar = TitleBarWithoutButton()
			titleBar.SetParent(self)
			titleBar.MakeTitleBar(0, "red")
			titleBar.SetPosition(8, 7)
			titleBar.Show()

			titleName = TextLine()
			titleName.SetParent(titleBar)
			titleName.SetPosition(0, 4)
			titleName.SetWindowHorizontalAlignCenter()
			titleName.SetHorizontalAlignCenter()
			titleName.Show()

			self.titleBar = titleBar
			self.titleName = titleName

			if self.withButton is FALSE:
				self.SetCloseEvent(self.Hide)

		def __del__(self):
			NewBoard.__del__(self)
			self.titleBar = None
			self.titleName = None

		def SetSize(self, width, height):
			self.titleBar.SetWidth(width - 15)
			NewBoard.SetSize(self, width, height)
			self.titleName.UpdateRect()

		def SetTitleColor(self, color):
			self.titleName.SetPackedFontColor(color)

		def SetTitleName(self, name):
			self.titleName.SetText(name)

		def SetCloseEvent(self, event):
			if self.withButton is FALSE:
				self.titleBar.SetCloseEvent(event)

class InvisibleBoard(Window):
	CORNER_WIDTH = 32
	CORNER_HEIGHT = 32
	LINE_WIDTH = 128
	LINE_HEIGHT = 128

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		self.skipMaxCheck = FALSE

		self.MakeBoard()

	def MakeBoard(self):
		self.Corners = []
		self.Lines = []
		self.Base = None

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):
		if not self.skipMaxCheck:
			width = max(self.CORNER_WIDTH*2, width)
			height = max(self.CORNER_HEIGHT*2, height)

		Window.SetSize(self, width, height)

class ThinBoard(Window):
	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16
	BOARD_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.45)

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		CornerFileNames = [ "d:/ymir work/ui/pattern/thinboardnew/ThinBoard_Corner_"+dir+".tga" for dir in ["LeftTop","LeftBottom","RightTop","RightBottom"] ]
		LineFileNames = [ "d:/ymir work/ui/pattern/thinboardnew/ThinBoard_Line_"+dir+".tga" for dir in ["Left","Right","Top","Bottom"] ]

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("attach")
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("attach")
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		Base = Bar()
		Base.SetParent(self)
		Base.AddFlag("attach")
		Base.AddFlag("not_pick")
		Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		Base.SetColor(self.BOARD_COLOR)
		Base.Show()
		self.Base = Base

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def __del__(self):
		Window.__del__(self)

	def ShowCorner(self, corner):
		self.Corners[corner].Show()
		self.SetSize(self.GetWidth(), self.GetHeight())

	def HideCorners(self, corner):
		self.Corners[corner].Hide()
		self.SetSize(self.GetWidth(), self.GetHeight())

	def ShowLine(self, line):
		self.Lines[line].Show()
		self.SetSize(self.GetWidth(), self.GetHeight())

	def HideLine(self, line):
		self.Lines[line].Hide()
		self.SetSize(self.GetWidth(), self.GetHeight())

	def SetSize(self, width, height):
		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Base.SetSize(width - self.CORNER_WIDTH*2, height - self.CORNER_HEIGHT*2)

	def ShowInternal(self):
		self.Base.Show()
		for wnd in self.Lines:
			wnd.Show()
		for wnd in self.Corners:
			wnd.Show()

	def HideInternal(self):
		self.Base.Hide()
		for wnd in self.Lines:
			wnd.Hide()
		for wnd in self.Corners:
			wnd.Hide()

	def SetAlpha(self, alpha):
		color = grp.GenerateColor(0.0, 0.0, 0.0, alpha)
		self.Base.SetColor(color)
		for wnd in self.Lines:
			wnd.SetAlpha(alpha)
		for wnd in self.Corners:
			wnd.SetAlpha(alpha)

class ThinBoardGold(Window):
	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16
	BOARD_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.51)

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		CornerFileNames = [ "d:/ymir work/ui/pattern/thinboardgold/ThinBoard_Corner_"+dir+".tga" for dir in ["LeftTop_gold", "LeftBottom_gold","RightTop_gold", "RightBottom_gold"]]
		LineFileNames = [ "d:/ymir work/ui/pattern/thinboardgold/ThinBoard_Line_"+dir+".tga" for dir in ["Left_gold", "Right_gold", "Top_gold", "Bottom_gold"]]

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("attach")
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("attach")
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		Base = ExpandedImageBox()
		Base.SetParent(self)
		Base.AddFlag("attach")
		Base.AddFlag("not_pick")
		Base.LoadImage("d:/ymir work/ui/pattern/thinboardgold/thinboard_bg_gold.tga")
		Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		Base.Show()
		self.Base = Base

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		if self.Base:
			self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)

	def ShowInternal(self):
		self.Base.Show()
		for wnd in self.Lines:
			wnd.Show()
		for wnd in self.Corners:
			wnd.Show()

	def HideInternal(self):
		self.Base.Hide()
		for wnd in self.Lines:
			wnd.Hide()
		for wnd in self.Corners:
			wnd.Hide()

class ThinBoardCircle(Window):
	CORNER_WIDTH = 4
	CORNER_HEIGHT = 4
	LINE_WIDTH = 4
	LINE_HEIGHT = 4
	BOARD_COLOR = grp.GenerateColor(255.0, 255.0, 255.0, 1.0)

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		CornerFileNames = [ "d:/ymir work/ui/pattern/thinboardcircle/ThinBoard_Corner_"+dir+".tga" for dir in ["LeftTop_circle","LeftBottom_circle","RightTop_circle","RightBottom_circle"] ]
		LineFileNames = [ "d:/ymir work/ui/pattern/thinboardcircle/ThinBoard_Line_"+dir+".tga" for dir in ["Left_circle","Right_circle","Top_circle","Bottom_circle"] ]

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("attach")
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("attach")
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		Base = Bar()
		Base.SetParent(self)
		Base.AddFlag("attach")
		Base.AddFlag("not_pick")
		Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		Base.SetColor(self.BOARD_COLOR)
		Base.Show()
		self.Base = Base

		if app.ENABLE_RENEWAL_BONUS_BOARD:
			self.ButtonText = None
			self.BonusId = 0

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Base.SetSize(width - self.CORNER_WIDTH*2, height - self.CORNER_HEIGHT*2)

	if app.ENABLE_RENEWAL_BONUS_BOARD:
		def SetText(self, text):
			if not self.ButtonText:
				textLine = TextLine()
				textLine.SetParent(self)
				textLine.SetPosition(self.GetWidth()/2, self.GetHeight()/2)
				textLine.SetVerticalAlignCenter()
				textLine.SetHorizontalAlignCenter()
				textLine.Show()
				self.ButtonText = textLine

			self.ButtonText.SetText(text)

		def GetText(self):
			if not self.ButtonText:
				return ""
			return self.ButtonText.GetText()

		def SetBonusId(self, bnsId):
			self.BonusId = bnsId

		def GetBonusId(self):
			if self.BonusId != 0:
				return self.BonusId

	def ShowInternal(self):
		self.Base.Show()
		for wnd in self.Lines:
			wnd.Show()
		for wnd in self.Corners:
			wnd.Show()

	def HideInternal(self):
		self.Base.Hide()
		for wnd in self.Lines:
			wnd.Hide()
		for wnd in self.Corners:
			wnd.Hide()

class ScrollBar(Window):
	SCROLLBAR_WIDTH = 17
	SCROLLBAR_MIDDLE_HEIGHT = 9
	SCROLLBAR_BUTTON_WIDTH = 17
	SCROLLBAR_BUTTON_HEIGHT = 17
	MIDDLE_BAR_POS = 5
	MIDDLE_BAR_UPPER_PLACE = 3
	MIDDLE_BAR_DOWNER_PLACE = 4
	TEMP_SPACE = MIDDLE_BAR_UPPER_PLACE + MIDDLE_BAR_DOWNER_PLACE

	class MiddleBar(DragButton):
		def __init__(self):
			DragButton.__init__(self)
			self.AddFlag("movable")
			#self.AddFlag("restrict_x")

		def MakeImage(self):
			top = ImageBox()
			top.SetParent(self)
			top.LoadImage("d:/ymir work/ui/pattern/ScrollBar_Top.tga")
			top.SetPosition(0, 0)
			top.AddFlag("not_pick")
			top.Show()
			bottom = ImageBox()
			bottom.SetParent(self)
			bottom.LoadImage("d:/ymir work/ui/pattern/ScrollBar_Bottom.tga")
			bottom.AddFlag("not_pick")
			bottom.Show()

			middle = ExpandedImageBox()
			middle.SetParent(self)
			middle.LoadImage("d:/ymir work/ui/pattern/ScrollBar_Middle.tga")
			middle.SetPosition(0, 4)
			middle.AddFlag("not_pick")
			middle.Show()

			self.top = top
			self.bottom = bottom
			self.middle = middle

		def SetSize(self, height):
			height = max(12, height)
			DragButton.SetSize(self, 10, height)
			self.bottom.SetPosition(0, height-4)

			height -= 4*3
			self.middle.SetRenderingRect(0, 0, 0, float(height)/4.0)

	def __init__(self):
		Window.__init__(self)

		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = lambda *arg: None
		self.lockFlag = FALSE
		self.scrollStep = 0.20

		self.CreateScrollBar()

	def __del__(self):
		Window.__del__(self)

	def CreateScrollBar(self):
		barSlot = Bar3D()
		barSlot.SetParent(self)
		barSlot.AddFlag("not_pick")
		barSlot.Show()

		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.MakeImage()
		middleBar.SetSize(12)

		upButton = Button()
		upButton.SetParent(self)
		upButton.SetEvent(__mem_func__(self.OnUp))
		upButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_up_button_01.sub")
		upButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_up_button_02.sub")
		upButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_up_button_03.sub")
		upButton.Show()

		downButton = Button()
		downButton.SetParent(self)
		downButton.SetEvent(__mem_func__(self.OnDown))
		downButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_down_button_01.sub")
		downButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_down_button_02.sub")
		downButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_down_button_03.sub")
		downButton.Show()

		self.upButton = upButton
		self.downButton = downButton
		self.middleBar = middleBar
		self.barSlot = barSlot

		self.SCROLLBAR_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
		self.SCROLLBAR_BUTTON_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_BUTTON_HEIGHT = self.upButton.GetHeight()

	def Destroy(self):
		self.middleBar = None
		self.upButton = None
		self.downButton = None
		self.eventScroll = lambda *arg: None

	def SetScrollEvent(self, event):
		self.eventScroll = event

	def SetMiddleBarSize(self, pageScale):
		realHeight = self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2
		self.SCROLLBAR_MIDDLE_HEIGHT = int(pageScale * float(realHeight))
		self.middleBar.SetSize(self.SCROLLBAR_MIDDLE_HEIGHT)
		self.pageSize = (self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)

	def SetScrollBarSize(self, height):
		self.pageSize = (height - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)
		self.SetSize(self.SCROLLBAR_WIDTH, height)
		self.upButton.SetPosition(0, 0)
		self.downButton.SetPosition(0, height - self.SCROLLBAR_BUTTON_HEIGHT)
		self.middleBar.SetRestrictMovementArea(self.MIDDLE_BAR_POS, self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE, self.MIDDLE_BAR_POS+2, height - self.SCROLLBAR_BUTTON_HEIGHT*2 - self.TEMP_SPACE)
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, 0)

		self.UpdateBarSlot()

	def UpdateBarSlot(self):
		self.barSlot.SetPosition(0, self.SCROLLBAR_BUTTON_HEIGHT)
		self.barSlot.SetSize(self.GetWidth() - 2, self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2 - 2)

	def GetPos(self):
		return self.curPos

	def SetPos(self, pos):
		pos = max(0.0, pos)
		pos = min(1.0, pos)

		newPos = float(self.pageSize) * pos
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, int(newPos) + self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE)
		self.OnMove()

	def SetScrollStep(self, step):
		self.scrollStep = step

	def GetScrollStep(self):
		return self.scrollStep

	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep)

	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep)

	def OnMove(self):

		if self.lockFlag:
			return

		if 0 == self.pageSize:
			return

		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(yLocal - self.SCROLLBAR_BUTTON_HEIGHT - self.MIDDLE_BAR_UPPER_PLACE) / float(self.pageSize)

		self.eventScroll()

	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		pickedPos = yMouseLocalPosition - self.SCROLLBAR_BUTTON_HEIGHT - self.SCROLLBAR_MIDDLE_HEIGHT/2
		newPos = float(pickedPos) / float(self.pageSize)
		self.SetPos(newPos)

	def LockScroll(self):
		self.lockFlag = TRUE

	def UnlockScroll(self):
		self.lockFlag = FALSE

if app.ENABLE_RENEWAL_SWITCHBOT:
	class ScrollBar2(Window):
		SCROLLBAR_WIDTH = 17
		SCROLLBAR_MIDDLE_HEIGHT = 9
		SCROLLBAR_BUTTON_WIDTH = 17
		SCROLLBAR_BUTTON_HEIGHT = 17
		MIDDLE_BAR_POS = 0
		MIDDLE_BAR_UPPER_PLACE = 3
		MIDDLE_BAR_DOWNER_PLACE = 4
		TEMP_SPACE = MIDDLE_BAR_UPPER_PLACE + MIDDLE_BAR_DOWNER_PLACE

		class MiddleBar(DragButton):
			def __init__(self):
				DragButton.__init__(self)
				self.AddFlag("movable")

			def MakeImage(self):

				middle = ExpandedImageBox()
				middle.SetParent(self)
				middle.LoadImage("d:/ymir work/ui/game/windows/scrollbar2/scrollbar_middle.tga")
				middle.SetPosition(0, 0)
				middle.AddFlag("not_pick")
				middle.Show()

				self.middle = middle

			def SetSize(self, height):
				height = max(12, height)
				DragButton.SetSize(self, 10, height)

				height -= 4*3
				self.middle.SetRenderingRect(0, 0, 0, float(height)/4.0)

		def __init__(self):
			Window.__init__(self)

			self.pageSize = 1
			self.curPos = 0.0
			self.eventScroll = lambda *arg: None
			self.lockFlag = FALSE
			self.scrollStep = 0.20

			self.eventFuncCall = TRUE

			self.CreateScrollBar()

		def __del__(self):
			Window.__del__(self)

		def CreateScrollBar(self):
			barSlot = ExpandedImageBox()
			barSlot.SetParent(self)
			barSlot.LoadImage("d:/ymir work/ui/game/windows/scrollbar2/base_scroll.tga")
			barSlot.AddFlag("not_pick")
			barSlot.Show()

			middleBar = self.MiddleBar()
			middleBar.SetParent(self)
			middleBar.SetMoveEvent(__mem_func__(self.OnMove))
			middleBar.Show()
			middleBar.MakeImage()
			middleBar.SetSize(12)

			self.middleBar = middleBar
			self.barSlot = barSlot

			self.SCROLLBAR_WIDTH = self.middleBar.GetWidth()
			self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
			self.SCROLLBAR_BUTTON_WIDTH = self.middleBar.GetWidth()
			self.SCROLLBAR_BUTTON_HEIGHT = self.middleBar.GetHeight()

		def Destroy(self):
			self.middleBar = None
			self.eventScroll = lambda *arg: None

			self.eventFuncCall = TRUE

		def SetEvnetFuncCall(self, callable):
			self.eventFuncCall = callable

		def SetScrollEvent(self, event):
			self.eventScroll = event

		def SetMiddleBarSize(self, pageScale):
			realHeight = self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2
			self.SCROLLBAR_MIDDLE_HEIGHT = int(pageScale * float(realHeight))
			self.middleBar.SetSize(self.SCROLLBAR_MIDDLE_HEIGHT)
			self.pageSize = (self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)

		def SetScrollBarSize(self, height):
			self.pageSize = (height - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)
			self.SetSize(self.SCROLLBAR_WIDTH, height)
			self.middleBar.SetRestrictMovementArea(self.MIDDLE_BAR_POS, self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE, self.MIDDLE_BAR_POS+2, height - self.SCROLLBAR_BUTTON_HEIGHT*2 - self.TEMP_SPACE)
			self.middleBar.SetPosition(self.MIDDLE_BAR_POS, 0)

			self.UpdateBarSlot()

		def UpdateBarSlot(self):
			self.barSlot.SetPosition(0, self.SCROLLBAR_BUTTON_HEIGHT)
			height =  - self.SCROLLBAR_BUTTON_HEIGHT*2 - 2
			new_height = float(self.GetHeight()) / float(self.barSlot.GetHeight())
			self.barSlot.SetRenderingRect(0.0, 0.0, 0.0, new_height - 2.8)

		def GetPos(self):
			return self.curPos

		def SetPos(self, pos, event_callable = TRUE):
			pos = max(0.0, pos)
			pos = min(1.0, pos)

			newPos = float(self.pageSize) * pos
			self.middleBar.SetPosition(self.MIDDLE_BAR_POS, int(newPos) + self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE)

			self.OnMove(event_callable)

		def SetScrollStep(self, step):
			self.scrollStep = step

		def GetScrollStep(self):
			return self.scrollStep

		def OnUp(self):
			self.SetPos(self.curPos-self.scrollStep, self.eventFuncCall)

		def OnDown(self):
			self.SetPos(self.curPos+self.scrollStep, self.eventFuncCall)

		def OnMove(self, event_callable = TRUE):
			if self.lockFlag:
				return

			if 0 == self.pageSize:
				return

			(xLocal, yLocal) = self.middleBar.GetLocalPosition()
			self.curPos = float(yLocal - self.SCROLLBAR_BUTTON_HEIGHT - self.MIDDLE_BAR_UPPER_PLACE) / float(self.pageSize)

			if event_callable:
				self.eventScroll()

		def OnMouseLeftButtonDown(self):
			(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
			pickedPos = yMouseLocalPosition - self.SCROLLBAR_BUTTON_HEIGHT - self.SCROLLBAR_MIDDLE_HEIGHT/2
			newPos = float(pickedPos) / float(self.pageSize)
			self.SetPos(newPos)

		def LockScroll(self):
			self.lockFlag = TRUE

		def UnlockScroll(self):
			self.lockFlag = FALSE

		def RunMouseWheel(self, nLen):
			if nLen > 0:
				self.OnUp()
			else:
				self.OnDown()

class ThinScrollBar(ScrollBar):

	def CreateScrollBar(self):
		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.SetUpVisual("d:/ymir work/ui/public/scrollbar_thin_middle_button_01.sub")
		middleBar.SetOverVisual("d:/ymir work/ui/public/scrollbar_thin_middle_button_02.sub")
		middleBar.SetDownVisual("d:/ymir work/ui/public/scrollbar_thin_middle_button_03.sub")

		upButton = Button()
		upButton.SetParent(self)
		upButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_thin_up_button_01.sub")
		upButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_thin_up_button_02.sub")
		upButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_thin_up_button_03.sub")
		upButton.SetEvent(__mem_func__(self.OnUp))
		upButton.Show()

		downButton = Button()
		downButton.SetParent(self)
		downButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_thin_down_button_01.sub")
		downButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_thin_down_button_02.sub")
		downButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_thin_down_button_03.sub")
		downButton.SetEvent(__mem_func__(self.OnDown))
		downButton.Show()

		self.middleBar = middleBar
		self.upButton = upButton
		self.downButton = downButton

		self.SCROLLBAR_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
		self.SCROLLBAR_BUTTON_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_BUTTON_HEIGHT = self.upButton.GetHeight()
		self.MIDDLE_BAR_POS = 0
		self.MIDDLE_BAR_UPPER_PLACE = 0
		self.MIDDLE_BAR_DOWNER_PLACE = 0
		self.TEMP_SPACE = 0

	def UpdateBarSlot(self):
		pass

class SmallThinScrollBar(ScrollBar):
	def CreateScrollBar(self):
		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.SetUpVisual("d:/ymir work/ui/public/scrollbar_small_thin_middle_button_01.sub")
		middleBar.SetOverVisual("d:/ymir work/ui/public/scrollbar_small_thin_middle_button_01.sub")
		middleBar.SetDownVisual("d:/ymir work/ui/public/scrollbar_small_thin_middle_button_01.sub")

		upButton = Button()
		upButton.SetParent(self)
		upButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_small_thin_up_button_01.sub")
		upButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_small_thin_up_button_02.sub")
		upButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_small_thin_up_button_03.sub")
		upButton.SetEvent(__mem_func__(self.OnUp))
		upButton.Show()

		downButton = Button()
		downButton.SetParent(self)
		downButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_small_thin_down_button_01.sub")
		downButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_small_thin_down_button_02.sub")
		downButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_small_thin_down_button_03.sub")
		downButton.SetEvent(__mem_func__(self.OnDown))
		downButton.Show()

		self.middleBar = middleBar
		self.upButton = upButton
		self.downButton = downButton

		self.SCROLLBAR_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
		self.SCROLLBAR_BUTTON_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_BUTTON_HEIGHT = self.upButton.GetHeight()
		self.MIDDLE_BAR_POS = 0
		self.MIDDLE_BAR_UPPER_PLACE = 0
		self.MIDDLE_BAR_DOWNER_PLACE = 0
		self.TEMP_SPACE = 0

	def UpdateBarSlot(self):
		pass

class ScrollBarFlat(Window):
	SCROLLBAR_WIDTH = 11
	SCROLLBAR_MIDDLE_HEIGHT = 12
	MIDDLE_BAR_POS = 3
	MIDDLE_BAR_UPPER_PLACE = 0
	MIDDLE_BAR_DOWNER_PLACE = 4
	TEMP_SPACE = MIDDLE_BAR_UPPER_PLACE + MIDDLE_BAR_DOWNER_PLACE

	class MiddleBar(DragButton):
		def __init__(self):
			DragButton.__init__(self)
			self.AddFlag("movable")

		def MakeScrollBar(self):
			self.scrollbar = Bar()
			self.scrollbar.SetParent(self)
			self.scrollbar.SetColor(0xFF6B655A)
			self.scrollbar.SetPosition(3, 3)
			self.scrollbar.SetSize(5, 10)
			self.scrollbar.AddFlag("not_pick")
			self.scrollbar.Show()

		def SetSize(self, height):
			height = max(12, height)
			self.scrollbar.SetSize(5, height)
			DragButton.SetSize(self, 8, height)

	def __init__(self):
		Window.__init__(self)
		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = lambda *arg: None
		self.lockFlag = FALSE
		self.scrollStep1 = 0.20
		self.scrollStep2 = 0.10
		self.CreateScrollBar()

	def __del__(self):
		Window.__del__(self)

	def CreateScrollBar(self):
		self.barSlotOutline = Bar()
		self.barSlotOutline.SetParent(self)
		self.barSlotOutline.SetSize(11, 50)
		self.barSlotOutline.SetPosition(0, 0)
		self.barSlotOutline.SetColor(0xFF000000)
		self.barSlotOutline.AddFlag("not_pick")
		self.barSlotOutline.Show()

		self.barSlotEdge = Bar()
		self.barSlotEdge.SetParent(self.barSlotOutline)
		self.barSlotEdge.SetSize(9, 48)
		self.barSlotEdge.SetPosition(1, 1)
		self.barSlotEdge.SetColor(0xFF6B655A)
		self.barSlotEdge.AddFlag("not_pick")
		self.barSlotEdge.Show()

		self.barSlotMiddle = Bar()
		self.barSlotMiddle.SetParent(self.barSlotOutline)
		self.barSlotMiddle.SetSize(7, 46)
		self.barSlotMiddle.SetPosition(2, 2)
		self.barSlotMiddle.SetColor(0xFF0C0C0C)
		self.barSlotMiddle.AddFlag("not_pick")
		self.barSlotMiddle.Show()

		self.middleBar = self.MiddleBar()
		self.middleBar.SetParent(self)
		self.middleBar.SetMoveEvent(__mem_func__(self.OnMove))
		self.middleBar.MakeScrollBar()
		self.middleBar.SetSize(12)
		self.middleBar.Show()
		self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()

	def Destroy(self):
		self.middleBar = None
		self.eventScroll = lambda *arg: None

	def SetScrollEvent(self, event):
		self.eventScroll = event

	def SetMiddleBarSize(self, pageScale):
		realHeight = self.GetHeight()
		self.SCROLLBAR_MIDDLE_HEIGHT = int(pageScale * float(realHeight))
		self.middleBar.SetSize(self.SCROLLBAR_MIDDLE_HEIGHT)
		self.pageSize = self.GetHeight() - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)

	def SetScrollBarSize(self, height):
		self.pageSize = height - self.SCROLLBAR_MIDDLE_HEIGHT - self.TEMP_SPACE
		self.SetSize(11, height)
		self.middleBar.SetRestrictMovementArea(self.MIDDLE_BAR_POS, self.MIDDLE_BAR_UPPER_PLACE, self.MIDDLE_BAR_POS, height - self.TEMP_SPACE)
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, 0)
		self.UpdateBarSlot()

	def UpdateBarSlot(self):
		self.barSlotOutline.SetSize(11, self.GetHeight() + 1)
		self.barSlotEdge.SetSize(9, self.barSlotOutline.GetHeight() - 2 + 1)
		self.barSlotMiddle.SetSize(7, self.barSlotOutline.GetHeight() - 4 + 1)

	def GetPos(self):
		return self.curPos

	def SetPos(self, pos):
		pos = max(0.0, pos)
		pos = min(1.0, pos)
		newPos = float(self.pageSize) * pos
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, int(newPos) + self.MIDDLE_BAR_UPPER_PLACE)
		self.OnMove()

	def SetScrollStep(self, step):
		self.scrollStep1 = step

	def GetScrollStep(self):
		return self.scrollStep1

	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep1)

	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep1)

	def OnUp2(self):
		self.SetPos(self.curPos-self.scrollStep2)

	def OnDown2(self):
		self.SetPos(self.curPos+self.scrollStep2)

	def OnMove(self):
		if self.lockFlag:
			return
		if 0 == self.pageSize:
			return
		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(yLocal - self.MIDDLE_BAR_UPPER_PLACE) / float(self.pageSize)
		self.eventScroll()

	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		pickedPos = yMouseLocalPosition
		newPos = float(pickedPos) / float(self.pageSize)
		self.SetPos(newPos)

	def LockScroll(self):
		self.lockFlag = TRUE

	def UnlockScroll(self):
		self.lockFlag = FALSE

class SliderBar(Window):

	def __init__(self):
		Window.__init__(self)

		self.curPos = 1.0
		self.pageSize = 1.0
		self.eventChange = None

		self.__CreateBackGroundImage()
		self.__CreateCursor()

	def __del__(self):
		Window.__del__(self)

	def __CreateBackGroundImage(self):
		img = ImageBox()
		img.SetParent(self)
		img.LoadImage("d:/ymir work/ui/game/windows/sliderbar.sub")
		img.Show()
		self.backGroundImage = img

		##
		self.SetSize(self.backGroundImage.GetWidth(), self.backGroundImage.GetHeight())

	def __CreateCursor(self):
		cursor = DragButton()
		cursor.AddFlag("movable")
		cursor.AddFlag("restrict_y")
		cursor.SetParent(self)
		cursor.SetMoveEvent(__mem_func__(self.__OnMove))
		cursor.SetUpVisual("d:/ymir work/ui/game/windows/sliderbar_cursor.sub")
		cursor.SetOverVisual("d:/ymir work/ui/game/windows/sliderbar_cursor.sub")
		cursor.SetDownVisual("d:/ymir work/ui/game/windows/sliderbar_cursor.sub")
		cursor.Show()
		self.cursor = cursor

		##
		self.cursor.SetRestrictMovementArea(0, 0, self.backGroundImage.GetWidth(), 0)
		self.pageSize = self.backGroundImage.GetWidth() - self.cursor.GetWidth()

	def __OnMove(self):
		(xLocal, yLocal) = self.cursor.GetLocalPosition()
		self.curPos = float(xLocal) / float(self.pageSize)

		if self.eventChange:
			self.eventChange()

	def SetSliderPos(self, pos):
		self.curPos = pos
		self.cursor.SetPosition(int(self.pageSize * pos), 0)

	def GetSliderPos(self):
		return self.curPos

	def SetEvent(self, event):
		self.eventChange = event

	def Enable(self):
		self.cursor.Show()

	def Disable(self):
		self.cursor.Hide()

	if app.ENABLE_FOV_OPTION:
		def SetBackgroundVisual(self, filename):
			if self.backGroundImage:
				self.backGroundImage.LoadImage(filename)

				self.SetSize(self.backGroundImage.GetWidth(), self.backGroundImage.GetHeight())
				self.pageSize = self.backGroundImage.GetWidth() - self.cursor.GetWidth()

			if self.cursor:
				self.cursor.SetRestrictMovementArea(0, 0, self.backGroundImage.GetWidth(), 0)

		def SetButtonVisual(self, path, up, over, down):
			if self.cursor:
				self.cursor.SetUpVisual(path + up)
				self.cursor.SetOverVisual(path + over)
				self.cursor.SetDownVisual(path + down)

class NewSliderBar(Window):

	def __init__(self):
		Window.__init__(self)

		self.curPos = 1.0
		self.pageSize = 1.0
		self.eventChange = None

		self.__CreateBackGroundImage()
		self.__CreateCursor()

	def __del__(self):
		Window.__del__(self)

	def __CreateBackGroundImage(self):
		img = ImageBox()
		img.SetParent(self)
		img.LoadImage("d:/ymir work/ui/game/option/new_slidbar_bg.tga")
		img.Show()
		self.backGroundImage = img

		self.SetSize(self.backGroundImage.GetWidth(), self.backGroundImage.GetHeight())

	def __CreateCursor(self):
		cursor = DragButton()
		cursor.AddFlag("movable")
		cursor.AddFlag("restrict_y")
		cursor.SetParent(self)
		cursor.SetMoveEvent(__mem_func__(self.__OnMove))
		cursor.SetUpVisual("d:/ymir work/ui/game/option/new_mid_bar_slidbar_bg.tga")
		cursor.SetOverVisual("d:/ymir work/ui/game/option/new_mid_bar_slidbar_bg.tga")
		cursor.SetDownVisual("d:/ymir work/ui/game/option/new_mid_bar_slidbar_bg.tga")
		cursor.Show()
		self.cursor = cursor

		self.cursor.SetRestrictMovementArea(0, 0, self.backGroundImage.GetWidth(), 0)
		self.pageSize = self.backGroundImage.GetWidth() - self.cursor.GetWidth()

	def __OnMove(self):
		(xLocal, yLocal) = self.cursor.GetLocalPosition()
		self.curPos = float(xLocal) / float(self.pageSize)

		if self.eventChange:
			self.eventChange()

	def SetSliderPos(self, pos):
		self.curPos = pos
		self.cursor.SetPosition(int(self.pageSize * pos), 0)

	def GetSliderPos(self):
		return self.curPos

	def SetEvent(self, event):
		self.eventChange = event

	def Enable(self):
		self.cursor.Show()

	def Disable(self):
		self.cursor.Hide()

	if app.ENABLE_FOV_OPTION:
		def SetBackgroundVisual(self, filename):
			if self.backGroundImage:
				self.backGroundImage.LoadImage(filename)

				self.SetSize(self.backGroundImage.GetWidth(), self.backGroundImage.GetHeight())
				self.pageSize = self.backGroundImage.GetWidth() - self.cursor.GetWidth()

			if self.cursor:
				self.cursor.SetRestrictMovementArea(0, 0, self.backGroundImage.GetWidth(), 0)

		def SetButtonVisual(self, path, up, over, down):
			if self.cursor:
				self.cursor.SetUpVisual(path + up)
				self.cursor.SetOverVisual(path + over)
				self.cursor.SetDownVisual(path + down)

def calculateRect(curValue, maxValue):
	try:
		return -1.0 + float(curValue) / float(maxValue)
	except:
		return 0.0

class ListBox(Window):

	TEMPORARY_PLACE = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		self.overLine = -1
		self.selectedLine = -1
		self.width = 0
		self.height = 0
		self.stepSize = 19 # 17
		self.basePos = 0
		self.showLineCount = 0
		self.itemCenterAlign = TRUE
		self.itemList = []
		self.keyDict = {}
		self.textDict = {}
		self.event = lambda *arg: None
	def __del__(self):
		Window.__del__(self)

	def SetWidth(self, width):
		self.SetSize(width, self.height)

	def SetSize(self, width, height):
		Window.SetSize(self, width, height)
		self.width = width
		self.height = height

	def SetTextCenterAlign(self, flag):
		self.itemCenterAlign = flag

	def SetBasePos(self, pos):
		self.basePos = pos
		self._LocateItem()

	def ClearItem(self):
		self.keyDict = {}
		self.textDict = {}
		self.itemList = []
		self.overLine = -1
		self.selectedLine = -1

	def InsertItem(self, number, text):
		self.keyDict[len(self.itemList)] = number
		self.textDict[len(self.itemList)] = text

		textLine = TextLine()
		textLine.SetParent(self)
		textLine.SetText(text)
		textLine.Show()

		if self.itemCenterAlign:
			textLine.SetWindowHorizontalAlignCenter()
			textLine.SetHorizontalAlignCenter()

		self.itemList.append(textLine)

		self._LocateItem()

	def ChangeItem(self, number, text):
		for key, value in self.keyDict.items():
			if value == number:
				self.textDict[key] = text

				if number < len(self.itemList):
					self.itemList[key].SetText(text)

				return

	def LocateItem(self):
		self._LocateItem()

	def _LocateItem(self):

		skipCount = self.basePos
		yPos = 0
		self.showLineCount = 0

		for textLine in self.itemList:
			textLine.Hide()

			if skipCount > 0:
				skipCount -= 1
				continue

			textLine.SetPosition(0, yPos + 3)

			yPos += self.stepSize

			if yPos <= self.GetHeight():
				self.showLineCount += 1
				textLine.Show()

	def ArrangeItem(self):
		self.SetSize(self.width, len(self.itemList) * self.stepSize)
		self._LocateItem()

	def GetViewItemCount(self):
		return int(self.GetHeight() / self.stepSize)

	def GetItemCount(self):
		return len(self.itemList)

	def SetEvent(self, event):
		self.event = event

	def SelectItem(self, line):

		if not self.keyDict.has_key(line):
			return

		if line == self.selectedLine:
			return

		self.selectedLine = line
		self.event(self.keyDict.get(line, 0), self.textDict.get(line, "None"))

	def GetSelectedItem(self):
		return self.keyDict.get(self.selectedLine, 0)

	def OnMouseLeftButtonDown(self):
		if self.overLine < 0:
			return

	def OnMouseLeftButtonUp(self):
		if self.overLine >= 0:
			self.SelectItem(self.overLine+self.basePos)

	def OnUpdate(self):
		self.overLine = -1

		if self.IsIn():
			x, y = self.GetGlobalPosition()
			height = self.GetHeight()
			xMouse, yMouse = wndMgr.GetMousePosition()

			if yMouse - y < height - 1:
				self.overLine = (yMouse - y) / self.stepSize

				if self.overLine < 0:
					self.overLine = -1
				if self.overLine >= len(self.itemList):
					self.overLine = -1

	def OnRender(self):
		xRender, yRender = self.GetGlobalPosition()
		yRender -= self.TEMPORARY_PLACE
		widthRender = self.width
		heightRender = self.height + self.TEMPORARY_PLACE*2

		if -1 != self.overLine:
			grp.SetColor(HALF_WHITE_COLOR)
			grp.RenderBar(xRender + 2, yRender + self.overLine*self.stepSize + 4, self.width - 3, self.stepSize)

		if -1 != self.selectedLine:
			if self.selectedLine >= self.basePos:
				if self.selectedLine - self.basePos < self.showLineCount:
					grp.SetColor(SELECT_COLOR)
					grp.RenderBar(xRender + 2, yRender + (self.selectedLine-self.basePos)*self.stepSize + 4, self.width - 3, self.stepSize)

class ListBox2(ListBox):
	def __init__(self, *args, **kwargs):
		ListBox.__init__(self, *args, **kwargs)
		self.rowCount = 10
		self.barWidth = 0
		self.colCount = 0

	def SetRowCount(self, rowCount):
		self.rowCount = rowCount

	def SetSize(self, width, height):
		ListBox.SetSize(self, width, height)
		self._RefreshForm()

	def ClearItem(self):
		ListBox.ClearItem(self)
		self._RefreshForm()

	def InsertItem(self, *args, **kwargs):
		ListBox.InsertItem(self, *args, **kwargs)
		self._RefreshForm()

	def OnUpdate(self):
		mpos = wndMgr.GetMousePosition()
		self.overLine = self._CalcPointIndex(mpos)

	def OnRender(self):
		x, y = self.GetGlobalPosition()
		pos = (x + 2, y)

		if -1 != self.overLine:
			grp.SetColor(HALF_WHITE_COLOR)
			self._RenderBar(pos, self.overLine)

		if -1 != self.selectedLine:
			if self.selectedLine >= self.basePos:
				if self.selectedLine - self.basePos < self.showLineCount:
					grp.SetColor(SELECT_COLOR)
					self._RenderBar(pos, self.selectedLine-self.basePos)

	def _CalcPointIndex(self, mpos):
		if self.IsIn():
			px, py = mpos
			gx, gy = self.GetGlobalPosition()
			lx, ly = px - gx, py - gy

			col = lx / self.barWidth
			row = ly / self.stepSize
			idx = col * self.rowCount + row
			if col >= 0 and col < self.colCount:
				if row >= 0 and row < self.rowCount:
					if idx >= 0 and idx < len(self.itemList):
						return idx

		return -1

	def _CalcRenderPos(self, pos, idx):
		x, y = pos
		row = idx % self.rowCount
		col = idx / self.rowCount
		return (x + col * self.barWidth, y + row * self.stepSize)

	def _RenderBar(self, basePos, idx):
		x, y = self._CalcRenderPos(basePos, idx)
		grp.RenderBar(x, y, self.barWidth - 3, self.stepSize)

	def _LocateItem(self):
		pos = (0, self.TEMPORARY_PLACE)

		self.showLineCount = 0
		for textLine in self.itemList:
			x, y = self._CalcRenderPos(pos, self.showLineCount)
			textLine.SetPosition(x, y)
			textLine.Show()

			self.showLineCount += 1

	def _RefreshForm(self):
		if len(self.itemList) % self.rowCount:
			self.colCount = len(self.itemList) / self.rowCount + 1
		else:
			self.colCount = len(self.itemList) / self.rowCount

		if self.colCount:
			self.barWidth = self.width / self.colCount
		else:
			self.barWidth = self.width

class ComboBox(Window):
	class ListBoxWithBoard(ListBox):
		def __init__(self, layer):
			ListBox.__init__(self, layer)

		def OnRender(self):
			xRender, yRender = self.GetGlobalPosition()
			yRender -= self.TEMPORARY_PLACE
			widthRender = self.width
			heightRender = self.height + self.TEMPORARY_PLACE*2
			grp.SetColor(BACKGROUND_COLOR)
			grp.RenderBar(xRender, yRender, widthRender, heightRender)
			grp.SetColor(DARK_COLOR)
			grp.RenderLine(xRender, yRender, widthRender, 0)
			grp.RenderLine(xRender, yRender, 0, heightRender)
			grp.SetColor(BRIGHT_COLOR)
			grp.RenderLine(xRender, yRender+heightRender, widthRender, 0)
			grp.RenderLine(xRender+widthRender, yRender, 0, heightRender)

			ListBox.OnRender(self)

	def __init__(self):
		Window.__init__(self)
		self.x = 0
		self.y = 0
		self.width = 0
		self.height = 0
		self.isSelected = FALSE
		self.isOver = FALSE
		self.isListOpened = FALSE
		self.event = lambda *arg: None
		self.enable = TRUE

		self.textLine = MakeTextLine(self)
		self.textLine.SetText(localeInfo.UI_ITEM)

		self.listBox = self.ListBoxWithBoard("TOP_MOST")
		self.listBox.SetPickAlways()
		self.listBox.SetParent(self)
		self.listBox.SetEvent(__mem_func__(self.OnSelectItem))
		self.listBox.Hide()

	def __del__(self):
		Window.__del__(self)

	def Destroy(self):
		self.textLine = None
		self.listBox = None

	def SetPosition(self, x, y):
		Window.SetPosition(self, x, y)
		self.x = x
		self.y = y
		self.__ArrangeListBox()

	def SetSize(self, width, height):
		Window.SetSize(self, width, height)
		self.width = width
		self.height = height
		self.textLine.UpdateRect()
		self.__ArrangeListBox()

	def __ArrangeListBox(self):
		self.listBox.SetPosition(0, self.height + 5)
		self.listBox.SetWidth(self.width)

	def Enable(self):
		self.enable = TRUE

	def Disable(self):
		self.enable = FALSE
		self.textLine.SetText("")
		self.CloseListBox()

	def SetEvent(self, event):
		self.event = event

	def ClearItem(self):
		self.CloseListBox()
		self.listBox.ClearItem()

	def InsertItem(self, index, name):
		self.listBox.InsertItem(index, name)
		self.listBox.ArrangeItem()

	def SetCurrentItem(self, text):
		self.textLine.SetText(text)

	def SelectItem(self, key):
		self.listBox.SelectItem(key)

	def OnSelectItem(self, index, name):

		self.CloseListBox()
		self.event(index)

	def CloseListBox(self):
		self.isListOpened = FALSE
		self.listBox.Hide()

	def OnMouseLeftButtonDown(self):

		if not self.enable:
			return

		self.isSelected = TRUE

	def OnMouseLeftButtonUp(self):

		if not self.enable:
			return

		self.isSelected = FALSE

		if self.isListOpened:
			self.CloseListBox()
		else:
			if self.listBox.GetItemCount() > 0:
				self.isListOpened = TRUE
				self.listBox.Show()
				self.__ArrangeListBox()

	def OnUpdate(self):

		if not self.enable:
			return

		if self.IsIn():
			self.isOver = TRUE
		else:
			self.isOver = FALSE

	def OnRender(self):
		self.x, self.y = self.GetGlobalPosition()
		xRender = self.x
		yRender = self.y
		widthRender = self.width
		heightRender = self.height
		grp.SetColor(BACKGROUND_COLOR)
		grp.RenderBar(xRender, yRender, widthRender, heightRender)
		grp.SetColor(DARK_COLOR)
		grp.RenderLine(xRender, yRender, widthRender, 0)
		grp.RenderLine(xRender, yRender, 0, heightRender)
		grp.SetColor(BRIGHT_COLOR)
		grp.RenderLine(xRender, yRender+heightRender, widthRender, 0)
		grp.RenderLine(xRender+widthRender, yRender, 0, heightRender)

		if self.isOver:
			grp.SetColor(HALF_WHITE_COLOR)
			grp.RenderBar(xRender + 2, yRender + 3, self.width - 3, heightRender - 5)

			if self.isSelected:
				grp.SetColor(WHITE_COLOR)
				grp.RenderBar(xRender + 2, yRender + 3, self.width - 3, heightRender - 5)

###################################################################################################
## Python Script Loader
###################################################################################################

class ScriptWindow(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		self.Children = []
		self.ElementDictionary = {}
	def __del__(self):
		Window.__del__(self)

	def ClearDictionary(self):
		self.Children = []
		self.ElementDictionary = {}
	def InsertChild(self, name, child):
		self.ElementDictionary[name] = child

	def IsChild(self, name):
		return self.ElementDictionary.has_key(name)
	def GetChild(self, name):
		return self.ElementDictionary[name]

	def GetChild2(self, name):
		return self.ElementDictionary.get(name, None)


class PythonScriptLoader(object):

	BODY_KEY_LIST = ( "x", "y", "width", "height" )

	#####

	DEFAULT_KEY_LIST = ( "type", "x", "y", )
	WINDOW_KEY_LIST = ( "width", "height", )
	IMAGE_KEY_LIST = ( "image", )
	EXPANDED_IMAGE_KEY_LIST = ( "image", )
	ANI_IMAGE_KEY_LIST = ( "images", )
	SLOT_KEY_LIST = ( "width", "height", "slot", )
	CANDIDATE_LIST_KEY_LIST = ( "item_step", "item_xsize", "item_ysize", )
	GRID_TABLE_KEY_LIST = ( "start_index", "x_count", "y_count", "x_step", "y_step", )
	EDIT_LINE_KEY_LIST = ( "width", "height", "input_limit", )
	COMBO_BOX_KEY_LIST = ( "width", "height", "item", )
	TITLE_BAR_KEY_LIST = ( "width", )
	HORIZONTAL_BAR_KEY_LIST = ( "width", )
	BOARD_KEY_LIST = ( "width", "height", )
	BOARD_WITH_TITLEBAR_KEY_LIST = ( "width", "height", "title", )
	BOX_KEY_LIST = ( "width", "height", )
	BAR_KEY_LIST = ( "width", "height", )
	LINE_KEY_LIST = ( "width", "height", )
	SLOTBAR_KEY_LIST = ( "width", "height", )
	GAUGE_KEY_LIST = ( "width", "color", )
	GAUGE2_KEY_LIST = ( "width", )
	SCROLLBAR_KEY_LIST = ( "size", )
	LIST_BOX_KEY_LIST = ( "width", "height", )

	if app.ENABLE_RENEWAL_QUEST:
		SUB_TITLE_BAR_KEY_LIST = ( "width", )
		LIST_BAR_KEY_LIST = ( "width", )

	if app.ENABLE_RENDER_TARGET:
		RENDER_TARGET_KEY_LIST = ( "index", )

	def __init__(self):
		self.Clear()

	def Clear(self):
		self.ScriptDictionary = { "SCREEN_WIDTH" : wndMgr.GetScreenWidth(), "SCREEN_HEIGHT" : wndMgr.GetScreenHeight() }
		self.InsertFunction = 0

	def LoadScriptFile(self, window, FileName):
		import exception
		import exceptions
		import os
		import errno
		self.Clear()

		print "===== Load Script File : %s" % (FileName)

		try:
			self.ScriptDictionary["PLAYER_NAME_MAX_LEN"] = chr.PLAYER_NAME_MAX_LEN
			self.ScriptDictionary["DRAGON_SOUL_EQUIPMENT_SLOT_START"] = player.DRAGON_SOUL_EQUIPMENT_SLOT_START
			self.ScriptDictionary["LOCALE_PATH"] = app.GetLocalePath()
			execfile(FileName, self.ScriptDictionary)
		except IOError, err:
			import sys
			import dbg
			dbg.TraceError("Failed to load script file : %s" % (FileName))
			dbg.TraceError("error  : %s" % (err))
			exception.Abort("LoadScriptFile1")
		except RuntimeError,err:
			import sys
			import dbg
			dbg.TraceError("Failed to load script file : %s" % (FileName))
			dbg.TraceError("error  : %s" % (err))
			exception.Abort("LoadScriptFile2")
		except:
			import sys
			import dbg
			dbg.TraceError("Failed to load script file : %s" % (FileName))
			exception.Abort("LoadScriptFile!!!!!!!!!!!!!!")

		Body = self.ScriptDictionary["window"]
		self.CheckKeyList("window", Body, self.BODY_KEY_LIST)

		window.ClearDictionary()
		self.InsertFunction = window.InsertChild

		window.SetPosition(int(Body["x"]), int(Body["y"]))
		window.SetSize(int(Body["width"]), int(Body["height"]))

		if TRUE == Body.has_key("style"):
			for StyleList in Body["style"]:
				window.AddFlag(StyleList)

		self.LoadChildren(window, Body)

	def LoadChildren(self, parent, dicChildren):
		if TRUE == dicChildren.has_key("style"):
			for style in dicChildren["style"]:
				parent.AddFlag(style)

		if FALSE == dicChildren.has_key("children"):
			return FALSE

		Index = 0

		ChildrenList = dicChildren["children"]
		parent.Children = range(len(ChildrenList))
		for ElementValue in ChildrenList:
			try:
				Name = ElementValue["name"]
			except KeyError:
				Name = ElementValue["name"] = "NONAME"

			try:
				Type = ElementValue["type"]
			except KeyError:
				Type = ElementValue["type"] = "window"

			if FALSE == self.CheckKeyList(Name, ElementValue, self.DEFAULT_KEY_LIST):
				del parent.Children[Index]
				continue

			if Type == "window":
				parent.Children[Index] = ScriptWindow()
				parent.Children[Index].SetParent(parent)
				self.LoadElementWindow(parent.Children[Index], ElementValue, parent)

			elif Type == "button":
				parent.Children[Index] = Button()
				parent.Children[Index].SetParent(parent)
				self.LoadElementButton(parent.Children[Index], ElementValue, parent)

			elif Type == "radio_button":
				parent.Children[Index] = RadioButton()
				parent.Children[Index].SetParent(parent)
				self.LoadElementButton(parent.Children[Index], ElementValue, parent)

			elif Type == "toggle_button":
				parent.Children[Index] = ToggleButton()
				parent.Children[Index].SetParent(parent)
				self.LoadElementButton(parent.Children[Index], ElementValue, parent)

			elif Type == "mark":
				parent.Children[Index] = MarkBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementMark(parent.Children[Index], ElementValue, parent)

			elif Type == "image":
				parent.Children[Index] = ImageBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementImage(parent.Children[Index], ElementValue, parent)

			elif Type == "expanded_image":
				parent.Children[Index] = ExpandedImageBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementExpandedImage(parent.Children[Index], ElementValue, parent)

			elif Type == "ani_image":
				parent.Children[Index] = AniImageBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementAniImage(parent.Children[Index], ElementValue, parent)

			elif Type == "slot":
				parent.Children[Index] = SlotWindow()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSlot(parent.Children[Index], ElementValue, parent)

			elif Type == "candidate_list":
				parent.Children[Index] = CandidateListBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementCandidateList(parent.Children[Index], ElementValue, parent)

			elif Type == "grid_table":
				parent.Children[Index] = GridSlotWindow()
				parent.Children[Index].SetParent(parent)
				self.LoadElementGridTable(parent.Children[Index], ElementValue, parent)

			elif Type == "text":
				parent.Children[Index] = TextLine()
				parent.Children[Index].SetParent(parent)
				self.LoadElementText(parent.Children[Index], ElementValue, parent)

			elif Type == "editline":
				parent.Children[Index] = EditLine()
				parent.Children[Index].SetParent(parent)
				self.LoadElementEditLine(parent.Children[Index], ElementValue, parent)

			elif Type == "titlebar":
				parent.Children[Index] = TitleBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementTitleBar(parent.Children[Index], ElementValue, parent)

			elif Type == "titlebar_without_button" and app.ENABLE_RENEWAL_SWITCHBOT:
				parent.Children[Index] = TitleBarWithoutButton()
				parent.Children[Index].SetParent(parent)
				self.LoadElementTitleBar(parent.Children[Index], ElementValue, parent)

			elif Type == "horizontalbar":
				parent.Children[Index] = HorizontalBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementHorizontalBar(parent.Children[Index], ElementValue, parent)

			elif Type == "board":
				parent.Children[Index] = Board()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "board_with_titlebar":
				parent.Children[Index] = BoardWithTitleBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoardWithTitleBar(parent.Children[Index], ElementValue, parent)

			elif Type == "border_a":
				parent.Children[Index] = BorderA()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBorderA(parent.Children[Index], ElementValue, parent)

			elif Type == "new_board" and app.ENABLE_RENEWAL_SWITCHBOT:
				parent.Children[Index] = NewBoard()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "new_board_with_titlebar" and app.ENABLE_RENEWAL_SWITCHBOT:
				parent.Children[Index] = NewBoardWithTitleBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoardWithTitleBar(parent.Children[Index], ElementValue, parent)

			elif Type == "thinboard":
				parent.Children[Index] = ThinBoard()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "thinboard_gold":
				parent.Children[Index] = ThinBoardGold()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoardGold(parent.Children[Index], ElementValue, parent)

			elif Type == "thinboard_circle":
				parent.Children[Index] = ThinBoardCircle()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoardCircle(parent.Children[Index], ElementValue, parent)

			elif Type == "box":
				parent.Children[Index] = Box()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBox(parent.Children[Index], ElementValue, parent)

			elif Type == "bar":
				parent.Children[Index] = Bar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBar(parent.Children[Index], ElementValue, parent)

			elif Type == "line":
				parent.Children[Index] = Line()
				parent.Children[Index].SetParent(parent)
				self.LoadElementLine(parent.Children[Index], ElementValue, parent)

			elif Type == "slotbar":
				parent.Children[Index] = SlotBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSlotBar(parent.Children[Index], ElementValue, parent)

			elif Type == "gauge":
				parent.Children[Index] = Gauge()
				parent.Children[Index].SetParent(parent)
				self.LoadElementGauge(parent.Children[Index], ElementValue, parent)

			elif Type == "gauge2":
				parent.Children[Index] = Gauge2()
				parent.Children[Index].SetParent(parent)
				self.LoadElementGauge2(parent.Children[Index], ElementValue, parent)

			elif Type == "scrollbar":
				parent.Children[Index] = ScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "thin_scrollbar":
				parent.Children[Index] = ThinScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "small_thin_scrollbar":
				parent.Children[Index] = SmallThinScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "scrollbar_flat":
				parent.Children[Index] = ScrollBarFlat()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "sliderbar":
				parent.Children[Index] = SliderBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSliderBar(parent.Children[Index], ElementValue, parent)

			elif Type == "newsliderbar":
				parent.Children[Index] = NewSliderBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSliderBar(parent.Children[Index], ElementValue, parent)

			elif Type == "listbox":
				parent.Children[Index] = ListBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBox(parent.Children[Index], ElementValue, parent)

			elif Type == "listbox2":
				parent.Children[Index] = ListBox2()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBox2(parent.Children[Index], ElementValue, parent)

			elif Type == "listboxex":
				parent.Children[Index] = ListBoxEx()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBoxEx(parent.Children[Index], ElementValue, parent)

			elif Type == "subtitlebar" and app.ENABLE_RENEWAL_QUEST:
				parent.Children[Index] = SubTitleBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSubTitleBar(parent.Children[Index], ElementValue, parent)

			elif Type == "listbar" and app.ENABLE_RENEWAL_QUEST:
				parent.Children[Index] = ListBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBar(parent.Children[Index], ElementValue, parent)

			elif Type == "scrollbar2" and app.ENABLE_RENEWAL_SWITCHBOT:
				parent.Children[Index] = ScrollBar2()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "checkbox_biolog" and app.ENABLE_BIOLOG_SYSTEM:
				parent.Children[Index] = CheckBox_Biolog()
				parent.Children[Index].SetParent(parent)
				self.LoadElementCheckBoxBiolog(parent.Children[Index], ElementValue, parent)

			elif Type == "render_target" and app.ENABLE_RENDER_TARGET:
				parent.Children[Index] = RenderTarget()
				parent.Children[Index].SetParent(parent)
				self.LoadElementRenderTarget(parent.Children[Index], ElementValue, parent)

			elif Type == "scrollbar3" and app.ENABLE_RENEWAL_OFFLINESHOP:
				parent.Children[Index] = ScrollBar3()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "listbox3" and app.ENABLE_OFFLINESHOP_SEARCH_SYSTEM:
				parent.Children[Index] = ListBox3()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBox(parent.Children[Index], ElementValue, parent)

			elif Type == "invisibleboard":
				parent.Children[Index] = InvisibleBoard()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "multi_text" and app.ENABLE_MULTI_TEXTLINE:
				parent.Children[Index] = MultiTextLine()
				parent.Children[Index].SetParent(parent)
				self.LoadElementMultiText(parent.Children[Index], ElementValue, parent)

			elif Type == "scrollbar4" and app.ENABLE_RENEWAL_BONUS_BOARD:
				parent.Children[Index] = ScrollBar4()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "scrollbar5" and app.ENABLE_EMOTICONS_SYSTEM:
				parent.Children[Index] = ScrollBar5()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "thinboard_special_1" and app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
				parent.Children[Index] = ThinBoardSpecial1()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "specialbar1" and app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
				parent.Children[Index] = SpecialTitleBar1()
				parent.Children[Index].SetParent(parent)
				self.LoadElementHorizontalBar(parent.Children[Index], ElementValue, parent)

			elif Type == "listbox4" and app.ENABLE_DUNGEON_TRACKING_SYSTEM:
				parent.Children[Index] = ListBox4()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBox(parent.Children[Index], ElementValue, parent)

			else:
				Index += 1
				continue

			parent.Children[Index].SetWindowName(Name)
			if 0 != self.InsertFunction:
				self.InsertFunction(Name, parent.Children[Index])

			self.LoadChildren(parent.Children[Index], ElementValue)
			Index += 1

	def CheckKeyList(self, name, value, key_list):

		for DataKey in key_list:
			if FALSE == value.has_key(DataKey):
				print "Failed to find data key", "[" + name + "/" + DataKey + "]"
				return FALSE

		return TRUE

	def LoadDefaultData(self, window, value, parentWindow):
		loc_x = int(value["x"])
		loc_y = int(value["y"])
		if value.has_key("vertical_align"):
			if "center" == value["vertical_align"]:
				window.SetWindowVerticalAlignCenter()
			elif "bottom" == value["vertical_align"]:
				window.SetWindowVerticalAlignBottom()

		if parentWindow.IsRTL():
			loc_x = int(value["x"]) + window.GetWidth()
			if value.has_key("horizontal_align"):
				if "center" == value["horizontal_align"]:
					window.SetWindowHorizontalAlignCenter()
					loc_x = - int(value["x"])
				elif "right" == value["horizontal_align"]:
					window.SetWindowHorizontalAlignLeft()
					loc_x = int(value["x"]) - window.GetWidth()
					## loc_x = parentWindow.GetWidth() - int(value["x"]) + window.GetWidth()
			else:
				window.SetWindowHorizontalAlignRight()

			if value.has_key("all_align"):
				window.SetWindowVerticalAlignCenter()
				window.SetWindowHorizontalAlignCenter()
				loc_x = - int(value["x"])
		else:
			if value.has_key("horizontal_align"):
				if "center" == value["horizontal_align"]:
					window.SetWindowHorizontalAlignCenter()
				elif "right" == value["horizontal_align"]:
					window.SetWindowHorizontalAlignRight()

		window.SetPosition(loc_x, loc_y)
		window.Show()

	## Window
	def LoadElementWindow(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.WINDOW_KEY_LIST):
			return FALSE

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## Button
	def LoadElementButton(self, window, value, parentWindow):

		if value.has_key("width") and value.has_key("height"):
			window.SetSize(int(value["width"]), int(value["height"]))

		if TRUE == value.has_key("x_scale") and TRUE == value.has_key("y_scale"):
			window.SetButtonScale(float(value["x_scale"]), float(value["y_scale"]))

		if TRUE == value.has_key("default_image"):
			window.SetUpVisual(value["default_image"])
		if TRUE == value.has_key("over_image"):
			window.SetOverVisual(value["over_image"])
		if TRUE == value.has_key("down_image"):
			window.SetDownVisual(value["down_image"])
		if TRUE == value.has_key("disable_image"):
			window.SetDisableVisual(value["disable_image"])

		if TRUE == value.has_key("text"):
			if TRUE == value.has_key("text_height"):
				window.SetText(value["text"], value["text_height"])
			else:
				window.SetText(value["text"])

			if value.has_key("text_color"):
				window.SetTextColor(value["text_color"])

			if value.has_key("text_outline"):
				if value["text_outline"]:
					window.SetOutline()

			if TRUE == value.has_key("text_x") and TRUE == value.has_key("text_y"):
				window.SetTextPosition(value["text_x"], value["text_y"])

		if TRUE == value.has_key("tooltip_text"):
			if TRUE == value.has_key("tooltip_x") and TRUE == value.has_key("tooltip_y"):
				window.SetToolTipText(value["tooltip_text"], int(value["tooltip_x"]), int(value["tooltip_y"]))
			else:
				window.SetToolTipText(value["tooltip_text"])

		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## Mark
	def LoadElementMark(self, window, value, parentWindow):

		#if FALSE == self.CheckKeyList(value["name"], value, self.MARK_KEY_LIST):
		#	return FALSE

		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## Image
	def LoadElementImage(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.IMAGE_KEY_LIST):
			return FALSE

		window.LoadImage(value["image"])
		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## AniImage
	def LoadElementAniImage(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.ANI_IMAGE_KEY_LIST):
			return FALSE

		if TRUE == value.has_key("delay"):
			window.SetDelay(value["delay"])

		for image in value["images"]:
			window.AppendImage(image)

		if value.has_key("width") and value.has_key("height"):
			window.SetSize(value["width"], value["height"])

		if TRUE == value.has_key("x_scale") and TRUE == value.has_key("y_scale"):
			window.SetScale(float(value["x_scale"]), float(value["y_scale"]))

		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## Expanded Image
	def LoadElementExpandedImage(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.EXPANDED_IMAGE_KEY_LIST):
			return FALSE

		window.LoadImage(value["image"])

		if TRUE == value.has_key("x_origin") and TRUE == value.has_key("y_origin"):
			window.SetOrigin(float(value["x_origin"]), float(value["y_origin"]))

		if TRUE == value.has_key("x_scale") and TRUE == value.has_key("y_scale"):
			window.SetScale(float(value["x_scale"]), float(value["y_scale"]))

		if TRUE == value.has_key("rect"):
			RenderingRect = value["rect"]
			window.SetRenderingRect(RenderingRect[0], RenderingRect[1], RenderingRect[2], RenderingRect[3])

		if TRUE == value.has_key("mode"):
			mode = value["mode"]
			if "MODULATE" == mode:
				window.SetRenderingMode(wndMgr.RENDERING_MODE_MODULATE)

		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## Slot
	def LoadElementSlot(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.SLOT_KEY_LIST):
			return FALSE

		global_x = int(value["x"])
		global_y = int(value["y"])
		global_width = int(value["width"])
		global_height = int(value["height"])

		window.SetPosition(global_x, global_y)
		window.SetSize(global_width, global_height)
		window.Show()

		r = 1.0
		g = 1.0
		b = 1.0
		a = 1.0

		if TRUE == value.has_key("image_r") and \
			TRUE == value.has_key("image_g") and \
			TRUE == value.has_key("image_b") and \
			TRUE == value.has_key("image_a"):
			r = float(value["image_r"])
			g = float(value["image_g"])
			b = float(value["image_b"])
			a = float(value["image_a"])

		SLOT_ONE_KEY_LIST = ("index", "x", "y", "width", "height")

		for slot in value["slot"]:
			if TRUE == self.CheckKeyList(value["name"] + " - one", slot, SLOT_ONE_KEY_LIST):
				wndMgr.AppendSlot(window.hWnd,
									int(slot["index"]),
									int(slot["x"]),
									int(slot["y"]),
									int(slot["width"]),
									int(slot["height"]))

		if TRUE == value.has_key("x_scale") and TRUE == value.has_key("y_scale"):
			window.SetSlotScale(float(value["x_scale"]), float(value["y_scale"]))

		if TRUE == value.has_key("image"):
			wndMgr.SetSlotBaseImage(window.hWnd,
									value["image"],
									r, g, b, a)

		return TRUE

	def LoadElementCandidateList(self, window, value, parentWindow):
		if FALSE == self.CheckKeyList(value["name"], value, self.CANDIDATE_LIST_KEY_LIST):
			return FALSE

		window.SetPosition(int(value["x"]), int(value["y"]))
		window.SetItemSize(int(value["item_xsize"]), int(value["item_ysize"]))
		window.SetItemStep(int(value["item_step"]))		
		window.Show()

		return TRUE
				
	## Table
	def LoadElementGridTable(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.GRID_TABLE_KEY_LIST):
			return FALSE

		xBlank = 0
		yBlank = 0
		if TRUE == value.has_key("x_blank"):
			xBlank = int(value["x_blank"])
		if TRUE == value.has_key("y_blank"):
			yBlank = int(value["y_blank"])

		window.SetPosition(int(value["x"]), int(value["y"]))

		window.ArrangeSlot(	int(value["start_index"]),
							int(value["x_count"]),
							int(value["y_count"]),
							int(value["x_step"]),
							int(value["y_step"]),
							xBlank,
							yBlank)
		if TRUE == value.has_key("image"):
			r = 1.0
			g = 1.0
			b = 1.0
			a = 1.0
			if TRUE == value.has_key("image_r") and \
				TRUE == value.has_key("image_g") and \
				TRUE == value.has_key("image_b") and \
				TRUE == value.has_key("image_a"):
				r = float(value["image_r"])
				g = float(value["image_g"])
				b = float(value["image_b"])
				a = float(value["image_a"])
			wndMgr.SetSlotBaseImage(window.hWnd, value["image"], r, g, b, a)

		if TRUE == value.has_key("style"):
			if "select" == value["style"]:
				wndMgr.SetSlotStyle(window.hWnd, wndMgr.SLOT_STYLE_SELECT)

		window.Show()
		return TRUE

	## Text
	def LoadElementText(self, window, value, parentWindow):
		if value.has_key("fontsize"):
			fontSize = value["fontsize"]

			if "SLARGE" == fontSize:
				window.SetFontName(localeInfo.UI_DEF_FONT_SLARGE)

			if "LARGE" == fontSize:
				window.SetFontName(localeInfo.UI_DEF_FONT_LARGE)

			if "XLARGE" == fontSize:
				window.SetFontName(localeInfo.UI_DEF_FONT_XLARGE)

			if "XXLARGE" == fontSize:
				window.SetFontName(localeInfo.UI_DEF_FONT_XXLARGE)

			if "SMALL" == fontSize:
				window.SetFontName(localeInfo.UI_DEF_FONT_SMALL)

		elif value.has_key("fontname"):
			fontName = value["fontname"]
			window.SetFontName(fontName)

		if value.has_key("text_horizontal_align"):
			if "left" == value["text_horizontal_align"]:
				window.SetHorizontalAlignLeft()
			elif "center" == value["text_horizontal_align"]:
				window.SetHorizontalAlignCenter()
			elif "right" == value["text_horizontal_align"]:
				window.SetHorizontalAlignRight()

		if value.has_key("text_vertical_align"):
			if "top" == value["text_vertical_align"]:
				window.SetVerticalAlignTop()
			elif "center" == value["text_vertical_align"]:
				window.SetVerticalAlignCenter()
			elif "bottom" == value["text_vertical_align"]:
				window.SetVerticalAlignBottom()

		if value.has_key("all_align"):
			window.SetHorizontalAlignCenter()
			window.SetVerticalAlignCenter()
			window.SetWindowHorizontalAlignCenter()
			window.SetWindowVerticalAlignCenter()

		if value.has_key("r") and value.has_key("g") and value.has_key("b"):
			window.SetFontColor(float(value["r"]), float(value["g"]), float(value["b"]))
		elif value.has_key("color"):
			window.SetPackedFontColor(value["color"])
		else:
			window.SetFontColor(0.8549, 0.8549, 0.8549)

		if value.has_key("outline"):
			if value["outline"]:
				window.SetOutline()
		if TRUE == value.has_key("text"):
			window.SetText(value["text"])

		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## EditLine
	def LoadElementEditLine(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.EDIT_LINE_KEY_LIST):
			return FALSE


		if value.has_key("secret_flag"):
			window.SetSecret(value["secret_flag"])
		if value.has_key("with_codepage"):
			if value["with_codepage"]:
				window.bCodePage = TRUE
		if value.has_key("only_number"):
			if value["only_number"]:
				window.SetNumberMode()
		if value.has_key("enable_codepage"):
			window.SetIMEFlag(value["enable_codepage"])
		if value.has_key("enable_ime"):
			window.SetIMEFlag(value["enable_ime"])
		if value.has_key("limit_width"):
			window.SetLimitWidth(value["limit_width"])
		if value.has_key("multi_line"):
			if value["multi_line"]:
				window.SetMultiLine()
		if value.has_key("overlay"):
			window.SetOverlayText(value["overlay"])
		if value.has_key("info_msg"):
			window.SetInfoMessage(value["info_msg"])

		window.SetMax(int(value["input_limit"]))
		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadElementText(window, value, parentWindow)

		return TRUE

	## TitleBar
	def LoadElementTitleBar(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.TITLE_BAR_KEY_LIST):
			return FALSE

		window.MakeTitleBar(int(value["width"]), value.get("color", "red"))
		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## HorizontalBar
	def LoadElementHorizontalBar(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.HORIZONTAL_BAR_KEY_LIST):
			return FALSE

		window.Create(int(value["width"]))
		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## Board
	def LoadElementBoard(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.BOARD_KEY_LIST):
			return FALSE

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## Board With TitleBar
	def LoadElementBoardWithTitleBar(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.BOARD_WITH_TITLEBAR_KEY_LIST):
			return FALSE

		window.SetSize(int(value["width"]), int(value["height"]))
		window.SetTitleName(value["title"])
		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## BoardA
	def LoadElementBorderA(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.BOARD_KEY_LIST):
			return FALSE

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## ThinBoard
	def LoadElementThinBoard(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.BOARD_KEY_LIST):
			return FALSE

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## ThinBoardGold
	def LoadElementThinBoardGold(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.BOARD_KEY_LIST):
			return FALSE

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## ThinBoardCircle
	def LoadElementThinBoardCircle(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.BOARD_KEY_LIST):
			return FALSE

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	if app.ENABLE_RENEWAL_QUEST:
		## SubTitleBar
		def LoadElementSubTitleBar(self, window, value, parentWindow):
			if FALSE == self.CheckKeyList(value["name"], value, self.SUB_TITLE_BAR_KEY_LIST):
				return FALSE

			window.MakeSubTitleBar(int(value["width"]), value.get("color", "red"))
			self.LoadElementButton(window, value, parentWindow)
			window.Show()
			return TRUE

		## ListBar
		def LoadElementListBar(self, window, value, parentWindow):
			if FALSE == self.CheckKeyList(value["name"], value, self.LIST_BAR_KEY_LIST):
				return FALSE

			window.MakeListBar(int(value["width"]), value.get("color", "red"))
			self.LoadElementButton(window, value, parentWindow)

			return TRUE

	if app.ENABLE_BIOLOG_SYSTEM:
		def LoadElementCheckBoxBiolog(self, window, value, parentWindow):

			if value.has_key("text"):
				window.SetText(value["text"])

			if value.has_key("checked") and value["checked"] == TRUE:
				window.SetChecked(window.STATE_SELECTED)

			if value.has_key("disabled") and value["disabled"] == TRUE:
				window.Disable()

			self.LoadDefaultData(window, value, parentWindow)

	## Box
	def LoadElementBox(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.BOX_KEY_LIST):
			return FALSE

		if TRUE == value.has_key("color"):
			window.SetColor(value["color"])

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## Bar
	def LoadElementBar(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.BAR_KEY_LIST):
			return FALSE

		if TRUE == value.has_key("color"):
			window.SetColor(value["color"])

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## Line
	def LoadElementLine(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.LINE_KEY_LIST):
			return FALSE

		if TRUE == value.has_key("color"):
			window.SetColor(value["color"])

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## Slot
	def LoadElementSlotBar(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.SLOTBAR_KEY_LIST):
			return FALSE

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## Gauge
	def LoadElementGauge(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.GAUGE_KEY_LIST):
			return FALSE

		window.MakeGauge(value["width"], value["color"])
		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## Gauge2
	def LoadElementGauge2(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.GAUGE2_KEY_LIST):
			return FALSE

		window.MakeGauge(value["width"])
		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## ScrollBar
	def LoadElementScrollBar(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.SCROLLBAR_KEY_LIST):
			return FALSE

		window.SetScrollBarSize(value["size"])
		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## SliderBar
	def LoadElementSliderBar(self, window, value, parentWindow):

		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## ListBox
	def LoadElementListBox(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.LIST_BOX_KEY_LIST):
			return FALSE

		if value.has_key("item_align"):
			window.SetTextCenterAlign(value["item_align"])

		window.SetSize(value["width"], value["height"])
		self.LoadDefaultData(window, value, parentWindow)

		return TRUE

	## ListBox2
	def LoadElementListBox2(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.LIST_BOX_KEY_LIST):
			return FALSE

		window.SetRowCount(value.get("row_count", 10)) 
		window.SetSize(value["width"], value["height"])
		self.LoadDefaultData(window, value, parentWindow)

		if value.has_key("item_align"):
			window.SetTextCenterAlign(value["item_align"])

		return TRUE

	def LoadElementListBoxEx(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.LIST_BOX_KEY_LIST):
			return FALSE

		window.SetSize(value["width"], value["height"])
		self.LoadDefaultData(window, value, parentWindow)

		if value.has_key("itemsize_x") and value.has_key("itemsize_y"):
			window.SetItemSize(int(value["itemsize_x"]), int(value["itemsize_y"]))

		if value.has_key("itemstep"):
			window.SetItemStep(int(value["itemstep"]))

		if value.has_key("viewcount"):
			window.SetViewItemCount(int(value["viewcount"]))

		return TRUE

	if app.ENABLE_RENDER_TARGET:
		def LoadElementRenderTarget(self, window, value, parentWindow):

			if FALSE == self.CheckKeyList(value["name"], value, self.RENDER_TARGET_KEY_LIST):
				return FALSE

			window.SetSize(value["width"], value["height"])

			if TRUE == value.has_key("style"):
				for style in value["style"]:
					window.AddFlag(style)

			self.LoadDefaultData(window, value, parentWindow)

			if value.has_key("index"):
				window.SetRenderTarget(int(value["index"]))

			return TRUE

	if app.ENABLE_MULTI_TEXTLINE:
		def LoadElementMultiText(self, window, value, parentWindow):

			if TRUE == value.has_key("width"):
				window.SetWidth(int(value.get("width", 0)))

			if TRUE == value.has_key("text_horizontal_align"):
				if value["text_horizontal_align"] == "center":
					window.SetTextHorizontalAlignCenter()

			if TRUE == value.has_key("text"):
				window.SetText(value["text"])

			self.LoadDefaultData(window, value, parentWindow)

			return TRUE

class ReadingWnd(Bar):

	def __init__(self):
		Bar.__init__(self,"TOP_MOST")

		self.__BuildText()
		self.SetSize(80, 19)
		self.Show()

	def __del__(self):
		Bar.__del__(self)

	def __BuildText(self):
		self.text = TextLine()
		self.text.SetParent(self)
		self.text.SetPosition(4, 3)
		self.text.Show()

	def SetText(self, text):
		self.text.SetText(text)

	def SetReadingPosition(self, x, y):
		xPos = x + 2
		yPos = y  - self.GetHeight() - 2
		self.SetPosition(xPos, yPos)

	def SetTextColor(self, color):
		self.text.SetPackedFontColor(color)

if app.ENABLE_BIOLOG_SYSTEM:
	class CheckBox_Biolog(Window):
		STATE_UNSELECTED = 0
		STATE_SELECTED = 1

		def __init__(self, layer = "UI"):
			Window.__init__(self, layer)

			self.state = self.STATE_UNSELECTED
			self.eventFunc = None
			self.eventArgs = None

			self.overIn = ""

			self.btnBox = {
				self.STATE_UNSELECTED : self.__init_MakeButton("d:/ymir work/ui/game/biolog_manager/checkbox_new_unselected.tga"),
				self.STATE_SELECTED : self.__init_MakeButton("d:/ymir work/ui/game/biolog_manager/checkbox_new_selected.tga", "d:/ymir work/ui/game/biolog_manager/checkbox_new_selected.tga"),
			}

			text = TextLine()
			text.SetParent(self)
			text.SetWindowVerticalAlignCenter()
			text.SetVerticalAlignCenter()
			text.Show()
			self.text = text

			self.__Refresh()

			self.SetWindowName("NONAME_CheckBox")

		def __del__(self):
			Window.__del__(self)

		def __ConvertPath(self, path, subStr):
			if path.find("%s") != -1:
				return path % subStr
			else:
				return path

		def __init_MakeButton(self, path, disablePath = None):
			btn = Button()
			btn.SetParent(self)
			btn.SetWindowVerticalAlignCenter()
			btn.SetUpVisual(self.__ConvertPath(path, "01"))
			btn.SetOverVisual(self.__ConvertPath(path, "02"))
			btn.SetDownVisual(self.__ConvertPath(path, "03"))
			if disablePath:
				btn.SetDisableVisual(disablePath)
			else:
				btn.SetDisableVisual(self.__ConvertPath(path, "01"))
			btn.SAFE_SetEvent(self.OnClickButton)
			btn.baseWidth = btn.GetWidth()
			return btn

		def __UpdateRect(self):
			if self.text.GetText():
				width = self.btnBox[self.state].baseWidth + 5 + self.text.GetTextWidth()
			else:
				width = self.btnBox[self.state].baseWidth
			height = max(self.btnBox[self.state].GetHeight(), self.text.GetTextHeight())
			self.SetSize(width, height)

			self.btnBox[self.state].SetSize(width, self.btnBox[self.state].GetHeight())
			self.text.SetPosition(self.btnBox[self.state].baseWidth + 5, 0)

			self.text.UpdateRect()
			self.btnBox[self.state].UpdateRect()
			self.UpdateRect()

		def __Refresh(self):
			self.__UpdateRect()

			self.btnBox[self.STATE_UNSELECTED].SetVisible(self.state == self.STATE_UNSELECTED)
			self.btnBox[self.STATE_SELECTED].SetVisible(self.state == self.STATE_SELECTED)

		def SAFE_SetOverInData(self, data):
			self.btnBox[self.state].SetToolTipText(data)

		def OnClickButton(self):
			if self.state == self.STATE_UNSELECTED:
				self.state = self.STATE_SELECTED
			else:
				self.state = self.STATE_UNSELECTED

			self.__Refresh()

			if self.eventFunc:
				apply(self.eventFunc, self.eventArgs)

		def SetChecked(self, state):
			self.state = state
			self.__Refresh()

		def IsChecked(self):
			return self.state != self.STATE_UNSELECTED

		def SetText(self, text):
			self.text.SetText(text)
			self.__UpdateRect()

		def SetEvent(self, event, *args):
			self.eventFunc = event
			self.eventArgs = args

		def SAFE_SetEvent(self, event, *args):
			self.eventFunc = __mem_func__(event)
			self.eventArgs = args

		def Disable(self):
			self.btnBox[self.STATE_UNSELECTED].Disable()
			self.btnBox[self.STATE_SELECTED].Disable()

		def Enable(self):
			self.btnBox[self.STATE_UNSELECTED].Enable()
			self.btnBox[self.STATE_SELECTED].Enable()

if app.ENABLE_RENDER_TARGET:
	class RenderTarget(Window):
		def __init__(self, layer = "UI"):
			Window.__init__(self, layer)

			if app.ENABLE_INGAME_WIKI_SYSTEM:
				self.eventDict = {}
				self.eventFunc = {"mouse_click" : None, "mouse_over_in" : None, "mouse_over_out" : None}
				self.eventArgs = {"mouse_click" : None, "mouse_over_in" : None, "mouse_over_out" : None}

		def Destroy(self):
			if app.ENABLE_INGAME_WIKI_SYSTEM:
				self.eventDict = {}
				self.eventFunc = 0
				self.eventArgs = 0

		def __del__(self):
			Window.__del__(self)

		def RegisterWindow(self, layer):
			self.hWnd = wndMgr.RegisterRenderTarget(self, layer)

		def SetRenderTarget(self, number):
			wndMgr.SetRenderTarget(self.hWnd, number)

		if app.ENABLE_INGAME_WIKI_SYSTEM:
			def SetRenderingRect(self, left, top, right, bottom):
				wndMgr.SetRenderingRect(self.hWnd, left, top, right, bottom)

			def SetEvent(self, func, *args):
				self.eventFunc[args[0]] = func
				self.eventArgs[args[0]] = args

			def OnMouseLeftButtonUp(self) :
				if self.eventFunc["mouse_click"] :
					apply(self.eventFunc["mouse_click"], self.eventArgs["mouse_click"])

			def OnMouseOverIn(self):
				try:
					if self.eventFunc["mouse_over_in"]:
						if self.eventArgs:
							apply(self.eventFunc["mouse_over_in"], self.eventArgs["mouse_over_in"])
						else:
							self.eventFunc["mouse_over_in"]()
				except KeyError:
					pass

			def OnMouseOverOut(self):
				try:
					if self.eventFunc["mouse_over_out"]:
						if self.eventArgs:
							apply(self.eventFunc["mouse_over_out"], self.eventArgs["mouse_over_out"])
						else:
							self.eventFunc["mouse_over_out"]()
				except KeyError:
					pass

if app.ENABLE_INGAME_WIKI_SYSTEM:
	class Grid:
		def __init__(self, width, height):
			self.width = width
			self.height = height
			self.reset()

		def find_blank(self, width, height):
			if width > self.width or height > self.height:
				return -1

			for row in range(self.height):
				for col in range(self.width):
					index = row * self.width + col
					if self.is_empty(index, width, height):
						return index
			return -1

		def put(self, pos, width, height):
			if not self.is_empty(pos, width, height):
				return FALSE

			for row in range(height):
				start = pos + (row * self.width)
				self.grid[start] = TRUE
				col = 1

				while col < width:
					self.grid[start + col] = TRUE
					col += 1

			return TRUE

		def clear(self, pos, width, height):
			if pos < 0 or pos >= (self.width * self.height):
				return

			for row in range(height):
				start = pos + (row * self.width)
				self.grid[start] = TRUE
				col = 1

				while col < width:
					self.grid[start + col] = FALSE
					col += 1

		def is_empty(self, pos, width, height):
			if pos < 0:
				return FALSE
			row = pos // self.width
			if (row + height) > self.height:
				return FALSE

			if (pos + width) > ((row * self.width) + self.width):
				return FALSE

			for row in range(height):
				start = pos + (row * self.width)
				if self.grid[start]:
					return FALSE
				col = 1

				while col < width:
					if self.grid[start + col]:
						return FALSE
					col += 1

			return TRUE

		def get_size(self):
			return self.width * self.height

		def reset(self):
			self.grid = [FALSE] * (self.width * self.height)

if app.ENABLE_RENEWAL_OFFLINESHOP:
	class ThinBoardNorm(Window):
		CORNER_WIDTH = 16
		CORNER_HEIGHT = 16
		CORNER_1_WIDTH = 48
		CORNER_1_HEIGHT = 48
		LINE_WIDTH = 16
		LINE_HEIGHT = 16
		BOARD_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.51)

		LT = 0
		LB = 1
		RT = 2
		RB = 3
		L = 0
		R = 1
		T = 2
		B = 3

		def __init__(self, layer = "UI", type = 0):
			Window.__init__(self, layer)
			self.Type = int(type)
			CornerFileNames = [ "d:/ymir work/ui/pattern/ThinBoard_Corner_"+dir+".tga" for dir in ["LeftTop","LeftBottom","RightTop","RightBottom"] ]
			LineFileNames = [ "d:/ymir work/ui/pattern/ThinBoard_Line_"+dir+".tga" for dir in ["Left","Right","Top","Bottom"] ]

			if type == 0: # Normal Shop
				CornerFileNames = [ "d:/ymir work/ui/pattern/ThinBoard_Corner_"+dir+".tga" for dir in ["LeftTop","LeftBottom","RightTop","RightBottom"] ]
				LineFileNames = [ "d:/ymir work/ui/pattern/ThinBoard_Line_"+dir+".tga" for dir in ["Left","Right","Top","Bottom"] ]
			elif type == 1:
				CornerFileNames = [ "D:/ymir work/ui/pattern/myshop/fire/p_fire_"+dir+".tga" for dir in ["left_top","left_bottom","right_top","right_bottom"] ]
				LineFileNames = [ "D:/ymir work/ui/pattern/myshop/fire/p_fire_"+dir+".tga" for dir in ["left","right","top","bottom"] ]
			elif type == 2:
				CornerFileNames = [ "D:/ymir work/ui/pattern/myshop/ice/p_ice_"+dir+".tga" for dir in ["left_top","left_bottom","right_top","right_bottom"] ]
				LineFileNames = [ "D:/ymir work/ui/pattern/myshop/ice/p_ice_"+dir+".tga" for dir in ["left","right","top","bottom"] ]
			elif type == 3:
				CornerFileNames = [ "D:/ymir work/ui/pattern/myshop/paper/p_paper_"+dir+".tga" for dir in ["left_top","left_bottom","right_top","right_bottom"] ]
				LineFileNames = [ "D:/ymir work/ui/pattern/myshop/paper/p_paper_"+dir+".tga" for dir in ["left","right","top","bottom"] ]
			elif type == 4:
				CornerFileNames = [ "D:/ymir work/ui/pattern/myshop/ribon/p_ribon_"+dir+".tga" for dir in ["left_top","left_bottom","right_top","right_bottom"] ]
				LineFileNames = [ "D:/ymir work/ui/pattern/myshop/ribon/p_ribon_"+dir+".tga" for dir in ["left","right","top","bottom"] ]
			elif type == 5:
				CornerFileNames = [ "D:/ymir work/ui/pattern/myshop/wing/p_wing_"+dir+".tga" for dir in ["left_top","left_bottom","right_top","right_bottom"] ]
				LineFileNames = [ "D:/ymir work/ui/pattern/myshop/wing/p_wing_"+dir+".tga" for dir in ["left","right","top","bottom"] ]

			self.Corners = []
			for fileName in CornerFileNames:
				Corner = ExpandedImageBox()
				Corner.AddFlag("attach")
				Corner.AddFlag("not_pick")
				Corner.LoadImage(fileName)
				Corner.SetParent(self)
				Corner.SetPosition(0, 0)
				Corner.Show()
				self.Corners.append(Corner)

			self.Lines = []
			for fileName in LineFileNames:
				Line = ExpandedImageBox()
				Line.AddFlag("attach")
				Line.AddFlag("not_pick")
				Line.LoadImage(fileName)
				Line.SetParent(self)
				Line.SetPosition(0, 0)
				Line.Show()
				self.Lines.append(Line)

			Base = Bar()
			Base.SetParent(self)
			Base.AddFlag("attach")
			Base.AddFlag("not_pick")
			Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
			Base.SetColor(self.BOARD_COLOR)
			Base.Show()
			self.Base = Base

			if self.Type==0:
				self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
				self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)
			else:
				self.Lines[self.T].SetPosition(self.CORNER_1_WIDTH, 0)

		def __del__(self):
			Window.__del__(self)

		def SetSize(self, width, height=20):
			if self.Type == 0:
				width = max(self.CORNER_WIDTH*2, width-50)
				height = max(self.CORNER_HEIGHT*2, height)
				Window.SetSize(self, width, height)

				self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
				self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
				self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
				self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
				self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

				verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
				horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
				self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
				self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
				self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
				self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
				self.Base.SetSize(width - self.CORNER_WIDTH*2, height - self.CORNER_HEIGHT*2)
			else:
				width = max(100, width)
				Window.SetSize(self, width, self.CORNER_1_HEIGHT)
				horizontalShowingPercentage = float((width - self.CORNER_1_WIDTH*2-4) - 32) / 16
				self.Corners[self.LB].SetPosition(0, self.CORNER_1_HEIGHT-16)
				self.Corners[self.RT].SetPosition(width - self.CORNER_1_WIDTH-20, 0)
				self.Corners[self.RB].SetPosition(width - self.CORNER_1_WIDTH-20,self.CORNER_1_HEIGHT-16)
				self.Lines[self.B].SetPosition(self.CORNER_1_HEIGHT, self.CORNER_1_HEIGHT-16)
				self.Lines[self.L].Hide()
				self.Lines[self.R].Hide()

				self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
				self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)

		def ShowInternal(self):
			self.Base.Show()
			for wnd in self.Lines:
				wnd.Show()
			for wnd in self.Corners:
				wnd.Show()

		def HideInternal(self):
			self.Base.Hide()
			for wnd in self.Lines:
				wnd.Hide()
			for wnd in self.Corners:
				wnd.Hide()

	class ScrollBar3(Window):
		SCROLLBAR_WIDTH = 13
		SCROLLBAR_MIDDLE_HEIGHT = 1
		SCROLLBAR_BUTTON_WIDTH = 17
		SCROLLBAR_BUTTON_HEIGHT = 17
		SCROLL_BTN_XDIST = 2
		SCROLL_BTN_YDIST = 2

		class MiddleBar(DragButton):
			def __init__(self):
				DragButton.__init__(self)
				self.AddFlag("movable")
				self.SetWindowName("scrollbar_middlebar")

			def MakeImage(self):
				top = ExpandedImageBox()
				top.SetParent(self)
				top.LoadImage("d:/ymir work/ui/game/windows/scrollbar3/scrollbar_middle_top.tga")
				top.AddFlag("not_pick")
				top.Show()
				topScale = ExpandedImageBox()
				topScale.SetParent(self)
				topScale.SetPosition(0, top.GetHeight())
				topScale.LoadImage("d:/ymir work/ui/game/windows/scrollbar3/scrollbar_middle_topscale.tga")
				topScale.AddFlag("not_pick")
				topScale.Show()

				bottom = ExpandedImageBox()
				bottom.SetParent(self)
				bottom.LoadImage("d:/ymir work/ui/game/windows/scrollbar3/scrollbar_middle_bottom.tga")
				bottom.AddFlag("not_pick")
				bottom.Show()
				bottomScale = ExpandedImageBox()
				bottomScale.SetParent(self)
				bottomScale.LoadImage("d:/ymir work/ui/game/windows/scrollbar3/scrollbar_middle_bottomscale.tga")
				bottomScale.AddFlag("not_pick")
				bottomScale.Show()

				middle = ExpandedImageBox()
				middle.SetParent(self)
				middle.LoadImage("d:/ymir work/ui/game/windows/scrollbar3/scrollbar_middle_middle.tga")
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
				DragButton.SetSize(self, 10, height)

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
			Window.__init__(self)

			self.pageSize = 1
			self.curPos = 0.0
			self.eventScroll = None
			self.eventArgs = None
			self.lockFlag = FALSE

			self.CreateScrollBar()
			self.SetScrollBarSize(0)

			self.scrollStep = 0.03
			self.SetWindowName("NONAME_ScrollBar")

		def __del__(self):
			Window.__del__(self)

		def CreateScrollBar(self):
			topImage = ExpandedImageBox()
			topImage.SetParent(self)
			topImage.AddFlag("not_pick")
			topImage.LoadImage("d:/ymir work/ui/game/windows/scrollbar3/scrollbar_top.tga")
			topImage.Show()
			bottomImage = ExpandedImageBox()
			bottomImage.SetParent(self)
			bottomImage.AddFlag("not_pick")
			bottomImage.LoadImage("d:/ymir work/ui/game/windows/scrollbar3/scrollbar_bottom.tga")
			bottomImage.Show()
			middleImage = ExpandedImageBox()
			middleImage.SetParent(self)
			middleImage.AddFlag("not_pick")
			middleImage.SetPosition(0, topImage.GetHeight())
			middleImage.LoadImage("d:/ymir work/ui/game/windows/scrollbar3/scrollbar_middle.tga")
			middleImage.Show()
			self.topImage = topImage
			self.bottomImage = bottomImage
			self.middleImage = middleImage

			middleBar = self.MiddleBar()
			middleBar.SetParent(self)
			middleBar.SetMoveEvent(__mem_func__(self.OnMove))
			middleBar.Show()
			middleBar.MakeImage()
			middleBar.SetSize(0) # set min height
			self.middleBar = middleBar

		def Destroy(self):
			self.eventScroll = None
			self.eventArgs = None

		def SetScrollEvent(self, event, *args):
			self.eventScroll = event
			self.eventArgs = args

		def SetMiddleBarSize(self, pageScale):
			self.middleBar.SetSize(int(pageScale * float(self.GetHeight() - self.SCROLL_BTN_YDIST*2)))
			realHeight = self.GetHeight() - self.SCROLL_BTN_YDIST*2 - self.middleBar.GetHeight()
			self.pageSize = realHeight

		def SetScrollBarSize(self, height):
			self.SetSize(self.SCROLLBAR_WIDTH, height)

			self.pageSize = height - self.SCROLL_BTN_YDIST*2 - self.middleBar.GetHeight()

			middleImageScale = float((height - self.SCROLL_BTN_YDIST*2) - self.middleImage.GetHeight()) / float(self.middleImage.GetHeight())
			self.middleImage.SetRenderingRect(0, 0, 0, middleImageScale)
			self.bottomImage.SetPosition(0, height - self.bottomImage.GetHeight())

			self.middleBar.SetRestrictMovementArea(self.SCROLL_BTN_XDIST, self.SCROLL_BTN_YDIST, \
				self.middleBar.GetWidth(), height - self.SCROLL_BTN_YDIST * 2)
			self.middleBar.SetPosition(self.SCROLL_BTN_XDIST, self.SCROLL_BTN_YDIST)

		def SetScrollStep(self, step):
			self.scrollStep = step

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

if app.ENABLE_OFFLINESHOP_SEARCH_SYSTEM:
	class ListBox3(Window):
		def __del__(self):
			Window.__del__(self)

		def Destroy(self):
			for item in self.itemList:
				item.Destroy()
			self.itemList = []

			self.scrollBar = None
			self.basePos = 0
			self.scrollLen = 0
			self.scrollLenExtra = 0
			self.isHorizontal = 0

		def __init__(self, isHorizontal = FALSE):
			Window.__init__(self)
			self.itemList = []
			self.Destroy()
			self.isHorizontal = isHorizontal

		def RemoveAllItems(self):
			for item in self.itemList:
				item.Destroy()
			self.itemList = []

			if self.scrollBar:
				self.scrollBar.SetPos(0)

			self.RefreshAll()

		def SetExtraScrollLen(self, extraLen):
			self.scrollLenExtra = extraLen

		def GetItems(self):
			return self.itemList

		def AppendItem(self, newItem):
			self.itemList.append(newItem)
			self.RefreshAll()

		def SetScrollBar(self, scrollBar):
			scrollBar.SetScrollEvent(__mem_func__(self.__OnScroll))
			self.scrollBar = scrollBar

		def OnRunMouseWheel(self, nLen):
			if self.scrollBar:
				if self.scrollBar.IsShow():
					if nLen > 0:
						self.scrollBar.OnUp()
					else:
						self.scrollBar.OnDown()
					return TRUE
			return FALSE

		def __OnScroll(self):
			self.SetBasePos(int(self.scrollBar.GetPos()*self.scrollLen))

		def RefreshAll(self):
			windowHeight = self.GetHeight()
			scrollBar = self.scrollBar
			screenSize = 0
			for child in self.itemList:
				if child.exPos[1]+child.GetHeight() > screenSize:
					screenSize = child.exPos[1]+child.GetHeight()

			if screenSize > windowHeight:
				scrollLen = screenSize-windowHeight
				if scrollLen != 0:
					scrollLen += self.scrollLenExtra
				self.scrollLen = scrollLen
				scrollBar.SetMiddleBarSize(float(windowHeight-5)/float(screenSize))
			else:
				scrollBar.SetMiddleBarSize(1.0)

		def Render(self, basePos):
			for item in self.itemList:
				(ex, ey) = item.exPos
				if self.isHorizontal:
					item.SetPosition(ex-(basePos), ey)
				else:
					item.SetPosition(ex, ey-(basePos))
				item.OnRender()

		def SetBasePos(self, basePos):
			if self.basePos == basePos:
				return

			self.Render(basePos)
			self.basePos = basePos

	class ComboBoxImage(Window):
		class ListBoxWithBoard(ListBox):
			def __init__(self, layer):
				ListBox.__init__(self, layer)

			def OnRender(self):
				xRender, yRender = self.GetGlobalPosition()
				yRender -= self.TEMPORARY_PLACE
				widthRender = self.width
				heightRender = self.height + self.TEMPORARY_PLACE*2
				grp.SetColor(BACKGROUND_COLOR)
				grp.RenderBar(xRender, yRender, widthRender, heightRender)
				grp.SetColor(DARK_COLOR)
				grp.RenderLine(xRender, yRender, widthRender, 0)
				grp.RenderLine(xRender, yRender, 0, heightRender)
				ListBox.OnRender(self)

		def __init__(self, parent, name, x ,y):
			Window.__init__(self)
			self.isSelected = FALSE
			self.isOver = FALSE
			self.isListOpened = FALSE
			self.event = lambda *arg: None
			self.enable = TRUE
			self.imagebox = None

			image = ImageBox()
			image.SetParent(parent)
			image.LoadImage(name)
			image.SetPosition(x, y)
			image.Show()
			self.imagebox = image

			self.x = x + 1
			self.y = y + 1
			self.width = self.imagebox.GetWidth() - 3
			self.height = self.imagebox.GetHeight() - 3
			self.SetParent(parent)

			self.textLine = MakeTextLine(self)
			self.textLine.SetText(localeInfo.UI_ITEM)

			self.listBox = self.ListBoxWithBoard("TOP_MOST")
			self.listBox.SetPickAlways()
			self.listBox.SetParent(self)
			self.listBox.SetEvent(__mem_func__(self.OnSelectItem))
			self.listBox.Hide()

			Window.SetPosition(self, self.x, self.y)
			Window.SetSize(self, self.width, self.height)
			self.textLine.UpdateRect()
			self.__ArrangeListBox()

		def __del__(self):
			Window.__del__(self)

		def Destroy(self):
			self.textLine = None
			self.listBox = None
			self.imagebox = None

		def SetPosition(self, x, y):
			Window.SetPosition(self, x, y)
			self.imagebox.SetPosition(x, y)
			self.x = x
			self.y = y
			self.__ArrangeListBox()

		def SetSize(self, width, height):
			Window.SetSize(self, width, height)
			self.width = width
			self.height = height
			self.textLine.UpdateRect()
			self.__ArrangeListBox()

		def __ArrangeListBox(self):
			self.listBox.SetPosition(0, self.height + 5)
			self.listBox.SetWidth(self.width)

		def Enable(self):
			self.enable = TRUE

		def Disable(self):
			self.enable = FALSE
			self.textLine.SetText("")
			self.CloseListBox()

		def SetEvent(self, event):
			self.event = event

		def ClearItem(self):
			self.CloseListBox()
			self.listBox.ClearItem()

		def InsertItem(self, index, name):
			self.listBox.InsertItem(index, name)
			self.listBox.ArrangeItem()

		def SetCurrentItem(self, text):
			self.textLine.SetText(text)

		def SelectItem(self, key):
			self.listBox.SelectItem(key)

		def OnSelectItem(self, index, name):
			self.CloseListBox()
			self.event(index)

		def CloseListBox(self):
			self.isListOpened = FALSE
			self.listBox.Hide()

		def OnMouseLeftButtonDown(self):
			if not self.enable:
				return

			self.isSelected = TRUE

		def OnMouseLeftButtonUp(self):
			if not self.enable:
				return

			self.isSelected = FALSE

			if self.isListOpened:
				self.CloseListBox()
			else:
				if self.listBox.GetItemCount() > 0:
					self.isListOpened = TRUE
					self.listBox.Show()
					self.__ArrangeListBox()

		def OnUpdate(self):
			if not self.enable:
				return

			if self.IsIn():
				self.isOver = TRUE
			else:
				self.isOver = FALSE

		def OnRender(self):
			self.x, self.y = self.GetGlobalPosition()
			xRender = self.x
			yRender = self.y
			widthRender = self.width
			heightRender = self.height
			if self.isOver:
				grp.SetColor(HALF_WHITE_COLOR)
				grp.RenderBar(xRender + 2, yRender + 3, self.width - 3, heightRender - 5)
				if self.isSelected:
					grp.SetColor(WHITE_COLOR)
					grp.RenderBar(xRender + 2, yRender + 3, self.width - 3, heightRender - 5)

if app.ENABLE_MULTI_TEXTLINE:
	class MultiTextLine(Window):
		RETURN_STRING = "[ENTER]"
		LINE_HEIGHT = 12

		def __init__(self):
			Window.__init__(self)
			self.lines = []
			self.alignCenter = FALSE
			self.text = ""

		def __del__(self):
			Window.__init__(self)

		def SetWidth(self, width):
			self.SetSize(width, self.GetHeight())
			self.SetText(self.GetText())

		def NewTextLine(self):
			line = TextLine()
			line.SetParent(self)
			line.SetPosition(0, len(self.lines) * self.LINE_HEIGHT)
			if self.alignCenter == TRUE:
				line.SetWindowHorizontalAlignCenter()
				line.SetHorizontalAlignCenter()
			line.Show()
			self.lines.append(line)

			return self.lines[len(self.lines) - 1]

		def Clear(self):
			self.text = ""
			self.lines = []

		def SetTextHorizontalAlignCenter(self):
			self.alignCenter = TRUE
			self.SetText(self.GetText())

		def SetText(self, text):
			self.Clear()

			self.text = text

			line = self.NewTextLine()
			pos = 0
			newStartPos = 0
			while pos < len(text):
				line.SetText(text[:pos+1])

				newLine = FALSE
				if len(text) >= pos + len(self.RETURN_STRING):
					if text[pos:pos+len(self.RETURN_STRING)] == self.RETURN_STRING:
						newLine = TRUE
						newStartPos = pos+len(self.RETURN_STRING)
				if newLine == FALSE and pos > 0:
					if line.GetTextWidth() > self.GetWidth():
						newLine = TRUE
						newStartPos = pos

				if newLine == TRUE:
					line.SetText(text[:pos])

					line = self.NewTextLine()
					text = text[newStartPos:]
					if text[:1] == " ":
						text = text[1:]
					pos = 0
				else:
					pos += 1

			self.SetSize(self.GetWidth(), len(self.lines) * self.LINE_HEIGHT)

		def GetText(self):
			return self.text

if app.ENABLE_RENEWAL_BONUS_BOARD:
	class ScrollBar4(Window):
		SCROLLBAR_WIDTH = 7
		SCROLL_BTN_XDIST = 0
		SCROLL_BTN_YDIST = 0

		class MiddleBar(DragButton):
			def __init__(self):
				DragButton.__init__(self)

				self.AddFlag("movable")
				self.SetWindowName("scrollbar_middlebar")

			def MakeImage(self):
				top = ExpandedImageBox()
				top.SetParent(self)
				top.LoadImage("d:/ymir work/ui/game/windows/scrollbar4/scrollbar_top.tga")
				top.AddFlag("not_pick")
				top.Show()

				topScale = ExpandedImageBox()
				topScale.SetParent(self)
				topScale.SetPosition(0, top.GetHeight())
				topScale.LoadImage("d:/ymir work/ui/game/windows/scrollbar4/scrollbar_scale.tga")
				topScale.AddFlag("not_pick")
				topScale.Show()

				bottom = ExpandedImageBox()
				bottom.SetParent(self)
				bottom.LoadImage("d:/ymir work/ui/game/windows/scrollbar4/scrollbar_bottom.tga")
				bottom.AddFlag("not_pick")
				bottom.Show()

				bottomScale = ExpandedImageBox()
				bottomScale.SetParent(self)
				bottomScale.LoadImage("d:/ymir work/ui/game/windows/scrollbar4/scrollbar_scale.tga")
				bottomScale.AddFlag("not_pick")
				bottomScale.Show()

				middle = ExpandedImageBox()
				middle.SetParent(self)
				middle.LoadImage("d:/ymir work/ui/game/windows/scrollbar4/scrollbar_mid.tga")
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
				DragButton.SetSize(self, 10, height)
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
			Window.__init__(self)

			self.pageSize = 1
			self.curPos = 0.0

			self.eventScroll = None
			self.eventArgs = None
			self.lockFlag = FALSE

			self.CreateScrollBar()
			self.SetScrollBarSize(0)
			self.scrollStep = 0.4

			self.SetWindowName("NONAME_ScrollBar")

		def __del__(self):
			Window.__del__(self)

		def CreateScrollBar(self):
			topImage = ExpandedImageBox()
			topImage.SetParent(self)
			topImage.AddFlag("not_pick")
			topImage.LoadImage("d:/ymir work/ui/game/windows/scrollbar4/scroll_top.tga")
			topImage.Show()

			bottomImage = ExpandedImageBox()
			bottomImage.SetParent(self)
			bottomImage.AddFlag("not_pick")
			bottomImage.LoadImage("d:/ymir work/ui/game/windows/scrollbar4/scroll_bottom.tga")
			bottomImage.Show()

			middleImage = ExpandedImageBox()
			middleImage.SetParent(self)
			middleImage.AddFlag("not_pick")
			middleImage.SetPosition(0, topImage.GetHeight())
			middleImage.LoadImage("d:/ymir work/ui/game/windows/scrollbar4/scroll_mid.tga")
			middleImage.Show()

			self.topImage = topImage
			self.bottomImage = bottomImage
			self.middleImage = middleImage

			middleBar = self.MiddleBar()
			middleBar.SetParent(self)
			middleBar.SetMoveEvent(__mem_func__(self.OnMove))
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
			self.SetPos(self.curPos - self.scrollStep)

		def OnDown(self):
			self.SetPos(self.curPos + self.scrollStep)

		def GetScrollStep(self):
			return self.scrollStep

		def GetPos(self):
			return self.curPos

		def OnUp(self):
			self.SetPos(self.curPos - self.scrollStep)

		def OnDown(self):
			self.SetPos(self.curPos + self.scrollStep)

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

if app.ENABLE_EMOTICONS_SYSTEM:
	class Ballon(Window):

		BASE_PATH = "d:/ymir work/ui/game/emoji/emoticons/gui/ballon"

		WIDTH = {
			'LEFT' : 6,
			'FILL_L' : 1,
			'ARROW' : 22,
			'FILL_R' : 1,
			'RIGHT' : 6
		}

		HEIGHT = 36

		ANIMATED = FALSE
		SHOWED = FALSE
		ALPHA = 0.0

		BallonText = None

		def __init__(self, layer = "UI"):
			Window.__init__(self, layer)

			self.__CreateUI()
			self.SetWidth(0)
			self.Hide()

		def __del__(self):
			Window.__del__(self)

		def __CreateUI(self):
			self.ANIMATED = FALSE
			self.SHOWED = FALSE
			self.ALPHA = 0.0

			self.__dictImages = {
				'LEFT' : ImageBox(),
				'FILL_L' : ExpandedImageBox(),
				'ARROW' : ImageBox(),
				'FILL_R' : ExpandedImageBox(),
				'RIGHT' : ImageBox()
			}

			for image in self.__dictImages.itervalues():
				image.SetParent(self)
				image.Show()

			self.__dictImages['LEFT'].LoadImage("%s/left.tga" % Ballon.BASE_PATH)
			self.__dictImages['FILL_L'].LoadImage("%s/fill.tga" % Ballon.BASE_PATH)
			self.__dictImages['ARROW'].LoadImage("%s/arrow.tga" % Ballon.BASE_PATH)
			self.__dictImages['FILL_R'].LoadImage("%s/fill.tga" % Ballon.BASE_PATH)
			self.__dictImages['RIGHT'].LoadImage("%s/right.tga" % Ballon.BASE_PATH)

			self.__dictImages['LEFT'].SetPosition(0, 0)
			self.__dictImages['FILL_L'].SetPosition(Ballon.WIDTH['LEFT'], 0)

		def SetWidth(self, width):
			if int(width) % 2 == 1:
				width += 1

			width = max(Ballon.WIDTH['LEFT'] + Ballon.WIDTH['FILL_L'] + Ballon.WIDTH['ARROW'] + Ballon.WIDTH['RIGHT'] + Ballon.WIDTH['FILL_R'], width)
			self.WIDTH = width
			self.SetSize(width, Ballon.HEIGHT)

			self.__dictImages['FILL_L'].SetScale(float(width - (Ballon.WIDTH['LEFT'] + Ballon.WIDTH['RIGHT'] + Ballon.WIDTH['ARROW'])) / float(2), 1.0)
			self.__dictImages['FILL_R'].SetPosition((float(width)/2.0 + (Ballon.WIDTH['ARROW'])/2), 0)
			self.__dictImages['FILL_R'].SetScale(float(width - (Ballon.WIDTH['LEFT'] + Ballon.WIDTH['RIGHT'] + Ballon.WIDTH['ARROW'])) / float(2), 1.0)
			self.__dictImages['ARROW'].SetPosition((float(width)/2.0 - float(Ballon.WIDTH['ARROW'])/2), 0)
			self.__dictImages['RIGHT'].SetPosition((width - Ballon.WIDTH['RIGHT']), 0)

		def SetText(self, text):
			if not self.BallonText:
				textLine = TextLine()
				textLine.SetParent(self)
				textLine.Show()
				self.BallonText = textLine
			self.BallonText.SetFontColor(1.0, 1.0, 1.0)
			self.BallonText.SetText(text)
			(width, heigh) = self.BallonText.GetTextSize()
			self.SetWidth(width + 20)
			self.BallonText.SetVerticalAlignCenter()
			self.BallonText.SetHorizontalAlignCenter()
			self.BallonText.SetPosition(self.GetWidth()/2, self.GetHeight()/2-6)

		def Hide(self):
			if self.ANIMATED:
				self.SHOWED = FALSE
			else:
				Window.Hide(self)

		def Show(self):
			Window.Show(self)
			if self.ANIMATED:
				self.SHOWED = TRUE

		def OnUpdate(self):
			if not self.ANIMATED:
				return

			if self.SHOWED and self.ALPHA < 1.0:
				self.ALPHA += 0.1
				if self.BallonText:
					self.BallonText.Hide()
				for image in self.__dictImages.itervalues():
					image.SetAlpha(self.ALPHA)
			elif self.SHOWED and self.ALPHA >= 1.0:
				if self.BallonText:
					self.BallonText.Show()
			elif self.ALPHA > 0.0 and not self.SHOWED:
				if self.BallonText:
					self.BallonText.Hide()
				self.ALPHA -= 0.2
				for image in self.__dictImages.itervalues():
					image.SetAlpha(self.ALPHA)
			elif self.ALPHA <= 0.0 and not self.SHOWED:
				self.Hide()

	class ScrollBar5(Window):

		PACH = "d:/ymir work/ui/game/emoji/emoticons/gui/scrollbar/"
		SCROLLBAR_WIDTH = 17
		SCROLLBAR_MIDDLE_HEIGHT = 9
		SCROLLBAR_BUTTON_WIDTH = 17
		SCROLLBAR_BUTTON_HEIGHT = 17
		MIDDLE_BAR_POS = 5
		MIDDLE_BAR_UPPER_PLACE = 3
		MIDDLE_BAR_DOWNER_PLACE = 4
		TEMP_SPACE = MIDDLE_BAR_UPPER_PLACE + MIDDLE_BAR_DOWNER_PLACE
		INTERFACE_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)

		class MiddleBar(DragButton):
			PACH = "d:/ymir work/ui/game/emoji/emoticons/gui/scrollbar/"

			def __init__(self):
				DragButton.__init__(self)
				self.AddFlag("movable")

			def MakeImage(self):
				self.top = ImageBox()
				self.top.SetParent(self)
				self.top.LoadImage(self.PACH + "btn_board_middle_top_01_normal" + ".tga")
				self.top.SetPosition(1, 0)
				self.top.AddFlag("not_pick")
				self.top.Show()

				self.bottom = ImageBox()
				self.bottom.SetParent(self)
				self.bottom.LoadImage(self.PACH + "btn_board_middle_bottom_01_normal" + ".tga")
				self.bottom.AddFlag("not_pick")
				self.bottom.Show()

				self.middle = ExpandedImageBox()
				self.middle.SetParent(self)
				self.middle.LoadImage(self.PACH + "btn_board_middle_center_01_normal" + ".tga")
				self.middle.SetPosition(1, 4)
				self.middle.AddFlag("not_pick")
				self.middle.Show()

				self.marcador = ImageBox()
				self.marcador.SetParent(self)
				self.marcador.LoadImage(self.PACH + "btn_board_middle_grip_01_normal" + ".tga")
				self.marcador.AddFlag("not_pick")
				self.marcador.Show()

			def SetSize(self, height):
				height = max(12, height)
				DragButton.SetSize(self, 10, height)
				self.bottom.SetPosition(1, height-4)
				self.marcador.SetPosition(1, (height/2)-3)

				height -= 4*3
				self.height = height
				self.middle.SetRenderingRect(0, 0, 0, float(height)/4.0)

			def OnMouseOverOut(self):
				self.top.LoadImage(self.PACH + "btn_board_middle_top_01_normal" + ".tga")
				self.bottom.LoadImage(self.PACH + "btn_board_middle_bottom_01_normal" + ".tga")
				self.middle.LoadImage(self.PACH + "btn_board_middle_center_01_normal" + ".tga")
				self.middle.SetRenderingRect(0, 0, 0, float(self.height)/4.0)
				self.marcador.LoadImage(self.PACH + "btn_board_middle_grip_01_normal" + ".tga")

			def OnMouseOverIn(self):
				self.top.LoadImage(self.PACH + "btn_board_middle_top_02_hover" + ".tga")
				self.bottom.LoadImage(self.PACH + "btn_board_middle_bottom_02_hover" + ".tga")
				self.middle.LoadImage(self.PACH + "btn_board_middle_center_02_hover" + ".tga")
				self.middle.SetRenderingRect(0, 0, 0, float(self.height)/4.0)
				self.marcador.LoadImage(self.PACH + "btn_board_middle_grip_02_hover" + ".tga")

		def __init__(self):
			Window.__init__(self)

			self.pageSize = 1
			self.curPos = 0.0
			self.eventScroll = lambda *arg: None
			self.lockFlag = FALSE
			self.scrollStep = 0.20

			self.CreateScrollBar()

		def __del__(self):
			Window.__del__(self)

		def CreateScrollBar(self):
			barSlot = Bar()
			barSlot.SetColor(self.INTERFACE_COLOR)
			barSlot.SetParent(self)
			barSlot.AddFlag("not_pick")
			barSlot.Show()

			middleBar = self.MiddleBar()
			middleBar.SetParent(self)
			middleBar.SetMoveEvent(__mem_func__(self.OnMove))
			middleBar.Show()
			middleBar.MakeImage()
			middleBar.SetSize(12)

			upButton = Button()
			upButton.SetParent(self)
			upButton.SetEvent(__mem_func__(self.OnUp))
			upButton.SetUpVisual(self.PACH + "btn_up_01_normal" + ".tga")
			upButton.SetOverVisual(self.PACH + "btn_up_02_hover" + ".tga")
			upButton.SetDownVisual(self.PACH + "btn_up_03_active" + ".tga")
			upButton.Show()

			downButton = Button()
			downButton.SetParent(self)
			downButton.SetEvent(__mem_func__(self.OnDown))
			downButton.SetUpVisual(self.PACH + "btn_down_01_normal" + ".tga")
			downButton.SetOverVisual(self.PACH + "btn_down_02_hover" + ".tga")
			downButton.SetDownVisual(self.PACH + "btn_down_03_active" + ".tga")
			downButton.Show()

			self.upButton = upButton
			self.downButton = downButton
			self.middleBar = middleBar
			self.barSlot = barSlot

			self.SCROLLBAR_WIDTH = self.upButton.GetWidth()
			self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
			self.SCROLLBAR_BUTTON_WIDTH = self.upButton.GetWidth()
			self.SCROLLBAR_BUTTON_HEIGHT = self.upButton.GetHeight()

		def Destroy(self):
			self.Hide()
			self.middleBar = None
			self.upButton = None
			self.downButton = None
			self.eventScroll = lambda *arg: None

		def SetScrollEvent(self, event):
			self.eventScroll = event

		def SetMiddleBarSize(self, pageScale):
			realHeight = self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2 - 6
			self.SCROLLBAR_MIDDLE_HEIGHT = int(pageScale * float(realHeight))
			self.middleBar.SetSize(self.SCROLLBAR_MIDDLE_HEIGHT)
			self.pageSize = (self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)
			newPos = float(self.pageSize) * self.curPos
			self.middleBar.SetPosition(self.MIDDLE_BAR_POS, int(newPos) + self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE)

		def SetScrollBarSize(self, height):
			self.pageSize = (height - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)
			self.SetSize(self.SCROLLBAR_WIDTH, height)
			self.upButton.SetPosition(0, 0)
			self.downButton.SetPosition(0, height - self.SCROLLBAR_BUTTON_HEIGHT)
			self.middleBar.SetRestrictMovementArea(self.MIDDLE_BAR_POS, self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE, self.MIDDLE_BAR_POS+2, height - self.SCROLLBAR_BUTTON_HEIGHT*2 - self.TEMP_SPACE)
			self.middleBar.SetPosition(self.MIDDLE_BAR_POS, 0)
			self.UpdateBarSlot()

		def UpdateBarSlot(self):
			self.barSlot.SetPosition(2, self.SCROLLBAR_BUTTON_HEIGHT)
			self.barSlot.SetSize(self.GetWidth()-4, self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2)

		def GetPos(self):
			return self.curPos

		def SetPos(self, pos):
			pos = max(0.0, pos)
			pos = min(1.0, pos)
			newPos = float(self.pageSize) * pos
			self.middleBar.SetPosition(self.MIDDLE_BAR_POS, int(newPos) + self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE)
			self.OnMove()

		def SetScrollStep(self, step):
			self.scrollStep = step

		def GetScrollStep(self):
			return self.scrollStep

		def OnUp(self):
			self.SetPos(self.curPos-self.scrollStep)

		def OnDown(self):
			self.SetPos(self.curPos+self.scrollStep)

		def OnMove(self):
			if self.lockFlag:
				return

			if 0 == self.pageSize:
				return

			(xLocal, yLocal) = self.middleBar.GetLocalPosition()
			if self.curPos  ==  float(yLocal - self.SCROLLBAR_BUTTON_HEIGHT - self.MIDDLE_BAR_UPPER_PLACE) / float(self.pageSize):
				return

			self.curPos = float(yLocal - self.SCROLLBAR_BUTTON_HEIGHT - self.MIDDLE_BAR_UPPER_PLACE) / float(self.pageSize)

			self.eventScroll()

		def OnMouseLeftButtonDown(self):
			(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
			pickedPos = yMouseLocalPosition - self.SCROLLBAR_BUTTON_HEIGHT - self.SCROLLBAR_MIDDLE_HEIGHT/2
			newPos = float(pickedPos) / float(self.pageSize)
			self.SetPos(newPos)

		def LockScroll(self):
			self.lockFlag = TRUE

		def UnlockScroll(self):
			self.lockFlag = FALSE

if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
	class SpecialTitleBar1(Window):

		BLOCK_WIDTH = 32
		BLOCK_HEIGHT = 17

		def __init__(self):
			Window.__init__(self)
			self.AddFlag("attach")
			self.eventDict = {}

		def __del__(self):
			Window.__del__(self)

		def Create(self, width):

			width = max(96, width)

			imgLeft = ImageBox()
			imgLeft.SetParent(self)
			imgLeft.AddFlag("not_pick")
			imgLeft.LoadImage("d:/ymir work/ui/game/teleport/special_titlebar_thinboard/left.png")
			imgLeft.Show()

			imgCenter = ExpandedImageBox()
			imgCenter.SetParent(self)
			imgCenter.AddFlag("not_pick")
			imgCenter.LoadImage("d:/ymir work/ui/game/teleport/special_titlebar_thinboard/center.png")
			imgCenter.Show()

			imgRight = ImageBox()
			imgRight.SetParent(self)
			imgRight.AddFlag("not_pick")
			imgRight.LoadImage("d:/ymir work/ui/game/teleport/special_titlebar_thinboard/right.png")
			imgRight.Show()

			self.imgLeft = imgLeft
			self.imgCenter = imgCenter
			self.imgRight = imgRight
			self.SetWidth(width)

		def SetWidth(self, width):
			self.imgCenter.SetRenderingRect(0.0, 0.0, float((width - self.BLOCK_WIDTH*2) - self.BLOCK_WIDTH) / self.BLOCK_WIDTH, 0.0)
			self.imgCenter.SetPosition(self.BLOCK_WIDTH, 0)
			self.imgRight.SetPosition(width - self.BLOCK_WIDTH, 0)
			self.SetSize(width, self.BLOCK_HEIGHT)

		def OnMouseOverIn(self):
			try:
				self.eventDict["MOUSE_OVER_IN"]()
			except KeyError:
				pass

		def OnMouseOverOut(self):
			try:
				self.eventDict["MOUSE_OVER_OUT"]()
			except KeyError:
				pass

		def SAFE_SetStringEvent(self, event, func):
			self.eventDict[event]=__mem_func__(func)

	class ThinBoardSpecial1(Window):
		CORNER_WIDTH = 16
		CORNER_HEIGHT = 16
		LINE_WIDTH = 16
		LINE_HEIGHT = 16
		BOARD_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.51)

		LT = 0
		LB = 1
		RT = 2
		RB = 3
		L = 0
		R = 1
		T = 2
		B = 3

		def __init__(self, layer = "UI"):
			Window.__init__(self, layer)
			CornerFileNames = [ "d:/ymir work/ui/game/teleport/special_thinboard/corner_"+dir+".png" for dir in ["left_top","left_bottom","right_top","right_bottom"] ]
			LineFileNames = [ "d:/ymir work/ui/game/teleport/special_thinboard/"+dir+".png" for dir in ["left","right","top","bottom"] ]

			self.Corners = []
			for fileName in CornerFileNames:
				Corner = ExpandedImageBox()
				Corner.AddFlag("attach")
				Corner.AddFlag("not_pick")
				Corner.LoadImage(fileName)
				Corner.SetParent(self)
				Corner.SetPosition(0, 0)
				Corner.Show()
				self.Corners.append(Corner)

			self.Lines = []
			for fileName in LineFileNames:
				Line = ExpandedImageBox()
				Line.AddFlag("attach")
				Line.AddFlag("not_pick")
				Line.LoadImage(fileName)
				Line.SetParent(self)
				Line.SetPosition(0, 0)
				Line.Show()
				self.Lines.append(Line)

			Base = ExpandedImageBox()
			Base.SetParent(self)
			Base.AddFlag("attach")
			Base.AddFlag("not_pick")
			Base.LoadImage("d:/ymir work/ui/game/teleport/special_thinboard/center.png")
			Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
			Base.Show()
			self.Base = Base

			self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
			self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

		def __del__(self):
			Window.__del__(self)

		def SetSize(self, width, height):

			width = max(self.CORNER_WIDTH*2, width)
			height = max(self.CORNER_HEIGHT*2, height)
			Window.SetSize(self, width, height)

			self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
			self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
			self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
			self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
			self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

			verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
			horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
			self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
			self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
			self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
			self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
			if self.Base:
				self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)

		def ShowInternal(self):
			self.Base.Show()
			for wnd in self.Lines:
				wnd.Show()
			for wnd in self.Corners:
				wnd.Show()

		def HideInternal(self):
			self.Base.Hide()
			for wnd in self.Lines:
				wnd.Hide()
			for wnd in self.Corners:
				wnd.Hide()

if app.ENABLE_DUNGEON_TRACKING_SYSTEM:
	class ListBox4(Window):
		def __del__(self):
			Window.__del__(self)

		def Destroy(self):
			for item in self.itemList:
				item.Destroy()
			self.itemList = []

			self.scrollBar = None

			self.basePos = 0
			self.scrollLen = 0
			self.scrollLenExtra = 0
			self.isHorizontal = 0

		def __init__(self, isHorizontal = FALSE):
			Window.__init__(self)
			self.itemList = []
			self.Destroy()
			self.isHorizontal = isHorizontal

		def RemoveAllItems(self):
			for item in self.itemList:
				item.Destroy()
			self.itemList = []

			if self.scrollBar:
				self.scrollBar.SetPos(0)
			self.RefreshAll()

		def SetExtraScrollLen(self, extraLen):
			self.scrollLenExtra = extraLen

		def GetItems(self):
			return self.itemList

		def AppendItem(self, newItem):
			self.itemList.append(newItem)
			self.RefreshAll()

		def SetScrollBar(self, scrollBar):
			scrollBar.SetScrollEvent(__mem_func__(self.__OnScroll))
			self.scrollBar = scrollBar

		def OnMouseWheel(self, nLen):
			if self.scrollBar:
				if self.scrollBar.IsShow():
					if nLen > 0:
						self.scrollBar.OnUp()
					else:
						self.scrollBar.OnDown()
					return TRUE
			return FALSE

		def __OnScroll(self):
			self.SetBasePos(int(self.scrollBar.GetPos()*self.scrollLen))

		def RefreshAll(self):
			windowHeight = self.GetHeight()
			scrollBar = self.scrollBar
			screenSize = 0

			for child in self.itemList:
				if child.exPos[1]+child.GetHeight() > screenSize:
					screenSize = child.exPos[1]+child.GetHeight()

			if screenSize > windowHeight:
				scrollLen = screenSize-windowHeight
				if scrollLen != 0:
					scrollLen += self.scrollLenExtra
				self.scrollLen = scrollLen
				scrollBar.SetMiddleBarSize(float(windowHeight-5)/float(screenSize))
			else:
				scrollBar.SetMiddleBarSize(1.0)

		def Render(self,basePos):
			for item in self.itemList:
				(ex,ey) = item.exPos
				if self.isHorizontal:
					item.SetPosition(ex-(basePos), ey)
				else:
					item.SetPosition(ex, ey-(basePos))
				item.OnRender()

		def SetBasePos(self, basePos):
			if self.basePos == basePos:
				return

			self.Render(basePos)
			self.basePos = basePos

def MakeSlotBar(parent, x, y, width, height):
	slotBar = SlotBar()
	slotBar.SetParent(parent)
	slotBar.SetSize(width, height)
	slotBar.SetPosition(x, y)
	slotBar.Show()
	return slotBar

def MakeImageBox(parent, name, x, y):
	image = ImageBox()
	image.SetParent(parent)
	image.LoadImage(name)
	image.SetPosition(x, y)
	image.Show()
	return image

def MakeTextLine(parent):
	textLine = TextLine()
	textLine.SetParent(parent)
	textLine.SetWindowHorizontalAlignCenter()
	textLine.SetWindowVerticalAlignCenter()
	textLine.SetHorizontalAlignCenter()
	textLine.SetVerticalAlignCenter()
	textLine.Show()
	return textLine

def MakeThinBoardCircle(parent, x, y, width, heigh, text, bnsId = 0):
	thin = ThinBoardCircle()
	thin.SetParent(parent)
	thin.SetSize(width, heigh)
	thin.SetPosition(x, y)
	thin.SetText(text)
	thin.SetBonusId(bnsId)
	thin.Show()
	return thin

def MakeButton(parent, x, y, tooltipText, path, up, over, down):
	button = Button()
	button.SetParent(parent)
	button.SetPosition(x, y)
	button.SetUpVisual(path + up)
	button.SetOverVisual(path + over)
	button.SetDownVisual(path + down)
	button.SetToolTipText(tooltipText)
	button.Show()
	return button

def MakeRadioButton(parent, x, y, path, up, over, down):
	button = RadioButton()
	button.SetParent(parent)
	button.SetPosition(x, y)
	button.SetUpVisual(path + up)
	button.SetOverVisual(path + over)
	button.SetDownVisual(path + down)
	button.Show()
	return button

def MakeListBox(parent, x, y, width, height, rowCount, event):
	listBox = ListBox2()
	listBox.SetParent(parent)
	listBox.SetPosition(x, y)
	listBox.SetSize(width, height)
	listBox.SetRowCount(rowCount)
	listBox.SetEvent(event)
	listBox.Show()
	return listBox

if app.ENABLE_RENEWAL_SWITCHBOT:
	def MakeScrollBar2(parent, x, y, height):
		scrollbar = ScrollBar2()
		scrollbar.SetParent(parent)
		scrollbar.SetPosition(x, y)
		scrollbar.SetScrollBarSize(height)
		scrollbar.Show()
		return scrollbar

if app.ENABLE_RENEWAL_BONUS_BOARD:
	def MakeButtonNew(parent, x, y, text, path, up, over, down):
		button = Button()
		button.SetParent(parent)
		button.SetPosition(x, y)
		button.SetUpVisual(path + up)
		button.SetOverVisual(path + over)
		button.SetDownVisual(path + down)
		button.SetText(text)
		button.UpdateRect()
		button.Show()
		return button

	def MakeHorizontalBar(parent, x, y, width, text):
		horizontalBar = HorizontalBar()
		horizontalBar.Create(width)
		horizontalBar.SetParent(parent)
		horizontalBar.SetPosition(x, y)
		horizontalBar.SetWidth(width)
		horizontalBar.SetText(text)
		horizontalBar.Show()
		return horizontalBar

if app.ENABLE_RENEWAL_BATTLE_PASS or app.ENABLE_HUNTING_SYSTEM:
	def AddTextLine(parent, x, y, text, outline = 0):
		textLine = TextLine()
		textLine.SetParent(parent)
		textLine.SetPosition(x, y)

		if outline != 0:
			textLine.SetOutline()

		textLine.SetText(text)
		textLine.Show()
		return textLine

	def MakeNewTextLine(parent, horizontalAlign = TRUE, verticalAlgin = TRUE, x = 0, y = 0):
		textLine = TextLine()
		textLine.SetParent(parent)

		if horizontalAlign == TRUE:
			textLine.SetWindowHorizontalAlignCenter()

		if verticalAlgin == TRUE:
			textLine.SetWindowVerticalAlignCenter()

		textLine.SetHorizontalAlignCenter()
		textLine.SetVerticalAlignCenter()

		if x != 0 and y != 0:
			textLine.SetPosition(x, y)

		textLine.Show()
		return textLine

	def MakeExpandedImageBox(parent, name, x, y, flag = ""):
		image = ExpandedImageBox()
		image.SetParent(parent)
		image.LoadImage(name)
		image.SetPosition(x, y)

		if flag != "":
			image.AddFlag(flag)

		image.Show()
		return image

if app.ENABLE_AUTO_SELL_SYSTEM:
	class ListBoxAutoSell(Window):
	
		class Item(Window):
			def __init__(self):
				Window.__init__(self)
				self.textLabel = None
	
			def __del__(self):
				Window.__del__(self)
	
			def SetParent(self, parent):
				Window.SetParent(self, parent)
				self.parent=proxy(parent)
	
			def SetText(self, text):
				if not self.textLabel:
					self.textLabel = TextLine()
					self.textLabel.SetParent(self)
					self.textLabel.SetPosition(5, 5)
					self.textLabel.Show()
				self.textLabel.SetText(text)
	
			def GetText(self):
				if self.textLabel:
					return self.textLabel.GetText()
				return ""
	
			def OnMouseLeftButtonDown(self):
				self.parent.SelectItem(self)
	
			def OnRender(self):
				if self.parent.GetSelectedItem()==self:
					self.OnSelectedRender()
	
			def OnSelectedRender(self):
				x, y = self.GetGlobalPosition()
				grp.SetColor(grp.GenerateColor(0.0, 0.0, 0.7, 0.7))
				grp.RenderBar(x, y, self.GetWidth(), self.GetHeight())
	
		def __init__(self):
			Window.__init__(self)
	
			self.viewItemCount=10
			self.basePos=0
			self.itemHeight=16
			self.itemStep=20
			self.selItem=0
			self.itemList=[]
			self.onSelectItemEvent = lambda *arg: None
	
	
			if hasattr(localeInfo, 'IsARABIC') and localeInfo.IsARABIC():
				self.itemWidth=130
			else:
				self.itemWidth=100
	
			self.scrollBar=None
			self.__UpdateSize()
	
		def __del__(self):
			Window.__del__(self)
	
		def __UpdateSize(self):
			height=self.itemStep*self.__GetViewItemCount()
	
			self.SetSize(self.itemWidth, height)
	
		def IsEmpty(self):
			if len(self.itemList)==0:
				return 1
			return 0
	
		def SetItemStep(self, itemStep):
			self.itemStep=itemStep
			self.__UpdateSize()
	
		def SetItemSize(self, itemWidth, itemHeight):
			self.itemWidth=itemWidth
			self.itemHeight=itemHeight
			self.__UpdateSize()
	
		def SetViewItemCount(self, viewItemCount):
			self.viewItemCount=viewItemCount
	
		def SetSelectEvent(self, event):
			self.onSelectItemEvent = event
	
		def SetBasePos(self, basePos):
			for oldItem in self.itemList[self.basePos:self.basePos+self.viewItemCount]:
				oldItem.Hide()
	
			self.basePos=basePos
	
			pos=basePos
			for newItem in self.itemList[self.basePos:self.basePos+self.viewItemCount]:
				(x, y)=self.GetItemViewCoord(pos, newItem.GetWidth())
				newItem.SetPosition(x, y)
				newItem.Show()
				pos+=1
	
		def GetItemIndex(self, argItem):
			return self.itemList.index(argItem)
	
		def GetItem(self, index):
			if index < 0 or index >= len(self.itemList):
				return None
			return self.itemList[index]
	
		def GetSelectedItem(self):
			return self.selItem
	
		def SelectIndex(self, index):
	
			if index >= len(self.itemList) or index < 0:
				self.selItem = None
				return
	
			try:
				self.selItem=self.itemList[index]
			except:
				pass
	
		def SelectItem(self, selItem):
			self.selItem=selItem
			self.onSelectItemEvent(selItem)
	
		def RemoveAllItems(self):
			self.selItem=None
			self.itemList=[]
	
			if self.scrollBar:
				self.scrollBar.SetPos(0)
	
		def RemoveItem(self, delItem):
			if delItem == self.selItem:
				self.selItem = None
		
			if isinstance(self.itemList, list):
				if delItem in self.itemList:
					self.itemList.remove(delItem)
					self.SetBasePos(self.basePos)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, "Item listede bulunamadı!")
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, "itemList bir liste değil!")
	
		def AppendItem(self, newItem):
			newItem.SetParent(self)
			newItem.SetSize(self.itemWidth, self.itemHeight)
	
			pos=len(self.itemList)
			if self.__IsInViewRange(pos):
				(x, y)=self.GetItemViewCoord(pos, newItem.GetWidth())
				newItem.SetPosition(x, y)
				newItem.Show()
			else:
				newItem.Hide()
	
			self.itemList.append(newItem)
	
		def SetScrollBar(self, scrollBar):
			scrollBar.SetScrollEvent(__mem_func__(self.__OnScroll))
			self.scrollBar=scrollBar
	
		def __OnScroll(self):
			self.SetBasePos(int(self.scrollBar.GetPos()*self.__GetScrollLen()))
	
		def __GetScrollLen(self):
			scrollLen=self.GetItemCount()-self.__GetViewItemCount()
			if scrollLen<0:
				return 0
	
			return scrollLen
	
		def __GetViewItemCount(self):
			return self.viewItemCount
	
		def GetItemCount(self):
			return len(self.itemList)
	
		def GetItemViewCoord(self, pos, itemWidth):
			if hasattr(localeInfo, 'IsARABIC') and localeInfo.IsARABIC():
				return (self.GetWidth()-itemWidth-10, (pos-self.basePos)*self.itemStep)
			else:
				return (0, (pos-self.basePos)*self.itemStep)
	
		def GetSelectedIndex(self):
			if self.selItem is None:
				return -1
			try:
				return self.itemList.index(self.selItem)
			except ValueError:
				return -1
	
	
		def __IsInViewRange(self, pos):
			if pos<self.basePos:
				return 0
			if pos>=self.basePos+self.viewItemCount:
				return 0
			return 1

def MakeBoardWithTitleBar(parent, flag, title, closeEvent, width, height):
	board = BoardWithTitleBar()
	board.SetParent(parent)
	board.SetSize(width, height)
	board.AddFlag(flag)
	board.SetTitleName(title)
	board.SetCloseEvent(closeEvent)
	board.Show()
	return board

def MakeTextLineNew(parent, x, y, text):
	textLine = TextLine()
	textLine.SetParent(parent)
	textLine.SetPosition(x, y)
	textLine.SetText(text)
	textLine.Show()
	return textLine

def RenderRoundBox(x, y, width, height, color):
	grp.SetColor(color)
	grp.RenderLine(x+2, y, width-3, 0)
	grp.RenderLine(x+2, y+height, width-3, 0)
	grp.RenderLine(x, y+2, 0, height-4)
	grp.RenderLine(x+width, y+1, 0, height-3)
	grp.RenderLine(x, y+2, 2, -2)
	grp.RenderLine(x, y+height-2, 2, 2)
	grp.RenderLine(x+width-2, y, 2, 2)
	grp.RenderLine(x+width-2, y+height, 2, -2)

def GenerateColor(r, g, b):
	r = float(r) / 255.0
	g = float(g) / 255.0
	b = float(b) / 255.0
	return grp.GenerateColor(r, g, b, 1.0)

def EnablePaste(flag):
	ime.EnablePaste(flag)

def GetHyperlink():
	return wndMgr.GetHyperlink()

RegisterToolTipWindow("TEXT", TextLine)
