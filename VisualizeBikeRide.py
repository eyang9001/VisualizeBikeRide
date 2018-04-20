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
	return (lat,lng,hr,alt)
# Creates normalized arrays to scale for display
def normalize(scale, lat, lng, hr, alt):
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

	return (nlat, nlng, nhr, nalt)
# Draws to window
def draw(scale, sideSize, rfRate, readRate, Nlat, Nlng, Nhr, Nalt, hr, alt):
	win = GraphWin("Ride", scale+(sideSize*2), scale)
	win.setBackground(color_rgb(0,0,0))
	length = len(Nlat)
	textSize = findTextSize(sideSize)

	drawLegends(scale, sideSize, textSize, win, np.min(alt), np.max(alt), np.min(hr), np.max(hr))

	pt2 = Point(Nlng[0]+sideSize,scale-Nlat[0])
	altRect = Rectangle(Point(0,0), Point(0,0))
	hrRect = Rectangle(Point(0,0), Point(0,0))

	iterDraw(0, scale, sideSize, rfRate, readRate, Nlat, Nlng, Nhr, Nalt, hr, alt, length, textSize, win, pt2, altRect, hrRect)

# Iterates through the arrays and draws to window
def iterDraw(x, scale, sideSize, rfRate, readRate, Nlat, Nlng, Nhr, Nalt, hr, alt, length, textSize, win, pt2, altRect, hrRect):
	x += readRate
	if x <= length:
		pt1 = pt2
		pt2 = Point(Nlng[x]+sideSize,scale-Nlat[x])
		ln = Line(pt1,pt2)
		ln.setOutline(color_rgb(0, 0, 255))
		ln.draw(win)
		# Clear the numerical values
		clearSidebar(scale, sideSize, win)
		# Clear previous altitude bar and re-draw
		altRect.undraw()
		altRect = Rectangle(Point((sideSize/3), (scale/5)), Point((2*sideSize/3), (scale/5)-Nalt[x]))
		altRect.setOutline(color_rgb(0, 255, 0))
		altRect.setFill(color_rgb(0, 250, 0))
		altRect.draw(win)
		# Clear previous heart rate bar and re-draw
		hrRect.undraw()
		hrRect = Rectangle(Point(scale+(4*sideSize/3), (scale/5)), Point(scale+(5*sideSize/3), (scale/5)-Nhr[x]))
		hrRect.setOutline(color_rgb(255, 0, 0))
		hrRect.setFill(color_rgb(250, 0, 0))
		hrRect.draw(win)
		# Draw the numerical values
		drawText(scale, sideSize, win, alt[x], hr[x], textSize)

		time.sleep(rfRate)
		iterDraw(x, scale, sideSize, rfRate, readRate, Nlat, Nlng, Nhr, Nalt, hr, alt, length, textSize, win, pt2, altRect, hrRect)
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
def drawLegends(scale, sideSize, textSize, win, minAlt, maxAlt, minHr, maxHr):
	altTitle = Text(Point(50, textSize/2), 'Altitude (m)')
	altTitle.setTextColor(color_rgb(0, 250, 0))
	altTitle.setSize(textSize)
	altTitle.setStyle('bold')
	altTitle.draw(win)
	hrTitle = Text(Point(scale + sideSize + 50, textSize/2), 'Heart Rate (bpm)')
	hrTitle.setTextColor(color_rgb(250, 0, 0))
	hrTitle.setSize(textSize)
	hrTitle.setStyle('bold')
	hrTitle.draw(win)

	# Draw the altitude maximum value
	altMxTtl = Text(Point(5*sideSize/6, textSize/2), 'Max- ' + str(maxAlt))
	altMxTtl.setTextColor(color_rgb(0, 250, 0))
	altMxTtl.setSize(textSize)
	altMxTtl.draw(win)
	# Draw the altitude minimum value
	altMnTtl = Text(Point(5*sideSize/6, scale/5-(textSize/2)), 'Min- ' + str(minAlt))
	altMnTtl.setTextColor(color_rgb(0, 250, 0))
	altMnTtl.setSize(textSize)
	altMnTtl.draw(win)
	# Draw the heartrate maximum value
	hrMxTtl = Text(Point(scale + 11*sideSize/6, textSize/2), 'Max- ' + str(maxHr))
	hrMxTtl.setTextColor(color_rgb(250, 0, 0))
	hrMxTtl.setSize(textSize)
	hrMxTtl.draw(win)
	# Draw the altitude minimum value
	hrMnTtl = Text(Point(scale + 11*sideSize/6, scale/5-(textSize/2)), 'Min- ' + str(minHr))
	hrMnTtl.setTextColor(color_rgb(250, 0, 0))
	hrMnTtl.setSize(textSize)
	hrMnTtl.draw(win)
	# Draw the compass image
	compass = Image(Point(sideSize+30, 30), "compass.gif")
	compass.draw(win)
# Draws the current values to graphs
def drawText(scale, sideSize, win, alt, hr, textSize):
	altTxt = Text(Point(sideSize/5, scale/10), alt)
	altTxt.setTextColor(color_rgb(0, 250, 0))
	altTxt.setSize(textSize)
	altTxt.draw(win)
	hrTxt = Text(Point((scale + sideSize*6/5), scale/10), hr)
	hrTxt.setTextColor(color_rgb(250, 0, 0))
	hrTxt.setSize(textSize)
	hrTxt.draw(win)
# Since Graphics.py doesn't have an 'undraw' function for text, this draws a black box over them to reset the numbers
def clearSidebar(scale, sideSize, win):
	# Clear the altitude number
	clear = Rectangle(Point(0, (scale/11)), Point((sideSize/3)-10, (scale*2/11)))
	clear.setOutline(color_rgb(0, 0, 0))
	clear.setFill(color_rgb(0, 0, 0))
	clear.draw(win)

	# Clear the heart rate number
	clear = Rectangle(Point(scale + sideSize + 10, (scale/11)), Point(scale + 4/3*sideSize-10, (scale*2/11)))
	clear.setOutline(color_rgb(0, 0, 0))
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
	(lat,lng,hr,alt) = readin(fileName)
	# Normalize data for visualization
	(Nlat, Nlng, Nhr, Nalt) = normalize(scale, lat, lng, hr, alt)
	draw(scale, sideSize, rfRate, readRate, Nlat, Nlng, Nhr, Nalt, hr, alt)

main()