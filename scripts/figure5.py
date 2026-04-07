import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

models_to_plot = ['MIROC6', 'CanESM5']
colors = {'MIROC6': '#04B431', 'CanESM5': '#FF8000'}
model_keys = {'MIROC6': 'MIR', 'CanESM5': 'CAN'}

ds_5a = xr.open_dataset("fig5a_zonal_sst_gradient_analysis.nc")
ds_5b = xr.open_dataset("fig5b_pacific_linkage_full_results.nc")
ds_5c = xr.open_dataset("fig5c_north_atlantic_sst_analysis.nc")
ds_5d = xr.open_dataset("fig5d_atlantic_arctic_linkage_analysis.nc")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
plt.subplots_adjust(hspace=0.35, wspace=0.3)

# -----------------------------------------------------------
# [5a] Zonal SST Gradient Change (Bar)
# -----------------------------------------------------------
ax = axes[0, 0]
vals_5a = [ds_5a.sst_grad_change.sel(model=m).values for m in models_to_plot]
ax.bar([1, 2], vals_5a, color=[colors[m] for m in models_to_plot], 
       width=0.5, hatch='//', edgecolor='black', linewidth=2)

ax.set_ylabel("Change in zonal SST gradient [℃]", fontsize=16)
ax.set_xticks([1, 2])
ax.set_xticklabels(models_to_plot, fontsize=15)
ax.set_ylim(-1.0, 0)
ax.set_title("a) Zonal SST gradient change", loc='left', fontsize=19, fontweight='bold')

# -----------------------------------------------------------
# [5b] Pacific Variability Linkage (Scatter + Saved Regression Line)
# -----------------------------------------------------------
ax = axes[0, 1]

for m in models_to_plot:
    key = model_keys[m]
    
    x = ds_5b[f"{key}_zonal_grad_change"].values
    y = ds_5b[f"{key}_sst_var_change"].values 

    ax.scatter(x, y, color=colors[m], marker='X', s=120, alpha=0.7, label=m)
    ax.scatter(np.nanmean(x), np.nanmean(y), color='black', marker='*', s=400, edgecolors='white', zorder=5)
    
    xx_ticks = ds_5b.xx_ticks.values
    reg_line = ds_5b.regression_line.sel(model=m).values
    
    slope = ds_5b.regression_slope.sel(model=m).values
    
    ax.plot(xx_ticks, reg_line, color=colors[m], linewidth=2.5, alpha=0.8)

ax.set_xlabel('Change in zonal SST gradient [℃]', fontsize=16)
ax.set_ylabel('Change in Niño3.4 variability [x10$^{-2}$ ℃$^2$]', fontsize=15)

ax.set_xlim(-1.2, -0.2)
ax.set_ylim(-0.5, 2.0)
ax.axhline(0, color='gray', linestyle='--', linewidth=1)
ax.set_title("b) Pacific variability linkage", loc='left', fontsize=19, fontweight='bold')

# -----------------------------------------------------------
# [5c] North Atlantic SST Change (Bar)
# -----------------------------------------------------------
ax = axes[1, 0]
vals_5c = [ds_5c.na_sst_change.sel(model=m).values for m in models_to_plot]
ax.bar([1, 2], vals_5c, color=[colors[m] for m in models_to_plot], 
       width=0.5, hatch='//', edgecolor='black', linewidth=2)

ax.set_ylabel("Change in North Atlantic SST [℃]", fontsize=16)
ax.set_xticks([1, 2])
ax.set_xticklabels(models_to_plot, fontsize=15)
ax.set_ylim(0, 6)
ax.set_title("c) North Atlantic SST change", loc='left', fontsize=19, fontweight='bold')

# -----------------------------------------------------------
# [5d] Atlantic-Arctic Linkage (Scatter)
# -----------------------------------------------------------
ax = axes[1, 1]
for m in models_to_plot:
    key = model_keys[m]
    x = ds_5d[f"{key}_na_sst_change"].values
    y = ds_5d[f"{key}_bks_sic_var_change"].values
    
    ax.scatter(x, y, color=colors[m], marker='X', s=120, alpha=0.7, label=m)
    ax.scatter(np.nanmean(x), np.nanmean(y), color='black', marker='*', s=400, edgecolors='white', zorder=5)

ax.set_xlabel('Change in North Atlantic SST [℃]', fontsize=16)
ax.set_ylabel('Change in BKS-SIC variability [%$^2$]', fontsize=16)
ax.set_xlim(2, 6)
ax.set_ylim(-120, 40)
ax.axhline(0, color='gray', linestyle='--', linewidth=1)
ax.set_title("d) Atlantic-Arctic linkage", loc='left', fontsize=19, fontweight='bold')

for ax in axes.flat:
    ax.tick_params(labelsize=13)
    ax.grid(linestyle=':', alpha=0.6)
    ax.legend(loc='upper right', fontsize=12)

plt.tight_layout()
plt.savefig("../figures/Figure5.png", dpi=300)
plt.show()
