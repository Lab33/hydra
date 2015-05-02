import ConfigParser
import os
import pymssql
import sqlite3
import re


#########################################################
####### TO DO
# - if the folder has a space the process will fail
# - replace('.',' ') doesnt work with Marvel, going to have to add a special rule
# - if the file begins with the release group then it stays in the show name .. look for [] ?


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
hostname = ConfigSectionMap("Database")['host']
username = ConfigSectionMap("Database")['user']
password_ = ConfigSectionMap("Database")['pass']
db = ConfigSectionMap("Database")['db']
debug = ConfigSectionMap("General")['debug']
move = ConfigSectionMap("General")['move']
server_name = ConfigSectionMap("NAS")['servername']
torrentfolder = ConfigSectionMap("NAS")['torrentfolder']
showfolder = ConfigSectionMap("NAS")['showfolder']

if debug == '1':
    print '################ DEBUG  ######################'
    print 'Provider: ',provider
    print 'Host: ', hostname
    print 'User: ', username
    print 'Password: ', password_
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

def check_dir(testshow):
    testshow = testshow.replace(' ','\ ')
    show_there=os.path.exists(showfolder+'/'+testshow)

    return show_there


def log_sql(t_file,t_loc,action,details):
    if provider == 'MSSQL':
        # connection string
        conn = pymssql.connect(host=hostname, user=username, password=password_, database=db)
        cur = conn.cursor()
        sqlCMD = 'exec sp_log_torrentmoves_Insert @t_file=%s,@t_loc=%s,@action=%s,@details=%s'

        if debug == '1':
            print 'writing to db....', sqlCMD

        cur.execute(sqlCMD,(t_file,t_loc,action,details,))
        conn.commit()
        conn.close()

def clean_filename(filename):
        show = filename.replace('.',' ')
        episode_code = re.search(regex,show)

        if episode_code:
                cut_off = (re.search(regex,show)).start()-1
                clean_show = show[:cut_off]
                ecode = episode_code.group()
                clean_season = ecode[1:-3]
                clean_episode = ecode[-2:]

                return clean_show,clean_season,clean_episode
        else:
                return 'not found','',''



def move_file(t_folder,t_file, show, season):
    	t_file = t_file.strip() # trim the file
    	move_files = 'mv -v '+torrentfolder+'/'+t_folder+'/'+t_file.replace(' ','\ ')+' '+showfolder+'/'+show.replace(' ','\ ')+'/Season\ '+season+'/'
        rm_folders = 'rm -rf '+torrentfolder+'/'+t_folder+'/'

        # remove
        # for debugging - print the statement instead of executing the command
        if move == '1' and debug == '1':
            log_sql(t_file,t_folder,'MOVE','GOOD TO GO')
            os.system(move_files)

            log_sql(t_file,t_folder,'DELETE','GOOD TO GO')
            os.system(rm_folders)   # remove the parent folder to the show

            print ' '

        elif move == '0' and debug == '1':
            log_sql(t_file,t_folder,'MOVE','GOOD TO GO')
            print 'Move command: ', move_files

            log_sql(t_file,t_folder,'DELETE','GOOD TO GO')
            print 'Remove command: ',rm_folders


def clean_torrents():
    for file in os.listdir(torrentfolder):
        filelist.append(file)
 
    for f in filelist:
        clean_filename(f)
        show, season,episode = clean_filename(f)

        if show == 'not found':
            continue

    	if season[:1] == '0':
            season = season[-1] # removes the leading zero from the season number

        if debug == '1':
            print '------------------------------------------'
            print 'Show: ', show
            print 'Season: ', season
            print 'Episode: ', episode


        if check_dir(show) is False:
            print 'CREATE DIR!!!!!!!!!!!!!!!!!!!!!!!!!!!'


        if debug == '1':
            print('ls '+showfolder+'/ | grep "'+show+'"')
        else:
            os.system('ls '+torrentfolder+' | grep "'+show+'"')

        if debug == '1':
            f = f.replace(' ','\ ')
            print 'ls '+torrentfolder+'/'+f+' | grep "mkv\|mp4\|avi"'

        try:
            t_file = (os.popen('ls '+torrentfolder+'/'+f+' | grep "mkv\|mp4\|avi"').readline())
            #sbreak
        except ValueError:
            print 'error...'
            break

        move_file(f,t_file,show,season)


        if debug == '1':
            print '------------------------------------------'
            print '\n'


# Main
if __name__ == "__main__":
    clean_torrents()
