"""Pure geometric kernel; semantic labels are conventional."""
import math
import numpy as np
BASE = np.array([[.5, math.sqrt(3)/2], [0.,0.], [1.,0.]])
def normalize(scores):
    s=np.asarray(scores,dtype=float)
    if s.shape!=(3,) or not np.all(np.isfinite(s)) or np.any(s<0) or s.sum()<=0:
        raise ValueError("Expected three finite nonnegative scores with positive sum")
    return s/s.sum()
def to_xy(weights):
    w=np.asarray(weights,dtype=float)
    if w.shape!=(3,) or not np.all(np.isfinite(w)) or np.any(w < -1e-12) or not np.isclose(w.sum(),1):
        raise ValueError("Invalid barycentric weights")
    return w @ BASE
def from_xy(xy,tolerance=1e-10):
    xy=np.asarray(xy,dtype=float)
    if xy.shape!=(2,) or not np.all(np.isfinite(xy)):
        raise ValueError("Expected finite xy pair")
    w=np.linalg.solve(np.vstack((BASE.T,np.ones(3))),np.r_[xy,1.])
    if np.any(w < -tolerance): raise ValueError("Point outside simplex")
    w=np.maximum(w,0)
    return w/w.sum()
def classify(weights,*,cutoff=.5,labels=("Theory","Evidence","Interpretation"),center="Explanation",tolerance=1e-10):
    w=np.asarray(weights,dtype=float)
    to_xy(w)
    if not (1/3 < cutoff < 1): raise ValueError("Invalid cutoff")
    if abs(w.max()-cutoff)<=tolerance: return "Region boundary"
    if w.max()<cutoff: return center
    return labels[int(w.argmax())]
def rotate_translate(angle_deg,center,base=BASE):
    a=math.radians(float(angle_deg))
    r=np.array([[math.cos(a),-math.sin(a)],[math.sin(a),math.cos(a)]])
    v=np.asarray(base,dtype=float);c=np.asarray(center,dtype=float)
    if v.shape!=(3,2) or c.shape!=(2,) or not np.all(np.isfinite(v)) or not np.all(np.isfinite(c)):
        raise ValueError("Invalid triangle or center")
    return (v-v.mean(axis=0))@r.T+c
def polygon_area(vertices):
    v=np.asarray(vertices,dtype=float)
    return abs(np.dot(v[:,0],np.roll(v[:,1],-1))-np.dot(v[:,1],np.roll(v[:,0],-1)))/2
