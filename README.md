# ICV-GST-Projections

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.xxxxxxx.svg)](https://doi.org/10.5281/zenodo.xxxxxxx)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the data processing, analysis, and visualization scripts required to reproduce the findings in the paper:
**"Diagnosis of the contribution of internal climate variability to global surface temperature projection under future warming"** by Sae-Yoon Oh, Sang-Wook Yeh, and Benjamin P. Kirtman.

## Abstract
Internal climate variability (ICV) is a critical source of uncertainty in global surface temperature (GST) projections. We found regional drivers of ICV in GST projections and investigate their evolution under anthropogenic forcing. Among four CMIP6 large ensemble simulations under historical and SSP5-8.5 scenarios, we focus on MIROC6 and CanESM5, which show contrasting behaviors of ICV related to GST behaviors. In MIROC6, ICV, quantified by ensemble variance, increases markedly from the historical to the future period, primarily driven by the tropical variability including El Niño-Southern Oscillation (ENSO). Conversely, CanESM5 exhibits stable ICV from the historical to the future period. In CanESM5, while both ENSO and Barents-Kara Sea ice are key drivers in the historical period, ENSO dominates in the future. These contrasts are associated with forced mean-state changes in tropical Pacific and North Atlantic sea surface temperature.

## Repository Structure

```text
.
├── README.md                  # Project overview, abstract, and instructions
├── LICENSE                    # MIT License
├── CITATION.cff               # Citation metadata for Zenodo and paper
├── environment.yml            # Conda environment configuration file
├── data/                      # Directory for data storage
│   ├── raw/                   # Raw data (CMIP6 LEs, ERA5, Berkeley Earth)
│   └── processed/             # Processed intermediate data (e.g., EOF results)
├── scripts/                   # Python scripts for core analysis and figure generation
│   ├── utils.py               # Common utility functions (area weighting, anomaly calculation)
│   ├── calc_seof.py           # Snapshot EOF calculation algorithm
│   ├── fig1_gst_variance.py   # Script to generate Figure 1
│   ├── fig2_spatial_var.py    # Script to generate Figure 2
│   ├── fig3_seof_patterns.py  # Script to generate Figure 3
│   ├── fig4_regional_var.py   # Script to generate Figure 4
│   └── fig5_mechanism.py      # Script to generate Figure 5
└── figures/                   # Output directory for high-resolution figures
```

## Data Availability
Due to size constraints, the raw climate data files are not included in this repository. To fully reproduce the analysis, please download the datasets from their respective sources and place them in the `data/raw/` directory:

* **CMIP6 Large Ensembles**: ACCESS-ESM1-5, CanESM5, MIROC6, and MPI-ESM1-2-LR are available via the Earth System Grid Federation (ESGF) nodes (e.g., [DKRZ](https://esgf-metagrid.cloud.dkrz.de/search/) and [LLNL](https://aims2.llnl.gov/search/cmip6/)).
* **ERA5 Reanalysis**: Near-surface temperature data are available from the [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels-monthly-means?tab=download).
* **Berkeley Earth**: Observational surface temperature records are obtained from [Berkeley Earth](http://berkeleyearth.org/data/).

## Environment Setup
To ensure reproducibility, a Conda environment file (`environment.yml`) is provided. This environment includes essential libraries for climate data analysis such as `xarray`, `numpy`, `matplotlib`, `scipy`, and `eofs`.

1. Clone this repository:
   ```bash
   git clone [https://github.com/osaeyoon/ICV-GST-Projections.git](https://github.com/osaeyoon/ICV-GST-Projections.git)
   cd ICV-GST-Projections
   ```

2. Create and activate the Conda environment:
   ```Bash
   conda env create -f environment.yml
   conda activate icv_gst_env
   ```

## How to Run
After setting up the environment and downloading the required raw data into data/raw/, execute the scripts in the following order to reproduce the analysis and figures:

1. Calculate Snapshot EOFs (SEOF):
   ```Bash
   python scripts/calc_seof.py
   ```

2. Generate Figures:
   ```Bash
   python scripts/figure1.py
   python scripts/figure2.py
   python scripts/figure3.py
   python scripts/figure4.py
   python scripts/figure5.py
   ```

All generated plots will be saved in the figures/ directory.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Citation
If you use this code or data in your research, please cite both the paper and the Zenodo archive of this repository:

* Paper: Oh, S.-Y., Yeh, S.-W., & Kirtman, B. P. (2026). Diagnosis of the contribution of internal climate variability to global surface temperature projection under future warming. Geophysical Research Letters, (In Press).

* Code: Oh, S.-Y. (2026). Code for: Diagnosis of the contribution of internal climate variability to global surface temperature projection under future warming. 
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19456453.svg)](https://doi.org/10.5281/zenodo.19456453)
