import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import LOA_share as loa
import os
from mpl_toolkits.basemap import Basemap
from matplotlib.gridspec import GridSpec

models = ['MIROC6', 'CanESM5']
years_snapshot = [1850, 2015]
year_range = np.arange(1850, 2100)

def load_seof(model, year):
    path = f'seof1_{model}_{year}.nc'
    with xr.open_dataset(path) as f:
        return f['eof1'].values, f['exp_var'].values, f['lon'].values, f['lat'].values

draw_maps, exp_vars = [], []
coords = {} 
awpc_1850_list, awpc_2015_list = [], []

def cal_weight(lat, lon):
    coslat = np.cos(np.deg2rad(lat))
    Wij = np.ones((len(lat), len(lon)))
    for i in range(len(lat)): Wij[i, :] = coslat[i]
    return Wij

def cal_AWPC(Wij, A, B):
    return np.sum(Wij * A * B) / (np.sqrt(np.sum(Wij * A**2)) * np.sqrt(np.sum(Wij * B**2)))

for m_idx, model in enumerate(models):
    e1850, x1850, lon, lat = load_seof(model, 1850)
    e2015, x2015, _, _ = load_seof(model, 2015)
    
    draw_maps.extend([e1850, e2015])
    exp_vars.extend([x1850, x2015])
    coords[model] = (lon, lat)

    wij = cal_weight(lat, lon)
    tmp_1850, tmp_2015 = [], []
    if model == 'CanESM5': ddir += 'ENS_p1/'
    
    for yr in year_range:
        with xr.open_dataset(ddir + f'seof1_{yr}.nc') as f:
            curr_eof = f['eof1'].values
            tmp_1850.append(abs(cal_AWPC(wij, e1850, curr_eof)))
            tmp_2015.append(abs(cal_AWPC(wij, e2015, curr_eof)))
            
    awpc_1850_list.append(np.array(tmp_1850))
    awpc_2015_list.append(np.array(tmp_2015))

fig = plt.figure(figsize=(15, 22))
gs = GridSpec(4, 2, height_ratios=[1, 1, 0.6, 0.6], hspace=0.35, wspace=0.2)

lon_ticks = np.arange(0, 361, 60)
lat_ticks = np.arange(-90, 91, 30)

# --- (a-d) Snapshot Maps ---
for i in range(4):
    m_idx = i // 2 # 0,1 -> MIROC6 | 2,3 -> CanESM5
    curr_model = models[m_idx]
    ax = fig.add_subplot(gs[m_idx, i % 2])
    
    curr_lon, curr_lat = coords[curr_model]
    m = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=0, urcrnrlon=360, resolution='c', ax=ax)
    
    lon2d, lat2d = np.meshgrid(curr_lon, curr_lat)
    x, y = m(lon2d, lat2d)
    
    levels, ncolors = loa.colorbarTicks(draw_maps[i], -1, 1, 0.2)
    cbar, cblevels = loa.getCbar(levels, 0, 'RdBu_r', ncolors)
    cs = m.contourf(x, y, draw_maps[i], levels, cmap=cbar, extend='both')
    m.drawcoastlines(linewidth=0.7)
    
    ax.set_xticks(lon_ticks)
    ax.set_yticks(lat_ticks)
    ax.set_xticklabels([f"{l}°E" if l!=0 else "0°" for l in lon_ticks], fontsize=11)
    ax.set_yticklabels([f"{l}°N" if l>0 else (f"{abs(l)}°S" if l<0 else "0°") for l in lat_ticks], fontsize=11)
    
    title_label = ['a','b','c','d'][i]
    ax.set_title(f'{title_label}) {curr_model} ({exp_vars[i]:.2f}%)', loc='left', fontsize=18)
    ax.set_title(f'{years_snapshot[i%2]}', loc='right', fontsize=18)

# --- (e-f) Pattern Correlations (MIROC6 & CanESM5) ---
for i in range(2):
    ax = fig.add_subplot(gs[i + 2, :])
    
    ax.plot(year_range, awpc_1850_list[i], marker='o', color='#1c1c1c', markersize=5, linestyle='')
    ax.plot(year_range[2015-1850:], awpc_2015_list[i][2015-1850:], marker='o', color='#d62728', markersize=5, linestyle='')
    
    ax.axvspan(2015, 2100, color='#fdebc2', alpha=0.35, zorder=0) # SSP5-8.5
    
    title_label = ['e','f'][i]
    ax.set_title(f'{title_label}) {models[i]}', loc='left', fontsize=20)
    ax.set_ylabel('Pattern Correlation', fontsize=16)
    ax.set_xlabel('Year', fontsize=16)
    ax.set_ylim(0, 1.0)
    ax.set_xlim(1845, 2105)
    ax.grid(True, linestyle='--', alpha=0.5)
    for spine in ax.spines.values(): spine.set_linewidth(2)

plt.savefig('../figures/Figure3.png', dpi=300, bbox_inches='tight')
plt.show()
