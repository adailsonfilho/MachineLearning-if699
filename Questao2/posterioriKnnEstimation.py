from ticTacToe import *
from enum import Enum
from classifier import *

##################
#### METHODS #####
##################

class PostKnnEstimation(Classifier):

	##################
	#####  VARS ######
	##################
	data = [] 			#pre-processed data
	k = None			#"k" neighbors parameter

	def read_data(self, path):
			with open(path) as f:
				for line in f:
					processedLine = pre_process(line, separator=',')
					self.data.append(processedLine)


	#return the "k" nearest neighbors of the given "x"
	def k_neighbors(self, k,x):												
		distances = []
		for i,sample in enumerate(self.data):
			d = dissimilarity(x, sample)
			distances.append({'index': i, 'distance:': d})

		distances = sorted(distances, key=lambda e:e['distance'])

		return [e['index'] for e in distances[0:k]]

	def classify(self,sample):
		sample = pre_process(sample, separator=',')
		kn = self.k_neighbors(self.k,sample)
		positive_votes = 0
		for i in kn:
			if data[i][1] == ClassEnum.positive.value:
				positive_votes+=1

		if len(kn) - positive_votes > positive_votes:
			return ClassEnum.negative.vale
		else:
			return ClassEnum.positive.value



if __name__ == "__main__":

	estimator = PostKnnEstimation()



	print("calma");

	naive_test = "o,x,o,o,x,o,o,x,o"
	resp = estimator.classify(naive_test)

	print(resp);

	