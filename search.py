#!/usr/bin/env python 
#coding=utf-8
'''

@author: zouyh
Created on 2014.05.10

a detailed explaination is here:http://www.mzwu.com/article.asp?id=3485
	
'''
import sys
import os,errno
import time
import urllib
import urllib2
import re
import gzip
import random
from StringIO import StringIO
try:
	from login import login
	from conf import USERNAME_1,PASSWORD_1,USERNAME_2,PASSWORD_2,USERNAME_3,PASSWORD_3,USERNAME_4,PASSWORD_4
	from conf import COOKIE_FILE
	from htmlparser import *
except ImportError:
        print >> sys.stderr
        sys.exit()

DEFAULT_SLEEPING_TIME = 100
ATTEMPT_TIME = 5

COOKIE_OUTOFDATE_ERROR = r'http://weibo.com/sso/login.php?ssosavestate'
VERIFICATION_ERROR = r'\u4f60\u7684\u884c\u4e3a\u6709\u4e9b\u5f02\u5e38\uff0c\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801\uff1a' #请输入验证码 
HTTP_HEADERS= {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}

class CrawlKeyword(object):
	
	def __init__(self, keyword):
		self.keyword = keyword
	

	def realtime_search(self,year_s,month_s,day_s,hour_s, year_end,month_end,day_end,hour_end):
		for year in range(year_s, year_end+1):
			for month in range(month_s, month_end+1):
				for day in range(day_s,day_end+1):
					hour_end = hour_end+1 if day == day_end else 24
                                        hour_s = hour_s if day == day_s else 0
					for hour in range(hour_s,hour_end):
						self.realtime_search1hour(year,month,day,hour)

	def search(self):
		self.realtime_search1hour()

	def realtime_search1hour(self,year='',month='',day='',hour=''):
		import timeit
		start = timeit.default_timer()

		year = str(year)
		month = str(month)
		day = str(day)
		hour = str(hour)
		timescope = year+'-'+month+'-'+day+'-'+hour if year and month and day and hour else ''
		print timescope

		if not self._login():
			attempts = 0
			while not self.relogin() and attempts < 5:
				time.sleep(10)
				attempts += 1
		else:
			page_range = self._get_pageNum(self._get_url(1,timescope,timescope))
			print 'available pages are ',page_range
                        if page_range < 5:
                            time.sleep(20)
			page = 1
			page_range += 1
			number = 0
			for page in range(page+1,page_range):
				end = timeit.default_timer()
				if (end-start)%3600 == 0:
					searched_page = self._get_page_again(self._get_url(page,timescope,timescope))
				else:
					searched_page = self._get_page(self._get_url(page,timescope,timescope))
				self.store(searched_page)
				
				if page%5 == 0:
					sleeping_time = random.uniform(DEFAULT_SLEEPING_TIME-20,DEFAULT_SLEEPING_TIME+20)
					print 'sleeping_time',sleeping_time
					time.sleep(sleeping_time)

					number += 1
					if number%4==0:
						if self.relogin(username=USERNAME_1,password=PASSWORD_1):
							print '1'
					elif number%4==1:
						if self.relogin(username=USERNAME_2,password=PASSWORD_2):
							print '2'
					elif number%4==2:
						if self.relogin(username=USERNAME_3,password=PASSWORD_3):
							print '3'
					else:
						if self.relogin(username=USERNAME_4,password=PASSWORD_4):
							print '4'

				page = page + 1

	def _get_pageNum(self,firstpage_url):
		
		firstpage = self._get_page(firstpage_url)
		print firstpage_url
		if not firstpage:
			print 'firstpage',firstpage
			firstpage = self._get_page_again(firstpage_url)

		if firstpage:
			if VERIFICATION_ERROR in firstpage:
				print 'VERIFICATION_ERROR',firstpage_url
				firstpage = self._get_page_again(firstpage_url)
				if not firstpage:
					time.sleep(3600)
			if COOKIE_OUTOFDATE_ERROR in firstpage:
				print 'COOKIE_OUTOFDATE_ERROR',firstpage_url
				firstpage = self._get_page_again(firstpage_url)
		
		page_number = 0
		if not firstpage:
			return page_number

		else:
			self.store(firstpage)
			page_numberList = re.findall(r'(?<=&page=)\d+',firstpage)
			page_number = int(page_numberList[-2]) if page_numberList else 0
		return page_number

	def _login(self):
		return login(USERNAME_1,PASSWORD_1,COOKIE_FILE)
	
	def _get_url(self,page,time_start='',time_end='',nodup=False):

		encoding_keyword = urllib.quote(self.keyword)
		url_part1 = 'http://s.weibo.com/wb/'+encoding_keyword+'&xsort=time'
		url_part2 = '&timescope=custom:'+time_start+':'+time_end if time_start and time_end else ''
		url_part3 = '&nodup=1&page='if nodup else '&page='
		url_part4 = str(page)
		return url_part1 + url_part2 + url_part3 + url_part4

	def _get_page_again(self,searching_url):

		self.relogin()
		time.sleep(5)
		searched_page = self._get_page(searching_url)
		return searched_page

	def _get_page(self,searching_url):
		print 'searching_url',searching_url
		search_request = urllib2.Request(url=searching_url,headers=HTTP_HEADERS)
		search_request.add_header('Accept-encoding','gzip')
		web_page = None
		try:
			web_page = urllib2.urlopen(search_request)
		except:
			print 'URLError',searching_url
			pass

		searched_page = web_page.read() if web_page else None
		if searched_page:
			print len(searched_page)

		if searched_page and web_page.info().get('Content-Encoding') == 'gzip':
			buffer_file = StringIO(searched_page)
			f = gzip.GzipFile(fileobj=buffer_file)
			searched_page = f.read()
		return searched_page
	
	def store(self,page,spe_chr=chr(29)):
		if '\u62b1\u6b49\uff0c\u672a\u627e\u5230\u201c' not in page:
			tweets = page2tweets(page) ##print tweets[0]
			print len(tweets),'tweets in this page'
			f = open(self.keyword,'a')
			for x in tweets:
				string2file = ''
				try:
					mid = midoftweet(x)
					uid = uidoftweet(x)
                                        content = cntnt_tweet(x).encode('utf-8')
                                        weiboinfo = info(x)
					n_likes = str(weiboinfo[1])
					n_forwards = str(weiboinfo[2])
					n_comments = str(weiboinfo[3])
                                        string2file = spe_chr.join([mid,uid,content,n_likes,n_forwards,n_comments])
                                        #string2file = 'mid:'+mid+' uid:'+uid+' content:'+content+' n_forwards:'+n_forwards+' n_comments:'+n_comments
				        f.write(string2file+'\n')
				except:
					pass
			f.close()
	def relogin(self,username=USERNAME_4,password=PASSWORD_4):
		self.remove_cookie()
		return login(username,password,COOKIE_FILE)

	def remove_cookie(self,cookie_file=COOKIE_FILE):
		
		try:
			os.remove(cookie_file)
		except OSError as e:
			if e.errno != errno.ENOENT:
				pass
def main():
	result = CrawlKeyword("奥迪")
	result.realtime_search(2014,5,1,0,2014,5,7,10)

if __name__ == '__main__':
	main() 
	
