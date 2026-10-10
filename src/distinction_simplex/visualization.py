"""Optional matplotlib visualization."""
from .geometry import BASE,normalize,to_xy,rotate_translate
def plot_positions(observations,path):
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(8,7))
    poly=list(BASE)+[BASE[0]]
    ax.plot([p[0] for p in poly],[p[1] for p in poly],color="black",lw=2)
    for obs in observations:
        xy=to_xy(normalize(obs.scores));ax.scatter(*xy,s=40);ax.annotate(obs.name,xy,xytext=(6,6),textcoords="offset points")
    for xy,label in zip(BASE,("A","P","R")):ax.annotate(label,xy,xytext=(0,12),textcoords="offset points",ha="center")
    ax.set_aspect("equal");ax.axis("off");fig.tight_layout();fig.savefig(path,dpi=180);plt.close(fig)
def plot_overlays(path,names,angles=None,centers=None):
    import matplotlib.pyplot as plt
    names=list(names)
    angles=list(angles) if angles is not None else [i*200/max(1,len(names)-1) for i in range(len(names))]
    centers=list(centers) if centers is not None else [(.5,.4)]*len(names)
    if len(names)!=len(angles) or len(names)!=len(centers):raise ValueError("Overlay lengths differ")
    fig,ax=plt.subplots(figsize=(9,8))
    for name,angle,center in zip(names,angles,centers):
        v=rotate_translate(angle,center);p=list(v)+[v[0]]
        ax.plot([x[0] for x in p],[x[1] for x in p],label=f"{name} ({angle} degrees)")
    ax.set_aspect("equal");ax.axis("off");ax.legend(loc="upper left",bbox_to_anchor=(1,1))
    fig.tight_layout();fig.savefig(path,dpi=180,bbox_inches="tight");plt.close(fig)
