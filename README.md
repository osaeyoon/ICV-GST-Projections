# ICV-GST-Projections
Code for the paper "Diagnosis of the contribution of internal climate variability to global surface temperature projection under future warming".

# Data Availability
Due to size constraints, the raw climate data files are not included in this repository. To fully reproduce the analysis, please download the datasets from their respective sources and place them in the data/raw/ directory:


CMIP6 Large Ensembles: ACCESS-ESM1-5, CanESM5, MIROC6, and MPI-ESM1-2-LR are available via the Earth System Grid Federation (ESGF) nodes (e.g., DKRZ and LLNL).


ERA5 Reanalysis: Near-surface temperature data are available from the Copernicus Climate Data Store.


Berkeley Earth: Observational surface temperature records are obtained from Berkeley Earth.

Environment Setup
To ensure reproducibility, a Conda environment file (environment.yml) is provided. This environment includes essential libraries for climate data analysis such as xarray, numpy, matplotlib, scipy, and eofs.

Clone this repository:

Bash
git clone [https://github.com/osaeyoon/ICV-GST-Projections.git](https://github.com/osaeyoon/ICV-GST-Projections.git)
cd ICV-GST-Projections
Create and activate the Conda environment:

Bash
conda env create -f environment.yml
conda activate icv_gst_env
How to Run
After setting up the environment and downloading the required raw data into data/raw/, execute the scripts in the following order to reproduce the analysis and figures:

Calculate Snapshot EOFs (SEOF):

Bash
python scripts/calc_seof.py
Generate Figures:

Bash
python scripts/fig1_gst_variance.py
python scripts/fig2_spatial_var.py
python scripts/fig3_seof_patterns.py
python scripts/fig4_regional_var.py
python scripts/fig5_mechanism.py
All generated plots will be saved in the figures/ directory.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Citation
If you use this code or data in your research, please cite both the paper and the Zenodo archive of this repository:

Paper: Oh, S.-Y., Yeh, S.-W., & Kirtman, B. P. (2026). Diagnosis of the contribution of internal climate variability to global surface temperature projection under future warming. Geophysical Research Letters, (In Press).

Code: Oh, S.-Y. (2026). Code for: Diagnosis of the contribution of internal climate variability to global surface temperature projection under future warming. Zenodo. https://www.google.com/url?sa=E&source=gmail&q=https://doi.org/10.5281/zenodo.xxxxxxx
