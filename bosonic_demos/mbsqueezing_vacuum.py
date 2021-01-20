# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 18:28:27 2021

@author: Xanadu
"""

import strawberryfields as sf
import numpy as np
import pylab as plt
from matplotlib.patches import Ellipse

def get_cov_ellipse(cov, centre, nstd, **kwargs):
    """
    Return a matplotlib Ellipse patch representing the covariance matrix
    cov centred at centre and scaled by the factor nstd.

    """

    # Find and sort eigenvalues and eigenvectors into descending order
    eigvals, eigvecs = np.linalg.eigh(cov)
    order = eigvals.argsort()[::-1]
    eigvals, eigvecs = eigvals[order], eigvecs[:, order]

    # The anti-clockwise angle to rotate our ellipse by 
    vx, vy = eigvecs[:,0][0], eigvecs[:,0][1]
    theta = np.arctan2(vy, vx)

    # Width and height of ellipse to draw
    width, height = 2 * nstd * np.sqrt(eigvals)
    return Ellipse(xy=centre, width=width, height=height,
                   angle=np.degrees(theta), **kwargs)

r = [0.3,1,2]
color = ['tab:red','seagreen','cornflowerblue']
style = [':','--','-']
label = ["Ideal", "Average map", "Single shot"]
e = [0,1,2]
fig,ax = plt.subplots(1,3, figsize = (12,4))
for j in range(3):
    prog = sf.Program(3)

    with prog.context as q:
        sf.ops.Sgate(r[j],0) | q[0]
        sf.ops.MbSgate(r[j],0,r_anc=1.2,eta_anc=0.99,avg=True) | q[1]
        sf.ops.MbSgate(r[j],0,r_anc=1.2,eta_anc=0.99,avg=False) | q[2]
        
    eng = sf.Engine("bosonic")
    results = eng.run(prog)
    
    state = results.state
    
    x = np.linspace(-4,4,1000)*np.sqrt(sf.hbar)*r[j]
    p = np.linspace(-4,4,1000)*np.sqrt(sf.hbar)*r[j]
    
    ax[j].set_title(r'$r_{target}=$'+str(r[j]))
    for i in range(3):
        cov = np.real_if_close(state.covs()[0,2*i:2*i+2,2*i:2*i+2])
        e[i] = get_cov_ellipse(cov, 
                            (state.means()[0,2*i], state.means()[0,2*i+1]), 
                            1,
                            facecolor='none',
                            edgecolor=color[i],
                            linestyle=style[i])
        ax[j].add_artist(e[i])
        ax[j].set_xlabel("x",fontsize = 14)
        ax[j].set_xlim(x[0],x[-1])
        ax[j].set_ylim(p[0],p[-1])
        
ax[0].set_ylabel("p",fontsize = 14)
ax[1].legend(e,label,ncol=3, bbox_to_anchor=(0.5,-0.3), loc = "lower center") 
#plt.savefig("squeezed_vac.pdf",bbox_inches = "tight")
plt.show()
    