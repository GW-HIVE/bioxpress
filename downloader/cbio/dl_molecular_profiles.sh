#!/bin/bash

output_dir="/data/shared/repos/bioxpress/downloads/cbio"
url="https://www.cbioportal.org/api/molecular-profiles?projection=SUMMARY&pageSize=100000&pageNumber=0&direction=ASC"
curl -G "${url}" \
     -H "accept: application/json" \
     -o "${output_dir}/all_molecular_profiles.json"

# If I give you study IDs (only TCGA study IDs), can you get me their molecular profile IDs and sample list IDs (I think I have this script in BioMuta)
# The next step would be getting entrez gene IDs from somewhere.
# These are the 3 things you need to download Z-scores.

# Create download directory and update current symlink
