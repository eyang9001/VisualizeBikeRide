import os
import numpy as np
from xml.etree import ElementTree
from graphics import *
import time

# Reads the xml file and stores the data into the returned arrays: lat (latitude), lng (longitude), hr (heart rate), alt (altitude) for each trackpoint
def readin(fileName):
	full_file = os.path.abspath(os.path.join(fileName))
	dom = ElementTree.parse(full_file)
	loc = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}'

	lat = np.array([], dtype='float32')
	lng = np.array([], dtype='float32')
	hr = np.array([], dtype='int16')
	alt = np.array([], dtype='float32')
	spd = np.array([], dtype='float32')

	#for each trackpoint in the xml file
	for trackpoints in dom.iter(loc + 'Trackpoint'):
		pos = trackpoints.find(loc + 'Position')
		latitude=pos.find(loc + 'LatitudeDegrees').text
		longitude=pos.find(loc + 'LongitudeDegrees').text
		lat = np.append(lat,float(latitude))
		lng = np.append(lng,float(longitude))
		rate = trackpoints.find(loc + 'HeartRateBpm')
		hr = np.append(hr,int(rate.find(loc + 'Value').text))
		alt = np.append(alt,float(trackpoints.find(loc + 'AltitudeMeters').text))
		extensions = trackpoints.find(loc + 'Extensions')
		tpx = extensions.find('{http://www.garmin.com/xmlschemas/ActivityExtension/v2}TPX')
		speed = tpx.find('{http://www.garmin.com/xmlschemas/ActivityExtension/v2}Speed').text
		spd = np.append(spd,float(speed))
	#convert speed from m/s to mph
	spd = [round(x*2.23694,1) for x in spd]
	return (lat,lng,hr,alt,spd)

# Creates normalized arrays to scale for display
def normalize(scale, lat, lng, hr, alt, spd):
	maxlat = np.max(lat)
	minlat = np.min(lat)
	rangelat = maxlat-minlat
	latstep = rangelat/scale
	nlat = [(x-minlat)/latstep for x in lat]

	maxlng = np.max(lng)
	minlng = np.min(lng)
	rangelng = maxlng-minlng
	lngstep = rangelng/scale
	nlng = [(x-minlng)/lngstep for x in lng]

	maxhr = np.max(hr)
	minhr = np.min(hr)
	rangehr = maxhr-minhr
	hrstep = rangehr/(scale/5)
	nhr = [(x-minhr)/hrstep for x in hr]

	maxalt = np.max(alt)
	minalt = np.min(alt)
	rangealt = maxalt-minalt
	altstep = rangealt/(scale/5)
	nalt = [(x-minalt)/altstep for x in alt]

	maxspd = np.max(spd)
	minspd = np.min(spd)
	rangespd = maxspd-minspd
	spdstep = rangespd/(scale/5)
	nspd = [(x-minspd)/spdstep for x in spd]

	return (nlat, nlng, nhr, nalt, nspd)
# Draws to window
def draw(scale, sideSize, rfRate, readRate, Nlat, Nlng, Nhr, Nalt, Nspd, hr, alt, spd):
	win = GraphWin("Ride", scale+sideSize, scale)
	win.setBackground(color_rgb(0,0,0))
	length = len(Nlat)
	textSize = findTextSize(sideSize)

	drawLegends(scale, sideSize, textSize, win, np.min(alt), np.max(alt), np.min(hr), np.max(hr), np.min(spd), np.max(spd))

	pt2 = Point(Nlng[0],scale-Nlat[0])
	altRect = Rectangle(Point(0,0), Point(0,0))
	hrRect = Rectangle(Point(0,0), Point(0,0))
	spdRect = Rectangle(Point(0,0), Point(0,0))

	iterDraw(0, scale, sideSize, rfRate, readRate, Nlat, Nlng, Nhr, Nalt, Nspd, hr, alt, spd, length, textSize, win, pt2, altRect, hrRect, spdRect)

