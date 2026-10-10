import numpy as np
import pytest
from distinction_simplex.geometry import BASE,normalize,to_xy,from_xy,classify,rotate_translate,polygon_area
def test_normalize(): assert np.allclose(normalize([2,3,5]),[.2,.3,.5])
def test_zero_invalid():
    with pytest.raises(ValueError):normalize([0,0,0])
def test_vertices(): assert np.allclose(to_xy([1,0,0]),BASE[0])
def test_inverse(): assert np.allclose(from_xy(to_xy([.2,.3,.5])),[.2,.3,.5])
def test_centroid(): assert classify([1/3]*3)=="Explanation"
def test_boundary(): assert classify([.5,.25,.25])=="Region boundary"
def test_rotation_area(): assert np.isclose(polygon_area(rotate_translate(43,[2,3])),polygon_area(BASE))
def test_medial_area():
    m=np.array([(BASE[0]+BASE[1])/2,(BASE[1]+BASE[2])/2,(BASE[2]+BASE[0])/2])
    assert np.isclose(polygon_area(m)/polygon_area(BASE),.25)
