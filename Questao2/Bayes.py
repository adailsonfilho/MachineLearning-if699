import os
from enum import Enum
from decimal import Decimal

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
		self.dataPositive = []
		self.dataNegative = []

	def preProcess(self, line, separator):
		#Adailson: Este método poderia ser feito com split(','), mas a performance ia cair um pouco (onde a gente puder ganhar em performance nesse tipo de aplicação é importante)

		features = []#ira armazenas os dados convertidos. Ex: "x,x,x,o,o,o,b,b,b,positivo" vira ([1,1,1,0,0,0,-1,-1,-1],1) (de acordo com a classe enum)
		classId = None
		acc = '' #acumulador

		#line += '$'#para servir de referencia do fim do token

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
					raise ValueError('Ops! Some class name is not correct in the data input.')
			else:
				features.append(FeatureEnum[acc].value) # salva a categoria comseu identificador de acordo com a classe enum
				acc = ''#reseta
		print(str(features)+" "+str(classId))
		return (features,classId)

	def readData(self, path):
		with open(path) as f:
			for line in f:
				processedLine = self.preProcess(line,separator=',')
				if processedLine[1] == ClassEnum.positive.value:
					self.dataPositive.append(processedLine)
				elif processedLine[1] == ClassEnum.negative.value:
					self.dataNegative.append(processedLine)


	def priori(self, classId):
		if classId == ClassEnum.negative.value:
			return self.totalNegative/(self.totalNegative+self.totalPositive)
		elif classId == ClassEnum.positive.value:
			return self.totalPositive/(self.totalNegative+self.totalPositive)

	def posteriori(self, classId, features):
		pass

	def conditionalDensity(self, features, classId):
		dataSource = None
		if classId == ClassEnum.negative.value:
			dataSource = self.dataNegative
		elif classId == ClassEnum.positive.value:
			dataSource = self.dataPositive

		#TODO(Adailson): CALCULAR PRODUTÓRIO AQUI! (acho que é possivel otimizar os laços calculando pij,qij e rij em um unico laço visto que o j é igual para ambos toda vez que este produtorio rodar um laço)

	#probabilidade condicional  pij = P(xi = 1|ωj ) -> 'x'

	def pij(i, classId):
		dataSource = None
		if classId == ClassEnum.negative.value:
			dataSource = self.dataNegative
		elif classId == ClassEnum.positive.value:
			dataSource = self.dataPositive

		sumAcc = Decimal(0) #acumulador de soma
		for example in self.dataSource:
			xi = example[0][i]
			sumAcc += Decimal(xi*(xi+1))/Decimal(2)

		return sumAcc

	#probabilidade condicional  qij = P(xi = 0|ωj ) -> 'o'
	def qij(xi, classId):
		dataSource = None
		if classId == ClassEnum.negative.value:
			dataSource = self.dataNegative
		elif classId == ClassEnum.positive.value:
			dataSource = self.dataPositive

		sumAcc = Decimal(0) #acumulador de soma
		for example in self.dataSource:
			xi = example[0][i]
			sumAcc += Decimal(1-xi**2)
			
		return sumAcc

	#probabilidade condicional  qij = P(xi = -1|ωj ) -> 'b'
	def rij(xi, classId):
		dataSource = None
		if classId == ClassEnum.negative.value:
			dataSource = self.dataNegative
		elif classId == ClassEnum.positive.value:
			dataSource = self.dataPositive

		sumAcc = Decimal(0) #acumulador de soma
		for example in self.dataSource:
			xi = example[0][i]
			sumAcc += Decimal(xi*(xi-1))/Decimal(2)

		return sumAcc

	def runForestRun(self):
		self.readData('../tic-tac-toe.data')

if __name__ == "__main__":

	bayes = Bayes() #Cria instancia da casse Bayes
	bayes.runForestRun()
	print("total de exemplos positivos " + str(bayes.totalPositive))
	print("total de exemplos negativos " + str(bayes.totalNegative))
	print("total de exemplos: " + str(bayes.totalNegative + bayes.totalPositive))