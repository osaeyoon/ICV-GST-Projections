import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import t

models = ['ACCESS-ESM1-5', 'CanESM5', 'MIROC6', 'MPI-ESM1-2-LR']
ens_nums = [40, 25, 50, 30]
colors = ['#e78ac3', '#FF8000', '#04B431', '#01A9DB']
year = np.arange(1850, 2100)
window_len = 11

def process_model_data(model, ens_num):
    raw_data = []
    anom_data = []
    
    for i in range(1, ens_num + 1):
        fname = f"tas_Amon_{model}_ssp585_r{i}i1p1f1_1850-2099_aave.nc"
        with xr.open_dataset(fname) as ds:
            tas = ds['tas'].values - 273.15
            raw_data.append(tas)
            ref = np.mean(tas[0:1901-1850])
            anom_data.append(tas - ref)
            
    raw_data = np.array(raw_data)
    anom_data = np.array(anom_data)
    
    ens_mean_anom = np.mean(anom_data, axis=0)
    ens_var = np.var(raw_data, axis=0, ddof=1) 
    
    return anom_data, ens_mean_anom, ens_var

all_anom, all_mean, all_var = [], [], []
for m, n in zip(models, ens_nums):
    anom, m_mean, v = process_model_data(m, n)
    all_anom.append(anom)
    all_mean.append(m_mean)
    all_var.append(v)

# Berkeley Earth 
best_path = f"Berkeley_Earth_Surface_Temperature.nc"
with xr.open_dataset(best_path) as ds_best:
    monthly_ano = ds_best['monthly_anomaly'].values[0]
    
annual_ano_best = []
for i in range(5, len(monthly_ano), 12):
    annual_ano_best.append(np.mean(monthly_ano[i:i+12], axis=0))

tas_best = np.array(annual_ano_best)
ref_best = np.mean(tas_best[0:1901-1850])
tas_best -= ref_best

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))

# [Figure 1a] 
for i in range(len(models)):
    ax1.fill_between(year, np.min(all_anom[i], axis=0), np.max(all_anom[i], axis=0), color=colors[i], alpha=0.2)
    ax1.plot(year, all_mean[i], color=colors[i], linewidth=2.5, label=models[i])
ax1.plot(np.arange(1850, 1850+len(tas_best)), tas_best, color='black', linewidth=1, label='Berkeley Earth')
ax1.axhline(0, color='gray', zorder=0)
ax1.set_title("a) Annual GST anomalies", loc='left', fontsize=18, fontweight='bold')
ax1.set_ylim(-1, 8)

# [Figure 1b] 
year_win = np.arange(1850 + window_len//2, 2100 - window_len//2)
for i in range(len(models)):

    var_win = np.convolve(all_var[i], np.ones(window_len)/window_len, mode='valid')
    y_plot = var_win * 100 # x10^-2 
    
    slope, _, _, _, std_err = stats.linregress(year_win, y_plot)
    ci95 = t.ppf(0.975, len(year_win)-2) * std_err
    
    ax2.plot(year, all_var[i]*100, color=colors[i], alpha=0.15, linewidth=0.8)
    ax2.plot(year_win, y_plot, color=colors[i], linewidth=3, label=f"{models[i]} ({slope*1e3:.2f} ± {ci95*1e3:.2f} ×10$^{{-3}}$)")

ax2.set_title("b) GST ensemble variance", loc='left', fontsize=18, fontweight='bold')
ax2.set_ylabel('x10$^{-2}$ ℃$^2$', fontsize=15)
ax2.set_ylim(0, 5)
ax2.legend(loc='upper left', fontsize=10, frameon=True)

plt.tight_layout()
plt.savefig('../figures/Figure1.png', dpi=300)
plt.show()
