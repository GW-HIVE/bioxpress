BioXpress Publisher Step
========================

*Step 4 of the BioXpress pipeline.*

**General Flow of Scripts**
---------------------------

de-publish-per-study.py -> de-publish-per-tissue.py

**Procedure**
-------------

*Publisher Step 1* : Run the script de-publish-per-study.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Summary*
"""""""""

The python script de-publish-per-study.py takes the output from running DESeq in the previous step for each TCGA study and combines into one master file.

*Method*
""""""""

Edit the hard-coded paths in the script de-publish-per-study.py

 - Specify the ``in_file`` for the disease ontology mapping file (line ~26)
 - Specify the ``in_file`` for the uniprot accession id (protein id) mapping file (line ~40)
 - Specify the ``in_file`` for the refseq mapping file (line ~51)
 - Specify the ``in_file`` for the list of TCGA studies to include in the final output (line ~72)
 - Specify the ``deseq_dir`` for the folder containing all deseq output (line ~80)
 - Specify the path to write the output (line ~135)

Run the python script ``python de-publish-per-study.py``

*Output*
""""""""

A csv file with the DEseq output for all TCGA studies, mapped to DO IDs, uniprot accession ids, and refseq ids. The path is specified in the script as one of the hard-coded lines edited during the method.

*Publisher Step 2* : Run the script de-publish-per-tissue.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Summary*
"""""""""

The python script de-publish-per-tissue.py takes the output from running DESeq in the previous step for each tissue and combines into one master file.

*Method*
""""""""

Edit the hard-coded paths in the script de-publish-per-study.py

 - Specify the ``in_file`` for the disease ontology mapping file (line ~26)
 - Specify the ``in_file`` for the uniprot accession id (protein id) mapping file (line ~40)
 - Specify the ``in_file`` for the refseq mapping file (line ~51)
 - Specify the ``in_file`` for the list of tissues to include in the final output (line ~72)
 - Specify the ``deseq_dir`` for the folder containing all deseq output (line ~80)
 - Specify the path to write the output (line ~135)

*Output*
""""""""

A csv file with the DEseq output for all tissues, mapped to DO IDs, uniprot accession ids, and refseq ids. The path is specified in the script as one of the hard-coded lines edited during the method.
