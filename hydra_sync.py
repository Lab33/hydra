import sys
import os
import commands
import pymssql

### init
node = 'blackwidow'
node_address = 'blackwidow.homeip.net'
local_shows = '/mnt/shows/'
remote_show_loc = ''
remote_user = 'ryan'

debug = 1

n_shows = 0
shows=[]

# connection string
conn = pymssql.connect(host='thanos', user='web', password='fr0zenfish!', database='hydra') # this needs to come from a config fie
cur = conn.cursor()

cur.callproc('sp_ShowsToSync',(node,))

for row in cur:
    print (row[0]),' actively synced shows for '
    remote_show_loc = row[6]
    shows.append(row[2])
    n_shows += 1  # might be a better way to do this.... oh well...

print n_shows , ' ', remote_show_loc

com_rsync = 'rsync -avzP -e "ssh -i vanmac_key" '+ local_shows +shows[0].replace(' ','\ ')+' '
com_rsync+= remote_user+'@'+node_address+':\''+ remote_show_loc+'\''


if debug == 1:
    print com_rsync

os.system(com_rsync)


conn.close()
