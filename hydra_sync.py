import sys
import os
import commands
import pymssql
import ConfigParser

### init


node = ''
node_address ='' #'vanmac.homeip.net'      #### this needs to come from the db
local_shows = '/mnt/shows/'             ### This comes from the config file
remote_show_loc = ''
remote_user = ''                    ### comes from the db

debug = 1

n_shows = 0
shows=[]


configLocName = 'hydra.conf'

# get config settings
Config = ConfigParser.ConfigParser()
Config.read(configLocName)
Config.sections()



class Node:
    def __init__(self, username, address, show_loc):
        self.username = username
        self.address = address
        self.show_loc = show_loc
        self.shows = []             #### creates a new empty list for each node


def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


# map settings
provider = ConfigSectionMap("Database")['provider']
hostname = ConfigSectionMap("Database")['host']
username = ConfigSectionMap("Database")['user']
password_ = ConfigSectionMap("Database")['pass']
db = ConfigSectionMap("Database")['db']
debug = ConfigSectionMap("General")['debug']
move = ConfigSectionMap("General")['move']
server_name = ConfigSectionMap("NAS")['servername']
showfolder = ConfigSectionMap("NAS")['showfolder']



def main():
    conn = pymssql.connect(host=hostname, user=username, password=password_, database=db)
    cur = conn.cursor()

    cur.execute('SELECT seq,node,address,shows_loc,username FROM nodes WHERE status=%s ORDER BY seq', 'active')
    row = cur.fetchone()
    while row:
        seq = (row[0])
    	node = (row[1])
        node_address = (row[2])
        node_user = (row[3])

        print 'seq: ' + str(seq) + ' - node: '+ node +' -  node_address: '+ node_address +' - ---'
        row = cur.fetchone()
    conn.commit()



######################################
######################################
##### Main
######################################
if __name__ == "__main__":
    main()


# connection string
conn = pymssql.connect(host=hostname, user=username, password=password_, database=db)
cur = conn.cursor()

cur.callproc('sp_ShowsToSync',(node,))

for row in cur:
    remote_show_loc = row[6]
    shows.append(row[2])
    n_shows += 1  # might be a better way to do this.... oh well...

print n_shows , ' ', remote_show_loc

com_rsync = 'rsync -avzP -e "ssh" '+ local_shows +shows[0].replace(' ','\ ')+' '
com_rsync+= remote_user+'@'+node_address+':\''+ remote_show_loc+'\''


if debug == 1:
    print com_rsync

os.system(com_rsync)


conn.close()





