README FOR BIOXPRESS REMAINING STEPS

NOTE: Earlier steps of download, binning, QC, DESeq, mapping to DO terms, and summarizing DESeq results have been completed by Brian and should be documented elsewhere. If this is not the case, we can add additional details. Remaining steps are outlined below. 

1. RERUN FOR POOLED SUBTYPES
	
	- For each tissue with multiple subtypes (lung and kidney), rerun DESeq with ALL tissue samples. 

	- i.e. there should be one LUNG analysis that was analyzed by DESeq with all read counts from both TCGA-LUAD and TCGA-LUSC

2. AUTOMATE QC REVIEW 
	
	- QC plots have been printed for all runs, need to identify method for reviewing and making action based on QC findings

3. MAP TO DO TERMS AND DOIDS, UBERON TERMS AND UBERON IDS

	- Using CDO slim mapping table, map cancer types to DO terms and IDs
	
	- Using Uberon mapping table, map cancer types to Uberon anatomical entity names and IDs

4. TREND COUNTS (Brian did not write script for this yet)

	- For each pair of tumor/normal, quantify the per-pair fold change .

	- For each cancer type, count the number of pairs with increased fold changes, the number with decreased fold changes, and the number with indeterminate or no change. 

5. ANNOTATIONS

As done with BioMuta, append gene/protein level annotations to the results in a column labeled site_annotation so that entries can be filtered by annotation using the "Apply/Reset site filters" option. Annotations from https://www.uniprot.org/core/ have been sorted in the file "Prioritized annotations for Bioxpress.xlsx" available at /data/share/bioXpress/Prioritized annotations for BioXpress.xlsx

	- Take ONLY annotations that with designated "change_priority" of "1" in this file (annotations have been sorted for priority, 1 is the highest priority, others me may add later)

	- For gene/proten level annotations, annotation label is sufficient as is; EX: Enzyme

	- For site level annotations, annotation + site combo is preferred (the reason for this is because unlike BioMuta, BioXpress results are summarized at the gene level, not at the site level) EX: Binding_Site_Annotation 328 328 Heme (covalent; via 1 link)

6. LITERATURE MINING (UD - DEXTER; manual)

As with previous version of BioXpress, the results for a given gene should be mapped to results from DEXTER (literature mining for cancer expression). Updated DEXTER file available from https://data.oncomx.org/ONCOMXDS000004

	- Map DE analysis results to the values in the uniprotkb_ac column such that results for a queried gene in the interface will display all DEXTER hits for that gene in a separate table below the Differential Expression summary

	- Similarly, map results to the values in doid column such that results for a queried cancer type in the interface will display all DEXTER hits for that cancer in a separate table below the DE summary

	- UPDATE (IN PROGRESS) - Compare original manual list of PMIDs with DEXTER hits; any not contained need to be added to this section

	- Implement filter for literature mining for the following: Extraction Type - options are "Manual" or "Automatic-DEXTER"; Sentence Type - options are "A" "B" "C" or "D"

7. NORMAL EXPRESSION (Bgee)

As with previous version of BioXpress, the results for a given gene should be mapped to corresponding results from Bgee (normal expression for human and mouse). Updated Bgee file available at https://data.oncomx.org/ONCOMXDS000012

	- Map DE analysis results to the values in the uniprotkb_ac column such that results for a queried gene in the interface will display all Bgee hits for that gene in a separate table below the DEXTER summary

	- NOTE: EITHER we can combine the human and mouse tables and add column "species" since both tables are structured the same, OR we can have the two tables in separate tabs

	- Similarly, map results using the CDOslim_uberon_mapping file available at [HAYLEY VERIFY PATH]such that results for a queried cancer type in the interface will display all Bgee hits with an Uberon ID (or child Uberon ID) corresponding to that doid in a separate table below the DEXTER results for both human and mouse

	- Implement filter for normal expression for the following: Expression relative to gene and Expression relative to tissue - options for both are "HIGH" "MEDIUM" "LOW" "NA"; Species - current options are "Human" and "Mouse" but eventually will expand

8. DATABASE LOADING

This is above my technical level of expertise, however, you may be able to use some of the scripts Brian was using. It is not clear if he created new scripts or repurposed Yu Hu's scripts. I had provided the following file at /data/share/bioXpress/bioxpress_april_2019_schema_draft.xlsx as a potential schema outlying the types of information in BioXpress and how they related to each other. Please refer to it if it is helpful or ignore it otherwise.

9. INTERFACE CHANGES/CONSIDERATIONS

As included above, the main changes are implementing filters and updating the results for DE analysis, literature, and  normal expression.

	- SEARCH BY GENE
		- DE RESULTS
		- IMAGES
		- FILTERS
		- LITERATURE MINING
		- NORMAL EXPRESSION

	- SEARCH BY CANCER
		- DE RESULTS
		- IMAGES
		- FILTERS
		- LITERATURE MINING
		- NORMAL EXPRESSION
