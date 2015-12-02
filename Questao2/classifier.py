from abc import ABCMeta, abstractmethod

class Classifier(metaclass=ABCMeta):

	@abstractmethod
	def __init__(self):
		pass

	@abstractmethod
	def classify(self,features):
		return NotImplemented