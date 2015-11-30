import os
import random
import math
import numpy as np
from enum import Enum
from decimal import *
from random import randint
import ipdb 						#iterator debuger =D

clear = lambda: os.system('cls')	#clear screen on windows
getcontext().prec += 30 			#augment Decimal values precision
track_steps = True

##################
# PRE-PROCESSING #
##################

class FeatureEnum(Enum): #how use that shit? Categories['x']
	x = 1
	o = 0
	b = -1

###################
# BASIC STRUCTURE #
###################

data = [] 							#stores all the data input as list of char
dis_matrix = []						#Dissimilarity matrix
G = []								#Prototypes sets
C = []								#Fuzzy Clusters

##################
### PARAMETERS ###
##################

k = 2							#number of clusters
q = 2							#size of prototypes sets
T = 150							#Maximo de iterações
m = 2							#level of cluster fuzziness
treshold = Decimal(10)**-10		#treshold de otimização

##################
#### METHODS #####
##################

def pre_process(line, separator = ','):
		return [FeatureEnum[item].value for item in line.split(separator)[0:-1]]

def read_data(path):								#read data from file
	with open(path) as f:
		for line in f:
			sample = pre_process(line)
			if random.random() > 0.5:				#shufle the samples read into the "data" var
				data.insert(0,{'features':sample,'membership':[],'jk':None})
			else:
				data.append({'features':sample,'membership':[],'jk':None})

def dissimilarity(sample_i,sample_j):					#calculate number of differents elements for each given line and column
	result = 0;
	for e1,e2 in zip(sample_i,sample_j):
		if(e1 != e2): result+=1
	return result

def debug(str):
	if _debug == True:
		print(str)

def exists(elem, list_of_lists):
	for l in list_of_lists:
		if elem in l:
			return True
	return False

def d(e1,e2): #USAR MATRIZZ DE DISSIMILARIDADE
	e1 = np.array(e1)
	e2 = np.array(e2)
	return Decimal(np.linalg.norm(e1-e2))

def D(e_i,prototypes):
	return sum([d(e_i,e) for g_k in prototypes for e in g_k])

def u(e_i,k):
	exp = Decimal(1)/Decimal(m-1)
	uik = sum([(Decimal(D(e_i,G[k]))/ Decimal(D(e_i,g_h))) for g_h in G])
	uik = (uik**exp)**-1
	return uik

def J(h):
	jk = []
	for sample in data:
		metric = (sample['membership'][h]**m)*D(sample['features'],G[h])
		jk.append(metric)
		sample['jk'] = metric
	min_data = sorted(data, key=lambda x:x['jk'], reverse=True)
	G[h] = [e['features'] for e in min_data[0:2]]
	return sum(jk)

def track(msg):
	if track_steps:
		print(msg)

##################
## MAIN METHOD ###
##################

if __name__ == '__main__':

	read_data('../tic-tac-toe.data')						#read file into "data"
	
	track("Dissimilarity matrix")													#dissimilarity matrix
	for sample_i in data:									#for each data
		line = []
		for sample_j in data: 								#compare to the others
			line.append(dissimilarity(sample_i['features'],sample_j['features']))
		dis_matrix.append(line) 							#add all comparations of sample_i with others samples in dissimilarity matrix

	track('Sorting prototypes')
	for i in range(k):										#for each cluster 
		random_prototype = []
		for j in range(q):
			r_index = random.randint(0,len(data))						#sort q samples for each clustar prototype
			if not exists(data[r_index]['features'],G):								#Warrant different elements in both Prototype sets, inclusive simultaneously
				print('INSERTED')
				random_prototype.append(data[r_index]['features'])
		G.append(random_prototype)

	previus_j = 0
	t = 0

	while True:													#EMUATE DO-WHILE, WTF PYTHON?

		track('Calculate membership')									#Calculate membership degree
		for e_i in data:
			for h in range(k):
				e_i['membership'].append(u(e_i['features'],h))

		track('> Iteration: '+str(t))
		current_j = Decimal(0)
		for h in range(k):
			current_j += J(h)
		track(' J: '+str(current_j))

		track("Prototypes")
		track(str(G))


		t+= 1
		if (t < T) and (math.fabs(current_j-previus_j) < treshold):
			break
		else:
			previus_j = current_j