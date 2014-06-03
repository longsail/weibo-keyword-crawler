#!/usr/bin/env/ python
#coding=utf-8
'''
    author: lyuxiao
    created on 2013.11.1
'''
try:
	import sys
	from searchparser_json import *

except ImportError:
        print >> sys.stderr

def store(page):
        f = open('keyword.txt','a')
	tweets = page2tweets(page) ##print tweets[0]
	print len(tweets),'tweets in this page'
	for x in tweets:
            cnt2file = ''
            try:
		mid = midoftweet(x).encode('utf-8')
		uid = uidoftweet(x).encode('utf-8')
	        content = cntnt_tweet(x).encode('utf-8')
		weiboinfo = info(x)
	        n_likes = weiboinfo[1].encode('utf-8')
		n_forwards = weiboinfo[2].encode('utf-8')
	        n_comments = weiboinfo[3].encode('utf-8')
                cnt2file = 'mid:'+mid+' '+'uid:'+uid+' '+'content:'+content+' '+'n_likes:'+n_likes+' '+'n_comments:'+n_comments+' '+'\n'
                f.write(cnt2file)
            except:
                pass
        f.close()

if __name__ == '__main__':
	s = open('strange.html','r').read()
	store(s)
