BioXpress Downloader Step
=========================

*Step 1 of the BioXpress pipeline*

The downloader step will use sample sheets obtained from `GDC Data Portal <https://portal.gdc.cancer.gov/repository>`_ to download raw counts from RNA-Seq for Primary Tumor and Normal Tissue in all available TCGA Studies.

**General Flow of Scripts**
---------------------------

get_data_all_samples.sh -> get_hits_into_dir.py -> merge_files_tumor_and_normal.sh

**Procedure**
-------------

*Downloader Step 1* : Get sample list files from the GDC Data Portal
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Summary*
"""""""""

Sample sheets are downloaded from the GDC data portal and used for the downstream scripts to obtain read count files.

*Method*
""""""""

Go to the `GDC Repository <https://portal.gdc.cancer.gov/repository>`_

Click on the button labeled ``Advanced Search`` on the upper right of the repository home page.

- All of the filters can also be selected manually using the search tree on the left side of the page at the link above. To select a files filter or a cases filter, that tab must be selected on the search bar

To get the Primary Tumor samples, enter the following into the query box

``files.analysis.workflow_type in ["HTSeq - Counts"]  and files.data_type in ["Gene Expression Quantification"]

and cases.samples.sample_type in ["Primary Tumor"] and cases.project.program.name in ["TCGA"]``

Click ``Submit Query``

The search results screen will now appear. On this screen, click ``Add All Files To Cart``
Then select the ``Cart`` on the upper right of the page.

Click ``Sample Sheet`` from the Cart page to download the Sample Sheet for the Primary Tumor samples.

- You will need to change the name for the sample sheet, otherwise when we download the sample sheet for Normal tissues it will have the same file name and overwrite the previous file. Add ``tumor`` or ``normal`` to the file names when downloaded.

Remove all samples from the cart, then repeat Step 1 for the Normal Tissue samples.

In the Advanced Search query box add enter the following for Normal Tissue samples:

``files.analysis.workflow_type in ["HTSeq - Counts"]  and files.data_type in ["Gene Expression Quantification"]

and cases.samples.sample_type in ["Solid Tissue Normal"] and cases.project.program.name in ["TCGA"]``

Once both Sample Sheets are downloaded, Primary Tumor and Normal Tissue, move both sample sheets to the server on which the pipeline will be ran, to the path ``/data/projects/bioxpress/$version/downloads/`` where $version one increment higher then the latest version of BioXpress i.e. latest version is ``v-4.0`` so new run will be ``v-5.0``.

*Downloader Step 2*: Run the script get_data_all_samples.sh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Summary*
"""""""""

The shell script get_data_all_samples.sh provides arguments to the python script get_data_all_samples.py. It generates a log file that is used to create directories and filter out TCGA studies with low sample numbers.

*Method*
""""""""

Edit the hard-coded paths in the script get_data_all_samples.sh

  - The shell script will call the python script once for the tumor samples and once for the normal sample, so for both tumor and normal you will need to specify the path to the appropriate sample sheet and the path to the log file

Edit a hard-coded path in the script get_data_all_samples.py

  - Edit the line (~line 44) ``path0 = "/data/projects/bioxpress/$version/downloads"`` with the version for your current run of bioxpress.

Run the shell script ``sh get_data_all_samples.sh``

*Output*
""""""""

After the script has completed, you will have a folder for each TCGA study with all read count files compressed into a file ``results.tar.gz``. You will also have three log files, one each for Tumor and Normal as well as a third log file that is the two combined ``get_data_all_samples.log``

*Downloader Step 3*: Run the script get_hits_into_dir.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Summary*
"""""""""

The python script get_hits_into_dir.py decompresses all read count files and uses the log file generated in the previous script to filter out all TCGA studies that have less than 10 Normal Tissue samples. Count files are generated and labeled as `intermediate` because they will be further manipulated in later Steps

*Method*
""""""""

Edit the hard-coded paths in get_hits_into_dir.py

  - Edit the line (line ~12) ``with open("/data/projects/bioxpress/$version/downloads/get_data_all_samples.log", 'r') as fil:`` with the version for your current run of BioXpress
    - Ensure that the log file is the joined log file from the previous script, it should contain information for both Primary Tumor and Solid Tissue normal
  - Edit the line (line ~44) ``topDir = "/data/projects/bioxpress/$version/downloads/"`` with the version for your current run of BioXpress

Run the python script ``python get_hits_into_dir.py``

*Output*
""""""""

For each TCGA study there will be a folder named ``$study_$sampletype_intermediate`` that contains a read count file for each sample within that study.

*Downloader Step 4*: Run the script merge_files_tumor_and_normal.sh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Summary*
"""""""""

The shell script merge_files_tumor_and_normal.sh provides arguments to the python script merge_files_tumor_and_normal.py. All read count files for Tumor and Normal from the intermediate folders are merged so that there is one read count file per study (All samples as fields and one row per gene) and one category file per study (defines whether a sample ID corresponds to Primary-Tumor or Solid Tissue Normal).

*Method*
""""""""

Edit the hard-coded paths in merge_files_tumor_and_normal.sh

- Specify the paths for the variables ``in_dir`` and ``out_dir``

Run the shell script ``sh merge_files_tumor_and_normal.sh``

*Output*
""""""""

The ``out_dir`` specified in merge_files_tumor_and_normal.sh contains two files per study, one for counts and one for categories. The counts files contains all read counts for that study for each gene and provide sample IDs as the fields. The categories file contains information on each sample ID as either Primary Tumor or Solid Tissue Normal.

For checking sample names and numbers lists from v-5.0, all lists and the sample log have been moved to the folder ``downloads/v-5.0/sample_lists``.