# Iterates through the arrays and draws to window
def iterDraw(x, scale, sideSize, rfRate, readRate, Nlat, Nlng, Nhr, Nalt, Nspd, hr, alt, spd, length, textSize, win, pt2, altRect, hrRect, spdRect):
	x += readRate
	if x <= length:
		pt1 = pt2
		pt2 = Point(Nlng[x],scale-Nlat[x])
		ln = Line(pt1,pt2)
		ln.setOutline(color_rgb(90, 97, 255))
		ln.draw(win)
		# Clear the numerical values
		clearSidebar(scale, sideSize, win, textSize)
		# Clear previous altitude bar and re-draw
		altRect.undraw()
		altRect = Rectangle(Point(scale + (sideSize/3), (scale/5)), Point(scale + (2*sideSize/3), (scale/5)-Nalt[x]))
		altRect.setOutline(color_rgb(0, 255, 0))
		altRect.setFill(color_rgb(153, 255, 167))
		altRect.draw(win)
		# Clear previous heart rate bar and re-draw
		hrRect.undraw()
		hrRect = Rectangle(Point(scale + (sideSize/3), (scale*2/5)), Point(scale + (2*sideSize/3), (scale*2/5)-Nhr[x]))
		hrRect.setOutline(color_rgb(255, 0, 0))
		hrRect.setFill(color_rgb(100, 30, 30))
		hrRect.draw(win)
		# Clear previous speed bar and re-draw
		spdRect.undraw()
		spdRect = Rectangle(Point(scale + (sideSize/3), (scale*3/5)), Point(scale + (2*sideSize/3), (scale*3/5)-Nspd[x]))
		spdRect.setOutline(color_rgb(0, 0, 255))
		spdRect.setFill(color_rgb(30, 80, 100))
		spdRect.draw(win)
		# Draw the numerical values
		drawText(scale, sideSize, win, alt[x], hr[x], spd[x], textSize)

		time.sleep(rfRate)
		iterDraw(x, scale, sideSize, rfRate, readRate, Nlat, Nlng, Nhr, Nalt, Nspd, hr, alt, spd, length, textSize, win, pt2, altRect, hrRect, spdRect)
	else:
		return
# Guardrail for text size, since Graphics.py can only handle sizes between 5 and 36
def findTextSize(sideSize):
	if sideSize/32 >= 36:
		return 36
	elif sideSize/32 <= 5:
		return 5
	else:
		return int(sideSize/32)
# Draws constant values on the window
def drawLegends(scale, sideSize, textSize, win, minAlt, maxAlt, minHr, maxHr, minSpd, maxSpd):
	altTitle = Text(Point(scale + 50, textSize/2), 'Altitude (m)')
	altTitle.setTextColor(color_rgb(0, 250, 0))
	altTitle.setSize(textSize)
	altTitle.setStyle('bold')
	altTitle.draw(win)
	hrTitle = Text(Point(scale + 50, (scale/5) + (textSize/2)), 'Heart Rate (bpm)')
	hrTitle.setTextColor(color_rgb(250, 0, 0))
	hrTitle.setSize(textSize)
	hrTitle.setStyle('bold')
	hrTitle.draw(win)
	spdTitle = Text(Point(scale + 50, (scale*2/5) + (textSize/2)), 'Speed (mph)')
	spdTitle.setTextColor(color_rgb(0, 0, 250))
	spdTitle.setSize(textSize)
	spdTitle.setStyle('bold')
	spdTitle.draw(win)

	# Draw the altitude maximum value
	altMxTtl = Text(Point(scale + (sideSize*5/6), textSize), 'Max- ' + str(maxAlt))
	altMxTtl.setTextColor(color_rgb(0, 250, 0))
	altMxTtl.setSize(textSize)
	altMxTtl.draw(win)
	# Draw the altitude minimum value
	altMnTtl = Text(Point(scale + (sideSize*5/6), (scale/5)-(textSize/2)), 'Min- ' + str(minAlt))
	altMnTtl.setTextColor(color_rgb(0, 250, 0))
	altMnTtl.setSize(textSize)
	altMnTtl.draw(win)
	# Draw the heartrate maximum value
	hrMxTtl = Text(Point(scale + (sideSize*5/6), (scale/5) + (textSize)), 'Max- ' + str(maxHr))
	hrMxTtl.setTextColor(color_rgb(250, 0, 0))
	hrMxTtl.setSize(textSize)
	hrMxTtl.draw(win)
	# Draw the altitude minimum value
	hrMnTtl = Text(Point(scale + (sideSize*5/6), (scale*2/5) - (textSize/2)), 'Min- ' + str(minHr))
	hrMnTtl.setTextColor(color_rgb(250, 0, 0))
	hrMnTtl.setSize(textSize)
	hrMnTtl.draw(win)
	# Draw the speed maximum value
	spdMxTtl = Text(Point(scale + (sideSize*5/6), (scale*2/5) + (textSize)), 'Max- ' + str(maxSpd))
	spdMxTtl.setTextColor(color_rgb(0, 0, 250))
	spdMxTtl.setSize(textSize)
	spdMxTtl.draw(win)
	# Draw the speed minimum value
	spdMnTtl = Text(Point(scale + (sideSize*5/6), (scale*3/5) - (textSize/2)), 'Min- ' + str(minSpd))
	spdMnTtl.setTextColor(color_rgb(0, 0, 250))
	spdMnTtl.setSize(textSize)
	spdMnTtl.draw(win)

	# Draw the compass image
	compass = Image(Point(30, 30), "compass.gif")
	compass.draw(win)
