from abc import ABCMeta, abstractmethod

class Classifier(metaclass=ABCMeta):

	@abstractmethod
	def __init__(self, path):
		pass

	@abstractmethod
	def read_data(self,features):
		pass

	@abstractmethod
	def classify(self,features):
		return NotImplemented