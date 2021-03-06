# Rhye's and Fall of Civilization - Dynamic resources

from CvPythonExtensions import *
import CvUtil
import PyHelpers  
#import Popup
import Consts as con
import RFCUtils # edead

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
utils = RFCUtils.RFCUtils()
localText = CyTranslator()

### Constants ###


# initialise bonuses variables

iHorse = con.iHorse
iBanana = con.iBanana
iCorn = con.iCorn
iCow = con.iCow
iPig = con.iPig
iSheep = con.iSheep
iWheat = con.iWheat
iSugar = con.iSugar
iWine = con.iWine
iCotton = con.iCotton
iDye = con.iDye
iRice = con.iRice
iClam = con.iClam
iFish = con.iFish
iCoffee = con.iCoffee
iTea = con.iTea
iTobacco = con.iTobacco
iSpices = con.iSpices
iIvory = con.iIvory
iIron = con.iIron
iDeer = con.iDeer

iCottage = con.iCottage
iSilk = con.iSilk
iRoad = 0
#Orka: Silk Road road locations
lSilkRoute = [(85,48), (86,49), (87,48), (88,47), (89,46), (90,47), (90,45), (91,47), (91,45), (92,48), (93,48), (93,46), (94,47), (95,47), (96,47), (97,47), (98,47), (99,46)]
lNewfoundlandCapes = [(34, 52), (34, 53), (34, 54), (35, 52), (36, 52), (35, 55), (35, 56), (35, 57), (36, 51), (36, 58), (36, 59)]

