import pyscf
import pyscf.fci
import matplotlib.pyplot as plt
import numpy as np
import h5py

def make_run(r=1.4, chkfile=None):
    if chkfile is None:
        chkfile = f"data/h2_{r}.hdf5"
    
    mol = pyscf.gto.M(
        atom=f"H 0. 0. 0.; H 0. 0. {r}",
        basis='ccpvtz',
        )

    mf = pyscf.scf.RHF(mol)
    mf.chkfile = chkfile
    mf.kernel()

    cisolver = pyscf.fci.FCI(mf)
    cisolver.nroots=6
    en, civec = cisolver.kernel()
    print('en', en)

    with h5py.File(chkfile, 'a') as f:
        f['r'] = r
        f['fci/e_tot'] = en
        f['fci/rdm1'] = cisolver.make_rdm1s(civec[0], norb=mf.mo_coeff.shape[0], nelec=2)
        #f['fci/rdm2'] = cisolver(civec, norb=mf.mo_coeff.shape[0], nelec=2)



if __name__=="__main__":
    for r in np.linspace(0.5, 1.4, 20):
        print("r", r)
        make_run(r)