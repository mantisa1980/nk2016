#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import random
from random import shuffle
import json
'''
clean procedure:
1. open with numbers app
2. delete column 5 if all empty
3. save as csv and encoding with utf-8
'''

input_file = "1000.numbers.csv"
clean_file = "{}_clean.csv".format(input_file)
shuffle_file = "{}_shuffle.csv".format(input_file)
json_file = "question.json"

class Option(object):
	def __init__(self,desc,is_answer):
		self.desc = desc
		self.bool_answer = is_answer

	def is_answer(self):
		return self.bool_answer

	def set_answer(self,ans):
		self.bool_answer = ans

class Question(object):
	def __init__(self,title,option_list):
		self.options = option_list
		self.title = title
		self.answer_index = None

		for i in range(0,len(option_list)):
			if option_list[i].is_answer():
				if self.answer_index == None:
					self.answer_index = i
				else:
					raise Exception("Find Multiple answer!title={}".format(title))
		assert(self.answer_index != None)
		self.show()

	def get_options(self):
		ret = []
		for i in self.options:
			ret.append(i.desc)
		return ret

	def show(self):
		print "Title:", self.title, " options:", self.options[0].desc , self.options[1].desc,self.options[2].desc, ", ans idx:", self.answer_index


def clean_data():
	f = io.open(input_file,'r',encoding='utf8')
	w = io.open(clean_file,"w",encoding="utf8")

	buf_subject = dict()
	buf_ans = dict()

	counter = 0
	for i in f:
		i = i.rstrip("\n").rstrip("\r")
		tokens = i.split(",")
		check = True

		if len(tokens) != 4:
			check = False
			#print "token count invalid", len(tokens)
		else:
			for j in tokens:
				if len(j) <=0:
					check = False
					#print "token len invalid"
					break

		if check is True:
			#w.write(i+"\n")
			s = ",".join([tokens[1],tokens[0],tokens[2],tokens[3]])
			print "writing ", s
			w.write(s+"\n")
		else:
			print "skipping counter ", counter, "##", i
			
		counter+=1
		if counter >= 1000:
			break
	f.close()
	w.close()

def generate_shuffle_question_set():
	fstream = io.open(clean_file  ,'r',encoding='utf8')
	wstream = io.open(shuffle_file,"w",encoding="utf8")
	jsonstream = io.open(json_file,"w",encoding="utf8")

	question_set = list()
	for line in fstream:
		line = line.rstrip("\n")
		tokens = line.split(",")
		assert(len(tokens)==4)
		lst = []
		
		title = tokens[0]
		tokens_option = tokens[1:]
		for t in tokens_option:
			lst.append(Option(t,False))

		lst[0].set_answer(True)
		shuffle(lst)
		que = Question(title,lst)
		question_set.append(que)

	counter = 0
	for q in question_set:

		s = ",".join([str(counter), q.title , str(q.answer_index) , ",".join(opt.desc for opt in q.options)]) + "\n"
		#s = q.title + "," + str(q.answer_index) + "," +  ",".join(opt.desc for opt in q.options) + "\n"",".join(opt.desc for opt in q.options)
		wstream.write(s)
		
		doc = {
			"qid": counter, 
			"title": q.title,
			"ans_idx":q.answer_index,
			"options":q.get_options()
		}
		counter +=1
		jsonstream.write( json.dumps(doc) + u"\n")

	jsonstream.close()
	fstream.close()
	wstream.close()


clean_data()
generate_shuffle_question_set()

