"""Diagnostics do not establish construct validity."""
from dataclasses import dataclass,asdict
from itertools import combinations
import numpy as np
from .geometry import normalize,to_xy,classify
@dataclass(frozen=True)
class Observation:
    name: str
    scores: tuple
    basis: str = "judgment"
    source: str | None = None
    assessor: str | None = None
    def __post_init__(self):
        normalize(self.scores)
        if self.basis not in {"judgment","measured","mixed","unspecified"}:
            raise ValueError("Invalid basis")
def analyze(obs,cutoff=.5):
    w=normalize(obs.scores);xy=to_xy(w)
    return {**asdict(obs),"raw_total":float(sum(obs.scores)),"weights":w.tolist(),"xy":xy.tolist(),"region":classify(w,cutoff=cutoff),"boundary_margin_barycentric":float(w.max()-cutoff),"claim_status":"geometric_embedding_only"}
def sensitivity(obs,delta=1.,lower=0.,upper=10.,cutoff=.5):
    if delta<=0 or lower<0 or upper<=lower: raise ValueError("Invalid perturbation settings")
    base=analyze(obs,cutoff);cases=[]
    for i in range(3):
        for direction in (-1,1):
            s=list(obs.scores);s[i]=max(lower,min(upper,s[i]+direction*delta))
            if sum(s)<=0:continue
            result=analyze(Observation(obs.name,tuple(s),obs.basis,obs.source,obs.assessor),cutoff)
            cases.append({"axis":"APR"[i],"direction":direction,"scores":s,"distance_xy":float(np.linalg.norm(np.array(result["xy"])-base["xy"])),"region":result["region"],"region_changed":result["region"]!=base["region"]})
    return {"base":base,"delta":delta,"cases":cases,"any_region_change":any(x["region_changed"] for x in cases)}
def pairwise_distances(observations):
    points=[(o.name,to_xy(normalize(o.scores))) for o in observations]
    return [{"first":a,"second":b,"distance_xy":float(np.linalg.norm(x-y))} for (a,x),(b,y) in combinations(points,2)]
def compare_assessors(observations):
    if len(observations)<2:raise ValueError("At least two assessments required")
    w=np.stack([normalize(o.scores) for o in observations])
    return {"assessors":[o.assessor for o in observations],"mean_weights":w.mean(axis=0).tolist(),"weight_ranges":(w.max(axis=0)-w.min(axis=0)).tolist(),"regions":[classify(row) for row in w],"warning":"Descriptive agreement does not establish reliability or construct validity"}
