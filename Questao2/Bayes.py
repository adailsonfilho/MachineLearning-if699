import os
from enum import Enum

#limpa tela
clear = lambda: os.system('cls') #to clear screen during use of console in windows

class Categories(Enum): #how use that shit? Categories['x']
    x = 1
    o = 0
    b = -1

class Class(Enum): #how use that shit? Class['positive']
    positive = 1
    negative = 0

class Bayes:
	def __init__(self):
		self.categories = Categories
		self.classes = Class
		self.data;

	def readData(self, path):
		with open(path) as f:
    		for line in f:
        		print(line)

	def priori(self,class):
		pass

	def posteriori(self,class,features):
		pass

	def runForestRun(self):
		self.readData('../tic-tac-toe.data')
		pass

	if __name__ == "__main__":
		self.runForestRun(self):