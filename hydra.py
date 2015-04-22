import ConfigParser
import sys
import os
import commands
import pymssql
import sqlite3
import re
import datetime



#########################################################
####### TO DO
# - if the folder has a space the process will fail
# - replace('.',' ') doesnt work with Marvel, going to have to add a special rule

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
server_name = ConfigSectionMap("NAS")['servername']
torrentfolder = ConfigSectionMap("NAS")['torrentfolder']
showfolder = ConfigSectionMap("NAS")['showfolder']

#if debug == '1':
print '################ DEBUG  ######################'
print 'Provider: ',provider
print 'Host: ', host
print 'User: ', user
print 'Password: ', password
print 'Database: ', db
print 'Debug: ', debug
print 'Server Name: ', server_name
print 'TorrentFolder: ', torrentfolder
print 'ShowFolder: ', showfolder
#os.system('pwd')
print '\n '


################################################################
#list folders only 
#ls -d */ | sed 's|[/]||g'


for file in os.listdir(torrentfolder):
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

	if season[:1] == '0':
#	    print 'REMOVE THE LEADING 0'
	    season = season[-1]
	    print season
	episode = ecode[-2:]
	
	file = (os.popen('ls '+torrentfolder+'/'+f+' | grep "mkv\|mp4\|avi"').readline()) # needs to be udpated

	file = file.strip()
	move_files = 'mv -v '+torrentfolder+'/'+f+'/'+file.replace(' ','\ ')+' '+showfolder+'/'+show.replace(' ','\ ')+'/Season\ '+season+'/' # change back to os.system
	
	if debug == '1':
		print move_files
		print torrentfolder

	os.system(move_files)	# temp - should always try and move

	folder = f.replace(' ','\ ')
    os.system('rm -rf '+torrentfolder+'/'+f+'/')

#	if debug == '1':
#            print show, season, episode
#    else:
#	if debug == '1':
#	    print 'not found'	


