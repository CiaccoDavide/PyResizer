 ################################################
# part of the PyResizer project by Ciacco Davide #
#  I just wanted to write a simple image         #
#  resizer. This is one of my first python       #
#  programs, and I'm using the Pillow module.    #
 ################################################
import os,sys
from PIL import Image

maxsize = sys.argv[1]
maxsize = (maxsize,maxsize)
outputFormat = "JPEG" #or "PNG", etc... 

for inputImage in sys.argv[2:]:						#loop through the images to process them
	img = Image.open(inputImage)					#loads the image file into img
	img.thumbnail(maxsize, PIL.Image.ANTIALIAS) 	#resizes the image using maxsize var for both the width and the height
	outputImageName=os.path.splitext(inputImage)[0] #nome del file in output (si potrebbe aggiungere una stringa all'inizio o alla fine a piacere)
	img.save(outputImageName,outputFormat) 			#il formato è definito all'inizio, se si vuole mantenere il formato originale di ciascuna foto basta usare img.save(outputImageName)


#non c'è controllo sulla sovrascrittura o su errori in input per ora
#try:
#	img.process.stuff...
#except IOError:
#	print "Got stuck on retreiving you image, sir."
