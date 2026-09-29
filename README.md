<div align="center">
  
  # 🛰️ Umbra SAR Metadata Explorer & Data Curation Pipeline
  
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=22&pause=1500&color=2E86C1&center=true&vCenter=true&width=800&lines=Automated+Data+Curation+for+Field+Phenotyping;SAR+Data+for+Phytosanitary+Monitoring;Epidemiological+Modeling+of+Tar+Spot+in+Maize;Cloud-Native+Geomatics+Pipeline" alt="Typing SVG" />
  </a>

  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/AWS_S3-Open_Data-FF9900.svg?style=for-the-badge&logo=amazonaws&logoColor=white" alt="AWS">
    <img src="https://img.shields.io/badge/Pandas-Data_Processing-150458.svg?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  </p>
</div>

<hr>

## 📖 Project Overview

This repository contains an automated cloud-native pipeline designed for the extraction, curation, and exploratory data analysis (EDA) of Synthetic Aperture Radar (SAR) metadata from the Umbra Open Data Catalog. 

Built entirely in Python, this tool connects anonymously to AWS S3 buckets to filter high-volume spatial data without the overhead of downloading heavy image files (CPHD/SICD formats). It standardizes radar physical parameters—such as range resolution, incidence angles, and orbital configurations—into structured datasets ready for statistical analysis.

## 🔬 Research Context & Application

This pipeline serves as the foundational data ingestion layer for the **Purdue Maize digital platform**. By isolating the geometric and temporal variables of X-Band SAR acquisitions over the Purdue University Farm Plot, the curated metadata enables advanced **automated data curation for field phenotyping**. 

The structured outputs (CSV datasets and EDA visualizations) are directly applied to:
* **Phytosanitary Monitoring:** Establishing temporal SAR baselines to detect canopy structural changes.
* **Epidemiological Modeling:** Correlating SAR backscatter anisotropy and incidence angles with the onset and progression of Tar Spot in maize crops.

## ⚙️ Core Features

* **☁️ Serverless Data Extraction:** Bypasses local storage limits by reading `JSON/STAC v2` metadata files directly from AWS S3 into local RAM via `boto3`.
* **🛡️ Fault-Tolerant Parsing:** Implements robust error handling (`errors='coerce'`) to manage irregular timestamps, corrupted metadata nodes, and mixed legacy/STAC formats.
* **📊 Automated EDA Generation:** Instantly outputs statistical distributions (temporal acquisition frequency, incidence angle histograms, and resolution scatter plots) using `seaborn` and `matplotlib`.

## 🚀 Installation & Usage

### 1. Dependencies
Ensure you have Python installed, then set up your environment:

```bash
pip install boto3 pandas matplotlib seaborn
