


from abc import ABC as _ABC, abstractmethod as _abstractmethod


class _frequentPatterns(_ABC):


    def __init__(self, iFile, minSup, sep="\t"):

        self._iFile = iFile
        self._sep = sep
        self._minSup = minSup
        self._finalPatterns = {}
        self._oFile = str()
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._startTime = float()
        self._endTime = float()

    @_abstractmethod
    def startMine(self):

        pass

    @_abstractmethod
    def getPatterns(self):

        pass

    @_abstractmethod
    def save(self, oFile):

        pass

    @_abstractmethod
    def getPatternsAsDataFrame(self):

        pass

    @_abstractmethod
    def getMemoryUSS(self):


        pass

    @_abstractmethod
    def getMemoryRSS(self):


        pass

    @_abstractmethod
    def getRuntime(self):


        pass

    @_abstractmethod
    def printResults(self):


        pass