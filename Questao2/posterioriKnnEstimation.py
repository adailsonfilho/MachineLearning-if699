from ticTacToeEnum import *

##################
#### METHODS #####
##################

from enum import Enum

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

if __name__ == "__main__":

	