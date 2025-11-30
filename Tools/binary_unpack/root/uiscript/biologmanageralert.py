import uiScriptLocale

window = {
	"name" : "BiologManagerAlert",

	"x" : (SCREEN_WIDTH-250)/2,
	"y" : 0,

	"style" : ("not_pick",),

	"width" : 240,
	"height" : 93,

	"children" :
	(
		{
			"name" : "Board",
			"style" : ("attach",),
			"type" : "expanded_image",

			"x" : 0,
			"y" : 0,

			"image" : "d:/ymir work/ui/game/biolog_manager/biolog_alert.tga",

			"children" :
			(
				{
					"name" : "Reason_Text",
					"type" : "text",

					"x" : 0,
					"y" : 60,

					"horizontal_align" : "center",
					"text_horizontal_align" : "center",

					"text" : "Biolog",
				},
				{
					"name" : "Start_Time_Text",
					"type" : "text",

					"x" : 0,
					"y" : 70,

					"horizontal_align" : "center",
					"text_horizontal_align" : "center",

					"text" : "",
				},
			),
		},
	),
}