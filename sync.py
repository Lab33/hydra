#!/usr/bin/python

__author__ = 'torall'

import sys
import getopt
import sqlite3
import os

addresses = []
nodes = []
shows = []
s_dir = []



def main(argv):
   node = ''
   sshlogin = ''
   dbname=''
   loc = ''
   remote=''

   try:
      opts, args = getopt.getopt(argv,"hn:u:d:l:r:",["node=","user=","db=","loc=","remote="])
   except getopt.GetoptError:
      print 'sync.py -n <node> -u <username> -d <sqlitedb> -l <locdir> -r <remotedir>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'sync.py -n <node> -u <username> -d <sqlitedb> -l <locdir> -r <remotedir>'
         sys.exit()
      elif opt in ("-n", "--node"):
         node = arg
      elif opt in ("-u", "--username"):
         sshlogin = arg
      elif opt in ("-d", "--db"):
         dbname = arg
      elif opt in ("-l","--locdir"):
         loc = arg
      elif opt in ("-r","--remotedir"):
         remote = arg

   get_nodes(node, dbname)
   get_shows(node, dbname)


   showdir = s_dir[0]

   for i in range(0, len(nodes)):
      print nodes[i], ' --- ', addresses[i],' ---- ', showdir
      address = addresses[i]


   show_string = ''

   for s in range(0, len(shows)):
       tempshow = shows[s]
       tempshow = tempshow.replace(' ','\ ')
       show_string += loc+tempshow+' '

   #print show_string
   #os.system("rsync -aP -e ssh "+ loc+tempshow+" "+sshlogin+"@"+address+":"+showdir)
   os.system("rsync -aP -e ssh "+ show_string +" "+sshlogin+"@"+address+":"+showdir)

def sync():
   pass


def get_nodes(node, database):
   db = sqlite3.connect(database)
   cursor = db.cursor()
   cursor.execute('''select node,address, showdir from nodes where node=?''', (node,))

   for row in cursor:
      nodes.append(row[0])
      addresses.append(row[1])
      s_dir.append(row[2])

   db.close()


def get_shows(node, database):
   db = sqlite3.connect(database)
   cursor = db.cursor()
   cursor.execute('''select node,show from active_shows where node=?''', (node,))

   for row in cursor:
      shows.append(row[1])

   db.close()


if __name__ == "__main__":
   main(sys.argv[1:])


