import matplotlib.pyplot as plt
import os
import sys
import cv2

def proceedList(resultlist, imagepath, outputpath): 
	with open(resultlist) as infile:
		for line in infile: 
			v = line.split() 
			imagename = '%s/%03d.png' % (imagepath, int(v[0])) 
			im = cv2.cvtColor(cv2.imread(imagename), cv2.COLOR_RGB2GRAY)
			plt.imshow(im, cmap=plt.cm.gray) 
			plt.plot(int(v[1]), int(v[2]), 'x')
			plt.savefig("%s/%03d.png" % (outputpath, int(v[0])))
			plt.clf()
			plt.close()
			
if __name__ == "__main__": 
	subfiles = os.listdir(sys.argv[1])
	topfile=sys.argv[1]
	for subfile in subfiles:
		if "plate" not in subfile: 
			continue
		subfiles2 = os.listdir(topfile+'/'+subfile)
		subfile3 = 'check_results'+ '/' + subfile
		os.mkdir(subfile3) 
		for subfile2 in subfiles2:
                        if subfile2 != "debug":
                                infile = topfile + '/' + subfile + '/' + subfile2 + '/'
                                print subfile
                                print subfile2
                                print subfile3
                                                                                                
                                if os.path.isdir("%s" % (infile))==True:
                                        resultlist = topfile + '/' + subfile + '/' + 'output_'+ subfile2 + '.txt'
                                        outfile = subfile3 + '/' + subfile2 + "plot"
                                        os.mkdir(outfile) 
                                        proceedList(resultlist, infile, outfile)
