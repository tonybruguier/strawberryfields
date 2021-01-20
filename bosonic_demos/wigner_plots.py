# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 15:15:36 2021

@author: Xanadu
"""

import strawberryfields as sf
import numpy as np
import matplotlib.pylab as plt
import matplotlib as mpl


#Phase space domain
sf.hbar = 1
x = np.linspace(-5,5,100)*sf.hbar
p = np.linspace(-5,5,100)*sf.hbar

#GKP demo
prog_GKP = sf.Program(1)

with prog_GKP.context as q:
    sf.ops.GKP(epsilon=0.1,cutoff=1e-15) | q[0]

eng_GKP = sf.Engine("bosonic")
results_GKP = eng_GKP.run(prog_GKP)
state_GKP = results_GKP.state

wigner_GKP = np.real_if_close(state_GKP.wigner(0,x,p))

#Cat (complex_rep) demo
prog_cat = sf.Program(1)

with prog_cat.context as q:
    sf.ops.Catstate(alpha=2,desc="complex") | q[0]

eng_cat = sf.Engine("bosonic")
results_cat = eng_cat.run(prog_cat)
state_cat = results_cat.state

wigner_cat = np.real_if_close(state_cat.wigner(0,x,p))


#Fock demo
prog_Fock = sf.Program(1)

with prog_Fock.context as q:
    sf.ops.Fock(1) | q[0]

eng_Fock = sf.Engine("bosonic")
results_Fock = eng_Fock.run(prog_Fock)
state_Fock = results_Fock.state

wigner_Fock = np.real_if_close(state_Fock.wigner(0,x,p))


#Plotting
cmax = np.real_if_close(np.amax([wigner_GKP,wigner_cat,wigner_Fock]))
cmin = np.real_if_close(np.amin([wigner_GKP,wigner_cat,wigner_Fock]))
if abs(cmin)<cmax:
    cmin = -cmax
else:
    cmax = -cmin
fig, axs = plt.subplots(1,4,figsize=(12,4),gridspec_kw={'width_ratios': [1,1,1,0.05]})
im0 = axs[0].contourf(x,p,wigner_GKP,levels=60,cmap=mpl.cm.RdBu,vmin=cmin,vmax=cmax)
im1 = axs[1].contourf(x,p,wigner_cat,levels=60,cmap=mpl.cm.RdBu,vmin=cmin,vmax=cmax)
im2 = axs[2].contourf(x,p,wigner_Fock,levels=60,cmap=mpl.cm.RdBu,vmin=cmin,vmax=cmax)
axs[0].set_title(r"(a) $|0\rangle_{GKP}$, $\epsilon=0.1$")
axs[1].set_title(r'(b) $|0\rangle_{cat}$, $\alpha=2$')
axs[2].set_title(r'(c) Single photon')
axs[0].set_ylabel("p",fontsize = 14)
axs[0].set_xlabel("x",fontsize = 14)
axs[1].set_xlabel("x",fontsize = 14)
axs[2].set_xlabel("x",fontsize = 14)

cmap=mpl.cm.RdBu
norm = mpl.colors.Normalize(vmin=cmin, vmax=cmax)
cb1 = mpl.colorbar.ColorbarBase(axs[3],cmap=cmap,
                                norm=norm,
                                orientation='vertical')
cb1.set_label('Wigner function')
fig.tight_layout()
for c in im0.collections:
    c.set_edgecolor("face")
for c in im1.collections:
    c.set_edgecolor("face")
for c in im2.collections:
    c.set_edgecolor("face")

#plt.savefig("Wigner_functions.pdf",bbox_inches="tight")
plt.show()
