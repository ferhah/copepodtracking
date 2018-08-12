import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import cv2

def getMeanImages(imagepath): 
	meanImage = cv2.cvtColor(cv2.imread("%s/%03d.png" % (imagepath, 1)), cv2.COLOR_RGB2GRAY)
	for idx in xrange(2,450):  	
		meanImage = np.dstack((meanImage, cv2.cvtColor(cv2.imread("%s/%03d.png" % (imagepath, idx)), cv2.COLOR_RGB2GRAY)))
	return np.mean(meanImage, axis=2)	
	
def proceedWell(imagepath, outfilename): 
	meanImage = getMeanImages(imagepath)
	with open(outfilename, 'w') as outfile: 
		for idx in xrange(1,450): 
			imagename = "%s/%03d.png" % (imagepath, idx)
			im = cv2.cvtColor(cv2.imread(imagename), cv2.COLOR_RGB2GRAY)
			imDiff = im - meanImage
			found = False
			while(not found):
				target = np.unravel_index(imDiff.argmin(), imDiff.shape)
				if np.linalg.norm((target[0]-130, target[1]-130)) > 117:
					imDiff[target[0], target[1]] = 100
				else:
					found = True
			outfile.write("%d %d %d\n" % (idx, target[1], target[0]))

def getTarget(self, threshold):
	[im, imDiff] = self.getImages()
	found = False
	while(not found):
		self._target = np.unravel_index(imDiff.argmin(), imDiff.shape)
		if np.linalg.norm((self._target[0]-130, self._target[1]-130)) > 117:
			imDiff[self._target[0], self._target[1]] = 100
		else:
			found = True
		return self._target

def proceedFolder(basedir): 
	plates = os.listdir(basedir)
	#print(plates)
	for plate in plates: 
		wells = os.listdir("%s/%s" % (basedir, plate))
		#print(wells)
		for well in wells:
                        if well != "debug":
                     	#images= os.listdir("%s/%s/%s" % (basedir, plate,well)) 
                        #print len(images)
                                if os.path.isdir("%s/%s/%s" % (basedir, plate, well))==True:
                        #if len(images) > 100 :
                                        print "%s/%s/%s/" % (basedir, plate, well)
                                        proceedWell("%s/%s/%s/" % (basedir, plate, well), 
						"%s/%s/output_%s.txt" % (basedir, plate, well))
                                else:
                                        print("FALSE")
                        else:
                                print("Debug")

if __name__ == "__main__": 
	proceedFolder(sys.argv[1]) 
		
	
