if __USE_DYNAMIC_MODULE__:
	import pyapi

app = __import__(pyapi.GetModuleName("app"))

import localeInfo
import uiScriptLocale

app.ServerName = None

SRVS = {
	1 : {
		"name" : "Anka2",
		"HOST" : "192.168.1.110",
		"AUTH" : 30001,
		"CH1" : 30101,
		"CH2" : 30201,
		"CH3" : 30301,
		"CH4" : 30401,
	},
	2 : {
		"name" : "Test",
		"HOST" : "192.168.1.110",
		"AUTH" : 30001,
		"CH1" : 30101,
		"CH2" : 30201,
		"CH3" : 30301,
		"CH4" : 30401,
	}
}

if app.ENABLE_RENEWAL_SERVER_LIST:
	STATE_NONE = localeInfo.CHANNEL_STATUS_OFFLINE
	STATE_DICT = {
		0 : localeInfo.CHANNEL_STATUS_OFFLINE,
		1 : localeInfo.CHANNEL_STATUS_VACANT,
		2 : localeInfo.CHANNEL_STATUS_RECOMMENDED,
		3 : localeInfo.CHANNEL_STATUS_BUSY,
		4 : localeInfo.CHANNEL_STATUS_FULL,
	}

	STATE_DICT_NAME = {
		localeInfo.CHANNEL_STATUS_OFFLINE : localeInfo.CHANNEL_STATUS_OFFLINE,
		localeInfo.CHANNEL_STATUS_VACANT : localeInfo.CHANNEL_STATUS_VACANT,
		localeInfo.CHANNEL_STATUS_RECOMMENDED : localeInfo.CHANNEL_STATUS_RECOMMENDED,
		localeInfo.CHANNEL_STATUS_BUSY : localeInfo.CHANNEL_STATUS_BUSY,
		localeInfo.CHANNEL_STATUS_FULL : localeInfo.CHANNEL_STATUS_FULL,
	}

	STATE_DICT_IMAGES = {
		localeInfo.CHANNEL_STATUS_OFFLINE : "offline.png",
		localeInfo.CHANNEL_STATUS_VACANT : "online.png",
		localeInfo.CHANNEL_STATUS_RECOMMENDED : "online.png",
		localeInfo.CHANNEL_STATUS_BUSY : "online.png",
		localeInfo.CHANNEL_STATUS_FULL : "online.png",
	}

	STATE_REVERSE_DICT = {}
	STATE_COLOR_DICT = { "..." : 0xffdadada}
	STATE_COLOR_LIST = [ 0xffffffff, 0xffdadada, 0xff00ff00, 0xffffc000, 0xffff0000 ]

	idx = 0
	for key, value in STATE_DICT.items():
		STATE_REVERSE_DICT[value] = key
		STATE_COLOR_DICT[value] = STATE_COLOR_LIST[idx % len(STATE_COLOR_LIST)]
		idx += 1

	SERVER_STATE_DICT = {
		"NONE" : 0,
		"NEW" : 1,
		"SPECIAL" : 2,
		"CLOSE" : 3
	}
else:
	STATE_NONE = "OFF"
	STATE_DICT = {
		0 : "OFF",
		1 : "NORM",
		2 : "BUSY",
		3 : "FULL"
	}

	STATE_DICT_NAME = {
		"OFF" : localeInfo.CHANNEL_STATUS_OFFLINE,
		"NORM" : localeInfo.CHANNEL_STATUS_RECOMMENDED,
		"BUSY" : localeInfo.CHANNEL_STATUS_BUSY,
		"FULL" : localeInfo.CHANNEL_STATUS_FULL,
	}

	STATE_DICT_IMAGES = {
		localeInfo.CHANNEL_STATUS_OFFLINE : "offline.png",
		localeInfo.CHANNEL_STATUS_RECOMMENDED : "online.png",
		localeInfo.CHANNEL_STATUS_BUSY : "online.png",
		localeInfo.CHANNEL_STATUS_FULL : "online.png",
	}

SERVER1_CHANNEL_DICT = {
	1:{"key":11,"name": uiScriptLocale.LOGIN_CHANNEL_1,"ip":SRVS[1]["HOST"],"tcp_port":SRVS[1]["CH1"],"udp_port":SRVS[1]["CH1"],"state":STATE_NONE,},
	2:{"key":12,"name": uiScriptLocale.LOGIN_CHANNEL_2,"ip":SRVS[1]["HOST"],"tcp_port":SRVS[1]["CH2"],"udp_port":SRVS[1]["CH2"],"state":STATE_NONE,},
	3:{"key":13,"name": uiScriptLocale.LOGIN_CHANNEL_3,"ip":SRVS[1]["HOST"],"tcp_port":SRVS[1]["CH3"],"udp_port":SRVS[1]["CH3"],"state":STATE_NONE,},
	4:{"key":14,"name": uiScriptLocale.LOGIN_CHANNEL_4,"ip":SRVS[1]["HOST"],"tcp_port":SRVS[1]["CH4"],"udp_port":SRVS[1]["CH4"],"state":STATE_NONE,},
}

SERVER2_CHANNEL_DICT = {
	1:{"key":21,"name": uiScriptLocale.LOGIN_CHANNEL_1,"ip":SRVS[2]["HOST"],"tcp_port":SRVS[2]["CH1"],"udp_port":SRVS[2]["CH1"],"state":STATE_NONE,},
	2:{"key":22,"name": uiScriptLocale.LOGIN_CHANNEL_2,"ip":SRVS[2]["HOST"],"tcp_port":SRVS[2]["CH2"],"udp_port":SRVS[2]["CH2"],"state":STATE_NONE,},
	3:{"key":23,"name": uiScriptLocale.LOGIN_CHANNEL_3,"ip":SRVS[2]["HOST"],"tcp_port":SRVS[2]["CH3"],"udp_port":SRVS[2]["CH3"],"state":STATE_NONE,},
	4:{"key":24,"name": uiScriptLocale.LOGIN_CHANNEL_4,"ip":SRVS[2]["HOST"],"tcp_port":SRVS[2]["CH4"],"udp_port":SRVS[2]["CH4"],"state":STATE_NONE,},
}

REGION_NAME_DICT = {
	0 : SRVS[1]["name"],
	1 : SRVS[2]["name"],
}

REGION_AUTH_SERVER_DICT = {
	0 : {
		1 : { "ip":SRVS[1]["HOST"], "port":SRVS[1]["AUTH"], },
		2 : { "ip":SRVS[2]["HOST"], "port":SRVS[2]["AUTH"], },
	}
}

REGION_DICT = {
	0 : {
		1 : { "name" : SRVS[1]["name"], "channel" : SERVER1_CHANNEL_DICT, "state" : "NEW", },
		2 : { "name" : SRVS[2]["name"], "channel" : SERVER2_CHANNEL_DICT, "state" : "SPECIAL", },
	},
}

MARKADDR_DICT = {
	10 : { "ip" : SRVS[1]["HOST"], "tcp_port" : SRVS[1]["CH1"], "mark" : "10.tga", "symbol_path" : "10", },
	20 : { "ip" : SRVS[2]["HOST"], "tcp_port" : SRVS[2]["CH1"], "mark" : "10.tga", "symbol_path" : "10", },
}
