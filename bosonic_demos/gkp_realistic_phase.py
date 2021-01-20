# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 17:21:08 2021

@author: Xanadu
"""

import strawberryfields as sf
import numpy as np
import pylab as plt
import matplotlib as mpl


sf.hbar = 1
x = np.linspace(-2,2,200)*np.sqrt(np.pi)
p = np.linspace(-2,2,200)*np.sqrt(np.pi)
xp = np.linspace(-5,5,500)*np.sqrt(np.pi)
wigners = []
marginals = []

#Ideal
prog_y = sf.Program(1)
with prog_y.context as q:
    sf.ops.GKP([np.pi/2,np.pi/2],epsilon=0.1) | q[0]
testy = sf.backends.bosonicbackend.backend.BosonicBackend()
testy.run_prog(prog_y,0)
wigners.append(testy.state().wigner(0,x,p))
marginals.append(testy.state().marginal(0,xp,np.pi/4))



rdB = np.array([14,10,6])
r_anc = np.log(10)*rdB/20
eta_anc = np.array([1,0.98,0.95])


for i in range(3):
    prog = sf.Program(1)
    with prog.context as q:
        sf.ops.GKP([-np.pi/2,0],epsilon=0.1) | q[0]
    test = sf.backends.bosonicbackend.backend.BosonicBackend()
    test.run_prog(prog,0)
    r = np.arccosh(np.sqrt(5/4))
    theta = np.arctan(0.5)
    phi = -np.pi / 2 * np.sign(0.5) - theta
    test.mbsqueeze(0, r, -phi, r_anc[i], eta_anc[i], True)
    test.rotation(theta,0)
    wigners.append(test.state().wigner(0,x,p))
    marginals.append(test.state().marginal(0,xp,np.pi/4))


#Plotting
cmax = np.real_if_close(np.amax(np.array(wigners)))
cmin = np.real_if_close(np.amin(np.array(wigners)))
if abs(cmin)<cmax:
    cmin = -cmax
else:
    cmax = -cmin
    
fig, axs = plt.subplots(1,5,figsize=(16,4),gridspec_kw={'width_ratios': [1,1,1,1,0.05]})
cmap=mpl.cm.RdBu
norm = mpl.colors.Normalize(vmin=cmin, vmax=cmax)
cb1 = mpl.colorbar.ColorbarBase(axs[4],cmap=cmap,
                                norm=norm,
                                orientation='vertical')
ims = np.empty(4,dtype=object)
axs[0].set_ylabel(r'p (units of $\sqrt{\hbar\pi}$)',fontsize = 12)
axs[0].set_title(r'$|+i\rangle_{GKP}$, $\epsilon$=0.1',fontsize = 14)
for i in range(4):
    ims[i] = axs[i].contourf(x/np.sqrt(np.pi),p/np.sqrt(np.pi),wigners[i],levels=60,cmap=mpl.cm.RdBu,vmin=cmin,vmax=cmax)
    axs[i].set_xlabel(r'x (units of $\sqrt{\hbar\pi}$)',fontsize = 12)
    if i>0:
        axs[i].set_title(r'$r_{anc}=$'+str(rdB[i-1])+r'dB, $\eta=$'+str(eta_anc[i-1]),fontsize = 14)
    for c in ims[i].collections:
        c.set_edgecolor("face")
cb1.set_label('Wigner function')
fig.tight_layout()
#plt.savefig("GKP_P_gate_wigner.pdf",bbox_inches="tight")
plt.show()

plt.ylabel(r'pdf(x+p)')
plt.xlabel(r'x+p (units of $\sqrt{\hbar\pi}$)')
plt.plot(np.sqrt(2)*xp/np.sqrt(np.pi),marginals[0],
         label=r'$|+i\rangle_{GKP}$, $\epsilon$=0.1',
         color="cornflowerblue")
colors = ['tab:red','seagreen']
styles = ['-','--']
for i in range(2):
    plt.plot(np.sqrt(2)*xp/np.sqrt(np.pi),marginals[2*i+1],
             label=r'$r_{anc}=$'+str(rdB[2*i])+r'dB, $\eta=$'+str(eta_anc[2*i]),
             color=colors[i],
             linestyle=styles[i])
plt.legend()
#plt.savefig("GKP_P_gate_marginals.pdf",bbox_inches="tight")
plt.show()