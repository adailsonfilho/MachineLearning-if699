from enum import Enum
from decimal import *
from functools import reduce
import math

def conffiance(history):
	mean = Decimal(reduce(lambda x, y: x + y, history)) / Decimal(len(history))
	sumAcc = Decimal(0)
	for h in history:
		sumAcc += (h-mean)**2
	sdev = Decimal(math.sqrt(sumAcc/Decimal(len(history))))
	z = Decimal(1.96) #coeficiente de confiança p ara 95%
	return z*sdev/Decimal(math.sqrt(len(history)))

#Enumerate the var's categories
class FeatureEnum(Enum): #how use that? FeatureEnum['x'] ou FeatureEnum.x
	x = 1
	o = 0
	b = -1

#Enumerate the classes
class ClassEnum(Enum): #how use that? ClassEnum['positive'] ou ClassEnum.positive
	positive = 1
	negative = 0

#Este método poderia ser feito com split(','), mas a performance ia cair um pouco (onde a gente puder ganhar em performance nesse tipo de aplicação é importante)
def pre_process(line, separator):	

	processed = []#irá armazenas os dados convertidos. Ex: "x,x,x,o,o,o,b,b,b,positivo" vira ([1,1,1,0,0,0,-1,-1,-1],1) (de acordo com a classe enum)
	classId = None
	acc = '' #acumulador

	#line += '$'#para servir de referencia do fim do token

	for x in line:
		if x != ',' and x != '\n':
			acc += x
		elif x == '\n':
			classId = ClassEnum[acc].value
		else:
			processed.append(FeatureEnum[acc].value) # salva a categoria comseu identificador de acordo com a classe enum
			acc = ''#reseta
	# print(str(features)+" "+str(classId))
	return (processed,classId)

def dissimilarity(sample_i,sample_j):					#calculate number of differents elements for each given line and column
	result = 0;
	for e1,e2 in zip(sample_i,sample_j):
		if(e1 != e2): result+=1
	return result

