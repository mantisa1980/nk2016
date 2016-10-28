#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io

#lst = dict()
f = io.open("utf8_src.csv",'r',encoding='utf8')
w = io.open("output.csv","w",encoding="utf-8")

buf_subject = dict()
buf_ans = dict()

counter = 0
for i in f:
	tokens = i.split(",")
	'''
	print i
	for i in tokens:
		print "token=",i

	print "======="
	'''
	#               subject             answer
	#lst[counter] = [unicode(tokens[1]),unicode(tokens[2])]

	subject = unicode(tokens[1])
	ans = unicode(tokens[2]).rstrip()

	if len(tokens) > 3:
		print "invalid!", i, "ㄝ##tokens=", tokens

	s = ans + u"," + subject +"\n"
	#print "s=", s

	if subject not in buf_subject:
		buf_subject[subject] = subject
		#w.write(s)
	else:
		pass
		#print "repeated ", subject

	
	#counter +=1
	#if counter >= 5:
	#	break

