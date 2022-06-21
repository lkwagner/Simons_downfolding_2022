import h5py
import glob
import pandas as pd
alldata = []
for fname in glob.glob("data/*.hdf5"):
    with h5py.File(fname, 'r') as f:
        r = f['r'][()]
        print(f['fci/e_tot'][()])
        for root, en in enumerate(f['fci/e_tot'][()]):
            alldata.append({
                'r':r,
                'en':en,
                'root':root,
                'method':'fci'
            })
df= pd.DataFrame(alldata)
print(df)
df.to_csv("data.csv", index=False)