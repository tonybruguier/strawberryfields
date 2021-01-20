# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 10:21:54 2021

@author: Xanadu
"""

import strawberryfields as sf
import numpy as np
import pylab as plt
import matplotlib as mpl

alpha = np.array([2,4,6])
sf.hbar=1
wigners = []
xs = []
ps = []

for i in range(3):
    prog=sf.Program(2)
    with prog.context as q:
        sf.ops.Catstate(alpha[i]) | q[0]
        sf.ops.Catstate(alpha[i]) | q[1]
        sf.ops.BSgate() | (q[0],q[1])
        sf.ops.LossChannel(0.99) | q[0]
        sf.ops.LossChannel(0.99) | q[1]
    
    eng_fock = sf.Engine("fock",backend_options = {"cutoff_dim":20})
    results_fock = eng_fock.run(prog)
    
    eng_bosonic = sf.Engine("bosonic")
    results_bosonic = eng_bosonic.run(prog)

    x = np.linspace(-3,3,50*alpha[i])*sf.hbar*alpha[i]
    p = np.linspace(-2,2,50*alpha[i])*sf.hbar
    
    wigners.append(results_fock.state.wigner(0,x,p))
    wigners.append(results_bosonic.state.wigner(0,x,p))
    xs.append(x)
    ps.append(p)
    print(results_bosonic.state.mean_photon(0))
    print(results_fock.state.mean_photon(0))
    
#Plotting
cmax = 0.3
cmin = 0
    
fig, axs = plt.subplots(2,4,figsize=(12,8),gridspec_kw={'width_ratios': [1,1,1,0.05]})
cmap=mpl.cm.Blues
norm = mpl.colors.Normalize(vmin=cmin, vmax=cmax)
cb1 = mpl.colorbar.ColorbarBase(axs[0,3],cmap=cmap,
                                norm=norm,
                                orientation='vertical')
cb2 = mpl.colorbar.ColorbarBase(axs[1,3],cmap=cmap,
                                norm=norm,
                                orientation='vertical')
ims = np.empty((2,3),dtype=object)
axs[0,0].set_ylabel(r'p',fontsize = 12)
axs[1,0].set_ylabel(r'p',fontsize = 12)
for i in range(3):
    ims[0,i] = axs[0,i].contourf(xs[i],ps[i],wigners[2*i],levels=60,cmap=cmap,vmin=cmin,vmax=cmax)
    ims[1,i] = axs[1,i].contourf(xs[i],ps[i],wigners[2*i+1],levels=60,cmap=cmap,vmin=cmin,vmax=cmax)
    axs[1,i].set_xlabel(r'x',fontsize = 12)
    axs[0,i].set_title(r'$\alpha=$'+str(alpha[i]),fontsize = 14)
    for c in ims[0,i].collections:
        c.set_edgecolor("face")
    for c in ims[1,i].collections:
        c.set_edgecolor("face")
cb1.set_label('Wigner, Fock with cutoff\n of 50 photons',fontsize= 16)
cb2.set_label('Wigner, Linear combination\n of Gaussians',fontsize= 16)
fig.tight_layout()
#plt.savefig("Cat_BS_bosonic_v_fock60.pdf",bbox_inches="tight")
plt.show()
