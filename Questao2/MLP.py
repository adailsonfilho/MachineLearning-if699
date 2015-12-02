from enum import Enum
from sklearn.neural_network import MLPClassifier

class FeatureEnum(Enum):
    x = 1
    o = 0
    b = -1

class ClassEnum(Enum):
    positive = 1
    negative = 0

class MLP():
    def __init__(self):

        self.total_positive = 0
        self.total_negative = 0

        #All data readed from files after pre-processed
        self.data_positive = []
        self.data_negative = []

        #data for learning after
        self.data_positive_learn = []
        self.data_negative_learn = []



    def preProcess(self, line, separator):
            features = []
            classId = None
            acc = ''

            for x in line:
                if x != ',' and x != '\n':
                    acc += x
                elif x == '\n':
                    classId = ClassEnum[acc].value
                else:
                    features.append(FeatureEnum[acc].value)
                    acc = ''

            return (features, classId)


    def readData(self, path):
            with open(path) as f:
                for line in f:
                    processedLine = self.preProcess(line, separator=',')
                    if processedLine[1] == ClassEnum.positive.value:
                        self.data_positive.append(processedLine)

                    elif processedLine[1] == ClassEnum.negative.value:
                        self.data_negative.append(processedLine)


            print(self.data_positive)
            print(self.data_negative)



    def calculateRange(self,next_range, set_size, max_length, is_last_set):
        #calculate test positive range
            start = next_range
            end = next_range + set_size

            #if passed of the end of examples, correct
            if end >= max_length or is_last_set:
                end = max_length

            return {"begin":start,"end":end}





    def runForestRun(self):
            self.readData('../tic-tac-toe.data')

if __name__ == "__main__":
    mlp = MLP()
    mlp.runForestRun()

    x = mlp.data_positive[0]# array of size [n_samples, n_features
    y = [0, 1]# array of n_samples which is the label, in this case 0, 1