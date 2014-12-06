#!/usr/bin/python

__author__ = 'torall'

import sys
import getopt
import sqlite3
import os

addresses = []
nodes = []
shows = []



def main(argv):
   node = ''
   sshlogin = ''
   dbname=''

   try:
      opts, args = getopt.getopt(argv,"hn:u:d:",["node=","user=","db="])
   except getopt.GetoptError:
      print 'sync.py -n <node> -u <username> -d <sqlitedb>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'sync.py -n <node> -u <username> -d <sqlitedb>'
         sys.exit()
      elif opt in ("-n", "--node"):
         node = arg
      elif opt in ("-u", "--username"):
         sshlogin = arg
      elif opt in ("-d", "--db"):
         dbname = arg

   get_nodes(node, dbname)
   get_shows(node, dbname)

   for i in range(0, len(nodes)):
      print nodes[i], ' --- ', addresses[i]

   for s in range(0, len(shows)):
      print shows[s]

def sync():
   pass


def get_nodes(node, database):
   db = sqlite3.connect(database)
   cursor = db.cursor()
   cursor.execute('''select node,address from nodes where node=?''', (node,))


   for row in cursor:
      nodes.append(row[0])
      addresses.append(row[1])

   db.close()

def get_shows(node, database):
   db2 = sqlite3.connect(database)
   cursor = db2.cursor()
   cursor.execute('''select node,show from active_shows where node=?''', (node,))

   for row in cursor:
      shows.append(row[1])

   db2.close()


if __name__ == "__main__":
   main(sys.argv[1:])


