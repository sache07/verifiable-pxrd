"""Rebuild the experimental adaptation schematic (Figure 4).

Requires matplotlib. No experimental data or solver jobs are accessed.
"""
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8,
    "axes.titlesize": 9, "axes.labelsize": 8.5,
    "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
    "legend.fontsize": 7.3, "axes.spines.top": False,
    "axes.spines.right": False, "axes.linewidth": .65,
    "pdf.fonttype": 42, "ps.fonttype": 42,
    "savefig.facecolor": "white",
})

# Paper-ready schematic; scientific roles and information flow, not executable controls.
fig = plt.figure(figsize=(7.35,3.7))
ax = fig.add_axes([.01,.02,.98,.96])
ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
def box(x,y,w,h,title,body,color):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.008,rounding_size=0.015",
                               facecolor=color,edgecolor="#9ca6b0",lw=.65))
    ax.text(x+w/2,y+h-.045,title,ha="center",va="top",fontsize=8.5,weight="bold")
    ax.text(x+w/2,y+h-.115,body,ha="center",va="top",fontsize=7.5,linespacing=1.45)
def arrow(a,b,label=None,rad=0):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=9,lw=.9,
                                color="#4e5c69",connectionstyle=f"arc3,rad={rad}"))
    if label:
        ax.text((a[0]+b[0])/2,(a[1]+b[1])/2+.017,label,ha="center",fontsize=6.8,
                bbox=dict(facecolor="white",edgecolor="none",pad=1))
box(.02,.77,.96,.19,"Interchangeable laboratory specification",
    "Synthesis family  •  plausible phases  •  instrument and specimen variation  •  solver inputs","#edf1f6")
box(.02,.39,.27,.26,"Synthetic cases",
    "Known phases and fractions\nRealistic profile + counting noise\nControls and missing references","#eef5f0")
box(.365,.39,.27,.26,"Blind solving agent",
    "Pattern + precursor metadata\nFresh workspace; frozen model\nStructures, fractions, final project","#edf3f8")
box(.71,.39,.27,.26,"Oracle-aware evolver",
    "Inspect trajectories and failures\nUse generating model + scores\nPropose and test revisions","#fbf0e6")
box(.365,.035,.27,.23,"Capability package",
    "Concise guidance + optional code\nRepeat tests and regression checks","#f5edf8")
box(.71,.035,.27,.23,"Experimental application",
    "Measured diffraction patterns\nPhase identification + refinement","#e9f5f3")
arrow((.15,.77),(.15,.65))
arrow((.295,.52),(.36,.52))
arrow((.64,.52),(.705,.52))
arrow((.84,.39),(.63,.265),"revise")
arrow((.50,.27),(.50,.385),"new attempt")
arrow((.64,.15),(.705,.15))
arrow((.22,.66),(.78,.66),"generating model / evaluator feedback",rad=-.10)
ax.text(.04,.19,"Same model plays both roles;\nonly the evolver sees\nsynthetic reference information.",
        fontsize=7.5,ha="left",va="center",color="#485362")
output = Path(os.environ.get("PXRD_RELEASE_OUTPUT", Path(__file__).resolve().parents[4] / ".runs/multiphase-reproduction")) / "figures/framework.pdf"
fig.savefig(output, bbox_inches="tight", pad_inches=0.035)
plt.close(fig)
print(output)
