# tcga-brca-multiomics-subtyping
Unsupervised subtyping of TCGA-BRCA patients using RNA-seq expression (and later multi-omics) with PCA, t-SNE/UMAP, clustering, and survival analysis.

## Environment Setup (Homebrew Python + venv)

1. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

The main goals are:

1. Download and organize TCGA-BRCA RNA-seq and clinical data.
2. Perform quality control and dimensionality reduction (PCA, t-SNE, UMAP).
3. Discover transcriptional subtypes using unsupervised clustering.
4. Relate the discovered clusters to clinical variables (stage, receptor status) and survival.
5. (Phase 2) Integrate additional omics layers (methylation, CNV) to refine subtypes.

---

## 1. Project Structure

```text
tcga-brca-multiomics-subtyping/
│
├─ README.md
├─ LICENSE
├─ .gitignore
├─ environment.yml
│
├─ data/
│   ├─ raw/          # raw TCGA files (not tracked in git)
│   └─ processed/    # expression matrices, clinical tables
│
├─ notebooks/
│   ├─ 01_download_and_organize_data.ipynb
│   ├─ 02_expression_qc_and_pca.ipynb
│   ├─ 03_tsne_umap_and_clustering.ipynb
│   ├─ 04_clinical_associations_and_survival.ipynb
│   └─ 05_multiomics_extension_methylation_cnv.ipynb
│
└─ src/
    ├─ __init__.py
    ├─ config.py
    ├─ data_loading.py
    ├─ preprocessing.py
    ├─ dimensionality_reduction.py
    ├─ clustering.py
    └─ visualization.py
```
## Downloading TCGA-BRCA Data

The below link contains all the video tutorials for creating cohorts and using the various analyses tools within GDC:  
https://docs.gdc.cancer.gov/Data_Portal/Users_Guide/Video_Tutorials/

Use the GDC **Cohort Builder** to construct a cohort and download files.

### Required Filters

**Cohort Builder Filters**
- **General Filters (Project):** `TCGA-BRCA`
- **Biospecimen Filters (Tumor Descriptor):** `Primary`


**File Level Filters (in Repository)**
- **Data Category:** `Transcriptome Profiling`
- **Data Type:** `Gene Expression Quantification`

**File Level Filters for Clinical Data (in Repository)**
- **Data Category:** `Clinical`  
- **Data Category:** `Biospecimen` (optional but recommended)

### Download
1. Save the cohort.
2. Go to the **Files** tab for the cohort.
3. Export a **Manifest**.
4. Download using the GDC Data Transfer Tool:
   ```bash
   gdc-client download -m gdc_manifest.txt -d data/raw/

### (Optional) Add `gdc-client` to Your Homebrew Path

To run `gdc-client` from any folder without typing the full path, you may place
the binary inside a directory managed by Homebrew.

For Apple Silicon (M1/M2/M3):

```bash
mv gdc-client /opt/homebrew/bin/
```

## STAR Gene Expression File Format (TCGA RNA-seq)

Each TCGA STAR quantification file is a tab-separated table containing the
expression values for one sample. The key columns are:

- **gene_id** – Ensembl gene identifier (e.g., ENSG00000141510)
- **gene_name** – Human-readable gene symbol (e.g., TP53)
- **gene_type** – Gene category (protein_coding, lncRNA, etc.)

### Raw Count Columns
- **unstranded** – Raw Illumina read counts per gene.  
  This is the primary column used in our analysis.
- **stranded_first / stranded_second** – Used only for strand-specific libraries
  (TCGA-BRCA is generally unstranded).

### Normalized Expression Columns
- **tpm_unstranded** – TPM-normalized expression
- **fpkm_unstranded** – FPKM-normalized expression
- **fpkm_uq_unstranded** – Upper-quartile FPKM

### Which Values We Use
For PCA, UMAP, clustering, and downstream modeling, we use the **`unstranded`**
raw counts and apply log-transformation or TPM normalization ourselves.  
These counts originate from Illumina RNA-seq reads aligned and quantified using
the STAR pipeline.


