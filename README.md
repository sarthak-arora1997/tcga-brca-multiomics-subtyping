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
## Understanding TCGA-BRCA on the GDC Portal

Before working with the data, it is useful to understand how the GDC Portal organizes
information for a TCGA project, such as **TCGA-BRCA (The Cancer Genome Atlas – Breast Invasive Carcinoma)**.

The GDC Project page summarizes the composition of the dataset and reports how many
patients ("cases") and how many files exist for each type of molecular data. These
summaries help determine which modalities are widely available and which are sparse,
allowing informed decisions when constructing a cohort for multi-omics analysis.

### 1. Cases vs. Files

Each TCGA project contains:
- **Cases** → individual patients.
- **Files** → data files generated for those patients (RNA-seq files, CNV files, clinical files, etc.).

In the project summary, you will see two columns:

- **Cases (n = X)**:  
  The number of patients that have *at least one* file of that data type.

- **Files (n = Y)**:  
  The number of individual data files belonging to that category.

### 2. Data Categories

Data Categories describe *what kind of biological data* is available. Examples include:
- **Transcriptome Profiling** (RNA-seq)
- **DNA Methylation**
- **Copy Number Variation**
- **Simple Nucleotide Variation** (mutations)
- **Clinical**
- **Proteome Profiling**

The "Cases" percentage shows how many patients have that type of data.  
The "Files" percentage shows how much of the total dataset consists of files from that category.

Large coverage (e.g., RNA-seq, methylation, CNV) is ideal for multi-omics projects.

### 3. Experimental Strategies

Experimental Strategies describe the *laboratory technology* used to generate a data type. Examples:
- **RNA-Seq** → gene expression
- **WXS (Whole Exome Sequencing)** → somatic mutations
- **Methylation Array** → epigenetic methylation
- **Genotyping Array** → copy number variation
- **Reverse Phase Protein Array** → proteomics
- **WGS (Whole Genome Sequencing)**
- **miRNA-Seq**
- **ATAC-Seq**

Each strategy lists:
- **Cases** → number of patients with data generated using that technology  
- **Files** → total files produced by that technology

### 4. How This Guides Your Analysis

These summaries help guide project design:
- **RNA-seq** has almost complete coverage → suitable for unsupervised clustering (PCA, UMAP).
- **DNA Methylation** and **CNV** also have near-complete coverage → good for multi-omics integration.
- **Proteomics** has ~80% coverage → useful, but not ideal for analyses requiring full cohort overlap.

In practice, most workflows begin with:
1. **RNA-seq** + **Clinical** data for initial subtyping.
2. Add **Methylation** and **CNV** once the expression-based framework is established.

### 5. Where to Download Data (Repository vs. Project Page)

While the **Project** page provides summaries, **actual data files are downloaded from the
"Repository" section** of the GDC Portal. This is where filters (Project, Data Category,
Data Type, Workflow Type) are applied and files are added to the **Cart** for download.
