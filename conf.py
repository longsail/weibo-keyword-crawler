#!/usr/bin/env/ python
#coding=utf-8
'''
    @author zouyh
    Created on 2014.05.10
'''
import os
import sys
try:
	import yaml
except ImportError:
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

USERNAME_1 = conf_dic['login'][0]['username_1']
PASSWORD_1 = conf_dic['login'][0]['password_1']

USERNAME_2 = conf_dic['login'][1]['username_2']
PASSWORD_2 = conf_dic['login'][1]['password_2']

USERNAME_3 = conf_dic['login'][2]['username_3']
PASSWORD_3 = conf_dic['login'][2]['password_3']

USERNAME_4 = conf_dic['login'][3]['username_4']
PASSWORD_4 = conf_dic['login'][3]['password_4']


COOKIE_FILE = conf_dic['cookie_file']

if __name__ == '__main__':
	print USERNAME_1,PASSWORD_1
	print USERNAME_2,PASSWORD_2
	print USERNAME_3,PASSWORD_3
	print USERNAME_4,PASSWORD_4
	print COOKIE_FILE
