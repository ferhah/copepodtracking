import sys
import os

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
import skimage.io
from skimage import feature
from skimage.feature import peak_local_max
from skimage.transform import hough_circle

def extractWells(imagename): 
    im = skimage.io.imread(imagename)
    edges = feature.canny(im)
    hough_radii = np.arange(130,131,2)
    hough_res = hough_circle(edges, hough_radii)
    peaks = peak_local_max(hough_res[0], num_peaks=30)#num_peaks gives the number of potential locations for wells; can be increased if oo few are found and decreased if wells are found in the wrong location
    plt.imshow(im, cmap=plt.cm.gray)
    outimages = []
    outPoints = []
    for [point, idx] in zip(peaks, range(len(peaks))):
        for pointTmp in peaks[:idx]: 
            if (abs(point[0]-pointTmp[0]) < 200) and (abs(point[1]-pointTmp[1]) < 200): 
                break
        else: 
            plt.scatter(point[1], point[0])
            plt.scatter(point[1]-130, point[0]-130, c='r', marker='+')
            plt.scatter(point[1]-130, point[0]+130, c='r', marker='+')
            plt.scatter(point[1]+130, point[0]-130, c='r', marker='+')
            plt.scatter(point[1]+130, point[0]+130, c='r', marker='+')
            
            plt.scatter(point[1]+130, point[0], c='r', marker='+')
            plt.scatter(point[1]-130, point[0], c='r', marker='+')
            plt.scatter(point[1], point[0]-130, c='r', marker='+')
            plt.scatter(point[1], point[0]+130, c='r', marker='+')
            outPoints.append(point)
            #outimages.append(im[point[0]-130:point[0]+130, point[1]-130:point[1]+130]) 
    # Get Points with smalles x
    outPoints = sorted(outPoints, key=lambda x:x[1])
    columns = []
    for idx in xrange(6): 
        columns.append(sorted(outPoints[idx*4:(idx+1)*4], key=lambda x:x[0]))
    imagedir = os.path.dirname(imagename)
    imageid = int(os.path.splitext(os.path.basename(imagename))[0])
    with open('%s/debug/%03d.csv'%(imagedir, imageid), 'w') as outfile: 
        for [point, idx] in zip(columns[0], range(4)): 
            plt.annotate("0_%d" % (idx), (point[1], point[0]))
            #plt.scatter(point[1], point[0], c='r') 
            outfile.write("0_%d: %d %d\n" % (idx, point[1], point[0]))
            #skimage.io.imsave('%s/0_%d/%03d.png'%(imagedir, idx, imageid), im[point[0]-130:point[0]+130, point[1]-130:point[1]+130])
        
        for [point, idx] in zip(columns[1], range(4)): 
            plt.annotate("1_%d" % (idx), (point[1], point[0]))
            #plt.scatter(point[1], point[0], c='y')
            outfile.write("1_%d: %d %d\n" % (idx, point[1], point[0]))
            #skimage.io.imsave('%s/1_%d/%03d.png'%(imagedir, idx, imageid), im[point[0]-130:point[0]+130, point[1]-130:point[1]+130])
        
        for [point, idx] in zip(columns[2], range(4)): 
            plt.annotate("2_%d" % (idx), (point[1], point[0]))
            #plt.scatter(point[1], point[0], c='g')
            outfile.write("2_%d: %d %d\n" % (idx, point[1], point[0]))
            #skimage.io.imsave('%s/2_%d/%03d.png'%(imagedir, idx, imageid), im[point[0]-130:point[0]+130, point[1]-130:point[1]+130])
        
        for [point, idx] in zip(columns[3], range(4)): 
            plt.annotate("3_%d" % (idx), (point[1], point[0]))
            #plt.scatter(point[1], point[0], c='r', marker='x')
            outfile.write("3_%d: %d %d\n" % (idx, point[1], point[0]))
            #skimage.io.imsave('%s/3_%d/%03d.png'%(imagedir, idx, imageid), im[point[0]-130:point[0]+130, point[1]-130:point[1]+130])
        
        for [point, idx] in zip(columns[4], range(4)): 
            plt.annotate("4_%d" % (idx), (point[1], point[0]))
            #plt.scatter(point[1], point[0], c='y', marker='x')
            outfile.write("4_%d: %d %d\n" % (idx, point[1], point[0]))
            #skimage.io.imsave('%s/4_%d/%03d.png'%(imagedir, idx, imageid), im[point[0]-130:point[0]+130, point[1]-130:point[1]+130])
        
        for [point, idx] in zip(columns[5], range(4)): 
            plt.annotate("5_%d" % (idx), (point[1], point[0]))
            #plt.scatter(point[1], point[0], c='g', marker='x')
            outfile.write("5_%d: %d %d\n" % (idx, point[1], point[0]))
            #skimage.io.imsave('%s/5_%d/%03d.png'%(imagedir, idx, imageid), im[point[0]-130:point[0]+130, point[1]-130:point[1]+130])
            
    
    
    plt.savefig('%s/debug/%03d.png'%(imagedir, imageid))
    
    return columns

def main(dirname): 
    images = os.listdir(dirname)
    for idx in xrange(6): 
        for jdx in xrange(4): 
            os.mkdir(dirname + '/%d_%d/' % (idx, jdx))
    os.mkdir(dirname+'/debug')
    columns = extractWells(dirname + '/' + images[0])
    for image in images: 
        try: 
            #print "Processing image", image
            im = skimage.io.imread(dirname + '/' + image)
            imagedir = dirname
            imageid = int(os.path.splitext(image)[0])
            for idx in xrange(6): 
                for jdx in xrange(4): 
                    point = columns[idx][jdx]
                    #print point
                    #print '%s/%d_%d/%03d.png'%(imagedir, idx, jdx, imageid)
                    #plt.close()
                    #plt.clf()
                    #plt.imshow(im[point[0]-130:point[0]+130, point[1]-130:point[1]+130])
                    #plt.show()
                    startX = max(point[0]-130, 0)
                    stopX = min(point[0]+130, im.shape[0])
                    startY = max(point[1]-130, 0)
                    stopY = min(point[1]+130, im.shape[1])
                    #print startX, stopX, startY, stopY
                    stopY = point[1]+130
                    skimage.io.imsave('%s/%d_%d/%03d.png'%(imagedir, idx, jdx, imageid),
                                      im[startX:stopX, startY:stopY])
                                      #im[point[0]-130:point[0]+130, point[1]-130:point[1]+130])
        except IOError: 
            print "Skip image", image, "because of IOError"

def main2(dirname): 
    subdirs = os.listdir(dirname)
    for subdir in subdirs: 
        try: 
            print dirname + '/' + subdir
            main(dirname + '/' + subdir + '/')
        except WindowsError: 
            print "Skip file", subdir

if __name__ == "__main__":
    main2(sys.argv[1])
