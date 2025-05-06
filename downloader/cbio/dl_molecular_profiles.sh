#!/bin/bash

output_dir="/data/shared/repos/bioxpress/downloads/current"
#url="https://www.cbioportal.org/api/molecular-profiles?projection=SUMMARY&pageSize=100000&pageNumber=0&direction=ASC"
#curl -G "${url}" \
#     -H "accept: application/json" \
#     -o "${output_dir}/all_molecular_profiles.json"

# If I give you study IDs (only TCGA study IDs), can you get me their molecular profile IDs and sample list IDs (I think I have this script in BioMuta)
# The next step would be getting entrez gene IDs from somewhere.
# These are the 3 things you need to download Z-scores.

cd "${output_dir}"
#jq '[.[] | select(
#  .molecularAlterationType == "MRNA_EXPRESSION" and 
#  (.molecularProfileId | test("tcga") and test("normal_"))
#)]' all_molecular_profiles.json > tcga_mrna_expression.json

# Extract study IDs
study_ids=$(jq -r '.[].studyId' tcga_mrna_expression.json)

# Make a directory to store sample lists
mkdir -p sample_lists

# Loop through each study ID
for id in $study_ids; do
    echo "Fetching sample lists for study: $id"
    
    # Perform API call
    curl -s -X 'GET' \
      "https://www.cbioportal.org/api/studies/${id}/sample-lists?projection=SUMMARY&pageSize=10000000&pageNumber=0&direction=ASC" \
      -H 'accept: application/json' \
      -o "sample_lists/${id}_sample_lists.json"
    
    echo "Saved to: ${id}_sample_lists.json"
    echo
done