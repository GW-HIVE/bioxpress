BioXpress DESeq step
====================

*Step 3 of the BioXpress pipeline.*

**General Flow of Scripts**
---------------------------

run_per_study.py -> run_per_tissue.py -> run_per_case.py

**Procedure**
-------------

*DESeq step 1:* Run the script run_per_study.sh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Summary*
"""""""""

The python script run_per_study.py provides arguments to the R script deseq.R. The count and category files generated  from the Annotation step are used to calculate differential expression and statistical significance.
The result is a series of files per tissue including the normalized reads (DESeq normalization method), the DE results and significance, and QC files such as the PCA plot.

  - Note: this step is time consuming (~2-3 hours of run time)

*Method*
""""""""

Edit the hard-coded paths in the script run_per_tissue.py

  - Specify the ``in_dir`` to be the folder containing the final output files of the Annotation steps for per study
  - Specify the ``out_dir``
  - Ensure that the file ``list_files/studies.csv`` contains all of the tissues you wish to process
    - Note: the studies can be run separately (in the event that 2-3 hours cannot be dedicated to run the all studies at once) by creating separate dat files with specific tissues to run

Run the shell script ``sh run_per_study.sh``

  - Note: the R libraries specified in deseq.R will need to be installed if running on a new server or system, as these installations are not included in the scripts

*Output*
""""""""

A set of files:

  - log file
  - deSeq_reads_normalized.csv
    - Normalized read counts (DESeq normalization method applied)
  - results_significance.csv
    - log2fc differential expression results and statistical significance (t-test)
  - dispersion.png
  - distance_heatmap.png
  - pca.png
    - Principal component analysis plot, important for observing how well the Primary Tumor and Solid Tissue Normal group together

*DESeq Step 2* : Run the script run_per_tissue.sh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Summary*
"""""""""

The python script run_per_tissue.py provides arguments to the R script deseq.R. The count and category files generated from the Annotation step are used to calculate differential expression and statistical significance. The result is a series of files per study including the normalized reads (DESeq normalization method), the DE results and significance, and QC files such as the PCA plot.

  - Note: this step is time consuming (~2-3 hours of run time)

*Method*
""""""""

Edit the hard-coded paths in the script run_per_tissue.py

  - Specify the ``in_dir`` to be the folder containing the final output files of the Annotation steps for per tissue
  - Specify the ``out_dir``
  - Ensure that the file ``list_files/tissue.dat`` contains all of the tissues you wish to process
    - Note: the tissues can be run separately (in the event that 2-3 hours cannot be dedicated to run the all tissues at once) by creating separate dat files with specific tissues to run

Run the shell script ``sh run_per_tissue.sh``

*Output*
""""""""

A set of files:

  - log file
  - deSeq_reads_normalized.csv
    - Normalized read counts (DESeq normalization method applied)
  - results_significance.csv
    - log2fc differential expression results and statistical significance (t-test)
  - dispersion.png
  - distance_heatmap.png
  - pca.png
    - Principal component analysis plot, important for observing how well the Primary Tumor and Solid Tissue Normal group together

*DESeq Step 3* : Run the script run_per_case.sh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Summary*
"""""""""

The python script run_per_case.py provides arguments to the R script deseq.R. The count and category files generated from the Annotation step are used to calculate differential expression and statistical significance. The result is a series of files per case including the normalized reads (DESeq normalization method), the DE results and significance, and QC files such as the PCA plot.

  - Note: this step is time consuming (~2-3 hours of run time)

*Method*
""""""""

Edit the hard-coded paths in the script run_per_case.py

  - Specify the ``in_dir`` to be the folder containing the final output files of the Annotation step for per_case
  - Specify the ``out_dir``
  - Ensure that the file ``list_files/cases.csv`` contains all of the cases you wish to process
    - Note: the cases can be run separately (in the event that 2-3 hours cannot be dedicated to run the all tissues at once) by creating separate dat files with specific cases to run

Run the shell script ``sh run_per_tissue.sh``

*Output*
""""""""

A set of files:

 - log file
 - deSeq_reads_normalized.csv
   - Normalized read counts (DESeq normalization method applied)
 - results_significance.csv
   - log2fc differential expression results and statistical significance (t-test)
 - dispersion.png
 - distance_heatmap.png
 - pca.png
   - Principal component analysis plot, important for observing how well the Primary Tumor and Solid Tissue Normal group together
