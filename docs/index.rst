BioXpress Pipeline v-5.0 README
===============================

.. toctree::
   downloader
   annotation
   deseq
   publisher
   updates
   oncomx_glygen


Last Updated August 2021 by Ned Cauley

Description
-----------

The BioXpress pipeline takes raw count data from TCGA studies for both Primary Tumor and Normal Tissue and performs differential expression.

The TCGA studies included in the BioXpress pipeline are (by **tissue**):

- **Bladder**
  - TCGA-BLCA (Bladder urothelial carcinoma)
- **Breast**
  - TCGA-BRCA (Breast invasive carcinoma)
- **Colorectal**
  - TCGA-COAD (Colon adenocarcinoma)
  - TCGA-READ (Rectum adenocarcinoma)
- **Esophageal**
  - TCGA-ESCA (Esophageal carcinoma)
- **Head and Neck**
  - TCGA-HNSC (Head and Neck squamous cell carcinoma)
- **Kidney**
  - TCGA-KICH (Kidney Chromophobe)
  - TCGA-KIRP (Kidney renal papillary cell carcinoma)
  - TCGA-KIRC (Kidney renal clear cell carcinoma)
- **Liver**
  - TCGA-LIHC (Liver hepatocellular carcinoma)
- **Lung**
  - TCGA-LUAD (Lung adenocarcinoma)
  - TCGA-LUSC (Lung squamous cell carcinoma)
- **Prostate**
  - TCGA-PRAD (Prostate adenocarcinoma)
- **Stomach**
  - TCGA-STAD (Stomach adenocarcinoma)
- **Thyroid**
  - TCGA-THCA (Thyroid carcinoma)
- **Uterine**
  - TCGA-UCEC (Uterine Corpus Endometrial Carcinoma)

Running the Pipeline
--------------------

To run the BioXpress pipeline, you need to download the scripts from the HIVE Lab github repo:
`GW HIVE Backend Code Repository <https://github.com/GW-HIVE/bioxpress>`_
If running Bioxpress on a HIVE Lab server (such as glygen-vm-dev), place scripts in your user folder ``/home/$yourusername/``.
Data and other output from the scripts is stored in ``/data/projects/bioxpress/``.

Pipeline Overview
-----------------

**Step 1: Downloader**

The downloader step will use sample sheets obtained from [GDC Data Portal](https://portal.gdc.cancer.gov/repository) to download raw counts from RNA-Seq for Primary Tumor and Normal Tissue in all available TCGA Studies.

Index for downloader: 

.. toctree::
    downloader

**Step 2: Annotation**

The annotation step maps transcripts to gene symbols and creates the organized read count and category files used in the DESeq step.

Index for annotation:

.. toctree::
    annotation

**Step 3: DESeq**

DESeq is used to calculated differential expression and determine statistical significance.

Index for DESeq:

.. toctree::
    deseq

**Step 4: Publisher**

Differential expression results for each tissue are combined into one master dataset.

Index for publisher: 

.. toctree::
    publisher

**Other documentation**

.. toctree::
   updates
   oncomx_glygen


