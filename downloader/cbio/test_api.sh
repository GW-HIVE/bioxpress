#!/bin/bash

curl -X 'POST' \
  'https://www.cbioportal.org/api/molecular-profiles/acc_tcga_rna_seq_v2_mrna/molecular-data/fetch?projection=DETAILED' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "sampleIds": [
    "string"
  ],
  "sampleListId": "acc_tcga_rna_seq_v2_mrna",
  "entrezGeneIds": [
    1073741824
  ]
}'