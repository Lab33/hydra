import sys
import os
import commands
import pymssql

# set to 1 for debug mode
debug =1

# Get user info
who = (os.popen('whoami').readline())
who = who.strip()
node = ''

if debug == 1:
    who = 'ariel'

def get_node_info(username):
    os.system('clear')
    print 'Welcome to HYDRA ', username

    # connection string
    conn = pymssql.connect(host=' ', user=' ', password=' ', database=' ') # this needs to come from a config fie
    cur = conn.cursor()
    # get the users home node
    cur.execute('Select HomeNode from Users where username=%s', username)
    row = cur.fetchone()
    while row:
	node = (row[0])
        print "HomeNode:" , node
        row = cur.fetchone()
    conn.commit()

    # get the number of shows both active and listed as contiuning from sickrage
    cur.callproc('sp_ActiveShows',(username,))
    for row in cur:
        print (row[0]),' actively synced shows for ', node

    conn.close()
    main_menu('n')

def main_menu(clear):
    menu = 'main'
    if clear == 'y':    
        os.system('clear')

    print '\n'
    print '1. Shows'
    print '2. Movies'
    print '0. Quit'
    input = raw_input(' >> ')
    exec_menu(input,menu)


def shows():
#    os.system('clear')
    menu = 'shows'
    print '1. List Available Shows'
    print '2. List shows on ', node
    print '3. Add'
    print '4. Remove'
    print '4. Request'
    input = raw_input(' >> ')
    exec_menu(input,menu)


def movies():
    menu = 'movies'
    print '1. List Available Shows'
    print '2. List movies on %s node',node
    print '2. Search'
    print '3. Transfer'
    input = raw_input(' >> ')
    exec_menu(input,menu)


# process the usrs input
def exec_menu(input, menu):
    if menu == 'main' and input == '1':
        shows()
    if menu == 'main' and input == '2':
	movies()
    if menu == 'shows' and input == '1':
	list_hydra_shows()
    if menu == 'shows' and input == '2':
        list_user_shows(menu)
    if menu =='shows' and input == '3':
        add_show(menu)

# List user shows
def list_user_shows(menu):
    print 'Here is a list of shows on your profile'
    input = raw_input(' >> ')
    exec_menu(input,menu)

# List HYDRA shows
def list_hydra_shows():
    # connection string
    conn = pymssql.connect(host='thanos', user='web', password='fr0zenfish!', database='hydra') # this needs to come from a config file
    cur = conn.cursor()
    # get the number of shows both active and listed as contiuning from sickrage
    cur.callproc('sp_ShowList',(who,))
    print '|ID	| Show	        	|'
    print '|----|-----------------------|' # need to build a function to build a "table"
    for row in cur:
	print('|%d  | %s      |' % (row[0], row[1]))
        print '|----|-----------------------|'

    conn.close()

# Add a show to the users node
def add_show(menu):
    input = raw_input('Please enter the name of the show: ')
    print ('you have entered, '), show
    

# Main
if __name__ == "__main__":
    get_node_info(who)
