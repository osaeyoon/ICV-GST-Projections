import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import LOA_share as loa
from scipy import stats

models = ['ACCESS-ESM1-5', 'CanESM5', 'MIROC6', 'MPI-ESM1-2-LR']
ens_nums = [40, 25, 50, 30]
colors = ['#e78ac3', '#FF8000', '#04B431', '#01A9DB']
target_idx = [2, 1] 
year = np.arange(1850, 2100)
window_len = 11

NINO34 = [190, 240, -5, 5]
BKS = [20, 90, 65, 85]

def get_region_stats(model, ens_n, region, var_name, is_ocean=True):
    prefix = "tos_Omon" if is_ocean else "siconc_SImon"
    
    tass = []
    for i in range(1, ens_n + 1):
        fname = f"{prefix}_{model}_ssp585_r{i}i1p1f1_1850-2099.nc"
        with xr.open_dataset(fname) as ds:
            data = ds[var_name].sel(lat=slice(region[2], region[3]), lon=slice(region[0], region[1])).values
            lon, lat = ds['lon'].sel(lon=slice(region[0], region[1])).values, ds['lat'].sel(lat=slice(region[2], region[3])).values

            data_m = np.ma.masked_invalid(data)
            aave = [loa.wgt_areaave(d, lat, lon) for d in data_m]
            tass.append(aave)
            
    tass = np.array(tass)
    ens_mean = np.mean(tass, axis=0)
    ens_var = np.var(tass, axis=0, ddof=1)
    return ens_mean, tass, ens_var

nino_data = {m: get_region_stats(m, n, NINO34, 'tos', True) for m, n in zip(models, ens_nums)}
bks_data = {m: get_region_stats(m, n, BKS, 'siconc', False) for m, n in zip(models, ens_nums)}

fig, axes = plt.subplots(2, 2, figsize=(15, 12))
plt.subplots_adjust(hspace=0.35, wspace=0.25)

year_win = np.arange(1850 + window_len//2, 2100 - window_len//2)

# --- Row 1, Col 1: Niño 3.4 SST Spread (Fig 4a) ---
ax = axes[0, 0]
for i in target_idx:
    m = models[i]
    mean, raw, _ = nino_data[m]
    ax.fill_between(year, np.min(raw, axis=0), np.max(raw, axis=0), color=colors[i], alpha=0.2)
    ax.plot(year, mean, color=colors[i], linewidth=2.5, label=m)
ax.set_title("a) Niño3.4 SST ensemble spread", loc='left', fontsize=18, fontweight='bold')
ax.set_ylabel('℃', fontsize=15)
ax.set_ylim(22, 36)

# --- Row 2, Col 1: Niño 3.4 SST Variance (Fig 4b) ---
ax = axes[1, 0]
for i in target_idx:
    m = models[i]
    _, _, var = nino_data[m]
    var_win = np.convolve(var, np.ones(window_len)/window_len, mode='valid')
    ax.plot(year, var*100, color=colors[i], alpha=0.15, linewidth=0.8)
    ax.plot(year_win, var_win*100, color=colors[i], linewidth=3, label=m)
ax.set_title("b) Niño3.4 SST ensemble variance", loc='left', fontsize=18, fontweight='bold')
ax.set_ylabel('x10$^{-2}$ ℃$^2$', fontsize=15)
ax.set_ylim(0, 250)

# --- Row 1, Col 2: BKS SIC Spread (Fig 4c) ---
ax = axes[0, 1]
for i in target_idx:
    m = models[i]
    mean, raw, _ = bks_data[m]
    ax.fill_between(year, np.min(raw, axis=0), np.max(raw, axis=0), color=colors[i], alpha=0.2)
    ax.plot(year, mean, color=colors[i], linewidth=2.5, label=m)
ax.axhline(0, color='gray', linewidth=1)
ax.set_title("c) BKS SIC ensemble spread", loc='left', fontsize=18, fontweight='bold')
ax.set_ylabel('%', fontsize=15)
ax.set_ylim(-5, 90)

# --- Row 2, Col 2: BKS SIC Variance (Fig 4d) ---
ax = axes[1, 1]
for i in target_idx:
    m = models[i]
    _, _, var = bks_data[m]
    var_win = np.convolve(var, np.ones(window_len)/window_len, mode='valid')
    ax.plot(year, var, color=colors[i], alpha=0.15, linewidth=0.8)
    ax.plot(year_win, var_win, color=colors[i], linewidth=3, label=m)
ax.set_title("d) BKS SIC ensemble variance", loc='left', fontsize=18, fontweight='bold')
ax.set_ylabel('%$^2$', fontsize=15)
ax.set_ylim(0, 100)

for ax in axes.flat:
    ax.set_xlim(1850, 2100)
    ax.set_xlabel('Year', fontsize=14)
    ax.axvspan(1850, 1899, color="gray", alpha=0.15, zorder=0)
    ax.axvspan(2050, 2099, color="gray", alpha=0.15, zorder=0)
    ax.grid(linestyle='--', alpha=0.5)
    ax.tick_params(labelsize=12)
    ax.legend(loc='upper left', fontsize=11, frameon=True).get_frame().set_edgecolor('lightgray')

#plt.savefig('../figures/Figure4_combined.png', dpi=300, bbox_inches='tight')
plt.show()