class Resources:

	# Leoreth: bonus removal alerts by edead
	def createResource(self, iX, iY, iBonus, textKey="TXT_KEY_MISC_DISCOVERED_NEW_RESOURCE"):
		"""Creates a bonus resource and alerts the plot owner"""
		
		if gc.getMap().plot(iX,iY).getBonusType(-1) == -1 or iBonus == -1: # only proceed if the bonus isn't already there or if we're removing the bonus
			if iBonus == -1:
				iBonus = gc.getMap().plot(iX,iY).getBonusType(-1) # for alert
				gc.getMap().plot(iX,iY).setBonusType(-1)
			else:
				gc.getMap().plot(iX,iY).setBonusType(iBonus)
				
			iOwner = gc.getMap().plot(iX,iY).getOwner()
			if iOwner >= 0 and textKey != -1: # only show alert to the tile owner
				# Leoreth: changed so different area cities are found if water resource is added (because sea is automatically a different area than land)
				bWater = gc.getMap().plot(iX, iY).isWater()
				city = gc.getMap().findCity(iX, iY, iOwner, TeamTypes.NO_TEAM, not bWater, bWater, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
				if not city.isNone():
					szText = localText.getText(textKey, (gc.getBonusInfo(iBonus).getTextKey(), city.getName()))
					CyInterface().addMessage(iOwner, False, con.iDuration, szText, "AS2D_DISCOVERBONUS", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getBonusInfo(iBonus).getButton(), ColorTypes(con.iWhite), iX, iY, True, True)


	def removeResource(self, iX, iY, textKey="TXT_KEY_MISC_EVENT_RESOURCE_EXHAUSTED"):
		"""Removes a bonus resource and alerts the plot owner"""
		if gc.getMap().plot(iX, iY).getBonusType(-1) == -1: return
		self.createResource(iX, iY, -1, textKey)
       	
	def checkTurn(self, iGameTurn):
		
		# Gujarati horses appear later so Harappa cannot benefit too early
		if iGameTurn == getTurnForYear(-1000):
			self.createResource(88, 37, iHorse)
			
		# Tamils
		if iGameTurn == getTurnForYear(-300)-1 and utils.getPlayerEnabled(con.iTamils):
			self.createResource(90, 28, iFish)

		#Orka: Silk Road
		if (iGameTurn == getTurnForYear(-200)): 
			for i in range( len(lSilkRoute) ):
			    gc.getMap().plot(lSilkRoute[i][0], lSilkRoute[i][1]).setRouteType(iRoad)
		
		#Orka: Silk Road
		if (iGameTurn == getTurnForYear(-100)):
			#CyGame().setPlotExtraYield(91, 45, YieldTypes.YIELD_FOOD, 2) #Khotan    
			#gc.getMap().plot(91, 45).setImprovementType(iCottage) #Khotan			       
			#CyGame().setPlotExtraYield(93, 48, YieldTypes.YIELD_FOOD, 2) #Turfan    
			#gc.getMap().plot(93, 48).setImprovementType(iCottage) #Turfan			    
			#gc.getMap().plot(90, 45).setBonusType(iCotton) #Kashgar
			#gc.getMap().plot(94, 47).setBonusType(iWheat) #Dunhuang
			#gc.getMap().plot(96, 48).setBonusType(iSilk) #Dunhuang
			#CyGame().setPlotExtraYield(97, 47, YieldTypes.YIELD_FOOD, 2) #Wuwei    
			#gc.getMap().plot(97, 47).setImprovementType(iCottage) #Wuwei    
			#CyGame().setPlotExtraYield(85, 38, YieldTypes.YIELD_FOOD, 2) #Lanzhou
			#gc.getMap().plot(99, 46).setImprovementType(iCottage) #Lanzhou
			#CyGame().setPlotExtraYield(95, 47, YieldTypes.YIELD_FOOD, 2) #Dunhuang
			#CyGame().setPlotExtraYield(89, 46, YieldTypes.YIELD_FOOD, 2) #Kashgar

			gc.getMap().plot(88, 47).setPlotType(PlotTypes.PLOT_HILLS, True, True)
			gc.getMap().plot(88, 47).setRouteType(iRoad)
			
			self.createResource(88, 47, iSilk)
			self.createResource(85, 46, iSilk)

		#Leoreth: Hanseong's pig appears later so China isn't that eager to found Sanshan
		if iGameTurn == getTurnForYear(-50):
			self.createResource(108, 47, iPig)

		#Leoreth: change Indus tiles to desert floodplains in 0 AD
		#if (iGameTurn == getTurnForYear(0)):
		#	for tPlot in [(86, 37), (86, 38), (87, 38)]:
		#		x, y = tPlot
		#		gc.getMap().plot(x,y).setTerrainType(2, True, True)
		#		gc.getMap().plot(x,y).setFeatureType(3, 0)
		#	for tPlot in [(85, 38), (85, 37)]:
		#		x, y = tPlot
		#		gc.getMap().plot(x,y).setFeatureType(3, 0)

		#if (iGameTurn == getTurnForYear(450)): #(dye added later to prevent Carthaginian UHV exploit)
		#	self.createResource(53, 51, iDye) # France
		#	self.createResource(53, 55, iDye) # England
		#if utils.getScenario() >= con.i600AD: #late start condition
		#	if (iGameTurn == getTurnForYear(600)):
		#		self.createResource(53, 51, iDye)
		#		self.createResource(53, 55, iDye)

		# Leoreth: remove floodplains in Sudan and ivory in Morocco and Tunisia
		if iGameTurn == getTurnForYear(550):
			gc.getMap().plot(67, 30).setFeatureType(-1, 0)
			gc.getMap().plot(67, 31).setFeatureType(-1, 0)
			
			self.removeResource(51, 36)
			self.removeResource(58, 37)

		# Leoreth: replicate silk route in 600 AD
		#if iGameTurn == getTurnForYear(600) and utils.getScenario() == con.i600AD:
		#	CyGame().setPlotExtraYield(91, 45, YieldTypes.YIELD_FOOD, 2) #Khotan			       
		#	CyGame().setPlotExtraYield(93, 48, YieldTypes.YIELD_FOOD, 2) #Turfan
		#	CyGame().setPlotExtraYield(97, 47, YieldTypes.YIELD_FOOD, 2) #Wuwei
		#	CyGame().setPlotExtraYield(95, 47, YieldTypes.YIELD_FOOD, 2) #Dunhuang
		#	CyGame().setPlotExtraYield(89, 46, YieldTypes.YIELD_FOOD, 2) #Kashgar
			
		# Leoreth: prepare Tibet
		if iGameTurn == getTurnForYear(630)-1 and utils.getPlayerEnabled(con.iTibet):
			self.createResource(95, 43, iWheat)
			self.createResource(97, 44, iHorse)
			
		# Leoreth: obstacles for colonization
		if iGameTurn == getTurnForYear(700):
			gc.getMap().plot(35, 54).setFeatureType(con.iMud, 0)
			for x, y in lNewfoundlandCapes:
				gc.getMap().plot(x, y).setFeatureType(con.iCape, 0)
				
			if utils.getHumanID() == con.iVikings:
				gc.getMap().plot(41, 58).setFeatureType(-1, 0)
		
		# Leoreth: New Guinea can be settled
		if iGameTurn == getTurnForYear(1000):
			gc.getMap().plot(113, 25).setFeatureType(-1, 0)
		
		# Leoreth: for respawned Egypt
		if iGameTurn == getTurnForYear(900):
			self.removeResource(71, 34)
			self.createResource(71, 34, iIron)
		    
		if (iGameTurn == getTurnForYear(1100)):
			#gc.getMap().plot(71, 30).setBonusType(iSugar) #Egypt
			
			self.createResource(72, 24, iSugar) # East Africa
			self.createResource(70, 17, iSugar) # Zimbabwe
			self.createResource(67, 11, iSugar) # South Africa
			
			self.createResource(66, 23, iBanana) # Central Africa
			self.createResource(64, 20, iBanana) # Central Africa
			
			if utils.getPlayerEnabled(con.iCongo):
				self.createResource(61, 22, iCotton) # Congo
				self.createResource(63, 19, iIvory) # Congo
				self.createResource(61, 24, iIvory) # Cameroon
			
			self.createResource(57, 46, iWine) # Savoy
			self.createResource(57, 45, iClam) # Savoy
			
			self.createResource(50, 44, iIron) # Portugal
			
		# Leoreth: route to connect Karakorum to Beijing and help the Mongol attackers
		if iGameTurn == getTurnForYear(con.tBirth[con.iMongolia]):
			for tPlot in [(101, 48), (100, 49), (100, 50), (99, 50)]:
				x, y = tPlot
				gc.getMap().plot(x, y).setRouteType(iRoad)
				
			# silk near Astrakhan
			self.createResource(78, 51, iSilk)

		if (iGameTurn == getTurnForYear(1250)):
			#gc.getMap().plot(57, 52).setBonusType(iWheat) #Amsterdam
			self.createResource(96, 36, iFish) # Calcutta, Dhaka, Pagan

		if iGameTurn == getTurnForYear(1350):
			gc.getMap().plot(102, 35).setFeatureType(-1, 0) #remove rainforest in Vietnam

		if (iGameTurn == getTurnForYear(1500)):
			gc.getMap().plot(35, 54).setFeatureType(-1, 0) # remove Marsh in case it had been placed
			for x, y in lNewfoundlandCapes:
				gc.getMap().plot(x, y).setFeatureType(-1, 0)
				
			# also remove Marsh on Port Moresby
			gc.getMap().plot(116, 24).setFeatureType(-1, 0)
			
			self.createResource(56, 54, iFish) # Amsterdam
			self.createResource(57, 52, iWheat) # Amsterdam
			self.createResource(58, 52, iCow) # Amsterdam
			
		if (iGameTurn == getTurnForYear(1600)):
			self.createResource(29, 52, iCow) # Montreal
			self.createResource(18, 53, iCow) # Alberta
			self.createResource(12, 52, iCow) # British Columbia
			self.createResource(28, 46, iCow) # Washington area
			self.createResource(30, 49, iCow) # New York area
			#self.createResource(25, 49, iCow) # Lakes
			self.createResource(23, 42, iCow) # Jacksonville area
			self.createResource(18, 46, iCow) # Colorado
			self.createResource(20, 45, iCow) # Texas
			self.createResource(37, 14, iCow) # Argentina
			self.createResource(33, 11, iCow) # Argentina
			self.createResource(35, 10, iCow) # Pampas
			
			self.createResource(24, 43, iCotton) # near Florida
			self.createResource(23, 45, iCotton) # Louisiana
			self.createResource(22, 44, iCotton) # Louisiana
			self.createResource(13, 45, iCotton) # California
			
			self.createResource(26, 49, iPig) # Lakes
			
			self.createResource(19, 51, iSheep) # Canadian border
			
			#self.createResource(21, 50, iWheat) # Canadian border
			self.createResource(19, 48, iWheat) # Midwest
			self.createResource(20, 53, iWheat) # Manitoba
			
			self.createResource(22, 33, iBanana) # Guatemala
			self.createResource(27, 31, iBanana) # Colombia
			self.createResource(43, 23, iBanana) # Brazil
			self.createResource(39, 26, iBanana) # Brazil
			
			self.createResource(49, 44, iCorn) # Galicia
			self.createResource(54, 48, iCorn) # France
			self.createResource(67, 47, iCorn) # Romania
			self.createResource(106, 50, iCorn) # Manchuria
			self.createResource(77, 52, iCorn) # Caricyn
			
			self.createResource(92, 35, iSpices) # Deccan
			gc.getMap().plot(92, 35).setFeatureType(con.iRainforest, 0)
			
			# remove floodplains in Transoxania
			for tuple in [(82, 47), (83, 46), (85, 49)]:
				x, y = tuple
				gc.getMap().plot(x, y).setFeatureType(-1, 0)
		       

		if (iGameTurn == getTurnForYear(1700)):
			self.createResource(16, 54, iHorse) # Alberta
			self.createResource(26, 45, iHorse) # Washington area
			self.createResource(21, 48, iHorse) # Midwest
			self.createResource(19, 45, iHorse) # Texas
			self.createResource(40, 25, iHorse) # Brazil
			self.createResource(33, 10, iHorse) # Buenos Aires area
			self.createResource(32, 8, iHorse) # Pampas
			
			self.createResource(27, 36, iSugar) # Caribbean
			self.createResource(39, 25, iSugar) # Brazil
			self.createResource(37, 20, iSugar) # inner Brazil
			self.createResource(29, 37, iSugar) # Hispaniola
			
			self.createResource(104, 52, iCorn) # Manchuria
			self.createResource(89, 36, iCorn) # India
			
			self.createResource(38, 18, iCoffee) # Brazil
			self.createResource(39, 20, iCoffee) # Brazil
			self.createResource(38, 22, iCoffee) # Brazil
			self.createResource(27, 30, iCoffee) # Colombia
			self.createResource(29, 30, iCoffee) # Colombia
			self.createResource(26, 27, iCoffee) # Colombia
			self.createResource(104, 25, iCoffee) # Java
			
			self.createResource(67, 44, iTobacco) # Turkey
			
			self.createResource(90, 35, iTea) # West Bengal
			
			self.createResource(39, 16, iFish) # Brazil
			
			self.createResource(70, 59, iDeer) # St Petersburg
			
		if iGameTurn == getTurnForYear(1800):
			if gc.getDefineINT("PLAYER_REBIRTH_MEXICO") != 0:
				self.createResource(17, 41, iHorse) # Mexico
				self.createResource(16, 42, iIron) # Mexico
				
			if gc.getDefineINT("PLAYER_REBIRTH_COLOMBIA") != 0:
				self.createResource(28, 31, iIron) # Colombia
			
			if utils.getPlayerEnabled(con.iArgentina):
				self.createResource(31, 10, iWine) # Mendoza, Argentina
				self.createResource(31, 6, iSheep) # Pampas, Argentina
				self.createResource(32, 11, iIron) # Argentina
			
			if utils.getPlayerEnabled(con.iBrazil):
				self.createResource(36, 18, iCorn) # Sao Paulo
				self.createResource(42, 18, iFish) # Rio de Janeiro

		if (iGameTurn == getTurnForYear(1850)):
			self.createResource(12, 45, iWine) # California
			self.createResource(31, 10, iWine) # Andes
			self.createResource(113, 12, iWine) # Barossa Valley, Australia
			
			self.createResource(114, 11, iSheep) # Australia
			self.createResource(116, 13, iSheep) # Australia
			self.createResource(121, 6, iSheep) # New Zealand
			
			self.createResource(58, 47, iRice) # Vercelli
			self.createResource(12, 49, iRice) # California
			
			self.createResource(11, 45, iFish) # California
			#self.createResource(10, 45, iFish) # California
			self.createResource(87, 35, iFish) # Bombay
			
			self.createResource(115, 52, iCow) # Hokkaido
			
			self.createResource(1, 38, iSugar) # Hawaii
			self.createResource(5, 36, iBanana) # Hawaii
			
			# flood plains in California
			for tPlot in [(11, 46), (11, 47), (11, 48)]:
				x, y = tPlot
				gc.getMap().plot(x,y).setFeatureType(3, 0)