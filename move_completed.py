#!/usr/bin/python

import os
import sqlite3
import sys
import re
import datetime


filelist = []
shows = []
regex = '[sS]+[0-9]+[eE]+[0-9]+[0-9]'
comp_dir = '/mnt/complete/'
show_dir = '/mnt/shows/'

def main():
	pass

def get_file_names():
	for file in os.listdir(comp_dir):
		if file.endswith(('.mp4','.mkv','.avi')):
			filelist.append(file)


def move_show(filename,show,season):
#	os.system('mv -v '+comp_dir+filename+' '+show_dir+show+'/Season\ '+season+'/') ## Works just commented out for testing


def check_dir(show):
	if os.path.isdir(show_dir+show):
		return True
	else:
		return False


def clean_filename(filename):
	show = filename.replace('.',' ')
	episode_code = re.search(regex,show)
	cut_off = (re.search(regex,show))

	if episode_code:
		cut_off = (re.search(regex,show)).start()-1
		show = show[:cut_off]
		ecode = episode_code.group()
		season = ecode[1:-3]
		episode = ecode[-2:]

		return show,season,episode
	else:
		return 'not found','',''

def new_season(show, season):
	if os.path.isdir(show_dir+show+'/Season '+str(int(season))):
		return 'Dir exist'
	else:
		show = show.replace(' ','\ ')
		os.system('mkdir '+show_dir+show+'/Season\ '+str(int(season)))
		return 'Need to create new dir'+ show+'_'+str(int(season))


def log_actions(filename,show,season,epsiode,action):
	now = datetime.datetime.now()
	db = sqlite3.connect('hydra.db')
	cursor = db.cursor()
	cursor.execute(''' INSERT INTO log_shows(filename,show,season,episode,action,timestamp)
				VALUES(?,?,?,?,?,?)''',(filename, show, season, episode, action, now)) ## episode is currently writting as a null value -- FIX LATER
	db.commit()


def create_season():
	print "Create a new season"

shows = []
move_files= []
seasons = []
episodes = []

main()
get_file_names()

for f in filelist:
	filename = clean_filename(f)
	show, season, episode = clean_filename(f)
	if show != 'not found':
		move_files.append(f)
		shows.append(show)
		seasons.append(season)
		episodes.append(episode)
	if show =='not found' or season == '' or episode == '':
		filelist.remove(f)
		

#	if check_dir(show) == False:
#		filelist.remove(f)
#		print 'mv -v '+f+' '+show_dir+show+'/Season\ '+season +'-----'
#	else:
#		print '_'+ show
	

files = len(move_files)

for n in range(0,files):
	temp_show = shows[n]
	temp_show = temp_show.replace(' ','\ ')

	log_actions(move_files[n],temp_show,str(seasons[n]),str(episodes[n]),'mv '+show_dir+temp_show+'/Season\ '+str(int(seasons[n])))
#	print new_season(shows[n],seasons[n])+'---'+ show_dir+temp_show+'/Season\ '+str(int(seasons[n]))+'---'+move_files[n]+' EPSIODE: '+episodes[n]
	
	move_show(move_files[n],temp_show,str(int(seasons[n])))

#test
#test test
