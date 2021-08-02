#!/bin/bash

#cancers="GBM"
cancers="LAML LGG LIHC LUSC PAAD PGPC READ SARC TGCT THYM UCEC"

for cancer in $cancers; do
	cd ${cancer}
	/softwares/gdc-client/gdc-client download -t ../gdc_token.txt -m ${cancer}_manifest.tsv >> ../re-download3.log
	cd ..
done
