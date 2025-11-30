import uiScriptLocale
import grp
import localeInfo

window = {
	"name" : "RefineDialog",
	"style" : ("movable", "float",),

	"x" : SCREEN_WIDTH - 550,
	"y" : 70 * 800 / SCREEN_HEIGHT,

	"width" : 0,
	"height" : 0,

	"children" :
	(
		{
			"name" : "Board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 0,
			"height" : 0,

			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 8,

					"width" : 0,
					"color" : "red",

					"children" :
					(
						{
							"name" : "TitleName",
							"type" : "text",

							"text" : uiScriptLocale.REFINE_TTILE,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",

							"x" : 0,
							"y" : 3,
						},
					),
				},
				{
					"name" : "ContentDesignBoard",
					"type" : "thinboard",

					"x" : 10,
					"y" : 35,

					"width" : 220,
					"height" : 150,

					"children" :
					(
						{
							"name": "ContentDesign",
							"type":"horizontalbar",

							"x": 0,
							"y": 0,

							"width": 220,

							"children" :
							(
								{
									"name": "curItem",
									"type": "text",

									"x": 5,
									"y": 1,

									"text": localeInfo.REFINE_UPGRADE,
								},
								{
									"name" : "AttachNextItem",
									"type" : "image",

									"x" : 0,
									"y" : 65,

									"horizontal_align" : "center",
									"vertical_align" : "center",

									"image" : "d:/ymir work/ui/game/windows/attach_metin_arrow.sub",
								},
							),
						},
					),
				},
				{
					"name" : "DesignCostBoard",
					"type" : "thinboard",

					"x": 10,
					"y": 190,

					"width" : 220,
					"height" : 65,

					"children" :
					(
						{
							"name": "DesignCost",
							"type":"horizontalbar",

							"x": 0,
							"y": 0,

							"width": 220,
						},
					),
				},
				{
					"name" : "DesignUpgradeBoard",
					"type" : "thinboard",

					"x": 235,
					"y": 35,

					"width" : 240,
					"height" : 150,

					"children" :
					(
						{
							"name": "DesignUpgrade",
							"type":"horizontalbar",

							"x": 0,
							"y": 0,

							"width": 240,

							"children" :
							(
								{
									"name": "textLine",
									"type": "text",

									"x": 5,
									"y": 1,

									"text": localeInfo.REFINE_NEED_ITEMS,
								},
							),
						},
					),
				},
				{
					"name" : "Slot",
					"type" : "slot",
					"x" : 0,
					"y" : 185,
					"width" : 200,
					"height" : 100,
					"slot" : (
						{
							"index": 0,
							"x": 20,
							"y": 12,
							"width": 32,
							"height": 32
						},
						{
							"index": 1,
							"x": 20 + 80,
							"y": 12,
							"width": 32,
							"height": 32
						},
						{
							"index": 2,
							"x": 20 + 80 + 80,
							"y": 12,
							"width": 32,
							"height": 32
						},
					),
				},
				{
					"name" : "DesignCostBoard",
					"type" : "thinboard",

					"x": 235,
					"y": 190,

					"width" : 240,
					"height" : 65,

					"children" :
					(
						{
							"name": "DesignCost",
							"type":"horizontalbar",

							"x": 0,
							"y": 0,

							"width": 240,

							"children" :
							(
								{
									"name": "textLine",
									"type": "text",

									"x": 5,
									"y": 1,

									"text": localeInfo.REFINE_COST_UPGRADE,
								},
							),
						},
						{
							"name": "SuccessPercentage",
							"type": "text",

							"x": 100,
							"y": 22,

							"text": "",
						},
						{
							"name" : "SlotCost",
							"type" : "image",

							"x" : 90,
							"y" : 40,

							"image": "d:/ymir work/ui/public/llgold_slot.sub",

							"children" :
							(
								{
									"name":"Money_Icon",
									"type": "image",

									"x": -18,
									"y": 2,

									"image": "d:/ymir work/ui/game/windows/money_icon.sub",
								},
								{
									"name" : "Cost",
									"type" : "text",

									"x" : 3,
									"y" : 2,

									"horizontal_align" : "right",
									"text_horizontal_align" : "right",

									"text" : "",
								},
							),
						},
					),
				},
				{
					"name" : "AcceptButton",
					"type" : "button",

					"x" : 45,
					"y" : 228,

					"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub",
					"over_image" : "d:/ymir work/ui/public/acceptbutton01.sub",
					"down_image" : "d:/ymir work/ui/public/acceptbutton02.sub",
					"disable_image" : "d:/ymir work/ui/public/acceptbutton02.sub",
				},
				{
					"name" : "CancelButton",
					"type" : "button",

					"x" : 130,
					"y" : 228,

					"default_image" : "d:/ymir work/ui/public/cancelbutton00.sub",
					"over_image" : "d:/ymir work/ui/public/cancelbutton01.sub",
					"down_image" : "d:/ymir work/ui/public/cancelbutton02.sub",
					"disable_image" : "d:/ymir work/ui/public/cancelbutton02.sub",
				},
			),
		},
	),
}