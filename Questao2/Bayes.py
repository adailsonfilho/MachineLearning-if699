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
		self.totalPositive = 0
		self.totalNegative = 0
		self.data = []

	def preProcess(self, line, separator):
		#Adailson: Este método poderia ser feito com split(','), mas a performance ia cair um pouco (onde a gente puder ganhar em performance nesse tipo de aplicação é importante)

		features = []#ira armazenas os dados convertidos. Ex: "x,x,x,o,o,o,b,b,b,positivo" vira ([1,1,1,0,0,0,-1,-1,-1],1) (de acordo com a classe enum)
		classId = None
		acc = '' #acumulador

		#line += '$'#para servir de referencia do fim do token

		print(line)
		for x in line:
			if x != ',' and x != '\n':
				acc += x
			elif x == '\n':
				classId = ClassEnum[acc].value
				if acc == ClassEnum.negative.name:
					self.totalNegative +=1
				elif acc == ClassEnum.positive.name:
					self.totalPositive +=1
			else:
				features.append(FeatureEnum[acc].value) # salva a categoria comseu identificador de acordo com a classe enum
				acc = ''#reseta
		print(str(features)+" "+str(classId))
		return (features,classId)

	def readData(self, path):
		with open(path) as f:
			for line in f:
				processedLine = self.preProcess(line,separator=',')
				self.data.append(processedLine)


	def priori(self, classId):
		if classId == ClassEnum.negative:
			return self.totalNegative/(self.totalNegative+self.totalPositive)
		elif classId == ClassEnum.positive:
			return self.totalPositive/(self.totalNegative+self.totalPositive)

	def posteriori(self, classId, features):
		pass

	def conditionalDensity(self, features, classId):
		pass

	#probabilidade condicional  pij = P(xi = 1|ωj ) -> 'x'
	def pij(xi, classId):
		pass

	#probabilidade condicional  qij = P(xi = 0|ωj ) -> 'o'
	def qij(xi, classId):
		pass

	#probabilidade condicional  qij = P(xi = -1|ωj ) -> 'b'
	def rij(xi, classId):
		pass

	def runForestRun(self):
		self.readData('../tic-tac-toe.data')

if __name__ == "__main__":

	bayes = Bayes() #Cria instancia da casse Bayes
	bayes.runForestRun()
	print(bayes.totalPositive)
	print(bayes.totalNegative)
	print(str(bayes.totalNegative+bayes.totalPositive))