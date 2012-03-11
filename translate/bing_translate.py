#!/usr/bin/env python
# -*= coding: utf-8 -*-

"""
Translation using Bing API

Copied from http://blog.roodo.com/thinkingmore/archives/10669585.html
"""

import sys
import os
from urllib import urlencode
import urllib2
from urllib2 import Request, urlopen, URLError, HTTPError
import json
#from translate import *

class BingTranslate:
	appid = 'appid'
	base_uri = "http://api.microsofttranslator.com/V1/Http.svc"

	def __read_from_req( self, req ):
		try:
			response = urllib2.urlopen( req )
			result = response.read()
		except HTTPError, e:
			print e.code
			print e.read()
			result=""
		return result

	def detect( self, text ):
		uri="%s/Detect?appId=%s" % ( self.base_uri, self.appid )
		req = urllib2.Request( uri, text, { 'Content-Type':'text/plain'} )
		return self.__read_from_req( req )

	def getLanguageNames( self, locale=None ):
		"""
		Thanks MSDN, I still don't know the value of parameter 'locale'
		Don't pass any parameter to getLanguageNames, or you will get error.
		"""
		uri="%s/GetLanguageNames?appId=%s" % ( self.base_uri, self.appid )
		req = urllib2.Request( uri, locale, { 'Content-Type':'text/plain'} )
		return self.__read_from_req( req ).split( '\n' )

	def getLanguages( self ):
		uri="%s/GetLanguages?appId=%s" % ( self.base_uri, self.appid )
		req = urllib2.Request( uri, None, { 'Content-Type':'text/plain'} )
		return self.__read_from_req( req ).split("\r\n")

	def translate( self, text, fr="en", to="zh-CHT" ):
		uri="%s/Translate?appId=%s&from=%s&to=%s" % ( self.base_uri,
				self.appid, fr, to )
		req = urllib2.Request( uri, text, { 'Content-Type':'text/plain'} )
		return self.__read_from_req( req )

if __name__ == "__main__":
	t = BingTranslate()
	print t.translate( "test" )
	print t.translate( "鬼", "zh-CHT", "en" )
	print t.detect( "中文測試" )
	print t.detect( "中文测试" )
	names = t.getLanguageNames()
	langs = t.getLanguages()
	print "Language Names (total %d):" % len(names)
	for l in names:
		print l
	print "Languages (total %d):" % len(langs)
	for l in langs:
		print l
