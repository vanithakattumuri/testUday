# ECLATbitset is one of the fundamental algorithm to discover frequent patterns in a transactional database.
#
# **Importing this algorithm into a python program**
# ---------------------------------------------------------
#
#             import PAMI.frequentPattern.basic.ECLATbitset as alg
#
#             obj = alg.ECLATbitset(iFile, minSup)
#
#             obj.mine()
#
#             frequentPatterns = obj.getPatterns()
#
#             print("Total number of Frequent Patterns:", len(frequentPatterns))
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


__copyright__ = """
Copyright (C)  2021 Rage Uday Kiran

     This program is free software: you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.

     This program is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.

     You should have received a copy of the GNU General Public License
     along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from PAMI.frequentPattern.basic import abstract as _ab
from deprecated import deprecated


class ECLATbitset(_ab._frequentPatterns):
    """
    :Description:  ECLATbitset is one of the fundamental algorithm to discover frequent patterns in a transactional database.

    :Reference:  Mohammed Javeed Zaki: Scalable Algorithms for Association Mining. IEEE Trans. Knowl. Data Eng. 12(3):
            372-390 (2000), https://ieeexplore.ieee.org/document/846291

    :param  iFile: str :
                   Name of the Input file to mine complete set of frequent patterns
    :param  oFile: str :
                   Name of the output file to store complete set of frequent patterns
    :param  minSup: int or float or str :
                   The user can specify minSup either in count or proportion of database size. If the program detects the data type of minSup is integer, then it treats minSup is expressed in count.
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.

    :Attributes:

        startTime : float
          To record the start time of the mining process

        endTime : float
          To record the completion time of the mining process

        finalPatterns : dict
          Storing the complete set of patterns in a dictionary variable

        memoryUSS : float
          To store the total amount of USS memory consumed by the program

        memoryRSS : float
          To store the total amount of RSS memory consumed by the program

        Database : list
          To store the transactions of a database in list


    **Methods to execute code on terminal**
    ------------------------------------------

    .. code-block:: console

      Format:

      (.venv) $ python3 ECLATbitset.py <inputFile> <outputFile> <minSup>

      Example Usage:

      (.venv) $ python3 ECLATbitset.py sampleDB.txt patterns.txt 10.0

    .. note:: minSup will be considered in percentage of database transactions


    **Importing this algorithm into a python program**
    ---------------------------------------------------------
    .. code-block:: python

            import PAMI.frequentPattern.basic.ECLATbitset as alg

            obj = alg.ECLATbitset(iFile, minSup)

            obj.mine()

            frequentPatterns = obj.getPatterns()

            print("Total number of Frequent Patterns:", len(frequentPatterns))

            obj.save(oFile)

            Df = obj.getPatternInDataFrame()

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)

    **Credits:**
    -------------------

               The complete program was written by Yudai Masu under the supervision of Professor Rage Uday Kiran.

    """

    _startTime = float()
    _endTime = float()
    _finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _sep = " "
    _minSup = str()
    _memoryUSS = float()
    _memoryRSS = float()
    _Database = []
    _mapSupport = {}
    _lno = 0

    def _convert(self, value):
        """
        To convert the user specified minSup value

        :param value: user specified minSup value

        :type value: int

        :return: converted type

        :rtype: int or float or string
        """
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

    def _creatingItemSets(self):
        """
        Storing the complete transactions of the database/input file in a database variable
        """
        self._Database = []
        self._mapSupport = {}
        if isinstance(self._iFile, _ab._pd.DataFrame):
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                self._Database = self._iFile['Transactions'].tolist()

        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._sep)]
                    temp = [x for x in temp if x]
                    self._Database.append(temp)
            else:
                try:
                    with open(self._iFile, 'r') as f:
                        for line in f:
                            self._lno += 1
                            splitter = [i.rstrip() for i in line.split(self._sep)]
                            splitter = [x for x in splitter if x]
                            self._Database.append(splitter)
                except IOError:
                    print("File Not Found")
        self._minSup = self._convert(self._minSup)

    @deprecated(
        "It is recommended to use 'mine()' instead of 'startMine()' for mining process. Starting from January 2025, 'startMine()' will be completely terminated.")
    def startMine(self):
        """
        Frequent pattern mining process will start from here
        We start with the scanning the itemSets and store the bitsets respectively.
        We form the combinations of single items and  check with minSup condition to check the frequency of patterns
        """
        self.mine()

    def _bitPacker(self, data, maxIndex):
        """
        It takes the data and maxIndex as input and generates integer as output value.

        :param data: it takes data as input.

        :type data: int or float

        :param maxIndex: It converts the data into bits By taking the maxIndex value as condition.

        :type maxIndex: int

        """
        packed_bits = 0
        for i in data:
            packed_bits |= 1 << (maxIndex - i)

        return packed_bits

    def mine(self) -> None:
        """
        Frequent pattern mining process will start from here
        # Bitset implementation
        """
        self._startTime = _ab._time.time()

        self._Database = []

        self._creatingItemSets()

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
        for key in items:
            if len(items[key]) >= self._minSup:
                self._finalPatterns["\t".join(key)] = len(items[key])
                cands.append(key)
                items[key] = self._bitPacker(items[key], index)
                # print(key, items[key])
            else:
                break

        while cands:
            newCands = []
            for i in range(len(cands)):
                for j in range(i + 1, len(cands)):
                    if cands[i][:-1] == cands[j][:-1]:
                        newCand = tuple(cands[i] + tuple([cands[j][-1]]))
                        intersection = items[tuple([newCand[0]])]
                        for k in range(1, len(newCand)):
                            intersection &= items[tuple([newCand[k]])]
                        count = int.bit_count(intersection)
                        if count >= self._minSup:
                            newCands.append(newCand)
                            newCand = "\t".join(newCand)
                            self._finalPatterns[newCand] = count
                    else:
                        break

            cands = newCands

        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Frequent patterns were generated successfully using Apriori algorithm ")

    def getMemoryUSS(self):
        """
        Total amount of USS memory consumed by the mining process will be retrieved from this function
        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryUSS

    def getMemoryRSS(self):
        """
        Total amount of RSS memory consumed by the mining process will be retrieved from this function
        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryRSS

    def getRuntime(self):
        """
        Calculating the total amount of runtime taken by the mining process
        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """

        return self._endTime - self._startTime

    def getPatternsAsDataFrame(self):
        """
        Storing final frequent patterns in a dataframe
        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a.replace('\t', ' '), b])
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'Support'])
        return dataFrame

    def save(self, outFile):
        """
        Complete set of frequent patterns will be loaded in to an output file
        :param outFile: name of the outputfile
        :type outFile: file
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            patternsAndSupport = x.strip() + ":" + str(y)
            writer.write("%s \n" % patternsAndSupport)

    def getPatterns(self):
        """
        Function to send the set of frequent patterns after completion of the mining process
        :return: returning frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def printResults(self):
        """
        This function is used to print the result
        """
        print("Total number of Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:", self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 4 or len(_ab._sys.argv) == 5:
        if len(_ab._sys.argv) == 5:
            _ap = ECLATbitset(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        if len(_ab._sys.argv) == 4:
            _ap = ECLATbitset(_ab._sys.argv[1], _ab._sys.argv[3])
        _ap.startMine()
        _ap.mine()
        print("Total number of Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")