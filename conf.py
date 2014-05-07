# -*- coding: utf-8 -*-
'''
	weibosearch db configuration
	
	Modified by lyuxiao
	on 2013.11.1


    @author Jiajun Huang
    Created on 2013/10/17
'''
import os
import sys
try:
	import yaml
except ImportError:
	print 'importerror'
        print >> sys.stderr
	sys.exit()

try:
	conf_file = open("weibosearch.yaml", 'r')
	conf_dic = yaml.load(conf_file)
except IOError:
	print 'No such file or directory','weibosearch.yaml'
	pass
finally:
	conf_file.close()

DBNAME = conf_dic['searchdb']['dbname']
DBHOST = conf_dic['searchdb']['host']
DBPORT = conf_dic['searchdb']['port']

BOOL_GETCOMMENTS = conf_dic['searchdb']['BOOL_getcomments']

USERNAME_1 = conf_dic['login'][0]['username_1']
PASSWORD_1 = conf_dic['login'][0]['password_1']

USERNAME_2 = conf_dic['login'][1]['username_2']
PASSWORD_2 = conf_dic['login'][1]['password_2']

USERNAME_3 = conf_dic['login'][2]['username_3']
PASSWORD_3 = conf_dic['login'][2]['password_3']

USERNAME_4 = conf_dic['login'][3]['username_4']
PASSWORD_4 = conf_dic['login'][3]['password_4']

#USERNAME_5 = conf_dic['login'][4]['username_5']
#PASSWORD_5 = conf_dic['login'][4]['password_5']

#USERNAME_6 = conf_dic['login'][5]['username_6']
#PASSWORD_6 = conf_dic['login'][5]['password_6']

#USERNAME_7 = conf_dic['login'][6]['username_7']
#PASSWORD_7 = conf_dic['login'][6]['password_7']

#USERNAME_8 = conf_dic['login'][7]['username_8']
#PASSWORD_8 = conf_dic['login'][7]['password_8']


COOKIE_FILE = conf_dic['cookie_file']
LOGDB = conf_dic['logdb']['dbname']
LOGHOST = conf_dic['logdb']['host']
LOGUSER = conf_dic['logdb']['user']
LOGPW = conf_dic['logdb']['password']


if __name__ == '__main__':
	print DBNAME, DBHOST, DBPORT
	print USERNAME_1,PASSWORD_1
	print USERNAME_2,PASSWORD_2
	print USERNAME_3,PASSWORD_3
	print USERNAME_4,PASSWORD_4
	#print USERNAME_5,PASSWORD_5
	#print USERNAME_6,PASSWORD_6
	#print USERNAME_7,PASSWORD_7
	#print USERNAME_8,PASSWORD_8
	print COOKIE_FILE
	print LOGDB, LOGHOST, LOGUSER, LOGPW
