if __USE_DYNAMIC_MODULE__:
	import pyapi

app = __import__(pyapi.GetModuleName("app"))
chrmgr = __import__(pyapi.GetModuleName("chrmgr"))

JOB_WARRIOR, JOB_ASSASSIN, JOB_SURA, JOB_SHAMAN = range(4)
RACE_WARRIOR_M, RACE_ASSASSIN_W, RACE_SURA_M, RACE_SHAMAN_W, RACE_WARRIOR_W, RACE_ASSASSIN_M, RACE_SURA_W, RACE_SHAMAN_M = range(8)

PASSIVE_GUILD_SKILL_INDEX_LIST = ( 151, )
ACTIVE_GUILD_SKILL_INDEX_LIST = ( 152, 153, 154, 155, 156, 157, )

def __LoadRaceHeight():
	directory = "locale/common/race_height.txt"
	try:
		lines = pack_open(directory, "r").readlines()
	except IOError:
		return

	for line in lines:
		tokens = line[:-1].split("\t")
		if len(tokens) == 0 or not tokens[0]:
			continue

		chrmgr.SetRaceHeight(int(tokens[0]), float(tokens[1]))

loadGameDataDict = {
	"RACE_HEIGHT" : __LoadRaceHeight,
}

def LoadGameData(name):
	global loadGameDataDict

	load = loadGameDataDict.get(name, 0)
	if load:
		loadGameDataDict[name]=0
		try:
			load()
		except:
			print name
			import exception
			exception.Abort("LoadGameData")
			raise
