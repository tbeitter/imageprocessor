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
  parser.add_argument('-s', '--size', default='1280x800')
  parser.add_argument('-q', '--quality', default=85, type=int)
  parser.add_argument('-v', '--verbose', action='store_true')
  parser.add_argument('directory') 
  args = parser.parse_args()

  # define directory structur
  dirSource   = os.path.abspath( args.directory )
  dirDestCR2  = dirSource + '/CR2'
  dirDestWeb  = dirSource + '/websize'

  # check if source directory exists
  if not os.path.exists(dirSource):
    print args.directory, "does not exist"
    sys.exit(1)

  # count files to give progress info
  iTotal  = len(sorted(os.listdir(dirSource)))

  # create needed subdirectory
  if not os.path.exists(dirDestWeb):
    os.makedirs(dirDestWeb)

  # move files to subdirs
  for index,filename in enumerate( sorted( os.listdir(dirSource) ) ):
    m = re.search(r'\.(.*)$', filename )
    if m:
      ext = m.group(1).lower()
      
      # move CR2 Sources to subfolder
      if ext == 'cr2':
 
        # create needed subdirectory
        if not os.path.exists(dirDestCR2):
          os.makedirs(dirDestCR2)

        victim  = dirSource + '/' + filename
        dest    = dirDestCR2 + '/' + filename
        shutil.move(victim, dest)

        if args.verbose:
          print '[' + iNow + '/' + iTotal + ']', 'moved:', filename

      # shrink images to websize and move them to subfolder 
      if ext in ['jpg', 'jpeg', 'png']:

        dest     = dirSource + '/' + filename
        victim   = dirDestWeb + '/' + filename
        command  = "convert -resize %s -quality %d %s %s" % (args.size, args.quality, dest, victim)
        (status, output) = commands.getstatusoutput(command)

        if args.verbose:
          print '[' + str(index + 1) + '/' + str(iTotal) + ']', 'resized:', filename


if __name__ == '__main__':
    main()
