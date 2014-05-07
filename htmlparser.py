#!/usr/bin/env python
#coding=utf-8

'''

@author: lyuxiao
created on 2013.12.22

'''
import os
import time
import sys
from StringIO import StringIO
import re

import json

try:
	from lxml import etree
except ImportError:
        print >> sys.stderr



def page2tweets(searchpage):

	searchpage = searchpage.replace(r'\n|\x..','')

	parser = etree.HTMLParser()
	tree = etree.fromstring(searchpage,parser)

	scripts = tree.xpath(u'//*/script//text()')#right

	for script in scripts:
		if r'pid":"pl_wb_feedlist",' in script:
			
# 			print script
			pagecontent = script.replace(r'STK && STK.pageletM && STK.pageletM.view(','')
			#print pagecontent[0:50]
			#print pagecontent[-20:-1]

			tweet_dic = json.loads(pagecontent[:-1])
			#print tweet_dic['html']
			parser = etree.HTMLParser()
			htmltree = etree.fromstring(tweet_dic['html'],parser)
			tweets = htmltree.xpath(u"//*/dl[@class='feed_list W_linecolor ']")
			return tweets


	return []

def midoftweet(tweet):

	if len(tweet.attrib['mid']):
		return tweet.attrib['mid']

def uidoftweet(tweet):

	img = tweet.xpath('./dt/a/*')
	if len(img) and img[0].attrib.has_key('usercard'):
		usercard = img[0].attrib['usercard']
		uid = re.findall('\d+',usercard)
		if len(uid):
			return uid[0]

def cntnt_tweet(tweet):

	try:
		c = tweet.xpath('./dd/p/em//text()')
	except:
		return None

	content = ' '.join(c)
	return content


def weibois_forward(tweet):

	if tweet.attrib.has_key('isforward'):
		return bool(tweet.attrib['isforward'])
	else :
		return False

def ref_forward(tweet):

	r = tweet.xpath('./dd/dl/dd/a')
	if len(r) and r[0].attrib.has_key('href'):
		ref = r[0].attrib['href']
		return ref


def cntnt_forward(tweet):

	try:
		c = tweet.xpath('./dd/dl/dt/em//text()')
	except:
		return None
	content = ' '.join(c)
	return content

#-------------------------------------------------------
# weibo info [time , n_like, n_forword, n_comment ]
def info(tweet):

	info = []

	t = tweet.xpath('./dd/p/a[@class="date"]')
	if len(t) and t[0].attrib.has_key('title'):
		time = t[0].attrib['title']
	else:
		time = None

	n_l = tweet.xpath('./dd/p/span/a[@action-type="feed_list_like"]//text()')
	if len(n_l) > 1:
		x = re.findall('\d+',n_l[1])
		if len(x):
			n_like = x[0]
		else:
			n_like = 0
	else:
		n_like = 0


	n_f = tweet.xpath('./dd/p/span/a[@action-type="feed_list_forward"]//text()')
	if len(n_f) :
		x = re.findall('\d+',n_f[0])
		if len(x):
			n_forward= x[0]
		else:
			n_forward = 0
	else:
		n_forward = 0

	n_c = tweet.xpath('./dd/p/span/a[@action-type="feed_list_comment"]//text()')
	if len(n_c) :
		x = re.findall('\d+',n_c[0])
		if len(x):
			n_comment = x[0]
		else:
			n_comment = 0
	else:
		n_comment = 0


	info = [time, n_like, n_forward, n_comment]
	return info

if __name__ == '__main__':

	testpage = open('test.html','r')
	tweets = page2tweets(testpage.read())
	print len(tweets),'tweets in test page'

	raw_input("check now")
	for tweet in tweets:
		print 'mid:',midoftweet(tweet)
		print 'uid:',uidoftweet(tweet)
		print 'content:',cntnt_tweet(tweet)
		print info(tweet)
		raw_input()

		is_f = weibois_forward(tweet)
		print 'isforward:',is_f

		if is_f:
			print ref_forward(tweet)
			print cntnt_forward(tweet)
