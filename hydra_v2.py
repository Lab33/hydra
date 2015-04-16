import os
import _mssql



# Get user info
who = (os.popen('whoami').readline())



##### SQL TEMP!!!!

conn = _mssql.connect(server='thanos', user='web', password='',database='hydra') # password needs to come from config file


numemployees = conn.execute_scalar("SELECT COUNT(*) FROM vw_tv_shows")
#numemployees = conn.execute_scalar("SELECT COUNT(*) FROM vw_tv_shows WHERE show_name LIKE 'J%'")    # note that '%' is not a special character here
employeedata = conn.execute_row("SELECT * FROM vw_tv_shows WHERE show_id=%d", 13)



print numemployees





def main_menu():
    os.system('clear')
    menu = 'main'

    print 'Hello, ', who
    print '1. Shows'
    print '2. Movies'
    print '0. Quit'

    input = raw_input(' >> ')
    exec_menu(input,menu)

def movies():
    os.system('clear')
    menu = 'movies'
    print '1. Search'
    print '2. Transfer'
    print '3. Request'
    print ''
    print '9. back'
    print '0. quit'

    input = raw_input(' >> ')
    exec_menu(input,menu)

def shows():
    os.system('clear')
    menu = 'shows'
    print '1. List'
    print '2. Add'
    print '3. Remove'
    print '4. Request'
    print ''
    print '9. back'
    print '0. quit'

    input = raw_input(' >> ')
    exec_menu(input,menu)

def exec_menu(input, menu):

    if menu == 'main' and input == '1':
        shows()
    if menu == 'main' and input == '2':
        movies()
    if menu == 'shows' and input == '1':
        list_user_shows(menu)
    if menu =='shows' and input == '2':
        add_show(menu)

# List user shows
def list_user_shows(menu):
    print 'Here is a list of shows on your profile'
    input = raw_input(' >> ')
    exec_menu(input,menu)


# Add a show to the users node
def add_show(menu):
    show = raw_input('Please enter the name of the show: ')
    print ('you have entered, '), show
    
# Main
if __name__ == "__main__":
    main_menu()