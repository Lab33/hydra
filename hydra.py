import ConfigParser
import sys
import os
import commands
import pymssql
import sqlite3
import re
import datetime



regex = '[sS]+[0-9]+[eE]+[0-9]+[0-9]' # expression to find shows
filelist = []
configLocName = 'hydra.conf'

# get local shell user
who = (os.popen('whoami').readline())
who = who.strip()
node = ''

# get config settings
Config = ConfigParser.ConfigParser()
Config.read(configLocName) 
Config.sections()

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
host = ConfigSectionMap("Database")['host']
user = ConfigSectionMap("Database")['user']
password = ConfigSectionMap("Database")['pass']
db = ConfigSectionMap("Database")['db']
debug = ConfigSectionMap("General")['debug']
servername = ConfigSectionMap("NAS"),['servername']
#torrentfolder = ConfigSectionMap("NAS"),['torrentfolder']
#showfolder = ConfigSectionMap("NAS"),['showfolder']

#if debug == '1':
print provider, host, user, password, db, debug#, servername
#print 'TorrentFolder: ', torrentfolder
#print 'ShowFolder: ', showfolder
#os.system('pwd')
print '\n '


################################################################
#list folders only 
#ls -d */ | sed 's|[/]||g'

for file in os.listdir('/home/ryan/share/'):
    filelist.append(file)
 

for f in filelist:
#    print f +' _____F_____'
    show = f.replace('.',' ')
    episode_code = re.search(regex,show)
#    print show +'____SHOW____'
    cut_off = (re.search(regex,show))
    
    if episode_code:
	cut_off = (re.search(regex,show)).start()-1
	show = show[:cut_off]
	ecode = episode_code.group()
	season = ecode[1:-3]
	episode = ecode[-2:]
	
	os.system('ls ~/share/'+f)
	if debug == '1':
            print show, season, episode
    else:
	if debug == '1':
	    print 'not found'	
