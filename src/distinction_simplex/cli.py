"""Dataset CLI: python -m distinction_simplex.cli examples/nine_thinkers.json --plot"""
import argparse,csv,json
from pathlib import Path
from .analysis import Observation,analyze,sensitivity,pairwise_distances
def main(argv=None):
    p=argparse.ArgumentParser(description="Geometric embedding, not empirical validation")
    p.add_argument("input");p.add_argument("--output",default="results");p.add_argument("--delta",type=float,default=1.);p.add_argument("--plot",action="store_true")
    args=p.parse_args(argv)
    data=json.loads(Path(args.input).read_text(encoding="utf-8"))
    obs=[Observation(x["name"],tuple(x["scores"]),x.get("basis","unspecified"),x.get("source"),x.get("assessor")) for x in data["observations"]]
    if not obs:p.error("No observations")
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    result={"schema_version":"0.2","axis_labels":data.get("axis_labels",["A","P","R"]),"axis_definitions":data.get("axis_definitions"),"observations":[analyze(o) for o in obs],"sensitivity":[sensitivity(o,delta=args.delta) for o in obs],"pairwise_distances":pairwise_distances(obs),"limitations":["Mathematical validity is not construct validity","Normalization removes magnitude","Scores and labels are user-supplied","Rotations preserve geometry, not semantic correspondence"]}
    (out/"analysis.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    with (out/"positions.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["name","basis","raw_total","a","p","r","x","y","region"]);w.writeheader()
        for x in result["observations"]:
            w.writerow({"name":x["name"],"basis":x["basis"],"raw_total":x["raw_total"],"a":x["weights"][0],"p":x["weights"][1],"r":x["weights"][2],"x":x["xy"][0],"y":x["xy"][1],"region":x["region"]})
    (out/"validity_report.md").write_text("# Validity report\n\nGeometric calculations are reproducible. Axis meanings, score assignments, labels, and construct validity are not established by the software. Normalization removes magnitude; raw totals remain available.\n",encoding="utf-8")
    if args.plot:
        from .visualization import plot_positions,plot_overlays
        plot_positions(obs,out/"positions.png");plot_overlays(out/"fixed_scale_overlays.png",[o.name for o in obs])
    print(f"Wrote {out}")
if __name__=="__main__":main()
