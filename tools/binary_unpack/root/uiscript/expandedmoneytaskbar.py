if __USE_DYNAMIC_MODULE__:
	import pyapi

app = __import__(pyapi.GetModuleName("app"))

import uiScriptLocale

ROOT = "d:/ymir work/ui/game/"

BOARD_ADD_X = 0

if app.ENABLE_COINS_INVENTORY:
	BOARD_ADD_X += 140

BOARD_X = SCREEN_WIDTH - (140 + BOARD_ADD_X)
BOARD_WIDTH = (140 + BOARD_ADD_X)
BOARD_HEIGHT = 40

window = {
	"name" : "ExpandedMoneyTaskbar",
	
	"x" : BOARD_X,
	"y" : SCREEN_HEIGHT - 65,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"style" : ("float",),

	"children" :
	[
		{
			"name" : "ExpanedMoneyTaskBar_Board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"children" :
			[
				{
					"name":"Money_Icon",
					"type":"image",
					
					"x":-5 + BOARD_ADD_X,
					"y":12,

					"image":"d:/ymir work/ui/game/windows/money_icon.sub",
				},
				{
					"name":"Money_Slot",
					"type":"button",

					"x":13 + BOARD_ADD_X,
					"y":10,

					"default_image" : "d:/ymir work/ui/public/llgold_slot.sub",
					"over_image" : "d:/ymir work/ui/public/llgold_slot.sub",
					"down_image" : "d:/ymir work/ui/public/llgold_slot.sub",

					"children" :
					(
						{
							"name" : "Money",
							"type" : "text",

							"x" : 4,
							"y" : 3,

							"horizontal_align" : "right",
							"text_horizontal_align" : "right",

							"text" : "19,999,999,999",
						},
					),
				},
			],
		},
	],
}

if app.ENABLE_COINS_INVENTORY:
	window["children"][0]["children"] = window["children"][0]["children"] + [
					{
						"name":"Coins_Icon",
						"type":"image",

						"x": BOARD_ADD_X - 125,
						"y": 12,

						"image":"d:/ymir work/ui/game/taskbar/coins.tga",
					},
					{
						"name":"Coins_Slot",
						"type":"button",

						"x": BOARD_ADD_X - 108,
						"y":10,

						"default_image" : "d:/ymir work/ui/public/coins_slot.sub",
						"over_image" : "d:/ymir work/ui/public/coins_slot.sub",
						"down_image" : "d:/ymir work/ui/public/coins_slot.sub",

						"children" :
						(
							{
								"name" : "Coins",
								"type" : "text",

								"x" : 4,
								"y" : 3,

								"horizontal_align" : "right",
								"text_horizontal_align" : "right",

								"text" : "9,999",
							},
						),
					},
					]