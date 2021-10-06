Major Changes from v-4.0
========================

*Major updates to the BioXpress from the previous version (v-4.0)*

**Tumor samples added for each tissue**
---------------------------------------

+----------------+----------------+----------------+
| Tissue         | TCGA Studies   | New Samples    |
+================+================+================+
| Bladder        | BLCA           | 126            |
+----------------+----------------+----------------+
| Breast         | BRCA           | 159            |
+----------------+----------------+----------------+
| Colorectal     | COAD/READ      | 159 (141/18)   |
+----------------+----------------+----------------+
| Esophageal     | ESCA           | 25             |
+----------------+----------------+----------------+
| Head and Neck  | HNSC           | 118            |
+----------------+----------------+----------------+
| Kidney         | KICH/KIRP/KIRC | 289(15/82/192) |
+----------------+----------------+----------------+
| Liver          | LIHC           | 169            |
+----------------+----------------+----------------+
| Lung           | LUAD/LUSC      | 264 (174/90)   |
+----------------+----------------+----------------+
| Prostate       | PRAD           | 116            |
+----------------+----------------+----------------+
| Stomach        | STAD           | 22             |
+----------------+----------------+----------------+
| Thyroid        | THCA           | 176            |
+----------------+----------------+----------------+
| Uterine        | UCEC           | 216            |
+----------------+----------------+----------------+

**Mapping files updated to reflect most recent mapping of DOIDs to UBERON IDs.**
--------------------------------------------------------------------------------

The following is a list of the current cancer tissue (DOID) to healthy tissue (UBERON ID) mapping:

+------------------------------------+------------------------------------+
| DO Name (DOID)                     | UBERON Name (UBERON ID)            |
+====================================+====================================+
| Stomach Cancer (DOID:10534)        | Stomach (UBERON:0000945)           |
+------------------------------------+------------------------------------+
| Thyroid Cancer (DOID:1781)         | Thyroid Gland (UBERON:0002046)     |
+------------------------------------+------------------------------------+
| Esophageal Cancer (DOID:5041)      | Esophagus (UBERON:0001043)         |
+------------------------------------+------------------------------------+
| Kidney Cancer (DOID:263)           | Adult Mammalian Kidney             |
|                                    |                                    |
|                                    | (UBERON:0000082)                   |
+------------------------------------+------------------------------------+
| Lung Cancer (DOID:1324)            | Lung (UBERON:0002048)              |
+------------------------------------+------------------------------------+
| Uterine Cancer (DOID:363)          | Uterine Cervix (UBERON:0000002)    |
+------------------------------------+------------------------------------+
| Bladder Cancer (DOID:11054)        | Urinary Bladder (UBERON:0001255)   |
+------------------------------------+------------------------------------+
| Prostate Cancer (DOID:10283)       | Prostate Gland (UBERON:0002367)    |
+------------------------------------+------------------------------------+
| Colorectal Cancer (DOID:9256)      | Colon (UBERON:0001155)             |
|                                    |                                    |
|                                    | Rectum (UBERON:0001052)            |
+------------------------------------+------------------------------------+
| Liver Cancer (DOID:3571)           | Liver (UBERON:0002107)             |
+------------------------------------+------------------------------------+
| Breast Cancer (DOID:1612)          | Thoracic Mammary Gland             |
|                                    | (UBERON:0005200)                   |
+------------------------------------+------------------------------------+
| Head and Neck  Cancer (DOID:11934) | Oral Cavity (UBERON:0000167)       |
+------------------------------------+------------------------------------+

**Automatic alphabetical re-ordering of count matrices for DESeq2**
-------------------------------------------------------------------

Due to the added samples in v-5.0, the ordering of samples in the count matrices needed for DESeq2 was disrupted and DESeq2 was producing randomized results. Column and row names in count matrices are now re-ordered as part of the `DESeq.R` script, so that samples are aligned correctly. This re-ordering should account for instances of added samples in future versions.

**Issue Running DESEq per case**
--------------------------------

The step for DESeq per case was performed, however the results were not used to calculate subjects up/down/total in the publisher step, as was the case in v-4.0. Also, a final publisher file per case was not generated.

The run_per_case.py script performs DESeq analysis using both the tumor and normal count files per case. For most cases, there is only one tumor counts file and one normal counts file. DESeq encounters an error when running analysis with a sample size of 1 per group:

``Error in checkForExperimentalReplicates(object, modelMatrix):```

`The design matrix has the same number of samples and coefficients to fit, so estimation of dispersion is not possible. Treating samples as replicates was deprecated in v1.20 and no longer supported since v1.22.`

The DESeq2 vignette also mentions DESeq analysis with no replicates in their `FAQ <http://bioconductor.org/packages/devel/bioc/vignettes/DESeq2/inst/doc/DESeq2.html#can-i-use-deseq2-to-analyze-a-dataset-without-replicates>`_:

``Can I use DESeq2 to analyze a dataset without replicates? No. This analysis is not possible in DESeq2.``

This is likely sue to the read count normalization model used by DESeq. DESeq's model contains a variable called the dispersion estimate, which relies on the variance of the one sample's read counts for a gene to the mean read count for that gene across the whole group (condition). If there are no other replicates on the group then there is no comparison to be made and no normalization can occur.

Even for cases that have only 2-3 replicates, the significance of the DE analysis should be heavily scrutinized as such a low replicate number is not a standard statistical practice, because low sample sizes may lead to an increase in false positive and false negatives.
