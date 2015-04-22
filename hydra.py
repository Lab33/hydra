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
move = ConfigSectionMap("General")['move']
server_name = ConfigSectionMap("NAS")['servername']
torrentfolder = ConfigSectionMap("NAS")['torrentfolder']
showfolder = ConfigSectionMap("NAS")['showfolder']

if debug == '1':
    print '################ DEBUG  ######################'
    print 'Provider: ',provider
    print 'Host: ', host
    print 'User: ', user
    print 'Password: ', password
    print 'Database: ', db
    print 'Debug: ', debug
    print 'Do Not Move: ', move
    print 'Server Name: ', server_name
    print 'TorrentFolder: ', torrentfolder
    print 'ShowFolder: ', showfolder
    print '\n '


################################################################
#list folders only 
#ls -d */ | sed 's|[/]||g'

def clean_torrents():
    for file in os.listdir(torrentfolder):
        filelist.append(file)
 
    for f in filelist:
        show = f.replace('.',' ')
        episode_code = re.search(regex,show)
        cut_off = (re.search(regex,show))

        if episode_code:
        	cut_off = (re.search(regex,show)).start()-1 
        	show = show[:cut_off]
        	ecode = episode_code.group()
        	season = ecode[1:-3]

    	if season[:1] == '0':
            season = season[-1] # removes the leading zero from the season number

#        os.system('ls '+torrentfolder+' | grep ',show)
        print('ls '+showfolder+'/ | grep "'+show+'"')



    	episode = ecode[-2:]
        if debug == '1':
            f = f.replace(' ','\ ')
            print 'ls '+torrentfolder+'/'+f+' | grep "mkv\|mp4\|avi"'+ '---- Trying to filter out video files only'

        file = (os.popen('ls '+torrentfolder+'/'+f+' | grep "mkv\|mp4\|avi"').readline())
    	file = file.strip() # trim the file

    	move_files = 'mv -v '+torrentfolder+'/'+f+'/'+file.replace(' ','\ ')+' '+showfolder+'/'+show.replace(' ','\ ')+'/Season\ '+season+'/'
        rm_folders = 'rm -rf '+torrentfolder+'/'+f+'/'
	
        if debug == '1':
            print '------------------------------------------'
            print 'Show: ', show
            print 'Season: ', season
            print 'Episode: ', episode
        
        # for debugging - print the statement instead of executing the comman
        if move == '1' and debug == '1':
            os.system(move_files)	# temp - should always try and move
            os.system(rm_folders)   # remove the parent folder to the show
            print ' '

        elif move == '0' and debug == '1':
            print 'Move command: ', move_files
            print 'Remove command: ',rm_folders
    	#folder = f.replace(' ','\ ')
        
        if debug == '1':
            print '------------------------------------------'
            print '\n'


# Main
if __name__ == "__main__":
    clean_torrents()



# to do #############################
# - if there is a space in the torrent folder name the function to check if there is a video fails
# - create a new var to hold the values of f and folder that are system friendly (have\ after\ each\ space)
