import fem

class World:
    def __init__(self, NWorldCoarse, NCoarseElement):
        self.NWorldCoarse = NWorldCoarse
        self.NCoarseElement = NCoarseElement

    @property
    def localBasis(self):
        if not hasattr(self, '_localBasis'):
            self._localBasis = fem.localBasis(self.NCoarseElement)
        return self._localBasis
    
    @property
    def MLocCoarse(self):
        if not hasattr(self, '_MLocCoarse'):
            self._MLocCoarse = fem.localMassMatrix(self.NWorldCoarse)
        return self._MLocCoarse

    @property
    def MLocFine(self):
        if not hasattr(self, '_MLocFine'):
            self._MLocFine = fem.localMassMatrix(self.NWorldCoarse*self.NCoarseElement)
        return self._MLocFine
    
    @property
    def ALocCoarse(self):
        if not hasattr(self, '_ALocCoarse'):
            self._ALocCoarse = fem.localStiffnessMatrix(self.NWorldCoarse)
        return self._ALocCoarse

    @property
    def ALocFine(self):
        if not hasattr(self, '_ALocFine'):
            self._ALocFine = fem.localStiffnessMatrix(self.NWorldCoarse*self.NCoarseElement)
        return self._ALocFine
    

