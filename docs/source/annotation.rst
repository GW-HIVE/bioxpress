BioXpress Annotation Step
=========================

*Step 2 of the BioXpress pipeline*

**General Flow of Scripts**
---------------------------

merge_per_study.sh -> merge_per_tissue.py -> split_per_case.py

**Procedure**
-------------

*Annotation Step 1* : Run the script merge_per_study.sh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Summary*
"""""""""

The shell script merge_per_study.sh provides arguments to the python script merge_per_study.py. This step maps all ENSG IDs to gene symbols based on a set of mapping files. It will also filter out microRNA genes. The steps for creating the mapping files are described in the annotation README.

*Method*
""""""""

The mapping files are available in the folder ``/annotation/mapping_files/`` and moved to a similar path in the version of your run of Bioxpress

  - mart_export.txt
  - mart_export_remap_retired.txt
  - new_mappings.txt

Edit the hard-coded paths in merge_per_study.sh

  - Specify the ``in_dir`` as the folder containing the final output of the Downloader step, count and category files per study.
  - Specify the ``out_dir`` so that it is now in the top folder ``generated/annotation`` not ``downloads``
  - Specify the location of the mapping files downloaded in the previous sub-step

Validate the file ``studies.dat`` contains all studies that you wish to process

Run the shell script ``sh merge_per_study.sh``

*Output*
""""""""

All ENSG IDs in the counts files have been replaced by gene symbols in new count files located in the `out_dir`. Transcripts have also been merged per gene and microRNA genes filtered out. The categories files remain the same but are copied over to the annotation folder.

*Annotation Step 2* : Run the script merge_per_tissue.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Summary*
"""""""""

The python script merge_per_tissue.py takes all files created by the script merge_per_study.sh and merges these files based on the file tissues.csv, which assigns TCGA studies to specific tissues terms.

*Method*
""""""""

Download the files tissues.csv from the previous version of BioXpress at ``/data/projects/bioxpress/$version/generated/misc/tissues.csv`` and place in a similar folder in the version of your run of BioXpress

Edit the hard-coded paths in merge_per_tissue.py

  - Edit the line (line ~23) ``in_file = "/data/projects/bioxpress/v$version/generated/misc/tissues.csv"`` with the version for your current run of BioXpress
  - Edit the line (line ~36) ``out_file_one = "/data/projects/bioxpress/v-5.0/generated/annotation/per_tissue/%s.htseq.counts" % (tissue_id)`` with the version for your current run of BioXpress
  - Edit the line (line ~37) ``out_file_two = "/data/projects/bioxpress/v-5.0/generated/annotation/per_tissue/%s.categories" % (tissue_id)`` with the version for your current run of BioXpress
  - Edit the line (line ~45) ``in_file = "/data/projects/bioxpress/v-5.0/generated/annotation/per_study/%s.categories" % (study_id)`` with the version for your current run of BioXpress
  - Edit the line (line ~52) ``in_file = "/data/projects/bioxpress/v-5.0/generated/annotation/per_study/%s.htseq.counts" % (study_id)`` with the version for your current run of BioXpress

Run the python script ``python merge_per_tissue.py``

*Output*
""""""""

Read count and category files are generated for each tissue specified in the tissues.csv file.

*Annotation Step 3* : Run the script split_per_case.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


*Summary*
"""""""""

The python script split_per_case.py takes case and sample IDs from the sample sheets downloaded from the GDC data portal and splits annotation data so that there is one folder per case with only that case's annotation data.

*Method*
""""""""

Edit the hard-coded paths in split_per_case.py

  - Edit the line (line ~29) ``in_file = "/data/projects/bioxpress/v-5.0/generated/misc/studies.csv"`` with the version for your current run of BioXpress
  - Edit the line (line ~38) ``in_file = "/data/projects/bioxpress/v-5.0/downloads/sample_list_from_gdc/gdc_sample_sheet.primary_tumor.tsv"`` with the version for your current run of BioXpress as well as the same of the sample sheet for tumor samples downloaded from the GDC data portal
  - Edit the line (line ~57) ``in_file = "/data/projects/bioxpress/v-5.0/downloads/sample_list_from_gdc/gdc_sample_sheet.solid_tissue_normal.tsv"`` with the version for your current run of BioXpress as well as the same of the sample sheet for normal samples downloaded from the GDC data portal
  - Edit the line (line ~81) ``out_file_one = "/data/projects/bioxpress/v-5.0/generated/annotation/per_case/%s.%s.htseq.counts" % (study_id,case_id)`` with the version for your current run of BioXpress
  - Edit the line (line ~82) ``out_file_two = "/data/projects/bioxpress/v-5.0/generated/annotation/per_case/%s.%s.categories" % (study_id,case_id)`` with the version for your current run of BioXpress
  - Edit the line (line ~85) ``in_file = "/data/projects/bioxpress/v-5.0/generated/annotation/per_study/%s.htseq.counts" % (study_id)`` with the version for your current run of BioXpress

Run the python script ``python split_per_case.py``

*Output*
""""""""

A folder is generated for each case ID that has a tumor sample and a normal tissue sample. Two files are generated per case: read counts and categories. These files are needed to run DESeq per case.
