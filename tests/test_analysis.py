import numpy as np
from distinction_simplex.analysis import Observation,analyze,sensitivity,pairwise_distances,compare_assessors
def test_magnitude_preserved(): assert analyze(Observation("x",(9,9,9)))["raw_total"]==27
def test_scale_invariant(): assert np.allclose(analyze(Observation("a",(9,9,9)))["weights"],analyze(Observation("b",(3,3,3)))["weights"])
def test_sensitivity(): assert len(sensitivity(Observation("x",(4,5,6)))["cases"])==6
def test_pairs(): assert len(pairwise_distances([Observation("a",(1,1,1)),Observation("b",(1,2,3))]))==1
def test_assessors(): assert len(compare_assessors([Observation("a",(1,2,3)),Observation("b",(3,2,1))])["regions"])==2
