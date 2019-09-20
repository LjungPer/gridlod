import numpy as np

from . import fem
from . import util

class World:
    def __init__(self, NWorldCoarse, NCoarseElement, boundaryConditions = None):
        d = np.size(NWorldCoarse)
        assert(np.size(NCoarseElement) == d)
        if boundaryConditions is None:
            boundaryConditions = np.zeros([d,2], dtype='int64')
        assert(boundaryConditions.shape == (d,2))

        NWorldFine = NWorldCoarse*NCoarseElement

        self.NWorldCoarse = NWorldCoarse
        self.NCoarseElement = NCoarseElement
        self.boundaryConditions = np.array(boundaryConditions)
        self.NWorldFine = NWorldFine
        
        self.NpFine = np.prod(NWorldFine+1)
        self.NtFine = np.prod(NWorldFine)
        self.NpCoarse = np.prod(NWorldCoarse+1)
        self.NtCoarse = np.prod(NWorldCoarse)

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
    
    @property
    def ALocMatrixCoarse(self):
        if not hasattr(self, '_ALocMatrixCoarse'):
            self._ALocMatrixCoarse = fem.localStiffnessTensorMatrixCoefficient(self.NWorldCoarse)
        return self._ALocMatrixCoarse
        
    @property
    def ALocMatrixFine(self):
        if not hasattr(self, '_ALocMatrixFine'):
            self._ALocMatrixFine = fem.localStiffnessTensorMatrixCoefficient(self.NWorldCoarse*self.NCoarseElement)
        return self._ALocMatrixFine
    
    @property
    def FLocCoarse(self):
        if not hasattr(self, '_FLocCoarse'):
            self._FLocCoarse = fem.localFaceMassMatrix(self.NWorldCoarse)
        return self._FLocCoarse

    @property
    def FLocFine(self):
        if not hasattr(self, '_FLocFine'):
            self._FLocFine = fem.localFaceMassMatrix(self.NWorldCoarse*self.NCoarseElement)
        return self._FLocFine

class Patch:
    def __init__(self, world, k, TInd):
        self.world = world
        self.k = k
        self.TInd = TInd

        iElementWorldCoarse = util.convertpLinearIndexToCoordIndex(world.NWorldCoarse-1, TInd)[:]
        self.iElementWorldCoarse = iElementWorldCoarse
        
        # Compute (NPatchCoarse, iElementPatchCoarse) from (k, iElementWorldCoarse, NWorldCoarse)
        d = np.size(iElementWorldCoarse)
        NWorldCoarse = world.NWorldCoarse
        iPatchWorldCoarse = np.maximum(0, iElementWorldCoarse - k).astype('int64')
        iEndPatchWorldCoarse = np.minimum(NWorldCoarse - 1, iElementWorldCoarse + k).astype('int64') + 1
        self.NPatchCoarse = iEndPatchWorldCoarse-iPatchWorldCoarse
        self.iElementPatchCoarse = iElementWorldCoarse - iPatchWorldCoarse
        self.iPatchWorldCoarse = iPatchWorldCoarse

        self.NPatchFine = self.NPatchCoarse*world.NCoarseElement
        
        self.NpFine = np.prod(self.NPatchFine+1)
        self.NtFine = np.prod(self.NPatchFine)
        self.NpCoarse = np.prod(self.NPatchCoarse+1)
        self.NtCoarse = np.prod(self.NPatchCoarse)