# Draws the current values to graphs
def drawText(scale, sideSize, win, alt, hr, spd, textSize):
	altTxt = Text(Point(scale + sideSize/5, scale/10), alt)
	altTxt.setTextColor(color_rgb(0, 250, 0))
	altTxt.setSize(textSize)
	altTxt.draw(win)
	hrTxt = Text(Point((scale + sideSize/5), scale*3/10), hr)
	hrTxt.setTextColor(color_rgb(250, 0, 0))
	hrTxt.setSize(textSize)
	hrTxt.draw(win)
	spdTxt = Text(Point((scale + sideSize/5), scale*5/10), spd)
	spdTxt.setTextColor(color_rgb(0, 0, 250))
	spdTxt.setSize(textSize)
	spdTxt.draw(win)
# Since Graphics.py doesn't have an 'undraw' function for text, this draws a black box over them to reset the numbers
def clearSidebar(scale, sideSize, win, textSize):
	# Clear the altitude number
	clear = Rectangle(Point(scale + 10, (scale/15)), Point(scale + (sideSize/3)-10, (scale*2/15)))
	clear.setOutline(color_rgb(0, 255, 0))
	clear.setFill(color_rgb(0, 0, 0))
	clear.draw(win)

	# Clear the heart rate number
	clear = Rectangle(Point(scale + 10, (scale*4/15)), Point(scale + (sideSize/3)-10, (scale*5/15)))
	clear.setOutline(color_rgb(255, 0, 0))
	clear.setFill(color_rgb(0, 0, 0))
	clear.draw(win)

	# Clear the speed number
	clear = Rectangle(Point(scale + 10, (scale*7/15)), Point(scale + (sideSize/3)-10, (scale*8/15)))
	clear.setOutline(color_rgb(0, 0, 255))
	clear.setFill(color_rgb(0, 0, 0))
	clear.draw(win)

def main():
	# Constants
	fileName = 'RacingSunsetFull.xml'
	scale = 500			#size of map
	sideSize = 300 		#width of sidebars
	rfRate = 0.05		#refresh rate
	readRate = 5		#rate of reading each trackpoint in xml. If set to 2, will skip every other point
	# Store raw data
	(lat,lng,hr,alt,spd) = readin(fileName)
	# Normalize data for visualization
	(Nlat, Nlng, Nhr, Nalt, Nspd) = normalize(scale, lat, lng, hr, alt, spd)
	draw(scale, sideSize, rfRate, readRate, Nlat, Nlng, Nhr, Nalt, Nspd, hr, alt, spd)

main()