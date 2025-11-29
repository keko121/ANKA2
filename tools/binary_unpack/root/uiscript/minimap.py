if __USE_DYNAMIC_MODULE__:
	import pyapi

app = __import__(pyapi.GetModuleName("app"))

ROOT = "d:/ymir work/ui/minimap/"

window = {
	"name" : "MiniMap",

	"x" : SCREEN_WIDTH - 136,
	"y" : 0,

	"width" : 136,
	"height" : 137,

	"children" :
	[
		## OpenWindow
		{
			"name" : "OpenWindow",
			"type" : "window",

			"x" : 0,
			"y" : 0,

			"width" : 136,
			"height" : 137,

			"children" :
			[
				{
					"name" : "OpenWindowBGI",
					"type" : "image",
					"x" : 0,
					"y" : 0,
					"image" : ROOT + "minimap.sub",
				},
				## MiniMapWindow
				{
					"name" : "MiniMapWindow",
					"type" : "window",

					"x" : 4,
					"y" : 5,

					"width" : 128,
					"height" : 128,
				},
				## ScaleUpButton
				{
					"name" : "ScaleUpButton",
					"type" : "button",

					"x" : 101,
					"y" : 116,

					"default_image" : ROOT + "minimap_scaleup_default.sub",
					"over_image" : ROOT + "minimap_scaleup_over.sub",
					"down_image" : ROOT + "minimap_scaleup_down.sub",
				},
				## ScaleDownButton
				{
					"name" : "ScaleDownButton",
					"type" : "button",

					"x" : 115,
					"y" : 103,

					"default_image" : ROOT + "minimap_scaledown_default.sub",
					"over_image" : ROOT + "minimap_scaledown_over.sub",
					"down_image" : ROOT + "minimap_scaledown_down.sub",
				},
				## MiniMapHideButton
				{
					"name" : "MiniMapHideButton",
					"type" : "button",

					"x" : 111,
					"y" : 6,

					"default_image" : ROOT + "minimap_close_default.sub",
					"over_image" : ROOT + "minimap_close_over.sub",
					"down_image" : ROOT + "minimap_close_down.sub",
				},
				## AtlasShowButton
				{
					"name" : "AtlasShowButton",
					"type" : "button",

					"x" : 12,
					"y" : 12,

					"default_image" : ROOT + "atlas_open_default.sub",
					"over_image" : ROOT + "atlas_open_over.sub",
					"down_image" : ROOT + "atlas_open_down.sub",
				},
				## ServerInfo
				{
					"name" : "ServerInfo",
					"type" : "text",
					
					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70,
					"y" : 150,

					"text" : "",
				},
				## PositionInfo
				{
					"name" : "PositionInfo",
					"type" : "text",
					
					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70,
					"y" : 170,

					"text" : "",
				},
				## ObserverCount
				{
					"name" : "ObserverCount",
					"type" : "text",

					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70,
					"y" : 190,
	
					"text" : "",
				},

				## FPSInfo
				{
					"name" : "FPSInfo",
					"type" : "text",
					
					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : -25,
					"y" : 15,

					"text" : "",
				},
			],
		},
		{
			"name" : "CloseWindow",
			"type" : "window",

			"x" : 0,
			"y" : 0,

			"width" : 132,
			"height" : 48,

			"children" :
			[
				## ShowButton
				{
					"name" : "MiniMapShowButton",
					"type" : "button",

					"x" : 100,
					"y" : 4,

					"default_image" : ROOT + "minimap_open_default.sub",
					"over_image" : ROOT + "minimap_open_default.sub",
					"down_image" : ROOT + "minimap_open_default.sub",
				},
			],
		},
	],
}

window["x"] = window["x"] - 15
window["width"] = window["width"] + 15
window["children"][0]["width"] = window["children"][0]["width"] + 15
window["children"][1]["width"] = window["children"][1]["width"] + 15

for idx in range(len(window["children"][0]["children"])):
	window["children"][0]["children"][idx]["x"] = window["children"][0]["children"][idx]["x"] + 15

window["children"][1]["children"][0]["x"] = window["children"][1]["children"][0]["x"] + 15
window["children"][1]["children"][0]["y"] = 2

window["children"][0]["children"][5]["x"] = 0
window["children"][0]["children"][5]["y"] = 57
if app.ENABLE_RENEWAL_BATTLE_PASS:
	window["children"][0]["children"] = window["children"][0]["children"] + [
					{
						"name" : "PortableBattlePassButton",
						"type" : "button",

						"x" : 5,
						"y" : 85,

						"default_image" : ROOT + "battlepass_open_default.tga",
						"over_image" : ROOT + "battlepass_open_over.tga",
						"down_image" : ROOT + "battlepass_open_down.tga",
					},]

if app.ENABLE_BIOLOG_SYSTEM:
	window["children"][0]["children"] = window["children"][0]["children"] + [
					{
						"name" : "PortableBiologButton",
						"type" : "button",

						"x" : 21,
						"y" : 107,

						"default_image" : ROOT + "biolog_open_default.tga",
						"over_image" : ROOT + "biolog_open_over.tga",
						"down_image" : ROOT + "biolog_open_down.tga",
					},]

if app.ENABLE_DUNGEON_TRACKING_SYSTEM:
	window["children"][0]["children"] = window["children"][0]["children"] + [
					## PortableDungeonInfoButton
					{
						"name" : "PortableDungeonInfoButton",
						"type" : "button",

						"x" : 45,
						"y" : 123,

						"default_image" : ROOT + "dungeon_open_default.tga",
						"over_image" : ROOT + "dungeon_open_over.tga",
						"down_image" : ROOT + "dungeon_open_down.tga",
					},]

if app.ENABLE_OFFLINESHOP_SEARCH_SYSTEM:
	window["children"][0]["children"] = window["children"][0]["children"] + [
					{
						"name" : "PortableSearchButton",
						"type" : "button",

						"x" : 80,
						"y" : 125,

						"default_image" : ROOT + "search_open_default.tga",
						"over_image" : ROOT + "search_open_over.tga",
						"down_image" : ROOT + "search_open_down.tga",
					},]

if app.ENABLE_EVENT_MANAGER:
	window["children"][0]["children"] = window["children"][0]["children"] + [
				## InGameEventButton
				{
					"name" : "InGameEventButton",
					"type" : "button",

					"x" : 2,
					"y" : 28,

					"default_image" : "d:/ymir work/ui/minimap/E_open_default.tga",
					"over_image" : "d:/ymir work/ui/minimap/E_open_over.tga",
					"down_image" : "d:/ymir work/ui/minimap/E_open_down.tga",
				},]
