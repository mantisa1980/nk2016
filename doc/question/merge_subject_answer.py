#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io

#lst = dict()
f1 = io.open("subject.csv",'r',encoding='utf8')
f2 = io.open("answer.csv",'r',encoding='utf8')
w = io.open("output.csv","w",encoding="utf-8")

buf_subject = dict()
buf_ans = dict()

counter = 0
for i in f1:
	
	'''
	print i
	for i in tokens:
		print "token=",i

	print "======="
	'''
	#               subject             answer
	#lst[counter] = [unicode(tokens[1]),unicode(tokens[2])]
	subject = unicode(i).rstrip().replace(",", u"，")
	ans = unicode(f2.readline()).rstrip().replace(",", u"，")
	s = ans +"," + subject + "\n"

	if subject not in buf_subject:
		buf_subject[subject] = subject
		w.write(s)
	else:
		print "repeated ", subject

	
	#counter +=1
	#if counter >= 5:
	#	break

