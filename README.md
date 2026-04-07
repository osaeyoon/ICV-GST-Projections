# ICV-GST-Projections
Code for the paper "Diagnosis of the contribution of internal climate variability to global surface temperature projection under future warming".

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
