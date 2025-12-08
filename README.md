# tcga-brca-multiomics-subtyping
Unsupervised subtyping of TCGA-BRCA patients using RNA-seq expression (and later multi-omics) with PCA, t-SNE/UMAP, clustering, and survival analysis.

## Environment Setup (Homebrew Python + venv)

- Install dependencies on macOS (assumes Homebrew Python):
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
  ```
- If you manage environments with `pyenv`, adjust the `python3` command accordingly (`pyenv local 3.11.x` before creating the venv).
- For Linux environments, the same commands apply; just make sure a suitable Python build is available (`apt install python3-venv` if needed).
- When working in notebooks, remember to install the IPython kernel inside the venv if you want to select it explicitly:
  ```bash
  python -m ipykernel install --user --name tcga-brca --display-name "tcga-brca (venv)"
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
    └─ plotting.py
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
4. Download using the GDC Data Transfer Tool and run the below in your terminal:
   ```bash
   gdc-client download -m gdc_manifest.txt -d data/raw/
   ```

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

## Clinical/Biospecimen XML Files

TCGA distributes rich patient metadata as XML files. XML (eXtensible Markup Language) is a hierarchical text format composed of nested tags (elements) with optional attributes and text content. Each XML document in this project adheres to the NCI TCGA schemas (`https://docs.gdc.cancer.gov/Data_Dictionary/viewer/#?_top=1`). We parse them with Python’s `xml.etree.ElementTree` helpers inside notebook `01_download_and_organize_data.ipynb`, flattening tags into `pandas` tables. The two key XML families we currently surface are:

- **Clinical (`nationwidechildrens.org_clinical.*.xml`)**: Patient-level records (demographics, diagnosis, receptor status, therapies, follow-up). Each file corresponds to one `bcr_patient_barcode` / `bcr_patient_uuid`. We extract a patient metadata table plus follow-up/drug sub-tables for downstream joins.
- **Biospecimen (`nationwidechildrens.org_biospecimen.*.xml`)**: Sample-level inventories (sample/portion/aliquot barcodes, UUIDs, analyte metadata). These files bridge expression columns to patients: `bcr_sample_uuid` matches the expression matrix column names, while `bcr_patient_barcode` ties back to the clinical table.

Each XML document contains nested sections (e.g., `<patient>`, `<samples>`, `<portions>`). In the notebook we:

1. Build manifests (DataFrames) of all XML files under `data/raw/clinical data/`.
2. Parse a sample file from each category via `xml.etree.ElementTree`, recursively flattening tags into dictionaries.
3. Display the resulting `pandas` tables (patient-level data, nested biospecimen entries, etc.) to understand fields before designing loaders.

When you need to integrate XML data, re-use the notebook parsing logic (or promote it into `src/data_loading.py`) so that downstream analyses can join expression matrices on the appropriate identifiers (`bcr_sample_uuid` ↔ columns, `bcr_patient_barcode` ↔ patient clinical metadata).

## Linking Biospecimen JSON to STAR Metadata

The GDC cart download also includes JSON manifests (e.g., `metadata.cart.*.json` for STAR counts, `biospecimen.cart.*.json` for biospecimen files). In `01_download_and_organize_data.ipynb` we:

1. Normalize the STAR metadata JSON to a DataFrame (`metadata_df`) and attach the nested `associated_entities` / `analysis.input_files` columns to the expression manifest (`expression_index`) using helper utilities from `src/notebook_utils.py`.
2. Load the biospecimen cart JSON (`biospecimen_metadata_df`) and traverse every case → sample → portion → analyte → aliquot entry to build an aliquot-level manifest.
3. Join the resulting aliquot rows to the expression manifest on the aliquot submitter ID (`TCGA-…-…`) so that each STAR count file is enriched with the biospecimen context (sample type, analyte metadata, aliquot quantities, etc.).

This linkage allows you to move seamlessly from a column in the expression matrix to its aliquot barcode/UUID, and then to the patient-level clinical table for downstream analyses.
