import localeInfo

BOARD_WIDTH = 334
BOARD_HEIGHT = 325

PAGE_LEFT_X_DIST = 10
PAGE_RIGHT_X_DIST = 10
PAGE_X_DIST = PAGE_LEFT_X_DIST + PAGE_RIGHT_X_DIST

PAGE_TOP_DIST = 33
PAGE_BOT_DIST = 10

ROOT_PATH = "d:/ymir work/ui/game/biolog_manager/"

window = {
	"name" : "BiologManagerWindow", "style" : ("movable", "float",),
	"x" : 0, "y" : 0,
	"width" : BOARD_WIDTH, "height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "BiologBoard", "type" : "board_with_titlebar",
			"style" : ("attach", "ltr"),
			"x" : 0, "y" : 0,
			"width" : BOARD_WIDTH, "height" : BOARD_HEIGHT,
			"title" : localeInfo.BIOLOG_MANAGER_TITLE,

			"children" :
			(
				{
					"name" : "Background", "type" : "image",
					"x" : PAGE_LEFT_X_DIST, "y" : PAGE_TOP_DIST,
					"image" : ROOT_PATH + "background.tga",
					"width" : BOARD_WIDTH - PAGE_X_DIST, "height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST),

					"children" :
					(
						{
							"name" : "BiologQuest", "type" : "image",
							"x" : 0, "y" : PAGE_BOT_DIST / 1,
							"horizontal_align" : "center",
							"image" : ROOT_PATH + "quest_blue_bg.tga",

							"children" :
							(
								{
									"name" : "BiologImage", "type" : "image",
									"x" : 3, "y" : 0, "vertical_align" : "center",
									"image" : ROOT_PATH + "biolog_image.tga",
								},
								{
									"name" : "BiologRequiredLevel", "type" : "text",
									"x" : 0, "y" : 0, "all_align" : TRUE,
									"text" : "Mission Biolog: Lv 30",
								},
							),
						},
						{
							"name" : "BiologItemInfoSeparator", "type" : "image",
							"x" : 0, "y" : PAGE_BOT_DIST / 2 + 66,
							"horizontal_align" : "center",
							"image" : ROOT_PATH + "separator.tga",

							"children" :
							(
								{
									"name" : "BiologItemInfo", "type" : "text",
									"x" : 0, "y" : 5,
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									"text" : "Orc Tooth+ (1/5)",
								},
							),
						},
						{
							"name" : "BiologRequiredItemSlot", "type" : "image",
							"x" : 45, "y" : PAGE_BOT_DIST / 2 + 95,
							"image" : ROOT_PATH + "slot.dds",
							"children" :
							(
								{
									"name" : "BiologRequiredItem", "type" : "slot",
									"x" : 3, "y" : PAGE_BOT_DIST - 15 / 2,
									"width" : 32, "height" : 32,
									"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32},),
								},
							),
						},
						{
							"name" : "AdditionalCheckbox_0", "type" : "checkbox_biolog",
							"x" : 97, "y" : -17,
							"vertical_align" : "center",
						},
						{
							"name" : "AdditionalItemSlot_0", "type" : "image",
							"x" : 113, "y" : PAGE_BOT_DIST / 2 + 95,
							"image" : ROOT_PATH + "slot.dds",

							"children" :
							(
								{
									"name" : "AdditionalItem_0", "type" : "slot",
									"x" : 5, "y" : 2,
									"width" : 32, "height" : 32,
									"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32},),
								},
							),
						},
						{
							"name" : "AdditionalCheckbox_1", "type" : "checkbox_biolog",
							"x" : 168, "y" : -17, "vertical_align" : "center",
						},
						{
							"name" : "AdditionalItemSlot_1", "type" : "image",
							"x" : 183, "y" : PAGE_BOT_DIST / 2 + 95,
							"image" : ROOT_PATH + "slot.dds",

							"children" :
							(
								{
									"name" : "AdditionalItem_1", "type" : "slot",
									"x" : 5, "y" : 2,
									"width" : 32, "height" : 32,
									"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32},),
								},
							),
						},
						{
							"name" : "SubmitButton", "type" : "button",
							"x" : 100, "y" : PAGE_BOT_DIST / 2 + 105,
							"horizontal_align" : "center",
							"default_image" : ROOT_PATH + "deliver_norm.tga",
							"over_image" : ROOT_PATH + "deliver_hover.tga",
							"down_image" : ROOT_PATH + "deliver_down.tga",
						},
						{
							"name" : "BiologTimeInfo", "type" : "image",
							"x" : 9, "y" : PAGE_BOT_DIST + 63 + PAGE_BOT_DIST / 2 + 65,
							"image" : ROOT_PATH + "info_bg.tga",

							"children" :
							(
								{
									"name" : "BiologCooldownInfo", "type" : "text",
									"x" : -20, "y" : -1, "all_align" : TRUE,
									"text" : "", "fontname" : "Verdana:12", "outline" : 1,
								},
								{
									"name" : "CheckBoxReminder", "type" : "checkbox_biolog",
									"x" : 215, "y" : 1,
									"vertical_align" : "center",
								},
								{
									"name" : "CooldownImage", "type" : "image",
									"x" : 235, "y" : 1, "vertical_align" : "center",
									"image" : ROOT_PATH + "clock.png",
								},
							),
						},
						{
							"name" : "BiologRewardSeparator", "type" : "image",
							"x" : 0, "y" : PAGE_BOT_DIST + 63 + PAGE_BOT_DIST / 2 + 101,
							"horizontal_align" : "center",
							"image" : ROOT_PATH + "separator.tga",

							"children" :
							(
								{
									"name" : "BiologRewardTitle", "type" : "text",
									"x" : 0, "y" : 5, "horizontal_align" : "center",
									"text_horizontal_align" : "center",
									"text" : localeInfo.BIOLOG_MANAGER_REWARD,
								},
							),
						},
						{
							"name" : "BiologRewardBackground", "type" : "image",
							"x" : 6, "y" : PAGE_BOT_DIST + 63 + PAGE_BOT_DIST / 2 + 84 + 44,
							"image" : ROOT_PATH + "rewards_bg.tga",

							"children" :
							(
								{
									"name" : "BiologRewardItem",
									"x" : 0, "y" : 0,
									"width" : 100, "height" : 45,

									"children" :
									(
										{
											"name" : "BiologRewardItemSlot", "type" : "image",
											"x" : 20, "y" : 13,
											"image" : ROOT_PATH + "slot.dds",

											"children" :
											(
												{
													"name" : "BiologRewardItem", "type" : "slot",
													"x" : (6) / 2, "y" : (6) / 2,
													"width" : 32, "height" : 32,
													"horizontal_align" : "center",
													"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32},),
												},
											),
										},
										{
											"name" : "RewardsStorage", "type" : "listboxex",
											"x" : 80, "y" : 6, "width" : 199, "height" : 45,
											"itemsize_x" : 199, "itemsize_y" : 15,
											"itemstep" : 20, "viewcount" : 3,
										},
									),
								},
							),
						},
					),
				},
			),
		},
	),
}