#!/usr/bin/python


import sqlite3
import sys
import getopt


# import os

'''
def main(argv):
	node =''
	try:
		opts, args = getopt.getopt(argv,'hi:o:',["node="])
'''

print 'Number of arguments: ', len(sys.argv), 'arguments.'
print 'Argument List: ', str(sys.argv)


db_name = 'hydra.db'
loc = '/mnt/media/shows/'
dest_show = '/mnt/media/shows/'
username = 'ryan'

addresses = []
nodes = []


db = sqlite3.connect(db_name)
cursor = db.cursor()
cursor.execute('''select node,address from nodes''')

for row in cursor:
    nodes.append(row[0])
    addresses.append(row[1])


def sync_node(node,show):
    pass


for i in range(0,len(nodes)):
    print nodes[i]+' - '+addresses[i]


