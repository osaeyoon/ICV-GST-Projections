import numpy as np
import xarray as xr
import LOA_share as loa

REGION = {
    'Tropics' : [0, 360, -30,  30],
    'NH'      : [0, 360,  30,  90],
    'SH'      : [0, 360, -90, -30]   
}

def get_area_weight(model):
    ddir = f"/home/osyoon/CDL/data/model/SMILEs/{model}/merge/GB/tas/ssp585/ann/JUNE/"
    with xr.open_dataset(ddir + f"tas_Amon_{model}_ssp585_r1i1p1f1_1850-2099.nc") as f:
        lon = f['lon'].values
        lat = f['lat'].values
        
    cos = np.cos(np.deg2rad(lat))
    Aall = (cos[:, None] * np.ones_like(lon)).sum()  
    
    w = {}
    for k, reg in REGION.items():
        lat_r = lat[(lat >= reg[2]) & (lat <= reg[3])]
        cos_r = np.cos(np.deg2rad(lat_r))
        Ar = (cos_r[:, None] * np.ones((len(lat_r), len(lon)))).sum()
        w[k] = Ar / Aall 
    return w

def weighted_series(model, ens_num):
    w = get_area_weight(model)
    band_keys = list(REGION.keys())
    series = {k: [] for k in band_keys}
    
    ddir = f"/home/osyoon/CDL/data/model/SMILEs/{model}/merge/GB/tas/ssp585/ann/JUNE/"
    
    for m in range(1, ens_num + 1):
        fname = f"tas_Amon_{model}_ssp585_r{m}i1p1f1_1850-2099.nc"
        with xr.open_dataset(ddir + fname) as ds:
            for k in band_keys:
                reg = REGION[k]
                tas = ds['tas'].sel(lat=slice(reg[2], reg[3]), lon=slice(reg[0], reg[1]))
                aave = [loa.wgt_areaave(t, tas.lat.values, tas.lon.values) for t in tas.values]
                series[k].append(aave)
                
    arr = np.stack([np.stack(series[k], axis=0) for k in band_keys], axis=-1)
    return arr, w

def contribution_4band(model, ens_num):
    arr, w_dict = weighted_series(model, ens_num)
    band_keys = list(REGION.keys())
    w_arr = np.array([w_dict[k] for k in band_keys])

    n_band = len(band_keys)
    n_time = arr.shape[1]

    Var_dict = {k: [] for k in band_keys}
    Cov_dict = {k: [] for k in band_keys}
    Cont_dict = {k: [] for k in band_keys}
    VarG_list = []

    for t in range(n_time):
        cov_raw = np.cov(arr[:, t, :].T, ddof=1) 
        cov_w = w_arr[:, None] * w_arr[None, :] * cov_raw
        
        for i, k in enumerate(band_keys):
            Var_dict[k].append(cov_w[i, i])
            cov_sum = np.sum(cov_w[i, :]) - cov_w[i, i]
            Cov_dict[k].append(cov_sum)

        varG = cov_w.sum()
        VarG_list.append(varG)

        for i, k in enumerate(band_keys):
            Cont_dict[k].append(np.sum(cov_w[i, :]) / varG)

    Var_dict = {k: np.array(v) for k, v in Var_dict.items()}
    Cov_dict = {k: np.array(v) for k, v in Cov_dict.items()}
    Cont_dict = {k: np.array(v) for k, v in Cont_dict.items()}
    VarG_arr = np.array(VarG_list)

    return Var_dict, Cov_dict, VarG_arr, Cont_dict
