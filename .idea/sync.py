#!/usr/bin/python

__author__ = 'torall'




import sys, getopt

def main(argv):
   node = ''
   username = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["node=","user="])
   except getopt.GetoptError:
      print 'sync.py -n <node> -u <username>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'sync.py -n <node> -u <username>'
         sys.exit()
      elif opt in ("-n", "--node"):
         node = arg
      elif opt in ("-u", "--username"):
         username = arg
   print 'node is "', node
   print 'Output file is "', username

if __name__ == "__main__":
   main(sys.argv[1:])