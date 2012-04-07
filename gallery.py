#!/usr/bin/python
import commands
import os
import sys
import argparse
import re
import shutil

def main():

    # get input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--comment', default='cc-by-sa Tilman Beitter')
    parser.add_argument('directory', )
    args = parser.parse_args()
    
    # define directory structur
    dirSource       = os.path.abspath( args.directory )
    dirDestSrc      = dirSource + '/sources'
    dirDestSrcCR2   = dirSource + '/sources/CR2'
    dirDestWeb      = dirSource + '/websize'

    # check if source directory exists
    if not os.path.exists(dirSource):
        print args.directory, "does not exist"
        sys.exit(1)

    # use source files if directory already processed
#    if os.path.exists(dirDestSrc):
#        dirSource = dirDestSrc

    # create needed directories
    if not os.path.exists(dirDestSrc):
        os.makedirs(dirDestSrc)
    if not os.path.exists(dirDestSrcCR2):
        os.makedirs(dirDestSrcCR2)
    if not os.path.exists(dirDestWeb):
        os.makedirs(dirDestWeb)

    # move files to subdirs
    for filename in os.listdir(dirSource):
        m = re.search(r'\.(.*)$', filename )
        if m:
            ext = m.group(1).lower()

            if ext == 'cr2':
                dest        = dirDestSrcCR2 + '/' + filename
                victimOrig  = dirSource + '/' + filename
                shutil.move(victimOrig, dest)
            elif ext in ['jpg', 'jpeg']:
                dest        = dirDestSrc + '/' + filename
                victimOrig  = dirSource + '/' + filename
                shutil.move(victimOrig, dest)

                # shrink to websize and insert licence comment
                victimWeb = dirDestWeb + '/' + filename
                command = "convert -resize 800x600 -quality 100 %s %s" % (dest, victimWeb)
                (status, output) = commands.getstatusoutput(command)
                command = "convert -size 800x84 -pointsize 12 xc:none -font Courier -gravity center -stroke black -strokewidth 2 -annotate 0 'cc-by-sa Tilman Beitter' -background none -shadow 100x3+0+0 +repage -stroke none -fill white -annotate 0 'cc-by-sa Tilman Beitter' %s +swap -gravity south -geometry +0-30 -composite %s" % (victimWeb, victimWeb)
                (status, output) = commands.getstatusoutput(command)

                # insert licence comment into origSize
                (status, output) = commands.getstatusoutput(command)
                command = "convert -size 800x84 -pointsize 80 xc:none -font Courier -gravity center -stroke black -strokewidth 2 -annotate 0 'cc-by-sa Tilman Beitter' -background none -shadow 100x3+0+0 +repage -stroke none -fill white -annotate 0 'cc-by-sa Tilman Beitter' %s +swap -gravity south -geometry +0+20 -composite %s" % (dest, victimOrig)
                (status, output) = commands.getstatusoutput(command)

if __name__ == '__main__':
    main()
