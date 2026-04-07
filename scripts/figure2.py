import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import LOA_share as loa
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.gridspec as gridspec

models = ['ACCESS-ESM1-5', 'CanESM5', 'MIROC6', 'MPI-ESM1-2-LR']
ens_nums = [40, 25, 50, 30]
colors_c = ['#23c473', '#dde632', '#5e6662'] # Tropics, NH, SH
window_len = 11

colors_a = [(0.0, "#ffffff"), (0.09, "#ffffff"), (0.2, "#e1ebfa"), (0.4, "#bee6be"),
            (0.7, "#ffffbf"), (1.2, "#f27a41"), (1.5, "#ed481f"), (1.8, "#ed1f1f"), (2.0, "#612e2e")]
norm_pos = [v[0]/2.0 for v in colors_a]
norm_col = [v[1] for v in colors_a]
cmap_a = LinearSegmentedColormap.from_list("cmap_a", list(zip(norm_pos, norm_col)))

fig = plt.figure(figsize=(24, 16))
gs = gridspec.GridSpec(3, 4, figure=fig, hspace=0.7, wspace=0.3, height_ratios=[1, 1, 0.5])

lon_ticks = np.arange(0, 361, 60)
lat_ticks = np.arange(-90, 91, 30)

# -----------------------------------------------------------
# [ROW 1 & 2] Figure 2a & 2b: Spatial Maps
# -----------------------------------------------------------
for i, model in enumerate(models):
    ds = xr.open_dataset(f"var_{model}_1850to2099_1x1.nc")
    lon, lat = ds['lon'].values, ds['lat'].values
    var_hist = np.mean(ds['var'].sel(time=slice('1850', '1899')).values, axis=0)
    var_fut = np.mean(ds['var'].sel(time=slice('2050', '2099')).values, axis=0)
    var_diff = var_fut - var_hist

    # --- Fig 2a ---
    ax_a = fig.add_subplot(gs[0, i])
    m_a = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=0, urcrnrlon=360, resolution='c', ax=ax_a)
    lon2d, lat2d = np.meshgrid(lon, lat)
    x, y = m_a(lon2d, lat2d)
    cs_a = m_a.contourf(x, y, var_hist, np.arange(0, 2.01, 0.1), cmap=cmap_a, extend='max')
    m_a.drawcoastlines(linewidth=0.5)
    ax_a.set_title(model, fontsize=22, fontweight='bold', pad=15)
    ax_a.set_xticks(lon_ticks)
    ax_a.set_yticks(lat_ticks)
    ax_a.set_xticklabels([f"{l}°E" if l!=0 else "0°" for l in lon_ticks], fontsize=11)
    ax_a.set_yticklabels([f"{l}°N" if l>0 else (f"{abs(l)}°S" if l<0 else "0°") for l in lat_ticks], fontsize=11)

    # --- Fig 2b ---
    ax_b = fig.add_subplot(gs[1, i])
    m_b = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=0, urcrnrlon=360, resolution='c', ax=ax_b)
    cs_b = m_b.contourf(x, y, var_diff, np.arange(-1.0, 1.01, 0.1), cmap='RdBu_r', extend='both')
    m_b.drawcoastlines(linewidth=0.5)
    ax_b.set_xticks(lon_ticks)
    ax_b.set_yticks(lat_ticks)
    ax_b.set_xticklabels([f"{l}°E" if l!=0 else "0°" for l in lon_ticks], fontsize=11)
    ax_b.set_yticklabels([f"{l}°N" if l>0 else (f"{abs(l)}°S" if l<0 else "0°") for l in lat_ticks], fontsize=11)

cbar_ax_a = fig.add_axes([0.325, 0.67, 0.35, 0.015])
fig.colorbar(cs_a, cax=cbar_ax_a, orientation='horizontal', label='Historical Variance [℃$^2$]')

cbar_ax_b = fig.add_axes([0.325, 0.37, 0.35, 0.015])
fig.colorbar(cs_b, cax=cbar_ax_b, orientation='horizontal', label='Future - Historical Variance [℃$^2$]')

# -----------------------------------------------------------
# [ROW 3] Figure 2c: Variance Decomposition 
# -----------------------------------------------------------
from utils import contribution_4band 

for i, (model, n) in enumerate(zip(models, ens_nums)):
    ax = fig.add_subplot(gs[2, i])
    
    Var, Cov, VarG, Cont = contribution_4band(model, n)
    
    year_win = np.arange(1850 + window_len//2, 2100 - window_len//2)
    all_var = [Var[k]+Cov[k] for k in ['Tropics', 'NH', 'SH']]
    all_var_win = [np.convolve(v, np.ones(window_len)/window_len, mode='valid') for v in all_var]
    all_cont_win = np.convolve(Cont['Tropics'], np.ones(window_len)/window_len, mode='valid')

    lower = np.zeros_like(all_var_win[0])
    for j, color in enumerate(colors_c):
        upper = lower + all_var_win[j]
        ax.fill_between(year_win, lower*100, upper*100, color=color, alpha=0.85)
        ax.plot(year_win, upper*100, color='black', linewidth=1 if j<2 else 2.5)
        lower = upper

    ax.set_xlim(1850, 2100)
    ax.set_ylim(0, 5)
    ax.set_xlabel('Year', fontsize=15)
    
    if i == 0:
        ax.set_ylabel('SAT uncertainty\n[x10$^{-2}$ ℃$^2$]', fontsize=17)
    else:
        ax.set_yticklabels([])

    ax2 = ax.twinx()
    ax2.plot(year_win, all_cont_win*100, color='orangered', linewidth=3, linestyle='--')
    ax2.set_ylim(0, 100)
    if i == 3:
        ax2.set_ylabel('Contributions\nof Tropics [%]', fontsize=17, color='orangered', labelpad=15)
    else:
        ax2.set_yticklabels([])

handles = [plt.Rectangle((0,0),1,1, color=c) for c in colors_c]
fig.legend(handles, ['Tropics', 'NH', 'SH'], loc='lower center', ncol=3, 
           fontsize=20, bbox_to_anchor=(0.5, 0.02), frameon=False)

plt.savefig('../figures/Figure2.png', dpi=300, bbox_inches='tight')
plt.show()
