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
    dirSource   = os.path.abspath( args.directory )
    dirDestCR2  = dirSource + '/CR2'
    dirDestWeb  = dirSource + '/websize'

    # check if source directory exists
    if not os.path.exists(dirSource):
        print args.directory, "does not exist"
        sys.exit(1)

    # create needed directories
    if not os.path.exists(dirDestCR2):
        os.makedirs(dirDestCR2)
    if not os.path.exists(dirDestWeb):
        os.makedirs(dirDestWeb)

    # move files to subdirs
    for filename in os.listdir(dirSource):
        m = re.search(r'\.(.*)$', filename )
        if m:
            ext = m.group(1).lower()

            # move CR2 Sources to subfolder
            if ext == 'cr2':

                victim  = dirSource + '/' + filename
                dest    = dirDestCR2 + '/' + filename
                shutil.move(victim, dest)
            
            # shrink images to websize and move them to subfolder 
            if ext in ['jpg', 'jpeg']:

                dest     = dirSource + '/' + filename
                victim   = dirDestWeb + '/' + filename
                command  = "convert -resize 800x600 -quality 100 %s %s" % (dest, victim)

                (status, output) = commands.getstatusoutput(command)


if __name__ == '__main__':
    main()
