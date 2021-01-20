# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 10:22:02 2020

@author: Xanadu
"""

import strawberryfields as sf
import numpy as np
import pylab as plt

#Cat states
x = np.linspace(-4,4,1000)*sf.hbar
prog_cat_x = sf.Program(1)
with prog_cat_x.context as q:
    sf.ops.Catstate(alpha = 2,desc="complex") | q[0] 

prog_cat_p = sf.Program(1)
with prog_cat_p.context as q:
    sf.ops.Catstate(alpha = 2,desc="complex") | q[0]
    sf.ops.Rgate(np.pi/2) | q[0]

test_cat_x = sf.backends.bosonicbackend.backend.BosonicBackend()
test_cat_x.run_prog(prog_cat_x,0)

test_cat_p = sf.backends.bosonicbackend.backend.BosonicBackend()
test_cat_p.run_prog(prog_cat_p,0)


x_cat_prob = test_cat_x.state().marginal(0,x)
p_cat_prob = test_cat_x.state().marginal(0,x,phi=np.pi/2)


x_cat_samples = test_cat_x.circuit.homodyne(0,shots=2000)
p_cat_samples = test_cat_p.circuit.homodyne(0,shots=2000)

fig,axs = plt.subplots(1,2,figsize=(12,4))
fig.suptitle(r'$|0\rangle_{cat}$, $\alpha=2$',fontsize=18)
axs[0].hist(x_cat_samples[:,0]/sf.hbar,bins=100,density = True,label="Samples",color="cornflowerblue")
axs[0].plot(x/sf.hbar,x_cat_prob*sf.hbar,"--",label="Ideal",color="tab:red")
axs[0].set_xlabel("x",fontsize=14)
axs[0].set_ylabel("pdf(x)",fontsize=14)
axs[1].hist(p_cat_samples[:,0]/sf.hbar,bins=100,density = True,label="Samples",color="cornflowerblue")
axs[1].plot(x/sf.hbar,p_cat_prob*sf.hbar,"--",label="Ideal",color="tab:red")
axs[1].set_xlabel("p",fontsize=14)
axs[1].set_ylabel("pdf(p)",fontsize=14)
axs[1].legend()
plt.savefig("Cat_CV_tomography.pdf",bbox_inches = "tight")
plt.show()


#GKP states
x = np.linspace(-4,4,1000)*sf.hbar*np.sqrt(np.pi)

prog_gkp_x = sf.Program(1)
with prog_gkp_x.context as q:
    sf.ops.GKP(epsilon=0.1,cutoff=1e-15) | q[0] 

prog_gkp_p = sf.Program(1)
with prog_gkp_p.context as q:
    sf.ops.GKP(epsilon=0.1,cutoff=1e-15) | q[0] 
    sf.ops.Rgate(np.pi/2) | q[0]

test_gkp_x = sf.backends.bosonicbackend.backend.BosonicBackend()
test_gkp_x.run_prog(prog_gkp_x,0)

test_gkp_p = sf.backends.bosonicbackend.backend.BosonicBackend()
test_gkp_p.run_prog(prog_gkp_p,0)


x_gkp_prob = test_gkp_x.state().marginal(0,x)
p_gkp_prob = test_gkp_x.state().marginal(0,x,phi=np.pi/2)

x_gkp_samples = test_gkp_x.circuit.homodyne(0,shots=2000)
p_gkp_samples = test_gkp_p.circuit.homodyne(0,shots=2000)

fig,axs = plt.subplots(1,2,figsize=(12,4))
fig.suptitle(r'$|0\rangle_{GKP}$, $\epsilon=0.1$',fontsize=18)
axs[0].hist(x_gkp_samples[:,0]/sf.hbar,bins=100,density = True,label="Samples",color="cornflowerblue")
axs[0].plot(x/sf.hbar,x_gkp_prob*sf.hbar,"--",label="Ideal",color="tab:red")
axs[0].set_xlabel("x",fontsize=14)
axs[0].set_ylabel("pdf(x)",fontsize=14)
axs[1].hist(p_gkp_samples[:,0]/sf.hbar,bins=100,density = True,label="Samples",color="cornflowerblue")
axs[1].plot(x/sf.hbar,p_gkp_prob*sf.hbar,"--",label="Ideal",color="tab:red")
axs[1].set_xlabel("p",fontsize=14)
axs[1].set_ylabel("pdf(p)",fontsize=14)
axs[1].legend()
plt.savefig("GKP_CV_tomography.pdf",bbox_inches = "tight")
plt.show()

# #Fock states
# x = np.linspace(-4,4,1000)*sf.hbar

# prog_fock_x = sf.Program(1)
# with prog_fock_x.context as q:
#     sf.ops.Fock(1) | q[0] 

# prog_fock_p = sf.Program(1)
# with prog_fock_p.context as q:
#     sf.ops.Fock(1) | q[0] 
#     sf.ops.Rgate(np.pi/2) | q[0]

# test_fock_x = sf.backends.bosonicbackend.backend.BosonicBackend()
# test_fock_x.run_prog(prog_fock_x,0)

# test_fock_p = sf.backends.bosonicbackend.backend.BosonicBackend()
# test_fock_p.run_prog(prog_fock_p,0)

# x_fock_prob = test_fock_x.state().marginal(0,x)
# p_fock_prob = test_fock_x.state().marginal(0,x,phi=np.pi/2)

# x_fock_samples = test_fock_x.circuit.homodyne(0,shots=1000)
# p_fock_samples = test_fock_p.circuit.homodyne(0,shots=1000)

# fig,axs = plt.subplots(1,2,figsize=(12,4))
# axs[0].hist(x_fock_samples[:,0]/sf.hbar,bins=100,density = True,label="Samples")
# axs[0].plot(x/sf.hbar,x_fock_prob*sf.hbar,label="Ideal")
# axs[0].set_xlabel("x")
# axs[0].set_ylabel("pdf(x)")
# axs[1].hist(p_fock_samples[:,0]/sf.hbar,bins=100,density = True,label="Samples")
# axs[1].plot(x/sf.hbar,p_fock_prob*sf.hbar,label="Ideal")
# axs[1].set_xlabel("p")
# axs[1].set_ylabel("pdf(p)")
# axs[1].legend()
# plt.show()