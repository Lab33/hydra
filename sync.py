#!/usr/bin/python

__author__ = 'torall'

import sys, getopt
import sqlite3

addresses = []
nodes = []


def main(argv):
   node = ''
   sshlogin = ''
   dbname=''

   try:
      opts, args = getopt.getopt(argv,"hn:u:d:",["node=","user=","db="])
   except getopt.GetoptError:
      print 'sync.py -n <node> -u <username> -d <sqlite db>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'sync.py -n <node> -u <username> -d <sqlite db>'
         sys.exit()
      elif opt in ("-n", "--node"):
         node = arg
      elif opt in ("-u", "--username"):
         sshlogin = arg
      elif opt in ("-d", "--db"):
         dbname = arg

   get_nodes(dbname)
   for i in range(0, len(nodes)):
      print nodes[i], ' --- ', addresses[i]

   print 'node is "', node
   print 'username is "', sshlogin
   print 'db is "', dbname


def sync(node,username,db):
   pass


def get_nodes(database):
   db = sqlite3.connect(database)
   cursor = db.cursor()
   cursor.execute('''select node,address from nodes''')

   for row in cursor:
      nodes.append(row[0])
      addresses.append(row[1])



if __name__ == "__main__":
   main(sys.argv[1:])


