import os
from enum import Enum

#limpa tela
clear = lambda: os.system('cls') #to clear screen during use of console in windows

#Enumera as variaveis categóricas
class FeatureEnum(Enum): #how use that shit? Categories['x']
	x = 1
	o = 0
	b = -1

#enumera as classes
class ClassEnum(Enum): #how use that shit? Class['positive']
	positive = 1
	negative = 0

class Bayes():
	def __init__(self):
		self.data = []

	def preProcess(self, line, separator):
		#Adailson: Este método poderia ser feito com split(','), mas a performance ia cair um pouco (onde a gente puder ganhar em performance nesse tipo de aplicação é importante)

		features = []#ira armazenas os dados convertidos. Ex: "x,x,x,o,o,o,b,b,b" vira [1,1,1,0,0,0,-1,-1,-1] (de acordo com a classe enum)
		classId = None
		acc = '' #acumulador

		# line += ','#para servir de referencia do fim do token

		print(line)
		for x in line:
			if x != ',':
				acc += x
			elif x == '\n':
				classId = ClassEnum[acc]
			else:
				features.append(FeatureEnum[acc]) # salva a categoria comseu identificador de acordo com a classe enum
				acc = ''#reseta
		

		return (features,classId)

	def readData(self, path):
		with open(path) as f:
			for line in f:
				processedLine = self.preProcess(line,',')
				self.data.append(processedLine)


	def priori(self, classId):
		pass

	def posteriori(self,classId,features):
		pass

	def runForestRun(self):
		self.readData('../tic-tac-toe.data')

if __name__ == "__main__":

	bayes = Bayes() #Cria instancia da casse Bayes
	bayes.runForestRun()