#!/usr/bin/env python

# coding=utf-8

import re
import math

def getwords(doc):
	splitter=re.compile('\\W*')
	print doc
	words=[s.lower() for s in splitter.split(doc)
		if len(s) > 2 and len(s) < 20]
	return dict([(w,1) for w in words])

class classifier:
	def __init__(self,getfeatures,filename=None):
		self.fc={}
		self.cc={}
		self.getfeatures=getfeatures
	
	def incf(self,f,cat):
		self.fc.setdefault(f,{})
		self.fc[cat]
		pass

	def fcount(self,f,cat):
		pass
		
	def incc(self, cat):
		pass

	def catcount(self,cat):
		pass

	def totalcount(self):
		pass
	
	def train(self,item, cat):
		pass

	def fprob(self,f,cat):
		pass

	def weightedprob(self,f,cat,weight=1.0,ap=0.5)
		pass

		










