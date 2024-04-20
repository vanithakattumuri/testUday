# Apriori is one of the fundamental algorithm to discover frequent patterns in a transactional database. This program employs apriori property (or downward closure property) to  reduce the search space effectively. This algorithm employs breadth-first search technique to find the complete set of frequent patterns in a transactional database.
#
# **Importing this algorithm into a python program**
# ----------------------------------------------------
#
#             import PAMI1.frequentPattern.basic.Apriori as alg
#
#             obj = alg.Apriori(iFile, minSup)
#
#             obj.mine()
#
#             frequentPattern = obj.getPatterns()
#
#             print("Total number of Frequent Patterns:", len(frequentPattern))
#
#             obj.save(oFile)
#
#             Df = obj.getPatternInDataFrame()
#
#             memUSS = obj.getMemoryUSS()
#
#             print("Total Memory in USS:", memUSS)
#
#             memRSS = obj.getMemoryRSS()
#
#             print("Total Memory in RSS", memRSS)
#
#             run = obj.getRuntime()
#
#             print("Total ExecutionTime in seconds:", run)
#


from PAMI1.frequentPattern.basic import abstract as _ab
from typing import Dict, Union
from deprecated import deprecated


class Apriori(_ab._frequentPatterns):

    """
        :Description: Apriori is one of the fundamental algorithm to discover frequent patterns in a transactional database. This program employs apriori property (or downward closure property) to  reduce the search space effectively. This algorithm employs breadth-first search technique to find the complete set of frequent patterns in a transactional database.

        :Reference:  Agrawal, R., Imieli ́nski, T., Swami, A.: Mining association rules between sets of items in large databases.
                In: SIGMOD. pp. 207–216 (1993), https://doi.org/10.1145/170035.170072

        :param  iFile: str :
                       Name of the Input file to mine complete set of frequent patterns
        :param  oFile: str :
                       Name of the output file to store complete set of frequent patterns
        :param  minSup: int or float or str :
                       The user can specify minSup either in count or proportion of database size. If the program detects the data type of minSup is integer, then it treats minSup is expressed in count. Otherwise, it will be treated as float.
        :param  sep: str :
                       This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.
    """


    _minSup = float()
    _startTime = float()
    _endTime = float()
    _finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _sep = " "
    _memoryUSS = float()
    _memoryRSS = float()
    _Database = []

    def _creatingItemSets(self) -> None:

        self._Database = []
        if isinstance(self._iFile, _ab._pd.DataFrame):
            temp = []
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                temp = self._iFile['Transactions'].tolist()

            for k in temp:
                self._Database.append(set(k))
        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._sep)]
                    temp = [x for x in temp if x]
                    self._Database.append(set(temp))
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line.strip()
                            temp = [i.rstrip() for i in line.split(self._sep)]
                            temp = [x for x in temp if x]
                            self._Database.append(set(temp))
                except IOError:
                    print("File Not Found")
                    quit()

    def _convert(self, value: Union[int, float, str]) -> Union[int, float]:

        if type(value) is int:
            value = int(value)
        if type(value) is float:
            value = (len(self._Database) * value)
        if type(value) is str:
            if '.' in value:
                value = float(value)
                value = (len(self._Database) * value)
            else:
                value = int(value)
        return value

    def startMine(self) -> None:

        self.mine()

    def mine(self) -> None:

        self._Database = []
        self._startTime = _ab._time.time()

        self._creatingItemSets()

        self._minSup = self._convert(self._minSup)

        items = {}
        index = 0
        for line in self._Database:
            for item in line:
                if tuple([item]) in items:
                    items[tuple([item])].append(index)
                else:
                    items[tuple([item])] = [index]
            index += 1

        # sort by length in descending order
        items = dict(sorted(items.items(), key=lambda x: len(x[1]), reverse=True))

        cands = []
        fileData = {}
        for key in items:
            if len(items[key]) >= self._minSup:
                cands.append(key)
                self._finalPatterns["\t".join(key)] = len(items[key])
                fileData[key] = set(items[key])
            else:
                break


        while cands:
            newKeys = []
            for i in range(len(cands)):
                for j in range(i+1, len(cands)):
                    if cands[i][:-1] == cands[j][:-1]:
                        newCand = cands[i] + tuple([cands[j][-1]])
                        intersection = fileData[tuple([newCand[0]])]
                        for k in range(1, len(newCand)):
                            intersection = intersection.intersection(fileData[tuple([newCand[k]])])
                        if len(intersection) >= self._minSup:
                            newKeys.append(newCand)
                            newCand = "\t".join(newCand)
                            self._finalPatterns[newCand] = len(intersection)
            del cands
            cands = newKeys
            del newKeys
            
        process = _ab._psutil.Process(_ab._os.getpid())
        self._endTime = _ab._time.time()
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Frequent patterns were generated successfully using Apriori algorithm ")

    def getMemoryUSS(self) -> float:

        return self._memoryUSS

    def getMemoryRSS(self) -> float:

        return self._memoryRSS

    def getRuntime(self) -> float:

        return self._endTime - self._startTime

    def getPatternsAsDataFrame(self) -> _ab._pd.DataFrame:

        dataFrame = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a.replace('\t', ' '), b])
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'Support'])
        # dataFrame = dataFrame.replace(r'\r+|\n+|\t+',' ', regex=True)
        return dataFrame

    def save(self, outFile) -> None:

        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            s1 = x.strip() + ":" + str(y)
            writer.write("%s \n" % s1)

    def getPatterns(self) -> Dict[str, int]:

        return self._finalPatterns

    def printResults(self) -> None:
        print("Total number of Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:", self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 4 or len(_ab._sys.argv) == 5:
        if len(_ab._sys.argv) == 5:
            _ap = Apriori(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        if len(_ab._sys.argv) == 4:
            _ap = Apriori(_ab._sys.argv[1], _ab._sys.argv[3])
        _ap.startMine()
        _ap.mine()
        print("Total number of Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save(_ap._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
